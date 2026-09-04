import pytest
from client import ask


def text_of(result: dict) -> str:
    return result.get("text", "").lower()


def tools_used(result: dict) -> list:
    used = result.get("agentFlowExecutedData") or []
    return [str(step) for step in used]


def test_station_status_is_retrieved_not_invented():
    """The agent must call the API and report the real error code."""
    result = ask("What is the status of station ST-02?")
    answer = text_of(result)
    assert "e-233" in answer
    assert "stopped" in answer


def test_running_station_reports_no_fault():
    """ST-01 is healthy. The agent must not invent a problem."""
    answer = text_of(ask("Is station ST-01 working normally?"))
    assert "running" in answer
    assert "e-233" not in answer


def test_manual_lookup_bit_replacement():
    """Manual only, no API involved. W-118 says 50,000 cycles."""
    answer = text_of(ask("How often should the screwdriving bit be replaced?"))
    assert "50" in answer


def test_unknown_station_is_handled():
    """ST-99 does not exist. The agent must say so, not fabricate data."""
    answer = text_of(ask("What is the status of station ST-99?"))
    assert "not found" in answer or "does not exist" in answer


def test_out_of_scope_question_is_refused():
    """Nothing in the manual covers this. The agent should admit it."""
    answer = text_of(ask("What is the warranty period for the UR10 arm?"))
    assert any(w in answer for w in ["not", "no information", "manual"])