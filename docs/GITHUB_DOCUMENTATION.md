# GitHub Documentation

This document tracks repository-level standards and QA updates managed by Muhammed Ali Avci.

## Branch and Commit Convention

- Branch naming: `feature/<scope>`, `fix/<scope>`, `docs/<scope>`, `test/<scope>`
- Commit message style:
  - `feat: <what and why>`
  - `fix: <what and why>`
  - `docs: <what and why>`
  - `test: <what and why>`
  - `chore: <what and why>`

## Pull Request Checklist

- [ ] Scope is limited to module ownership in `docs/TASK_DISTRIBUTION.md`
- [ ] Tests pass locally with `python -m pytest tests -v`
- [ ] `requirements.txt` stays versioned and conflict-free
- [ ] i18n keys in `assets/languages.json` are symmetric in `tr` and `en`
- [ ] README reflects latest architecture and QA status

## QA Reporting Policy (Ali)

- Weekly report is stored in `docs/WEEKLY_PROGRESS_ALI.md`
- Tests focus on:
  - language key consistency
  - dependency hygiene
  - smoke scenarios against teammates' modules without changing their code
- Each weekly report must include:
  - executed command(s)
  - pass/fail summary
  - detected risks
  - action recommendations
