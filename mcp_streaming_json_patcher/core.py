"""Core RFC 6902 Streaming JSON Patcher."""
from typing import Dict, List, Any, Optional
import copy

class PatchOperation:
    def __init__(self, op: str, path: str, value: Optional[Any] = None):
        self.op = op
        self.path = path
        self.value = value

class StreamingJsonPatcher:
    def __init__(self, initial_document: Optional[Dict[str, Any]] = None):
        self.document: Dict[str, Any] = copy.deepcopy(initial_document or {})

    def apply_patch(self, patch: PatchOperation) -> Dict[str, Any]:
        parts = [p for p in patch.path.split("/") if p]
        if not parts:
            if patch.op == "replace":
                self.document = copy.deepcopy(patch.value)
                return self.document
            raise ValueError("Root path requires replace operation")

        target = self.document
        for part in parts[:-1]:
            if isinstance(target, dict):
                target = target.setdefault(part, {})
            elif isinstance(target, list):
                target = target[int(part)]

        last_key = parts[-1]

        if patch.op == "add" or patch.op == "replace":
            if isinstance(target, dict):
                target[last_key] = patch.value
            elif isinstance(target, list):
                idx = int(last_key)
                if patch.op == "add":
                    target.insert(idx, patch.value)
                else:
                    target[idx] = patch.value
        elif patch.op == "remove":
            if isinstance(target, dict) and last_key in target:
                del target[last_key]
            elif isinstance(target, list):
                del target[int(last_key)]
        else:
            raise NotImplementedError(f"Unsupported patch operation: {patch.op}")

        return self.document
