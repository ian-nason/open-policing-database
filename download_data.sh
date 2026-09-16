#!/usr/bin/env bash
# Stanford Open Policing Project: one zipped CSV of standardized stops per location.
# https://openpolicing.stanford.edu/data/  (manifest: download_list.txt, 88 files, ~4.8 GB)
set -uo pipefail
cd "$(dirname "$0")"
mkdir -p data/raw
failed=0
while read -r url; do
  [[ -z "$url" ]] && continue
  f="data/raw/$(basename "$url")"
  [[ -s "$f" ]] && continue
  curl --fail -L --retry 5 --retry-delay 15 -sS -A "Mozilla/5.0 (datapond-maintenance)" -o "$f.part" "$url" \
    && python3 -c "import zipfile,sys; sys.exit(0 if zipfile.is_zipfile('$f.part') else 1)" \
    && mv "$f.part" "$f" && echo "ok $f $(stat -c %s "$f")" || { rm -f "$f.part"; echo "FAIL $f" >&2; failed=$((failed + 1)); }
done < download_list.txt
if [[ $failed -gt 0 ]]; then echo "$failed download(s) failed" >&2; exit 1; fi
