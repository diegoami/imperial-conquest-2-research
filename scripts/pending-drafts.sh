#!/usr/bin/env bash
# Lists ic2-conquest finding drafts that have no row in docs/findings-intake.md, or that changed
# since the commit the ledger says they were reviewed at. Read-only; reads GitHub, never a clone.
# Prints one "<draft> <branch> <why>" line per pending draft, then "pending: N".
# Usage: scripts/pending-drafts.sh        (needs gh; GH_TOKEN in CI)
set -euo pipefail
src=diegoami/ic2-conquest
ledger=${LEDGER:-$(dirname "$0")/../docs/findings-intake.md}

# ledger rows: "<draft>\t<reviewed commit>" from the first two columns.
rows=$(awk -F'|' '/^\| `/ { d=$2; c=$3; gsub(/[ `]/,"",d); gsub(/[ `]/,"",c); print d "\t" c }' "$ledger")

n=0
# One tree call per distinct branch head (many branches share one), and one compare per distinct
# version of a draft, not per branch: the cost stays small as branches pile up.
declare -A tree_cache
pairs=""   # "<branch> <draft> <blob>"
while read -r b sha; do
  if [[ -z "${tree_cache[$sha]+x}" ]]; then
    tree_cache[$sha]=$(gh api "repos/$src/git/trees/$sha?recursive=1" --jq '
      (if .truncated then "TRUNCATED x" else empty end),
      (.tree[] | select(.type=="blob" and (.path|test("^findings/.+\\.md$")) and (.path|test("/(README|PROMPT)")|not))
               | "\(.path|ltrimstr("findings/")) \(.sha)")')
    [[ ${tree_cache[$sha]} == TRUNCATED* ]] && { echo "tree of $b is truncated" >&2; exit 2; }
  fi
  while read -r draft blob; do [[ -n "$draft" ]] && pairs+="$b $draft $blob"$'\n'; done <<<"${tree_cache[$sha]}"
done < <(gh api "repos/$src/branches" --paginate --jq '.[] | "\(.name) \(.commit.sha)"')

# a draft is judged once per distinct blob: first by ledger, then by compare against the reviewed commit.
while read -r draft; do
  reviewed=$(awk -F'\t' -v d="$draft" '$1==d { print $2 }' <<<"$rows")
  if [[ -z "$reviewed" ]]; then
    echo "$draft $(awk -v d="$draft" '$2==d {print $1; exit}' <<<"$pairs") unledgered"; n=$((n+1)); continue
  fi
  while read -r b blob; do
    # changed since the reviewed commit on this branch? A compare that fails is reported, not ignored.
    if files=$(gh api "repos/$src/compare/$reviewed...$b" --jq '.files[].filename' 2>/dev/null); then
      if grep -qxF "findings/$draft" <<<"$files"; then
        echo "$draft $b changed-since-review($reviewed)"; n=$((n+1)); break
      fi
    else
      echo "$draft $b cannot-compare($reviewed)"; n=$((n+1)); break
    fi
  done < <(awk -v d="$draft" '$2==d && !seen[$3]++ { print $1, $3 }' <<<"$pairs")
done < <(awk 'NF {print $2}' <<<"$pairs" | sort -u)
echo "pending: $n"
