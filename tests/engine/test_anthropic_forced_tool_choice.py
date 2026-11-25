"""Newer Claude models reject a forced tool_choice; JSON output must still work."""

from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from openjarvis.core.types import Message, Role
from openjarvis.engine._stubs import ResponseFormat
from openjarvis.engine.cloud import PRICING, CloudEngine, estimate_cost


def _engine(model):
    response = SimpleNamespace(
        content=[SimpleNamespace(type="text", text="ok")],
        usage=SimpleNamespace(input_tokens=2, output_tokens=1),
        model=model,
        stop_reason="end_turn",
    )
    client = MagicMock()
    client.messages.create.return_value = response
    engine = CloudEngine.__new__(CloudEngine)
    engine._anthropic_client = client
    return engine, client


def _call(model):
    engine, client = _engine(model)
    engine._generate_anthropic(
        [
            Message(role=Role.SYSTEM, content="Be brief."),
            Message(role=Role.USER, content="Hi"),
        ],
        model=model,
        temperature=0.5,
        max_tokens=100,
        response_format=ResponseFormat(schema={"type": "object"}),
    )
    return client.messages.create.call_args.kwargs


@pytest.mark.parametrize(
    "model", ["claude-opus-5-5", "claude-sonnet-5-5", "claude-fable-5-2"]
)
def test_no_forced_tool_choice_on_models_that_reject_it(model):
    kwargs = _call(model)
    assert kwargs["tool_choice"] == {"type": "auto"}
    assert kwargs["system"].startswith("Be brief.")
    assert "json_output" in kwargs["system"]


@pytest.mark.parametrize("model", ["claude-opus-5", "claude-haiku-5-5"])
def test_forced_tool_choice_kept_where_supported(model):
    kwargs = _call(model)
    assert kwargs["tool_choice"] == {"type": "tool", "name": "json_output"}
    assert kwargs["system"] == "Be brief."


@pytest.mark.parametrize(
    "model", ["claude-opus-5-5", "claude-sonnet-5-5", "claude-haiku-5-5"]
)
def test_current_models_are_priced(model):
    assert model in PRICING
    assert estimate_cost(model, 1_000_000, 0) == PRICING[model][0]
