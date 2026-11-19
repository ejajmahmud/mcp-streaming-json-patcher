"""Tests for Streaming JSON Patcher."""
import unittest
from mcp_streaming_json_patcher.core import StreamingJsonPatcher, PatchOperation

class TestStreamingJsonPatcher(unittest.TestCase):
    def test_add_replace_remove(self):
        p = StreamingJsonPatcher({"user": {"name": "Alice"}})
        p.apply_patch(PatchOperation("add", "/user/age", 30))
        self.assertEqual(p.document["user"]["age"], 30)

        p.apply_patch(PatchOperation("replace", "/user/name", "Bob"))
        self.assertEqual(p.document["user"]["name"], "Bob")

        p.apply_patch(PatchOperation("remove", "/user/age"))
        self.assertNotIn("age", p.document["user"])
