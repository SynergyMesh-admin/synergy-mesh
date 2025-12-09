#!/usr/bin/env python3
"""Generate a repository self-awareness summary from docs/project-manifest.md."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path

SECTION_PATTERN = re.compile(r"^## +(?P<title>.+?)\s*$", re.MULTILINE)


@dataclass
class SectionSummary:
    identity: str
    needs: list[str]
    guardrails: list[str]
    signals: list[str]


@dataclass
class AutomationResult:
    label: str
    command: str
    exit_code: int
    success: bool
    output_tail: list[str]


def _parse_sections(manifest_text: str) -> dict[str, str]:
    """Return a mapping of section title -> body text."""
    matches = list(SECTION_PATTERN.finditer(manifest_text))
    sections: dict[str, str] = {}

    for index, match in enumerate(matches):
        title = match.group("title").strip()
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(manifest_text)
        sections[title.lower()] = manifest_text[start:end].strip()

    return sections


def _split_bullets(section_text: str) -> list[str]:
    bullets: list[str] = []
    current: list[str] = []

    for raw_line in section_text.splitlines():
        stripped = raw_line.strip()

        if stripped.startswith("- "):
            if current:
                bullets.append(" ".join(current).strip())
                current = []
            current.append(stripped[2:].strip())
        elif stripped and current:
            current.append(stripped)

    if current:
        bullets.append(" ".join(current).strip())

    return bullets


def _summarize_sections(sections: dict[str, str]) -> SectionSummary:
    identity = sections.get("identity & mission", "Not documented.").strip()
    if not identity:
        identity = "Not documented."

    needs = _split_bullets(sections.get("active needs (what we want)", ""))
    guardrails = _split_bullets(sections.get("guardrails (what we avoid)", ""))
    signals = _split_bullets(sections.get("proof & self-check signals", ""))

    return SectionSummary(identity=identity, needs=needs, guardrails=guardrails, signals=signals)


def _run_command_summary(
    label: str, command: str | None, cwd: Path, max_lines: int
) -> AutomationResult | None:
    """Execute a command and capture its output summary.
    
    Security Note: This function uses shell=True for compatibility with
    complex shell commands (pipes, redirects, etc). Commands should come from
    trusted sources only (CLI arguments from authorized developers).
    For programmatic usage with untrusted input, refactor to use shlex.split()
    and shell=False.
    """
    if not command:
        return None

    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True,
        cwd=str(cwd),
    )

    joined_lines = [
        line
        for line in (result.stdout or "").splitlines() + (result.stderr or "").splitlines()
        if line
    ]
    tail = joined_lines[-max_lines:] if joined_lines else []

    return AutomationResult(
        label=label,
        command=command,
        exit_code=result.returncode,
        success=result.returncode == 0,
        output_tail=tail,
    )


def _render_report(
    summary: SectionSummary, automation_results: list[AutomationResult] | None = None
) -> str:
    identity = summary.identity
    needs = summary.needs
    guardrails = summary.guardrails
    signals = summary.signals

    automation_md: list[str] = []
    if automation_results:
        for result in automation_results:
            icon = "✅" if result.success else "❌"
            automation_md.append(f"- {icon} {result.label} (`{result.command}`)")
            automation_md.append(f"  - Exit code: {result.exit_code}")
            if result.output_tail:
                automation_md.append("  - Last output lines:")
                automation_md.extend(f"    {line}" for line in result.output_tail)
            else:
                automation_md.append("  - Last output lines:\n    (no output)")
    else:
        automation_md.append("- (no automation signals captured)")

    needs_md = "\n".join(f"- {item}" for item in needs) if needs else "- (none listed)"
    guardrails_md = (
        "\n".join(f"- {item}" for item in guardrails) if guardrails else "- (none listed)"
    )
    signals_md = "\n".join(f"- {item}" for item in signals) if signals else "- (none listed)"

    sections_md = [
        "## 📣 Repository Self-Awareness Report",
        "",
        "**Identity & Mission**",
        identity.strip(),
        "",
        "**Current Needs**",
        needs_md,
        "",
        "**Guardrails / Anti-Goals**",
        guardrails_md,
        "",
        "**Verification Signals**",
        signals_md,
        "",
        "**Automation Signals**",
        "\n".join(automation_md),
        "",
    ]

    return "\n".join(sections_md)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--manifest",
        default="docs/project-manifest.md",
        help="Path to the manifest markdown file.",
    )
    parser.add_argument(
        "--output",
        default="-",
        help="Where to write the markdown report (default: stdout).",
    )
    parser.add_argument(
        "--json-output",
        help="Optional path to write the structured JSON report (use '-' for stdout).",
    )
    parser.add_argument(
        "--repo-root",
        default=None,
        help="Repository root directory (defaults to the manifest's parent).",
    )
    parser.add_argument(
        "--lint-cmd",
        help="Command to run for lint verification.",
    )
    parser.add_argument(
        "--test-cmd",
        help="Command to run for test verification.",
    )
    parser.add_argument(
        "--max-log-lines",
        type=int,
        default=5,
        help="Number of log lines to capture from each automation command.",
    )
    parser.add_argument(
        "--automation-cmd",
        action="append",
        help="Additional automation commands in the form Label=command (can be repeated).",
    )
    parser.add_argument(
        "--fail-on-errors",
        action="store_true",
        help="Exit with status 1 if any automation command fails.",
    )
    args = parser.parse_args()

    manifest_path = Path(args.manifest)
    manifest_text = manifest_path.read_text(encoding="utf-8")
    sections = _parse_sections(manifest_text)
    section_summary = _summarize_sections(sections)
    repo_root = Path(args.repo_root) if args.repo_root else manifest_path.parent.parent
    automation_results: list[AutomationResult] = []
    command_pairs: list[tuple[str, str | None]] = [
        ("Lint", args.lint_cmd),
        ("Tests", args.test_cmd),
    ]

    if args.automation_cmd:
        for entry in args.automation_cmd:
            if not entry or "=" not in entry:
                raise ValueError("automation-cmd entries must be in the form Label=command")
            label, command = entry.split("=", 1)
            command_pairs.append((label.strip() or "Custom", command.strip()))

    for label, command in command_pairs:
        summary = _run_command_summary(label, command, repo_root, args.max_log_lines)
        if summary:
            automation_results.append(summary)

    report = _render_report(section_summary, automation_results)

    if args.output == "-":
        print(report)
    else:
        Path(args.output).write_text(report, encoding="utf-8")

    json_output = args.json_output
    if json_output:
        generated_at = datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
        payload = {
            "generated_at": generated_at,
            "manifest_path": str(manifest_path),
            "sections": asdict(section_summary),
            "automation": [asdict(result) for result in automation_results],
            "automation_summary": {
                "total": len(automation_results),
                "success": sum(1 for result in automation_results if result.success),
                "failed": sum(1 for result in automation_results if not result.success),
            },
        }

        if json_output.strip() == "-":
            print(json.dumps(payload, indent=2))
        else:
            json_path = Path(json_output)
            json_path.parent.mkdir(parents=True, exist_ok=True)
            json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    if args.fail_on_errors and any(not result.success for result in automation_results):
        sys.exit(1)


if __name__ == "__main__":
    main()
