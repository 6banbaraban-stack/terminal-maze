# Terminal Maze

A maze game in two flavours: a browser version (`index.html`) and a terminal version (`maze.py`).

## Play in the browser

Open `index.html` in any modern browser — no install needed.

| Control | Action |
|---------|--------|
| Arrow keys or WASD | Move |
| R | New maze |

Choose a size (Small → XL) from the dropdown and reach the ★ in the bottom-right corner.

## Play in the terminal

Requires Python 3 and a terminal that supports curses (Linux/macOS).

```bash
python maze.py          # default 20×12
python maze.py 30 15    # custom width height
```

| Key | Action |
|-----|--------|
| Arrow keys | Move |
| R | Restart |
| Q | Quit |

## How it works

Both versions use **recursive backtracking** to carve a perfect maze (every cell reachable, no loops). The player starts at the top-left `(0,0)` and must reach the bottom-right goal.
