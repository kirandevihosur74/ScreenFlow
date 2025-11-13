from utils.helpers import detect_app_from_task, extract_app_name, slugify


def test_extract_app_name_strips_common_prefixes() -> None:
    url = "https://app.linear.app/projects"
    assert extract_app_name(url) == "linear"


def test_extract_app_name_handles_missing_subdomain() -> None:
    url = "https://www.notion.so/workspace"
    assert extract_app_name(url) == "notion"


def test_slugify_turns_text_into_safe_identifier() -> None:
    text = "Create a Project in Linear!"
    assert slugify(text) == "create_a_project_in_linear"


def test_slugify_truncates_long_strings() -> None:
    text = "x" * 100
    assert slugify(text) == "x" * 50


def test_detect_app_from_task_matches_known_app() -> None:
    task = "Create a new project in Linear"
    known_apps = {"linear": "https://linear.app"}
    assert detect_app_from_task(task, known_apps) == "linear"


def test_detect_app_from_task_returns_none_when_unknown() -> None:
    task = "Draft an email to the team"
    known_apps = {"linear": "https://linear.app"}
    assert detect_app_from_task(task, known_apps) is None

