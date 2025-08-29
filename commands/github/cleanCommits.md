You are an expert software engineer with advanced git knowledge.

Your task is to rewrite the **commit history of the current branch only — starting from its divergence point with the base (mother) branch — leaving the mother branch completely untouched**, cleaning up authorship and commit messages without altering the file content, commit order, or dates.

### Scope:

🚨 **Only rewrite commits that exist on the current branch beyond the common ancestor with the base branch. Do NOT modify or rewrite history of the mother/base branch. Leave the mother branch untouched.**

### Preliminary step:

🔍 Determine the commit hash of the most recent common ancestor (merge base) between the current branch and the base branch (e.g., `main`, `develop`):

```bash
git merge-base <base-branch> HEAD
```

where <base-branch> is the name of the mother branch. This is the point where the two branches diverged.
From this point onward (exclusive), only rewrite commits that belong to the current branch.

### Verification and Validation:

✅ Ensure every commit in the current branch beyond the merge-base has only one author and one committer: the current git user as configured in git (git config user.name and git config user.email)
✅ Remove all co-author metadata and attribution from commit messages.
✅ Remove the line 🤖 Generated with [Claude Code](https://claude.ai/code) from commit messages.
✅ Confirm that no unrelated changes were introduced.
✅ Confirm that the branch contents remain identical to pre-cleaning.
✅ Confirm that the mother branch’s history is not modified in any way.
✅ Confirm that the current branch now has clean, properly authored commits with no extraneous metadata.

### Notes:

Do NOT touch or rewrite the mother branch. Only operate on the commits that exist solely on the current branch since divergence.
Do not output any list of commits, diffs, or other content.
Only output a single, clear statement confirming that the cleaning has been completed and validated successfully.
If the cleaning cannot be fully validated, output a clear error and request user intervention.

### ⚠️ Critical Warning - git-filter-repo Usage:

**DANGER**: `git-filter-repo` without proper constraints will rewrite the ENTIRE repository history, not just the target branch. This can cause catastrophic data loss.

**What went wrong in previous attempt:**
- Used `git-filter-repo --message-callback` without proper branch limiting
- Despite using `--refs feat/unified-memory-bridge ^main`, the tool processed all 1247 commits in the repository
- This rewrote the entire repository history, changing all commit SHAs throughout the project
- Recovery required resetting all branches to their remote origins

**Safer alternatives for commit message cleaning:**
1. **Interactive rebase** (preferred for small number of commits):
   ```bash
   git rebase -i $(git merge-base main HEAD)
   # Manually edit each commit message during rebase
   ```

2. **Targeted git-filter-repo with extreme caution**:
   ```bash
   # ALWAYS test on a separate clone first
   # Create backup branches for ALL branches before running
   git branch backup-main main
   git branch backup-feature-branch feature-branch
   
   # Use very specific targeting
   git filter-repo --force --refs HEAD ^main --message-callback 'script'
   ```

3. **Manual commit amendment** (safest for recent commits):
   ```bash
   # For the last few commits, amend them individually
   git commit --amend -m "cleaned message"
   git rebase --continue
   ```

**Recovery procedure if git-filter-repo damages entire repository:**
1. Stop immediately
2. Do NOT push any changes
3. Re-clone repository from remote: `git clone <remote-url> <new-directory>`
4. Cherry-pick or manually re-apply only the necessary changes
5. Use safer methods for commit message cleaning

**Prevention:**
- ALWAYS work on a separate clone when using git-filter-repo
- Test the command on a single commit first
- Verify the commit count before and after the operation
- Check that only the target branch commits were modified
