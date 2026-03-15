# Contributing

Thank you for your interest in contributing to the Document Reading Agent! This page explains how to set up a development environment, the standards we follow, and the process for submitting changes.

---

## Code of Conduct

Please be respectful and constructive in all interactions. We follow the [Contributor Covenant](https://www.contributor-covenant.org/) code of conduct.

---

## Getting Started

### 1. Fork and Clone

1. Click **Fork** on the [GitHub repository page](https://github.com/codymayhew11-lang/Document-Reading-Agent).
2. Clone your fork locally:

```bash
git clone https://github.com/<your-username>/Document-Reading-Agent.git
cd Document-Reading-Agent
```

### 2. Set Up a Development Environment

```bash
python -m venv .venv
source .venv/bin/activate          # macOS / Linux
# .venv\Scripts\activate.bat       # Windows Command Prompt

pip install -r requirements.txt
```

### 3. Create a Feature Branch

Always work on a dedicated branch rather than committing directly to `main`.

```bash
git checkout -b feature/my-feature
# or for bug fixes:
git checkout -b fix/issue-42
```

---

## Making Changes

- Keep changes focused. One pull request should address one concern.
- Follow the existing code style (PEP 8, type hints, docstrings).
- Add or update docstrings for any new or changed public API.
- Update the relevant wiki pages in `docs/` if your change affects user-facing behaviour.

---

## Commit Messages

Use clear, imperative commit messages:

```
Add support for .odt documents
Fix ValueError when file path contains spaces
Update wiki: document --query flag behaviour
```

---

## Pull Request Process

1. Ensure your branch is up to date with `main`:

```bash
git fetch origin
git rebase origin/main
```

2. Push your branch:

```bash
git push origin feature/my-feature
```

3. Open a Pull Request against `main` on GitHub.
4. Fill in the PR template (description, motivation, testing steps).
5. A maintainer will review your changes and may request revisions.
6. Once approved, your PR will be merged.

---

## Adding a New Document Format

To add support for a new file format (e.g. `.odt`, `.rtf`):

1. Add the new extension to `DocumentReader.SUPPORTED_EXTENSIONS` in `agent/reader.py`.
2. Implement a private `_read_<ext>()` method following the same pattern as `_read_pdf()` (lazy import, descriptive `ImportError`).
3. Add a dispatch branch in `DocumentReader.read()`.
4. Update [Installation](Installation.md) with the new optional dependency.
5. Update [Usage](Usage.md) with the new supported format.
6. Update the [API Reference](API-Reference.md) with the new private method.

---

## Reporting Bugs

Open a [GitHub Issue](https://github.com/codymayhew11-lang/Document-Reading-Agent/issues) and include:

- Your Python version (`python --version`)
- The command you ran
- The full error output
- (If possible) a minimal example document that reproduces the issue

---

## Requesting Features

Open a GitHub Issue labelled **enhancement** describing:

- The problem you are trying to solve
- Your proposed solution or API
- Any alternatives you considered

---

## License

By contributing to this project you agree that your contributions will be licensed under the project's [MIT License](../README.md#license).
