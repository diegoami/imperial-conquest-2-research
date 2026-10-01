#!/usr/bin/env bash
# Lists ic2-conquest finding drafts that have no row in docs/findings-intake.md, or that changed
# since the commit the ledger says they were reviewed at. Read-only; reads GitHub, never a clone.
# Prints one "<draft> <branch> <why>" line per pending draft, then "pending: N".
# Usage: scripts/pending-drafts.sh        (needs gh, jq; GH_TOKEN in CI)
set -euo pipefail
src=diegoami/ic2-conquest
ledger=${LEDGER:-$(dirname "$0")/../docs/findings-intake.md}

# ledger rows: "<draft>\t<reviewed commit>" from the first two columns.
rows=$(awk -F'|' '/^\| `/ { d=$2; c=$3; gsub(/[ `]/,"",d); gsub(/[ `]/,"",c); print d "\t" c }' "$ledger")

n=0
# one "<branch> <path>" line per draft per branch.
pairs=$(gh api "repos/$src/branches" --paginate --jq '.[] | "\(.name) \(.commit.sha)"' | while read -r b sha; do
  gh api "repos/$src/git/trees/$sha?recursive=1" --jq '.tree[] | select(.type=="blob") | .path' |
    grep -E '^findings/.+\.md$' | grep -v -e '/README' -e '/PROMPT' | sed "s|^findings/||; s|^|$b |"
done)

# a draft on several branches is judged once: first by ledger, then by the branch with the newest head.
while read -r draft; do
  reviewed=$(awk -F'\t' -v d="$draft" '$1==d { print $2 }' <<<"$rows")
  branches=$(awk -v d="$draft" '$2==d { print $1 }' <<<"$pairs")
  if [[ -z "$reviewed" ]]; then
    echo "$draft $(head -1 <<<"$branches") unledgered"; n=$((n+1)); continue
  fi
  for b in $branches; do
    # changed since the reviewed commit on this branch? A compare that fails is reported, not ignored.
    if files=$(gh api "repos/$src/compare/$reviewed...$b" --jq '.files[].filename' 2>/dev/null); then
      if grep -qxF "findings/$draft" <<<"$files"; then
        echo "$draft $b changed-since-review($reviewed)"; n=$((n+1)); break
      fi
    else
      echo "$draft $b cannot-compare($reviewed)"; n=$((n+1)); break
    fi
  done
done < <(awk '{print $2}' <<<"$pairs" | sort -u)
echo "pending: $n"
