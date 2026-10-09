import json

import pytest

from llm_redteam.adapters import FixtureAdapter, OpenAIAdapter


def test_fixture_adapter_is_deterministic():
    adapter = FixtureAdapter()
    first = adapter.complete(system_prompt="system", user_prompt="ignore this")
    second = adapter.complete(system_prompt="system", user_prompt="ignore this")
    assert first == second
    assert first.model == "fixture-v0"


def test_openai_adapter_requires_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    with pytest.raises(RuntimeError, match="OPENAI_API_KEY is required"):
        OpenAIAdapter()


def test_openai_adapter_parses_mocked_response(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")

    class FakeResponse:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def read(self):
            return json.dumps({"choices": [{"message": {"content": "mock response"}}]}).encode()

    def fake_urlopen(request, timeout):
        assert request.full_url == "https://example.test/v1/chat/completions"
        assert request.get_header("Authorization") == "Bearer test-key"
        assert timeout == 60.0
        body = json.loads(request.data)
        assert body["messages"][0]["role"] == "system"
        return FakeResponse()

    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)
    response = OpenAIAdapter(model="mock-model", base_url="https://example.test/v1").complete(
        system_prompt="system", user_prompt="user"
    )
    assert response.text == "mock response"
    assert response.model == "mock-model"
    assert response.latency_ms >= 0
