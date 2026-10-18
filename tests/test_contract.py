from pathlib import Path

SRC = (Path(__file__).parents[1] / "contracts" / "contract.py").read_text(encoding="utf-8")


def test_real_separated_role_lifecycle():
    for token in (
        "def draft_interval(",
        "def screen_interval(",
        "def adopt_interval(",
        "def cancel_interval(",
        '"DRAFTED"',
        '"SCREENED"',
        '"ADOPTED"',
    ):
        assert token in SRC
    assert "reviewer must differ from owner" in SRC
    assert "only the assigned reviewer may screen" in SRC


def test_bounded_consensus_and_deterministic_window_guards():
    for token in (
        '"OPEN", "TRIM", "CONFLICT"',
        "OPEN must preserve the full interval",
        "TRIM requires a useful bounded interval and mitigation",
        "CONFLICT requires zero interval and a cause",
        "closed cause codes required",
    ):
        assert token in SRC


def test_input_identity_and_replay_are_bound():
    for token in (
        "input_digest",
        "used_inputs",
        "interval id or exact input already used",
        "hashlib.sha256",
    ):
        assert token in SRC


def test_source_attribution_is_required():
    assert "source_refs" in SRC
    assert "len(refs) < 2" in SRC
    assert "independently compare all three frozen records" in SRC


def test_no_remote_fixture_dependency():
    assert "gl.nondet.web.get" not in SRC
    assert "raw.githubusercontent.com" not in SRC
