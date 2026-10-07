import importlib
import os
import sys
import unittest
from pathlib import Path
from types import ModuleType, SimpleNamespace
from unittest.mock import patch


SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC_DIR))

client = SimpleNamespace(
    chat=SimpleNamespace(completions=SimpleNamespace(create=None))
)
openai_module = ModuleType("openai")
openai_module.OpenAI = lambda: client

context_module = ModuleType("context")
context_module.TWIN_SYSTEM_PROMPT = "system prompt"

tools_module = ModuleType("tools")
tools_module.tools = [{"type": "function", "function": {"name": "test"}}]
tools_module.handle_tool_calls = lambda tool_calls: []

styles_module = ModuleType("styles")
styles_module.CSS = ""
styles_module.JS = ""
styles_module.EXAMPLES = []

dotenv_module = ModuleType("dotenv")
dotenv_module.load_dotenv = lambda **kwargs: None

with (
    patch.dict(os.environ, {"OPENAI_API_KEY": "test-api-key"}),
    patch.dict(
        sys.modules,
        {
            "openai": openai_module,
            "context": context_module,
            "tools": tools_module,
            "styles": styles_module,
            "dotenv": dotenv_module,
            "gradio": ModuleType("gradio"),
        },
    ),
):
    app = importlib.import_module("app")


def make_response(content, finish_reason="stop", tool_calls=None):
    message = SimpleNamespace(content=content, tool_calls=tool_calls)
    choice = SimpleNamespace(finish_reason=finish_reason, message=message)
    return SimpleNamespace(choices=[choice])


class ChatTests(unittest.TestCase):
    def setUp(self):
        self.create_patcher = patch.object(
            app.openai.chat.completions, "create"
        )
        self.create = self.create_patcher.start()
        self.addCleanup(self.create_patcher.stop)

    def test_returns_model_response_with_system_history_and_user_message(self):
        self.create.return_value = make_response("Hello!")
        history = [{"role": "user", "content": "Hi"}]

        result = app.chat("How are you?", history)

        self.assertEqual(result, "Hello!")
        self.create.assert_called_once_with(
            model=app.MODEL_NAME,
            messages=app.system + history + [
                {"role": "user", "content": "How are you?"}
            ],
            tools=app.tools,
        )
        self.assertEqual(history, [{"role": "user", "content": "Hi"}])

    def test_handles_tool_call_then_returns_follow_up_response(self):
        tool_call = SimpleNamespace(id="call-1")
        first_response = make_response(
            None, finish_reason="tool_calls", tool_calls=[tool_call]
        )
        self.create.side_effect = [first_response, make_response("Done.")]
        tool_result = {
            "role": "tool",
            "content": '"OK"',
            "tool_call_id": "call-1",
        }
        with patch.object(
            app, "handle_tool_calls", return_value=[tool_result]
        ) as handle:
            result = app.chat("Save my details", [])

        self.assertEqual(result, "Done.")
        handle.assert_called_once_with([tool_call])
        self.assertEqual(self.create.call_count, 2)
        for call in self.create.call_args_list:
            self.assertEqual(call.kwargs["model"], app.MODEL_NAME)
            self.assertEqual(call.kwargs["tools"], app.tools)
        second_messages = self.create.call_args_list[1].kwargs["messages"]
        self.assertEqual(
            second_messages,
            app.system
            + [{"role": "user", "content": "Save my details"}]
            + [first_response.choices[0].message, tool_result],
        )


if __name__ == "__main__":
    unittest.main()
