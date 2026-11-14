# renpy-choice-tracker

`renpy-choice-tracker` is a lightweight, zero-configuration drop-in utility for Ren'Py visual novels. It automatically marks in-game choices by prepending `[*]` to options you have previously chosen across playthroughs, and `[ ]` to unseen options.

---

## Features

- **Persistent Tracking**: Reads Ren'Py's native `persistent._chosen` record across saves and playthroughs.
- **Clear Visual Distinction**:
  - `[*]` indicates a choice you have picked before.
  - `[ ]` indicates a brand new, unvisited choice.
- **Rollback and Restart Safe**: Guards against double-prefixing during rollbacks, skips, or script restarts.
- **Universal Compatibility**: Works across all Ren'Py 7 and 8 versions without modifying existing game scripts or UI screen files.
- **Zero Styling Dependencies**: Uses plain text brackets without custom fonts, color tags, screen overlays, or hotkeys.
- **Configurable**: Easily customize prefixes to any indicator string you prefer.

---

## Installation & Setup

1. Copy `renpy_choice_tracker.rpy` into your Ren'Py project's `game/` directory:
   ```bash
   cp renpy_choice_tracker.rpy /path/to/renpy-project/game/
   ```

2. Launch your game normally. That is all: choice menus will now display indicators automatically.

3. To uninstall, delete `renpy_choice_tracker.rpy` (and the generated `.rpyc` file) from your `game/` folder.

---

## Visual Example

When encountering a choice menu during gameplay:

### Default Game Script
```renpy
menu:
    "Ask Alice about the missing key":
        jump alice_key
    "Search the library quietly":
        jump library_search
    "Leave the estate immediately":
        jump leave_estate
```

### In-Game Choice Menu Display
```text
┌──────────────────────────────────────────────────┐
│  [*] Ask Alice about the missing key             │
│  [ ] Search the library quietly                  │
│  [ ] Leave the estate immediately                │
└──────────────────────────────────────────────────┘
```

In the example above, "Ask Alice about the missing key" was selected in a previous playthrough, while the other two options remain unvisited.

---

## Configuration

To customize prefix symbols, edit the constants near the top of `renpy_choice_tracker.rpy`:

```python
init 999 python:
    # Remember: in Ren'Py text, '[[' escapes to a literal '['
    RCT_SEEN_PREFIX = "[[*] "   # Previously chosen: displays as [*]
    RCT_NEW_PREFIX  = "[[ ] "   # Never chosen: displays as [ ]
```

For example, to use arrows instead:
```python
    RCT_SEEN_PREFIX = "> "
    RCT_NEW_PREFIX  = "  "
```

