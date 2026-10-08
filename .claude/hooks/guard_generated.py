"""PreToolUse hook: block direct edits to build outputs; point at the source instead."""
import json
import sys

GENERATED = {
    "participant-runbook/runbook.html": "participant-runbook/content/*.md or template/",
    "facilitator-deck/facilitator-deck.html": "facilitator-deck/src/",
    "speech/01-greenfield/greenfield-deck.html": "speech/01-greenfield/src/slides.json",
    "speech/01-greenfield/greenfield-handout.md": "speech/01-greenfield/src/slides.json",
}

path = (json.load(sys.stdin).get("tool_input") or {}).get("file_path", "").replace("\\", "/")
for output, source in GENERATED.items():
    if path.endswith(output):
        print(f"{output} is a build output. Edit {source} instead, then run the release-materials skill.",
              file=sys.stderr)
        sys.exit(2)
