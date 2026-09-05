from __future__ import annotations

import argparse
import json
from pathlib import Path

from .engine import evaluate, load_json
from .report import markdown


def main() -> int:
    parser = argparse.ArgumentParser(prog="changebench", description="Evaluate an infrastructure-agent proposal")
    parser.add_argument("scenario")
    parser.add_argument("proposal")
    parser.add_argument("--format", choices=("json", "markdown"), default="markdown")
    parser.add_argument("--output")
    args = parser.parse_args()

    result = evaluate(load_json(args.scenario), load_json(args.proposal))
    rendered = json.dumps(result.as_dict(), indent=2) if args.format == "json" else markdown(result)
    if args.output:
        Path(args.output).write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)
    return 0 if result.passed else 2


if __name__ == "__main__":
    raise SystemExit(main())

