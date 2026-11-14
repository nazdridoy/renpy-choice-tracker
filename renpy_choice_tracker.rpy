# Copyright (c) 2026 nazDridoy
# SPDX-License-Identifier: MIT
#
# renpy-choice-tracker
# ===========================================================================
# Drop-in Ren'Py choice tracker: prepends [*] to previously chosen choices
# and [ ] to unseen ones across playthroughs.
#
# Compatible with all Ren'Py 7 and 8 versions.
# Requires no colors, font tags, overlays, hotkeys, or complex classes.
#
# Install: Drop this file into the game's `game/` folder.
# Remove:  Delete this file (and .rpyc).
# ===========================================================================

init 999 python:
    """
    renpy-choice-tracker
    ================================
    Prepends [*] to previously chosen choices and [ ] to unseen ones.
    """

    # Configurable text prefixes
    # Note: in Ren'Py text, '[[' escapes to a literal '[' so Ren'Py
    # does not confuse [ ] with python variable interpolation.
    # Displays visually in-game as: [*] and [ ]
    RCT_SEEN_PREFIX = "[[*] "   # Previously chosen: displays as [*]
    RCT_NEW_PREFIX  = "[[ ] "   # Never chosen: displays as [ ]

    # Backwards compatibility alias
    UCT_SEEN_PREFIX = RCT_SEEN_PREFIX
    UCT_NEW_PREFIX  = RCT_NEW_PREFIX

    # Save original menu handlers
    _rct_orig_store_menu = getattr(renpy.store, "menu", None)
    _rct_orig_display_menu = getattr(renpy.exports, "display_menu", None)

    def _rct_process(items):
        if not items:
            return items

        try:
            chosen = getattr(renpy.game.persistent, "_chosen", {})
            loc = getattr(renpy.game.context(), "current", None)
        except Exception:
            chosen, loc = {}, None

        new_items = []
        for item in items:
            try:
                cap = item[0] if isinstance(item, (list, tuple)) else getattr(item, "caption", None)
                if not cap or not isinstance(cap, (str, type(u""))):
                    new_items.append(item)
                    continue

                # Don't double-prefix on rollback or restart
                if (cap.startswith(RCT_SEEN_PREFIX) or cap.startswith(RCT_NEW_PREFIX)
                        or cap.startswith("[*] ") or cap.startswith("[ ] ")):
                    new_items.append(item)
                    continue

                # Check if this choice was picked before at this menu location
                is_seen = False
                if chosen and loc:
                    for (c_loc, c_cap) in chosen:
                        if c_loc == loc and cap in c_cap:
                            is_seen = True
                            break

                prefix = RCT_SEEN_PREFIX if is_seen else RCT_NEW_PREFIX

                if isinstance(item, tuple):
                    new_items.append((prefix + cap,) + item[1:])
                elif isinstance(item, list):
                    new_items.append([prefix + cap] + item[1:])
                elif hasattr(item, "caption"):
                    item.caption = prefix + cap
                    new_items.append(item)
                else:
                    new_items.append(item)
            except Exception:
                new_items.append(item)

        return new_items

    def _rct_menu(items, *args, **kwargs):
        try:
            items = _rct_process(items)
        except Exception:
            pass

        if _rct_orig_store_menu:
            return _rct_orig_store_menu(items, *args, **kwargs)
        elif _rct_orig_display_menu:
            return _rct_orig_display_menu(items, *args, **kwargs)
        return items

    # Install the hook
    if hasattr(renpy.store, "menu"):
        renpy.store.menu = _rct_menu
    if hasattr(renpy.exports, "display_menu"):
        renpy.exports.display_menu = _rct_menu
        renpy.display_menu = _rct_menu

