#!/usr/bin/env python3
import sys

filename = sys.argv[1] if len(sys.argv) > 1 else "requirements.txt"

platform_marker = '; platform_system == "Windows"'

with open(filename, 'r') as f:
    lines = f.readlines()

changed = False
new_lines = []
for line in lines:
    stripped = line.strip()
    if stripped.startswith('pywin32==') and platform_marker not in stripped:
        # Add platform marker
        line = line.rstrip('\n') + platform_marker + '\n'
        changed = True
    new_lines.append(line)

if changed:
    with open(filename, 'w') as f:
        f.writelines(new_lines)
    print(f"Fixed {filename}: added platform marker to pywin32")

# Exit 0 to allow commit (pre-commit expects exit 0 on success)
sys.exit(0)
