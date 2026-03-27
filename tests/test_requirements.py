from pathlib import Path


def _effective_requirement_lines():
    lines = Path("requirements.txt").read_text(encoding="utf-8").splitlines()
    cleaned = []
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        cleaned.append(stripped)
    return cleaned


def test_requirements_are_pinned_with_compatible_release_operator():
    lines = _effective_requirement_lines()
    assert lines, "requirements.txt should not be empty."
    assert all("~=" in line for line in lines), "All dependencies should be version-pinned using ~=."


def test_requirements_have_no_duplicates():
    lines = _effective_requirement_lines()
    names = [line.split("~=", 1)[0].strip().lower() for line in lines]
    assert len(names) == len(set(names)), "Duplicate dependency entries found in requirements.txt."
