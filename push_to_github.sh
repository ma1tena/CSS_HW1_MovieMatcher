#!/usr/bin/env bash
#
# push_to_github.sh
# Quick helper to commit and push all changes to GitHub.
#
# Usage:
#   ./push_to_github.sh "Your commit message"
#
# If no message is given, a default one with a timestamp is used.
#
# Run this from the root of the repo (CSS_HW1_MovieMatcher/).

set -e  # stop immediately if any command fails

COMMIT_MESSAGE="${1:-"Update: $(date '+%Y-%m-%d %H:%M')"}"

# Files that should NEVER be committed (large raw data / ML artifacts).
# .gitignore should already block these, but we double-check here so a
# broken .gitignore rule doesn't silently commit a 1GB+ file.
RISKY_PATTERNS=(
  "backend/data/raw/*.tsv"
  "backend/data/raw/*.tsv.gz"
  "backend/ml/*.pkl"
  "backend/ml/*.parquet"
)

echo "Checking working tree status..."
git status --short

echo ""
echo "Checking for large/raw files that should not be committed..."
FOUND_RISKY=false
for pattern in "${RISKY_PATTERNS[@]}"; do
  # shellcheck disable=SC2086
  if git status --short | grep -E "$(basename "$pattern" | sed 's/\*/.*/')" > /dev/null 2>&1; then
    echo "  WARNING: files matching '$pattern' appear in git status."
    FOUND_RISKY=true
  fi
done

if [ "$FOUND_RISKY" = true ]; then
  echo ""
  echo "Stop: it looks like raw data or model files are about to be committed."
  echo "Check your .gitignore before continuing. Aborting."
  exit 1
fi

echo ""
echo "Staging all changes..."
git add .

# If there is nothing to commit, exit cleanly instead of failing on git commit.
if git diff --cached --quiet; then
  echo "Nothing to commit — working tree already matches the last commit."
  exit 0
fi

echo "Committing with message: \"$COMMIT_MESSAGE\""
git commit -m "$COMMIT_MESSAGE"

echo "Pushing to origin..."
git push

echo ""
echo "Done. Changes are on GitHub."
