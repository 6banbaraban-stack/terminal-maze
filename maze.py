import curses
import random
import time

# Maze cell flags
N, S, E, W = 1, 2, 4, 8
OPPOSITE = {N: S, S: N, E: W, W: E}
DX = {E: 1, W: -1, N: 0, S: 0}
DY = {N: -1, S: 1, E: 0, W: 0}


def generate_maze(cols, rows):
    """Recursive backtracking maze generation."""
    grid = [[0] * cols for _ in range(rows)]
    visited = [[False] * cols for _ in range(rows)]

    def carve(cx, cy):
        visited[cy][cx] = True
        directions = [N, S, E, W]
        random.shuffle(directions)
        for d in directions:
            nx, ny = cx + DX[d], cy + DY[d]
            if 0 <= nx < cols and 0 <= ny < rows and not visited[ny][nx]:
                grid[cy][cx] |= d
                grid[ny][nx] |= OPPOSITE[d]
                carve(nx, ny)

    carve(0, 0)
    return grid


def draw_maze(stdscr, grid, px, py, cols, rows, steps, elapsed):
    stdscr.erase()
    h, w = stdscr.getmaxyx()

    # Each cell = 2 wide, 1 tall (plus borders)
    cell_w, cell_h = 2, 1
    maze_w = cols * cell_w + 1
    maze_h = rows * cell_h + 1
    ox = max(0, (w - maze_w) // 2)
    oy = max(0, (h - maze_h - 3) // 2)

    COLOR_WALL  = curses.color_pair(1)
    COLOR_PATH  = curses.color_pair(2)
    COLOR_PLAYER= curses.color_pair(3)
    COLOR_GOAL  = curses.color_pair(4)
    COLOR_UI    = curses.color_pair(5)

    for row in range(rows):
        for col in range(cols):
            cell = grid[row][col]
            sx = ox + col * cell_w
            sy = oy + row * cell_h

            # Top wall
            top = "+-" if not (cell & N) else "+ "
            if sy < h and sx + 1 < w:
                stdscr.addstr(sy, sx, top, COLOR_WALL)

            # Right wall (drawn by next cell or trailing edge)
            right_wall = " " if (cell & E) else "|"
            if sy + 1 < h and sx + cell_w < w:
                stdscr.addstr(sy + 1, sx + cell_w, right_wall, COLOR_WALL)

            # Left wall
            left_wall = "|" if not (cell & W) else " "
            if sy + 1 < h and sx < w:
                stdscr.addstr(sy + 1, sx, left_wall, COLOR_WALL)

            # Cell interior
            if row == py and col == px:
                ch, color = "@", COLOR_PLAYER
            elif row == rows - 1 and col == cols - 1:
                ch, color = "$", COLOR_GOAL
            else:
                ch, color = " ", COLOR_PATH
            if sy + 1 < h and sx + 1 < w:
                stdscr.addstr(sy + 1, sx + 1, ch + " ", color)

    # Bottom border
    bottom_y = oy + rows * cell_h
    for col in range(cols):
        sx = ox + col * cell_w
        if bottom_y < h and sx + 1 < w:
            stdscr.addstr(bottom_y, sx, "+-", COLOR_WALL)
    if bottom_y < h and ox + maze_w - 1 < w:
        stdscr.addstr(bottom_y, ox + maze_w - 1, "+", COLOR_WALL)

    # UI
    ui_y = oy + maze_h + 1
    if ui_y + 1 < h:
        stdscr.addstr(ui_y, ox, f" Steps: {steps}   Time: {elapsed:.1f}s ", COLOR_UI)
        stdscr.addstr(ui_y + 1, ox, " Arrow keys: move  |  R: restart  |  Q: quit ", COLOR_UI)


def play(stdscr, cols, rows):
    curses.curs_set(0)
    stdscr.nodelay(True)
    curses.start_color()
    curses.use_default_colors()

    curses.init_pair(1, curses.COLOR_CYAN,  -1)          # walls
    curses.init_pair(2, -1,                 -1)           # path
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLUE)   # player
    curses.init_pair(4, curses.COLOR_BLACK,  curses.COLOR_GREEN)  # goal
    curses.init_pair(5, curses.COLOR_WHITE,  curses.COLOR_BLACK)  # UI

    grid = generate_maze(cols, rows)
    px, py = 0, 0
    steps = 0
    start_time = time.time()
    won = False

    while True:
        elapsed = time.time() - start_time
        draw_maze(stdscr, grid, px, py, cols, rows, steps, elapsed)

        if won:
            h, w = stdscr.getmaxyx()
            msg = f"  You won!  {steps} steps  {elapsed:.1f}s  — R: play again  Q: quit  "
            stdscr.addstr(h // 2, max(0, (w - len(msg)) // 2), msg, curses.color_pair(4))

        stdscr.refresh()
        key = stdscr.getch()

        if key in (ord('q'), ord('Q')):
            break
        elif key in (ord('r'), ord('R')):
            grid = generate_maze(cols, rows)
            px, py = 0, 0
            steps = 0
            start_time = time.time()
            won = False
        elif not won:
            nx, ny = px, py
            cell = grid[py][px]
            if key == curses.KEY_UP    and cell & N: ny -= 1
            elif key == curses.KEY_DOWN  and cell & S: ny += 1
            elif key == curses.KEY_RIGHT and cell & E: nx += 1
            elif key == curses.KEY_LEFT  and cell & W: nx -= 1

            if (nx, ny) != (px, py):
                px, py = nx, ny
                steps += 1
                if px == cols - 1 and py == rows - 1:
                    won = True

        curses.napms(16)


def main():
    import sys
    cols = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    rows = int(sys.argv[2]) if len(sys.argv) > 2 else 12
    cols = max(5, min(cols, 40))
    rows = max(5, min(rows, 20))
    curses.wrapper(play, cols, rows)
    print("Thanks for playing Terminal Maze!")


if __name__ == "__main__":
    main()
