#!/usr/bin/env python3
import sys
import bisect

def read_all_lines():
    return [line.rstrip("\n") for line in sys.stdin]

def find_marker(lines, start, marker):
    marker_l = marker.lower()
    for i in range(start, len(lines)):
        if lines[i].strip().lower() == marker_l:
            return i
    return -1

def collect_instructions(lines, start_index, count):
    instr = []
    i = start_index
    while i < len(lines) and len(instr) < count:
        if lines[i].strip() != "":
            instr.append(lines[i])
        i += 1
    return instr, i

def parse_input(lines):
    i = 0
    while i < len(lines) and lines[i].strip() == "":
        i += 1
    N = int(lines[i].strip())
    i += 1

    idx = find_marker(lines, i, "shuffled")
    i = idx + 1
    shuffled, i = collect_instructions(lines, i, N)

    idx = find_marker(lines, i, "original")
    i = idx + 1
    original, i = collect_instructions(lines, i, N)

    return N, shuffled, original

def min_cut_insert_moves(N, shuffled, original):
    pos = {instr: idx for idx, instr in enumerate(original)}
    seq = [pos[s] for s in shuffled]

    # Find LIS length
    lis = []
    for x in seq:
        idx = bisect.bisect_left(lis, x)
        if idx == len(lis):
            lis.append(x)
        else:
            lis[idx] = x
    return N - len(lis)

def main():
    lines = read_all_lines()
    try:
        N, shuffled, original = parse_input(lines)
        print(min_cut_insert_moves(N, shuffled, original))
    except Exception:
        print(-1)

if __name__ == "__main__":
    main()
