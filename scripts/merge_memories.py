#!/usr/bin/env python3
"""Merge two Hermes memory files (§-delimited entries, deduplicated by content hash).

Usage: python3 merge_memories.py <local_file> <remote_file>

Writes the merged result back to <local_file>. Prints the entry count to stdout.
"""
import sys
import hashlib

def entries(path):
    with open(path, encoding='utf-8') as f:
        text = f.read()
    return [e.strip() for e in text.split('\u00a7') if e.strip()]

def main():
    if len(sys.argv) < 3:
        print("Usage: merge_memories.py <local> <remote>", file=sys.stderr)
        sys.exit(1)
    local_path = sys.argv[1]
    remote_path = sys.argv[2]
    local = entries(local_path)
    remote = entries(remote_path)
    seen = set()
    merged = []
    for e in local + remote:
        h = hashlib.md5(e.encode('utf-8')).hexdigest()
        if h not in seen:
            seen.add(h)
            merged.append(e)
    out = '\u00a7\n\n'.join(merged) + '\n'
    with open(local_path, 'w', encoding='utf-8') as f:
        f.write(out)
    print(len(merged))

if __name__ == '__main__':
    main()
