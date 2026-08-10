from __future__ import annotations

import json
from datetime import date
from pathlib import Path

from media_ops.factory import (
    build_release_package,
    hydrate_assets,
    plan_campaign,
    promote_asset,
    red_team_copy,
)
from media_ops.vsrr import VSRRState
from media_ops.runner import execute_release


BRANDS = {
    "core-power": {"display_name": "Core Power", "cta": "DM CORE for private early access."},
    "drive-out": {"display_name": "Drive Out", "cta": "DM DRIVE for the driver toolkit."},
    "stuck-to-done": {"display_name": "Stuck To Done", "cta": "DM DONE for early access."},
}


def test_plan_campaign_is_deterministic_and_balanced() -> None:
    first = plan_campaign(BRANDS, date(2026, 8, 10), days=7, posts_per_day=1)
    second = plan_campaign(BRANDS, date(2026, 8, 10), days=7, posts_per_day=1)

    assert first == second
    assert len(first) == 7
    assert [item["brand"] for item in first[:4]] == [
        "core-power",
        "drive-out",
        "stuck-to-done",
        "core-power",
    ]
    assert {item["brand"] for item in first} == set(BRANDS)
    assert all(item["publish_state"] == "READY_TO_POST" for item in first)


def test_promote_asset_requires_numeric_and_semantic_pass() -> None:
    passing = {"numeric_decision": "PASS", "semantic_decision": "PASS"}
    numeric_only = {"numeric_decision": "PASS", "semantic_decision": "REJECT"}

    assert promote_asset(passing) == "PROMOTED"
    assert promote_asset(numeric_only) == "REJECTED"


def test_vsrr_parks_route_after_two_failures_and_preserves_blocker_id(tmp_path: Path) -> None:
    state_path = tmp_path / "state.json"
    state = VSRRState.load(state_path, job_id="release-20260810")

    state.record_failure("publisher", "SOCIAL-PUBLISH-AUTH-001", "No authenticated publisher", "route-a")
    assert state.route_status("publisher") == "RETRY_WITH_DIFFERENT_METHOD"

    state.record_failure("publisher", "SOCIAL-PUBLISH-AUTH-001", "No authenticated publisher", "route-b")
    assert state.route_status("publisher") == "PARKED"
    assert state.data["blockers"]["publisher"]["blocker_id"] == "SOCIAL-PUBLISH-AUTH-001"

    reloaded = VSRRState.load(state_path, job_id="release-20260810")
    assert reloaded.route_status("publisher") == "PARKED"


def test_build_release_package_copies_assets_and_does_not_claim_publication(tmp_path: Path) -> None:
    source = tmp_path / "source.png"
    source.write_bytes(b"verified-image-bytes")
    schedule = [{
        "slot_id": "2026-08-10-core-power-01",
        "date": "2026-08-10",
        "time_local": "09:15",
        "brand": "core-power",
        "brand_name": "Core Power",
        "source": str(source),
        "caption": "Private practice. Clear next steps.",
        "cta": "DM CORE for private early access.",
        "alt_text": "A fully clothed adult man practicing hip mobility at home.",
        "publish_state": "READY_TO_POST",
        "qa": {"numeric_decision": "PASS", "semantic_decision": "PASS"},
        "provenance": {"source_route": "chatgpt-local", "source_url_or_receipt": "receipt-1"},
        "copy_red_team": {"decision": "PASS", "failures": []},
    }]

    receipt = build_release_package(schedule, tmp_path / "release", job_id="release-20260810")

    assert receipt["status"] == "READY_TO_POST"
    assert receipt["external_publish"] is False
    assert receipt["counts"] == {"planned": 1, "promoted": 1, "rejected": 0}
    manifest = json.loads((tmp_path / "release" / "publishing-manifest.json").read_text(encoding="utf-8"))
    assert manifest["assets"][0]["publish"] is False
    assert Path(manifest["assets"][0]["asset_path"]).read_bytes() == b"verified-image-bytes"
    assert manifest["assets"][0]["provenance"]["source_route"] == "chatgpt-local"
    assert manifest["assets"][0]["copy_red_team"]["decision"] == "PASS"
    assert (tmp_path / "release" / "calendar.csv").exists()
    dashboard = (tmp_path / "release" / "index.html").read_text(encoding="utf-8")
    assert "Core Power" in dashboard
    assert "READY TO POST" in dashboard


def test_hydrate_assets_uses_authoritative_numeric_and_semantic_receipts(tmp_path: Path) -> None:
    source = tmp_path / "asset.png"
    source.write_bytes(b"asset")
    numeric = tmp_path / "numeric.csv"
    numeric.write_text(
        "file,numeric_decision,laplacian_variance,entropy,megapixels,sha256\n"
        "asset.png,PASS,1900.0,6.9,2.0736,abc\n",
        encoding="utf-8",
    )
    semantic = tmp_path / "semantic.csv"
    semantic.write_text(
        "file,final_decision,source_route,source_url_or_receipt\n"
        "asset.png,PASS,chatgpt-local,receipt-1\n",
        encoding="utf-8",
    )
    brands = {"core-power": {"assets": [{"source": str(source)}]}}

    hydrated = hydrate_assets(brands, numeric, semantic)

    qa = hydrated["core-power"]["assets"][0]["qa"]
    assert qa["numeric_decision"] == "PASS"
    assert qa["semantic_decision"] == "PASS"
    assert qa["laplacian_variance"] == 1900.0
    assert hydrated["core-power"]["assets"][0]["provenance"]["source_route"] == "chatgpt-local"


def test_red_team_rejects_medical_guarantee_and_uncited_driver_entitlement() -> None:
    assert red_team_copy("core-power", "Cure ED in seven days.") == ["MEDICAL_OUTCOME_GUARANTEE"]
    assert red_team_copy("drive-out", "You are owed $500 today.") == ["UNCITED_DRIVER_ENTITLEMENT"]
    assert red_team_copy(
        "drive-out",
        "NYC minimum rates changed this year.",
        source_url="https://www.nyc.gov/site/tlc/about/driver-pay-rates.page",
    ) == []


def test_execute_release_writes_completed_state_and_scenario_receipt(tmp_path: Path) -> None:
    source = tmp_path / "asset.png"
    source.write_bytes(b"asset")
    numeric = tmp_path / "numeric.csv"
    numeric.write_text(
        "file,numeric_decision,laplacian_variance,entropy,megapixels,sha256\n"
        "asset.png,PASS,1900,6.9,2.0736,abc\n",
        encoding="utf-8",
    )
    semantic = tmp_path / "semantic.csv"
    semantic.write_text(
        "file,final_decision,source_route,source_url_or_receipt\n"
        "asset.png,PASS,chatgpt-local,receipt-1\n",
        encoding="utf-8",
    )
    brands = {
        "core-power": {
            "display_name": "Core Power",
            "cta": "DM CORE for private early access.",
            "assets": [{
                "source": str(source),
                "caption": "Private practice without medical guarantees.",
                "alt_text": "An adult practicing mobility at home.",
            }],
        }
    }

    receipt = execute_release(
        brands=brands,
        numeric_scorecard=numeric,
        semantic_scorecard=semantic,
        output_root=tmp_path / "out",
        start_date=date(2026, 8, 11),
        days=1,
        posts_per_day=1,
        job_id="release-20260811",
    )

    assert receipt["status"] == "READY_TO_POST"
    state = json.loads((tmp_path / "out" / "release-20260811" / "state.json").read_text(encoding="utf-8"))
    assert state["status"] == "completed"
    assert state["blockers"]["publisher"]["status"] == "PARKED"
    assert len(state["blockers"]["publisher"]["attempts"]) == 2
    scenario = json.loads((tmp_path / "out" / "release-20260811" / "scenario-plan.json").read_text(encoding="utf-8"))
    assert scenario["publisher"]["state"] == "BLOCKED_AUTH"
    assert scenario["publisher"]["blocker_id"] == "SOCIAL-PUBLISH-AUTH-001"
