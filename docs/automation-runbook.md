# Automation Runbook

This repo is designed for daily useful GitHub contributions around AI tooling and coding-agent work.

## Daily Streams

- 09:05 Madrid, `GitHub AI Lab Note`: create or improve one technical note under `labs/`.
- 14:10 Madrid, `GitHub AI Recipe`: add one reusable workflow, prompt, checklist, or implementation pattern under `recipes/`.
- 20:20 Madrid, `GitHub Profile Maintenance`: update indexes, README links, and commit/push any useful changes.

## Commit Rule

No empty commits. No timestamp-only changes. No filler.

The scripts should commit only when files changed and should push only when a remote is configured.

## GitHub Setup

This machine currently needs GitHub authentication before remote publishing can work.

1. Create a public GitHub repository named exactly like your GitHub username. That special repository powers the profile README.
2. From this folder, add the remote:

   ```sh
   git remote add origin git@github.com:USERNAME/USERNAME.git
   ```

3. Configure a Git identity that matches a verified GitHub email:

   ```sh
   git config user.name "Manuel Sampedro"
   git config user.email "YOUR_VERIFIED_GITHUB_EMAIL"
   ```

4. If a local commit was created before the identity was configured, amend it:

   ```sh
   git commit --amend --reset-author
   ```

5. Push the first version:

   ```sh
   git push -u origin main
   ```

If SSH is not configured, use GitHub's HTTPS remote or install and authenticate the GitHub CLI.

## Automation Safety

Automations can prepare, commit, and push useful public artifacts. They should not:

- invent credentials,
- commit secrets,
- create fake contributions,
- publish private notes,
- claim tool results that were not verified.
