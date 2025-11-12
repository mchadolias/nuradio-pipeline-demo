#!/usr/bin/env bash
# clean_datafiles.sh - remove generated data and figures directories
# Usage: clean_datafiles.sh [-f|--force] [-n|--dry-run] [path1 path2 ...]
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
FORCE=0
DRY_RUN=0
ARGS=()

while (( "$#" )); do
    case "$1" in
        -f|--force) FORCE=1; shift;;
        -n|--dry-run) DRY_RUN=1; shift;;
        -h|--help) echo "Usage: $0 [-f|--force] [-n|--dry-run] [paths...]"; exit 0;;
        --) shift; while (( "$#" )); do ARGS+=("$1"); shift; done;;
        *) ARGS+=("$1"); shift;;
    esac
done

# Default targets if none provided
if [ "${#ARGS[@]}" -eq 0 ]; then
    ARGS=("$SCRIPT_DIR/data" "$SCRIPT_DIR/figures")
fi

to_delete=()
for p in "${ARGS[@]}"; do
    if [ -e "$p" ]; then
        to_delete+=("$p")
    else
        printf 'Skipping: %s (not found)\n' "$p"
    fi
done

if [ "${#to_delete[@]}" -eq 0 ]; then
    printf 'Nothing to remove.\n'
    exit 0
fi

printf 'Will remove the following:\n'
for d in "${to_delete[@]}"; do printf '  %s\n' "$d"; done

if [ "$DRY_RUN" -eq 1 ]; then
    printf 'Dry run enabled, no files will be removed.\n'
    exit 0
fi

if [ "$FORCE" -ne 1 ]; then
    read -r -p "Proceed? [y/N] " resp
    case "$resp" in
        [yY][eE][sS]|[yY]) : ;;
        *) printf 'Aborted.\n'; exit 1;;
    esac
fi

for d in "${to_delete[@]}"; do
    if [ -d "$d" ] || [ -f "$d" ] || [ -L "$d" ]; then
        rm -rf -- "$d"
        printf 'Removed: %s\n' "$d"
    else
        printf 'Skipped (not removable): %s\n' "$d"
    fi
done

exit 0