import time
import os
from typing import List, Dict

# ----------------------------------------
# Tower of Hanoi Visualizer (ASCII)
# ----------------------------------------

def clear_screen():
    # Cross-platform clear (optional; comment out if you don't want clearing)
    os.system('cls' if os.name == 'nt' else 'clear')

def render_towers(pegs: Dict[str, List[int]], n_disks: int, move_no: int):
    """Render the three pegs with ASCII disks.
    Smallest disk has width 1, disk k has width = 2*k - 1.
    """
    names = ['A', 'B', 'C']
    max_width = 2 * n_disks - 1
    rod = '|'

    # Build a height-aligned copy (top at index 0 visually)
    padded = {}
    for name in names:
        stack = pegs[name][:]
        # pad with zeros (empty spots) on top so each has length n_disks
        padded[name] = [0] * (n_disks - len(stack)) + stack

    print(f"Move #{move_no}")
    print("=" * (max_width * 3 + 8))
    # Print levels from top (0) to bottom (n_disks-1)
    for level in range(n_disks):
        line_parts = []
        for name in names:
            disk = padded[name][level]
            if disk == 0:
                # empty: show rod centered
                spaces = ' ' * ((max_width - 1) // 2)
                part = spaces + rod + spaces
            else:
                width = 2 * disk - 1
                pad = (max_width - width) // 2
                part = ' ' * pad + '=' * width + ' ' * pad
            line_parts.append(part)
        print("  ".join(line_parts))
    # Base + labels
    base = '-' * max_width
    print(f"{base}  {base}  {base}")
    label_parts = []
    for name in names:
        center_pad = (max_width - 1) // 2
        label_parts.append(' ' * center_pad + name + ' ' * center_pad)
    print("  ".join(label_parts))
    print("=" * (max_width * 3 + 8))
    print()

def move_disk(pegs: Dict[str, List[int]], src: str, dst: str):
    pegs[dst].append(pegs[src].pop())

def hanoi(n: int, src: str, aux: str, dst: str, pegs: Dict[str, List[int]],
          n_disks: int, delay: float, move_counter: List[int], step_mode: bool):
    """Recursive Tower of Hanoi."""
    if n == 0:
        return
    hanoi(n - 1, src, dst, aux, pegs, n_disks, delay, move_counter, step_mode)
    move_disk(pegs, src, dst)
    move_counter[0] += 1
    clear_screen()
    render_towers(pegs, n_disks, move_counter[0])
    if step_mode:
        input("Press Enter for next move...")
    else:
        time.sleep(delay)
    hanoi(n - 1, aux, src, dst, pegs, n_disks, delay, move_counter, step_mode)

def run_visualizer():
    print("=== Tower of Hanoi Visualizer (ASCII) ===")
    try:
        n = int(input("Number of disks (e.g., 3-8) [default 4]: ") or 4)
    except ValueError:
        n = 4
    n = max(1, min(n, 10))  # keep it reasonable for terminal

    mode = (input("Mode: (a)uto or (s)tep-by-step? [a/s, default a]: ").strip().lower() or 'a')
    step_mode = (mode == 's')

    delay = 0.5
    if not step_mode:
        try:
            delay = float(input("Auto delay per move in seconds [default 0.5]: ") or 0.5)
        except ValueError:
            delay = 0.5

    # Initialize pegs: A has all disks (largest at bottom), B and C empty
    pegs = {
        'A': list(range(n, 0, -1)),  # [n, n-1, ..., 1] top is end of list
        'B': [],
        'C': []
    }

    move_counter = [0]  # use list to mutate inside recursion

    clear_screen()
    print("Initial State:\n")
    render_towers(pegs, n, move_counter[0])
    if step_mode:
        input("Press Enter to start...")

    # Solve: move from A to C using B
    hanoi(n, 'A', 'B', 'C', pegs, n, delay, move_counter, step_mode)

    print(f"✅ Completed in {move_counter[0]} moves (optimal = {2**n - 1}).")

if __name__ == "__main__":
    run_visualizer()
