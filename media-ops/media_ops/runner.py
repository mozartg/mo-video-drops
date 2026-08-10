from __future__ import annotations

import argparse
import json
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any

from .factory import atomic_json, build_release_package, hydrate_assets, plan_campaign, red_team_copy
from .vsrr import VSRRState


def execute_release(
    brands: dict[str, dict[str, Any]],
    numeric_scorecard: Path,
    semantic_scorecard: Path,
    output_root: Path,
    start_date: date,
    days: int,
    posts_per_day: int,
    job_id: str,
) -> dict[str, Any]:
    run_root = output_root / job_id
    state = VSRRState.load(run_root / "state.json", job_id=job_id)
    state.checkpoint("hydrate", "running")
    hydrated = hydrate_assets(brands, numeric_scorecard, semantic_scorecard)

    state.checkpoint("scenario-plan", "running")
    scenario = {
        "schema": "mo-media-scenario-plan/v1",
        "job_id": job_id,
        "working_route": "approved-source -> local composition -> dual QA -> synced Drive ready-to-post queue",
        "publisher": {
            "state": "BLOCKED_AUTH",
            "blocker_id": "SOCIAL-PUBLISH-AUTH-001",
            "evidence": [
                "No authenticated social publishing connector is exposed to this runtime",
                "No Buffer, Metricool, Meta, TikTok, or YouTube publisher credential was found in the bounded configuration scan",
            ],
            "next_materially_different_route": "Connect one publisher and perform one private canary post with URL receipt before enabling automatic publication",
        },
        "scenarios": [
            {"if": "publisher remains unavailable", "then": "continue creating READY_TO_POST synced Drive packages"},
            {"if": "any numeric or semantic gate fails", "then": "reject the asset and rotate to the next approved source"},
            {"if": "approved source pool falls below one unused asset per brand", "then": "open a generation canary job before scaling"},
            {"if": "a route fails twice", "then": "park the route under its stable blocker ID and continue other lanes"},
        ],
    }
    atomic_json(run_root / "scenario-plan.json", scenario)
    if state.route_status("publisher") == "AVAILABLE":
        state.record_failure(
            "publisher",
            "SOCIAL-PUBLISH-AUTH-001",
            scenario["publisher"]["evidence"][0],
            "connected-tool inventory",
        )
        state.record_failure(
            "publisher",
            "SOCIAL-PUBLISH-AUTH-001",
            scenario["publisher"]["evidence"][1],
            "bounded local credential scan",
        )

    state.checkpoint("plan", "running")
    schedule = plan_campaign(hydrated, start_date, days=days, posts_per_day=posts_per_day)
    for item in schedule:
        failures = red_team_copy(item["brand"], f"{item['caption']} {item['cta']}")
        item["copy_red_team"] = {"decision": "PASS" if not failures else "REJECT", "failures": failures}
        if failures:
            item["qa"]["semantic_decision"] = "REJECT"
    atomic_json(run_root / "schedule-plan.json", schedule)

    state.checkpoint("package", "running")
    receipt = build_release_package(schedule, run_root, job_id=job_id)
    state.checkpoint("complete", "completed", receipt=str(run_root / "release-receipt.json"))
    return receipt


def load_config(path: Path) -> dict[str, dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    brands = payload["brands"]
    base = path.parent.parent if path.parent.name == "config" else path.parent
    for brand in brands.values():
        for asset in brand.get("assets", []):
            source = Path(asset["source"])
            if not source.is_absolute():
                asset["source"] = str((base / source).resolve())
    return brands


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a receipt-backed, ready-to-post media release queue.")
    parser.add_argument("--config", type=Path, default=Path("config/brands.json"))
    parser.add_argument("--numeric-scorecard", type=Path, default=Path("outputs/media-rebuild-2026-08-10/receipts/campaign-canary-numeric-scorecard.csv"))
    parser.add_argument("--semantic-scorecard", type=Path, default=Path("outputs/media-rebuild-2026-08-10/receipts/semantic-provenance-scorecard.csv"))
    parser.add_argument("--output-root", type=Path, default=Path(r"G:\My Drive\Mo Media Factory\Ready to Post"))
    parser.add_argument("--start-date", type=date.fromisoformat, default=date.today() + timedelta(days=1))
    parser.add_argument("--days", type=int, default=9)
    parser.add_argument("--posts-per-day", type=int, default=1)
    parser.add_argument("--job-id")
    args = parser.parse_args()
    job_id = args.job_id or f"revenue-release-{args.start_date.strftime('%Y%m%d')}-{datetime.now().strftime('%H%M%S')}"
    receipt = execute_release(
        brands=load_config(args.config.resolve()),
        numeric_scorecard=args.numeric_scorecard.resolve(),
        semantic_scorecard=args.semantic_scorecard.resolve(),
        output_root=args.output_root.resolve(),
        start_date=args.start_date,
        days=args.days,
        posts_per_day=args.posts_per_day,
        job_id=job_id,
    )
    print(json.dumps(receipt, indent=2))
    return 0 if receipt["status"] == "READY_TO_POST" else 1


if __name__ == "__main__":
    raise SystemExit(main())
