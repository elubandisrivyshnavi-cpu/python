#!/usr/bin/env python3
import sys

def read_all_lines():
    return [line.rstrip("\n") for line in sys.stdin]

def find_marker(lines, start, marker):
    marker_l = marker.lower()
    i = start
    while i < len(lines):
        if lines[i].strip().lower() == marker_l:
            return i
        i += 1
    return -1

def collect_instructions(lines, start_index, count):
    instr = []
    i = start_index
    while i < len(lines) and len(instr) < count:
        # Accept lines even if they are blank as instructions only if necessary,
        # but commonly blank separator lines should be skipped.
        # We'll skip lines that are exactly empty (after stripping) until we gather count.
        if lines[i].strip() != "":
            instr.append(lines[i])
        i += 1
    if len(instr) < count:
        # try to include empty lines if not enough (fallback)
        i = start_index
        instr = []
        while i < len(lines) and len(instr) < count:
            instr.append(lines[i])
            i += 1
    return instr, i

def parse_input(lines):
    i = 0
    # skip leading blank lines
    while i < len(lines) and lines[i].strip() == "":
        i += 1
    if i >= len(lines):
        raise ValueError("No input")
    # read N
    try:
        N = int(lines[i].strip())
    except Exception:
        raise ValueError("First non-empty line must be integer N")
    i += 1
    # find 'shuffled'
    idx = find_marker(lines, i, "shuffled")
    if idx == -1:
        raise ValueError("Missing 'shuffled' marker")
    i = idx + 1
    shuffled, i = collect_instructions(lines, i, N)
    if len(shuffled) != N:
        raise ValueError("Insufficient shuffled instructions")
    # find 'original'
    idx = find_marker(lines, i, "original")
    if idx == -1:
        raise ValueError("Missing 'original' marker")
    i = idx + 1
    original, i = collect_instructions(lines, i, N)
    if len(original) != N:
        raise ValueError("Insufficient original instructions")
    return N, shuffled, original

def min_cut_insert_moves(N, shuffled, original):
    pos = {}
    for idx, instr in enumerate(original):
        # use exact instruction strings (after rstrip) for mapping
        pos[instr.rstrip("\n")] = idx
    try:
        perm = tuple(pos[s.rstrip("\n")] for s in shuffled)
    except KeyError:
        # If some instruction in shuffled not in original, impossible
        return -1
    target = tuple(range(N))
    if perm == target:
        return 0

    # BFS using list-as-queue to avoid relying on collections
    queue = [perm]
    head = 0
    dist = {perm: 0}
    while head < len(queue):
        cur = queue[head]
        head += 1
        d = dist[cur]
        for i in range(N):
            for j in range(i, N):
                seg = cur[i:j+1]
                rest = cur[:i] + cur[j+1:]
                for k in range(len(rest) + 1):
                    if k == i:
                        continue
                    new = rest[:k] + seg + rest[k:]
                    if new == target:
                        return d + 1
                    if new not in dist:
                        dist[new] = d + 1
                        queue.append(new)
    return -1

def main():
    lines = read_all_lines()
    try:
        N, shuffled, original = parse_input(lines)
    except Exception:
        print(-1)
        return
    print(min_cut_insert_moves(N, shuffled, original))

if __name__ == "__main__":
    main()

   
