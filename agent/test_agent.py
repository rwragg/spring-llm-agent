"""Unit tests for the agent module — run without a live Ollama server."""
import unittest

from agent import build_payload, ask


class TestBuildPayload(unittest.TestCase):
    def test_payload_contains_prompt_and_model(self):
        payload = build_payload("hello", "llama3.2")
        self.assertIn("hello", payload["prompt"])
        self.assertEqual(payload["model"], "llama3.2")
        self.assertFalse(payload["stream"])


class TestAsk(unittest.TestCase):
    def test_ask_returns_error_struct_when_ollama_down(self):
        # No Ollama running -> ask() must return a structured error, not raise.
        result = ask("ping", "llama3.2")
        self.assertIsNone(result["answer"])
        self.assertIsNotNone(result["error"])
        self.assertEqual(result["prompt"], "ping")


if __name__ == "__main__":
    unittest.main()