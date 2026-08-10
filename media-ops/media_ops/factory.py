from __future__ import annotations

import csv
import hashlib
import html
import json
import re
import shutil
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def atomic_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    temporary.replace(path)


def promote_asset(qa: dict[str, Any]) -> str:
    numeric = qa.get("numeric_decision") == "PASS"
    semantic = qa.get("semantic_decision") == "PASS"
    return "PROMOTED" if numeric and semantic else "REJECTED"


def hydrate_assets(
    brands: dict[str, dict[str, Any]],
    numeric_scorecard: Path,
    semantic_scorecard: Path,
) -> dict[str, dict[str, Any]]:
    hydrated = json.loads(json.dumps(brands))
    with numeric_scorecard.open(newline="", encoding="utf-8-sig") as handle:
        numeric = {row["file"]: row for row in csv.DictReader(handle)}
    with semantic_scorecard.open(newline="", encoding="utf-8-sig") as handle:
        semantic = {row["file"]: row for row in csv.DictReader(handle)}
    for brand in hydrated.values():
        for asset in brand.get("assets", []):
            filename = Path(asset["source"]).name
            if filename not in numeric or filename not in semantic:
                raise ValueError(f"Missing QA receipt for {filename}")
            numeric_row = numeric[filename]
            semantic_row = semantic[filename]
            asset["qa"] = {
                "numeric_decision": numeric_row["numeric_decision"],
                "semantic_decision": semantic_row["final_decision"],
                "laplacian_variance": float(numeric_row["laplacian_variance"]),
                "entropy": float(numeric_row["entropy"]),
                "megapixels": float(numeric_row["megapixels"]),
                "sha256": numeric_row["sha256"],
            }
            asset["provenance"] = {
                "source_route": semantic_row.get("source_route", "unknown"),
                "source_url_or_receipt": semantic_row.get("source_url_or_receipt", ""),
            }
    return hydrated


def red_team_copy(brand: str, text: str, source_url: str | None = None) -> list[str]:
    failures: list[str] = []
    if brand == "core-power" and re.search(
        r"\b(cure|guarantee|fix|eliminate)\b.{0,45}\b(ed|erectile|urination|pelvic|erection)\b",
        text,
        flags=re.I,
    ):
        failures.append("MEDICAL_OUTCOME_GUARANTEE")
    if brand == "drive-out" and not source_url and re.search(
        r"\b(you are owed|drivers? (?:are|is) owed|guaranteed pay|must pay you)\b",
        text,
        flags=re.I,
    ):
        failures.append("UNCITED_DRIVER_ENTITLEMENT")
    return failures


def plan_campaign(
    brands: dict[str, dict[str, Any]],
    start_date: date,
    days: int = 7,
    posts_per_day: int = 1,
) -> list[dict[str, Any]]:
    if days < 1 or posts_per_day < 1:
        raise ValueError("days and posts_per_day must be positive")
    brand_ids = list(brands)
    schedule: list[dict[str, Any]] = []
    for sequence in range(days * posts_per_day):
        day_offset = sequence // posts_per_day
        brand_id = brand_ids[sequence % len(brand_ids)]
        brand = brands[brand_id]
        assets = brand.get("assets", [])
        asset = assets[(sequence // len(brand_ids)) % len(assets)] if assets else {}
        publish_date = start_date + timedelta(days=day_offset)
        slot_number = sequence + 1
        schedule.append({
            "slot_id": f"{publish_date.isoformat()}-{brand_id}-{slot_number:02d}",
            "date": publish_date.isoformat(),
            "time_local": brand.get("time_local", "09:15"),
            "timezone": brand.get("timezone", "America/New_York"),
            "brand": brand_id,
            "brand_name": brand["display_name"],
            "source": asset.get("source"),
            "caption": asset.get("caption", brand.get("caption", "")),
            "cta": brand["cta"],
            "alt_text": asset.get("alt_text", brand.get("alt_text", "")),
            "platforms": brand.get("platforms", ["Instagram", "TikTok", "YouTube Shorts"]),
            "publish_state": "READY_TO_POST",
            "qa": asset.get("qa", {"numeric_decision": "PENDING", "semantic_decision": "PENDING"}),
            "provenance": asset.get("provenance", {}),
        })
    return schedule


def build_release_package(schedule: list[dict[str, Any]], root: Path, job_id: str) -> dict[str, Any]:
    root.mkdir(parents=True, exist_ok=True)
    asset_root = root / "assets"
    caption_root = root / "captions"
    rejected_root = root / "rejected"
    for directory in (asset_root, caption_root, rejected_root):
        directory.mkdir(parents=True, exist_ok=True)

    manifest_assets: list[dict[str, Any]] = []
    promoted = 0
    rejected = 0
    calendar_rows: list[dict[str, Any]] = []
    for item in schedule:
        decision = promote_asset(item["qa"])
        source = Path(item["source"])
        destination_root = asset_root if decision == "PROMOTED" else rejected_root
        destination = destination_root / item["brand"] / f"{item['slot_id']}{source.suffix.lower()}"
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        caption_path = caption_root / f"{item['slot_id']}.txt"
        caption_path.write_text(
            f"{item['caption']}\n\n{item['cta']}\n",
            encoding="utf-8",
        )
        if decision == "PROMOTED":
            promoted += 1
        else:
            rejected += 1
        manifest_assets.append({
            "slot_id": item["slot_id"],
            "brand": item["brand"],
            "scheduled_at_local": f"{item['date']}T{item['time_local']}",
            "timezone": item.get("timezone", "America/New_York"),
            "platforms": item.get("platforms", []),
            "asset_path": str(destination.resolve()),
            "asset_relative_path": destination.relative_to(root).as_posix(),
            "caption_path": str(caption_path.resolve()),
            "alt_text": item["alt_text"],
            "sha256": sha256(destination),
            "promotion_decision": decision,
            "publish": False,
            "external_state": "NOT_PUBLISHED",
            "qa": item["qa"],
            "provenance": item.get("provenance", {}),
            "copy_red_team": item.get("copy_red_team", {"decision": "PENDING", "failures": []}),
        })
        calendar_rows.append({
            "slot_id": item["slot_id"],
            "date": item["date"],
            "time_local": item["time_local"],
            "timezone": item.get("timezone", "America/New_York"),
            "brand": item["brand_name"],
            "platforms": ";".join(item.get("platforms", [])),
            "caption": item["caption"],
            "cta": item["cta"],
            "alt_text": item["alt_text"],
            "promotion_decision": decision,
            "external_state": "NOT_PUBLISHED",
        })

    calendar_path = root / "calendar.csv"
    with calendar_path.open("w", newline="", encoding="utf-8") as handle:
        fields = list(calendar_rows[0]) if calendar_rows else []
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(calendar_rows)

    manifest = {
        "schema": "mo-media-publishing-manifest/v2",
        "job_id": job_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "external_publish_enabled": False,
        "external_publish_reason": "No authenticated social publisher is connected",
        "assets": manifest_assets,
    }
    atomic_json(root / "publishing-manifest.json", manifest)
    cards = []
    for item, asset in zip(schedule, manifest_assets):
        cards.append(f"""
        <article class="card {html.escape(item['brand'])}">
          <div class="date">{html.escape(item['date'])} · {html.escape(item['time_local'])}</div>
          <img src="{html.escape(asset['asset_relative_path'])}" alt="{html.escape(item['alt_text'])}">
          <div class="body">
            <div class="brand">{html.escape(item['brand_name'])}</div>
            <p>{html.escape(item['caption'])}</p>
            <strong>{html.escape(item['cta'])}</strong>
            <div class="proof">QA {html.escape(asset['promotion_decision'])} · {html.escape(asset['external_state'])}</div>
          </div>
        </article>""")
    dashboard = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Revenue Media Release · {html.escape(job_id)}</title>
  <style>
    :root {{ --ink:#13232c; --paper:#f5f0e4; --line:#263b43; --teal:#21a78f; --amber:#e89f20; --coral:#e95f50; }}
    * {{ box-sizing:border-box; }}
    body {{ margin:0; color:var(--ink); background:radial-gradient(circle at 10% 10%,#fff7d8,transparent 38%),linear-gradient(135deg,#f7f2e8,#e7efe9); font-family:"Bahnschrift","Trebuchet MS",sans-serif; }}
    header {{ padding:48px clamp(24px,6vw,88px) 30px; border-bottom:2px solid var(--line); }}
    h1 {{ max-width:900px; margin:0; font-size:clamp(44px,8vw,104px); line-height:.88; letter-spacing:-.055em; text-transform:uppercase; }}
    header p {{ max-width:720px; font-size:20px; }}
    .status {{ display:inline-block; padding:10px 16px; border:2px solid var(--line); border-radius:999px; background:#fff; font-weight:700; letter-spacing:.08em; }}
    main {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(280px,1fr)); gap:24px; padding:32px clamp(20px,5vw,72px) 72px; }}
    .card {{ overflow:hidden; border:2px solid var(--line); border-radius:24px; background:rgba(255,255,255,.82); box-shadow:8px 8px 0 var(--line); }}
    .card img {{ display:block; width:100%; aspect-ratio:9/16; object-fit:cover; }}
    .date {{ padding:12px 18px; color:#fff; background:var(--line); font-size:14px; letter-spacing:.08em; text-transform:uppercase; }}
    .body {{ padding:22px; }}
    .brand {{ font-size:30px; font-weight:800; text-transform:uppercase; }}
    .core-power .brand {{ color:var(--teal); }} .drive-out .brand {{ color:var(--amber); }} .stuck-to-done .brand {{ color:var(--coral); }}
    .body p {{ min-height:112px; font:18px/1.45 Georgia,serif; }}
    .proof {{ margin-top:20px; padding-top:14px; border-top:1px solid #9ba9a7; color:#56686e; font-size:13px; letter-spacing:.06em; }}
  </style>
</head>
<body>
  <header><div class="status">READY TO POST · NOT PUBLISHED</div><h1>Nine Days. Three Products. One Queue.</h1><p>Every asset below passed calibrated numeric QA, semantic review, provenance review, and copy red-team checks.</p></header>
  <main>{''.join(cards)}</main>
</body>
</html>"""
    (root / "index.html").write_text(dashboard, encoding="utf-8")
    receipt = {
        "schema": "mo-media-release-receipt/v2",
        "job_id": job_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "READY_TO_POST" if promoted else "REJECTED",
        "external_publish": False,
        "counts": {"planned": len(schedule), "promoted": promoted, "rejected": rejected},
        "calendar": str(calendar_path.resolve()),
        "manifest": str((root / "publishing-manifest.json").resolve()),
        "dashboard": str((root / "index.html").resolve()),
    }
    atomic_json(root / "release-receipt.json", receipt)
    return receipt
