# Git Sparse-Checkout - Include Everything Except Specific Paths

To _exclude_ just a few patterns (e.g. your enterprise folders) and get **everything else**, you’ll need to switch out of “cone” mode (which only does positive includes) and use Git’s full-pattern sparse-checkout with _negative_ globs. Here’s how:

---

### 1. Reconfigure sparse-checkout for full patterns

```bash
# 1.1 Turn on sparse-checkout (if not already)
git sparse-checkout init --no-cone
```

---
### 2. Define your include/exclude list

#### **A) One-liner with `git sparse-checkout set`**

```bash
git sparse-checkout set \
  '/*' \
  '!web/src/app/ee/' \
  '!backend/ee/' \
  '!backend/tests/unit/ee/'
```
- The first pattern `/*` says “bring _everything_ in”.
- Each `!…` afterward says “but drop this path (or glob)”.

Then run:
```bash
git read-tree -mu HEAD
```

---
### 3. Verify your working tree

```bash
# Should list everything *except* your excluded patterns:
git sparse-checkout list
```

You’ll see your negative globs at the bottom, and your working directory will now contain _all_ files except the ones you explicitly excluded.

---

### 4. Future upstream merges

When you pull in changes:

```bash
git fetch upstream
git merge upstream/main
git sparse-checkout reapply   # (optional, only needed if you change your git sparse-checkout set)
```

#### If excluded paths reappear after a merge

When you merge changes from upstream, Git sometimes puts excluded files back into your working tree or keeps them tracked in the index, even though your sparse-checkout rules say they should be gone.

This can happen if:

- The upstream branch changed or deleted files you normally exclude
- You temporarily included those files to fix a merge conflict
- Git tries to update them but warns "paths exist outside of your sparse-checkout definition"

---

## **How to keep it clean**
1. **After merges:** run
   ```bash
   git sparse-checkout reapply
   ```
   → reapplies the rules and removes reintroduced files.

2. **If files get stuck in the index:** run
   ```bash
   git rm --sparse -r <path/to/excluded>
   git rm --sparse -r backend/ee
   ```
   → removes them from both the index and the working tree.
---
This tells Git:

1. "Remove these files from my index" (so Git stops tracking them in the commit you’ll make)
2. "Also delete them from my working directory" (so they disappear from your local folder)
3. "Respect sparse-checkout rules" (the --sparse flag means: only remove them if they’re outside your sparse-checkout definition)

That way any new enterprise files creeping in will be kept out of your working tree automatically.

---
