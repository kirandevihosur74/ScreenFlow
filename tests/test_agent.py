from pathlib import Path

import pytest

from core.agent import AgentB


class FakeCapture:
    def __init__(self) -> None:
        self.calls = []

    def capture_workflow(self, task: str, app_url: str, app_name: str, **_) -> dict:
        self.calls.append(
            {
                "task": task,
                "app_url": app_url,
                "app_name": app_name,
            }
        )
        return {
            "success": True,
            "task": task,
            "app": app_name,
            "starting_url": app_url,
            "screenshots": [],
            "action_history": [],
            "total_steps": 1,
        }


class FakeStorage:
    def __init__(self) -> None:
        self.saved = None

    def save_workflow(self, workflow_result: dict) -> Path:
        self.saved = workflow_result
        return Path("fake/output")


@pytest.fixture
def agent_with_fakes() -> tuple[AgentB, FakeCapture, FakeStorage]:
    agent = AgentB()
    fake_capture = FakeCapture()
    fake_storage = FakeStorage()
    agent.capture = fake_capture
    agent.storage = fake_storage
    return agent, fake_capture, fake_storage


def test_handle_request_requires_task(agent_with_fakes: tuple[AgentB, FakeCapture, FakeStorage]) -> None:
    agent, _, _ = agent_with_fakes
    result = agent.handle_request({})
    assert not result["success"]
    assert "No task provided" in result["error"]


def test_handle_request_detects_app_and_saves_workflow(
    agent_with_fakes: tuple[AgentB, FakeCapture, FakeStorage]
) -> None:
    agent, _, fake_storage = agent_with_fakes
    request = {"task": "Create a new issue in Linear"}
    result = agent.handle_request(request)

    assert result["success"]
    assert result["app"] == "linear"
    assert result["starting_url"] == "https://linear.app"
    assert result["output_dir"] == "fake/output"
    assert fake_storage.saved is not None


def test_handle_request_fails_when_app_unknown(agent_with_fakes: tuple[AgentB, FakeCapture, FakeStorage]) -> None:
    agent, _, _ = agent_with_fakes
    request = {"task": "Review quarterly budget"}
    result = agent.handle_request(request)

    assert not result["success"]
    assert "Could not determine app URL" in result["error"]

