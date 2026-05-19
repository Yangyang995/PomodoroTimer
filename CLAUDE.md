# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

A single-file desktop Pomodoro timer using Python 3 + tkinter. No external dependencies beyond the Python standard library.

## Running

```bash
python pomodoro.py
```

No build step, no virtual environment needed. Requires Python 3 with tkinter (included in the standard Windows Python installer).

## Architecture

`pomodoro.py` — single `PomodoroTimer` class, ~180 lines.

- **Timer constants** at module level: `FOCUS_SECONDS = 25 * 60`, `BREAK_SECONDS = 5 * 60`
- **Phase state machine**: `self.phase` toggles between `"focus"` and `"break"`, driven by `_on_timer_end()`
- **Tick loop**: `_tick()` decrements `self.remaining` every second via `tk.after(1000, ...)`, not threading. This avoids tkinter thread-safety issues
- **UI**: built in `_build_ui()` with Catppuccin Mocha colors (`#1e1e2e` bg, `#f38ba8` focus accent, `#a6e3a1` break accent). Progress bar drawn on a tkinter Canvas
- **Button logic**: Start disables itself and enables Pause; Pause re-enables Start; Reset stops everything and returns to focus phase

## Git remotes

- `origin` → `Yangyang995/PomodoroTimer` (public)
- `yangyang` → `lhy129/Yangyang` (public)
