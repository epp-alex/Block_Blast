# 🟦 Block Blast: Master Edition

A fast-paced block placement puzzle game built with Python and pygame.  
Drop blocks onto the grid, clear rows and columns, and chase the highest score!

---

## 📥 Download & Run (No Python needed)

| Platform | File | Instructions |
|----------|------|--------------|
| 🪟 Windows | `block_blast.7z` | Extract with [7-Zip](https://www.7-zip.org/), run `Block_Blast.exe` |
| 🍎 macOS | `Block_Blast.dmg` | Open DMG, drag app to Applications, double-click to launch |
| 🐧 Linux | `Block_Blast.tar.gz` | `tar -xzf Block_Blast.tar.gz && ./Block_Blast` |

> **Linux note:** If the binary does not start, make it executable first:
> ```bash
> chmod +x Block_Blast
> ./Block_Blast
> ```

---

## 🎮 How to Play

- **Drag** a block from the selection area onto the grid
- **Right-click** or press **R** while dragging to rotate a block
- Clear full **rows** or **columns** to score points
- The game ends when no block can be placed anymore

### Controls

| Key / Action | Function |
|---|---|
| Drag block | Place block on grid |
| Right-click / R | Rotate block |
| P | Pause / Resume |
| R | Restart (Game Over screen) |
| Q / Esc | Quit |

---

## ✨ Features

- **14 block shapes** — sticks, squares, L-shapes, T-shapes, Z-steps, and more
- **Bomb power-up** — clears the center area of the grid, earns one per level
- **Combo system** — clear multiple lines at once to multiply your score
- **Level progression** — speed and difficulty increase every 1500 points
- **Persistent highscore** — saved locally and shown on screen
- **Particles & screen shake** — visual feedback for clears and bombs
- **Responsive layout** — adapts to any screen size and aspect ratio (16:9, 3:4, portrait)
- **Maximized window** — runs borderless fullscreen on Windows, macOS and Linux

---

## 🌍 Languages

The language can be switched in-game at any time using the buttons in the top-left corner. The choice is saved automatically and remembered on next launch.

| Language | Language |
|---|---|
| 🇩🇪 Deutsch | 🇬🇧 English |
| 🇫🇷 Français | 🇪🇸 Español |
| 🇮🇹 Italiano | 🇳🇱 Nederlands |
| 🇵🇱 Polski | 🇷🇺 Русский |
| 🇺🇦 Українська | 🇭🇺 Magyar |
| 🇹🇷 Türkçe | 🇬🇷 Ελληνικά |

### Adding a new language

Open `Block_Blast.py` and add a new entry to the `LANG` dictionary — the language button appears automatically in-game:

```python
"Français": {
    "flag_stripes": [                        # Flag as colored rectangles
        ((0,  35, 149), (0,     0, 0.333, 1.0)),  # (R,G,B), (x%, y%, w%, h%)
        ((255,255,255), (0.333, 0, 0.334, 1.0)),
        ((223, 11,  42), (0.667, 0, 0.333, 1.0)),
    ],
    "level_up":     "NIVEAU SUPÉRIEUR !",
    "game_over":    "FIN DE PARTIE",
    "restart_quit": "R = Recommencer   Q = Quitter",
    "pause":        "PAUSE (P)",
    "best":         "SCORE MAX",
    "bomb":         "BOMBE",
    "hint":         "Clic droit ou R = Pivoter",
},
```

Settings are stored per platform:

| Platform | Path |
|---|---|
| Windows | `%APPDATA%\BlockBlast\settings.json` |
| macOS | `~/Library/Application Support/BlockBlast/settings.json` |
| Linux | `~/.config/BlockBlast/settings.json` |



## 🐍 Run from Source

**Requirements:** Python 3.8+ and pygame

pip install pygame
python Block_Blast.py

## 📄 License

MIT License — free to use, modify and distribute.

<img width="1920" height="1080" alt="Screenshot 2026-06-10 085031" src="https://github.com/user-attachments/assets/77d0ff9d-1af9-42bd-bb20-a0443d7b9ca4" />

