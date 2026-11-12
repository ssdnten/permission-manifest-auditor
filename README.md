# Permission Manifest Auditor

Review an exported POSIX mode manifest for world-writable files, special permission bits and exposed private files.

Educational cybersecurity portfolio project. Built with AI assistance and supplied with synthetic fixtures and automated tests. It is a learning implementation, not a production security product.

## Quick start

Requires Python 3.11 or newer. Uses only the Python standard library; no pip installation or network access is needed.

From this repository's directory:

```console
python main.py samples/permissions.json
```

On Windows, use `py` in place of `python` if that is your installed launcher. Output is JSON on stdout. To save it, append `> report.json` in your terminal. Paths are relative to your current working directory.

## How it works

Parse octal mode strings and apply bit masks. A sticky world-writable directory receives a review finding distinct from an unrestricted world-writable file. Input is an explicit export, so the analyzer runs on Windows as well as Linux.

## Input and example

The `samples/` directory contains the complete minimal input schema and fictional data. The checked `samples/expected-output.json` records the output of the quick-start command (for the integrity monitor, the final check command).

## Tests

```console
python -m unittest discover -s tests -v
```

Tests cover core behavior, boundary cases and invalid input. GitHub Actions is configured to run them on Windows and Ubuntu with Python 3.11–3.13; see the Actions tab for actual remote results.

## Limitations

Does not inspect local Windows ACLs or live Linux permissions. Ownership, ACLs, capabilities, mount options and ancestor traversal rights are not modeled. setgid and sticky-bit findings may describe intentional configurations.

Successful analysis exits 0 unless stated otherwise above; command/input errors exit 2. Findings are not automatically remediated. Only use data you are authorized to analyze. Do not commit real credentials, customer logs or personal data.

## Learning notes

See [LEARNING_RU.md](LEARNING_RU.md) for an exercise and interview questions. Explain the algorithm, run the demo and implement an extension before presenting this as a skill you can use independently.
