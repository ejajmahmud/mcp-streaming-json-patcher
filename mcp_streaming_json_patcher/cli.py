"""CLI for Streaming JSON Patcher."""
import argparse
from .core import StreamingJsonPatcher, PatchOperation

def main():
    parser = argparse.ArgumentParser(description="MCP Streaming JSON Patcher CLI")
    parser.add_argument("--demo", action="store_true", help="Run patcher demo")
    args = parser.parse_args()

    patcher = StreamingJsonPatcher({"status": "running", "progress": 0})
    patcher.apply_patch(PatchOperation("replace", "/progress", 50))
    patcher.apply_patch(PatchOperation("add", "/completed_steps", ["init"]))
    print(f"Patched document: {patcher.document}")

if __name__ == "__main__":
    main()
