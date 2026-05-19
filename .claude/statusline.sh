#!/bin/bash
input=$(cat)

model=$(echo "$input" | sed -n 's/.*"display_name"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')
cwd=$(echo "$input" | sed -n 's/.*"current_dir"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')
used_pct=$(echo "$input" | sed -n 's/.*"used_percentage"[[:space:]]*:[[:space:]]*\([0-9.]*\).*/\1/p')

[ -z "$model" ] && model="Claude"
[ -z "$cwd" ] && cwd="."
used_int=$(printf "%.0f" "${used_pct:-0}")

printf "%s | %s | ctx %d%%" "$model" "$(basename "$cwd")" "$used_int"
