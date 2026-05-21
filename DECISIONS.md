# Decisions

## 2026-05-21 - Profile Repo as AI Builder Workbench

Use the GitHub profile repository as the professional front door and daily AI workbench.

Rationale:

- The profile README stays readable.
- Daily work remains visible in structured folders.
- Contributions can be useful without creating empty commits.
- The system works locally first and can push once GitHub authentication is configured.

## 2026-05-21 - No Fake Activity

Automations must skip commits when they cannot produce useful content.

Rationale:

- Empty contribution farming weakens the profile.
- Useful artifacts compound into a credible public body of work.
- This keeps the account aligned with platform trust and professional reputation.

## 2026-05-21 - Live GitHub Account

Use `manuelsampedro1/manuelsampedro1` as the live GitHub profile repository.

Rationale:

- The browser-authenticated GitHub account is `manuelsampedro1`.
- GitHub publicly recognizes `manuelsampedro1/manuelsampedro1` as the special profile README repository.
- Commits are authored with the account's no-reply address: `202281585+manuelsampedro1@users.noreply.github.com`.

## 2026-05-21 - Weekly Quality Guard

Add a weekly quality audit automation in addition to the daily contribution automations.

Rationale:

- Daily publishing needs a guard against generic filler.
- The audit checks recent artifacts against the profile's topic and usefulness bar.
- Corrective actions go into `TODO.md` instead of silently letting automation drift.

## 2026-05-21 - Refresh All Public Indexes During Maintenance

The maintenance commit should refresh the folder indexes for `labs/`, `recipes/`, and `radar/`.

Rationale:

- The profile README should point to current public artifacts, not stale folders.
- Daily recipe and radar additions need the same discoverability as lab notes.
- Index refresh belongs in maintenance because it is lightweight and deterministic.
