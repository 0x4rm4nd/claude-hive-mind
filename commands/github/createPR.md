You are an expert developer with excellent git and GitHub workflow knowledge.

Your task is to create a pull request from the current branch to the repository’s default base branch.

### Workflow:

1. Verify the current branch is pushed to the remote:
   - If not yet pushed, run:
     ```bash
     git push --no-verify -u origin $(git branch --show-current)
     ```
   - Use `--no-verify` explicitly to skip hooks and save context tokens.
2. Infer a clear, concise, conventional PR title:
   - Start from the current branch name, converting it into human-readable form.
   - Optionally refine it using the most recent meaningful commit messages.
   - Use conventional commit prefixes if appropriate (`feat:`, `fix:`, `chore:`, etc.).
3. Read the `.github/PULL_REQUEST_TEMPLATE.md` file in the repository root.
4. Parse the template:
   - If the template contains checkboxes (e.g., `[ ] Docs updated`, `[ ] Tests added`), analyze the current changes to determine which apply.
   - Replace `[ ]` with `[x]` for each checkbox that applies to the current changes.
   - Leave other checkboxes as `[ ]`.
   - Leave the rest of the template intact.
5. Create a pull request on the remote repository with:
   - The inferred title
   - The updated PR body
   - The current branch as source
   - The default branch as target
6. Output only the PR URL or ID upon creation.

### Notes:

- Do not fabricate or assume work that was not done; only check boxes that genuinely reflect the changes.
- Do not modify or remove sections of the template beyond checking/unchecking applicable items.
- Do not include any attribution or comments.
- If the template is ambiguous or no applicable checkboxes can be determined, leave them unchecked and ask the user for clarification.
- If the remote branch is behind or diverged from the base branch, stop and alert the user to rebase first.
