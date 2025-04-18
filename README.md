# 🦊 CipherFox

**CipherFox** is a terminal-based XOR encoding and decoding tool with a stylized TUI (Text User Interface) built using Python's `curses` module. It supports multilevel XOR ciphers with output in either Base64 or raw binary format. Inspired by retro cyberpunk aesthetics and fox-themed flair.

Created by **Alayna Ferdarko**.

---

## 🔧 Features

- XOR encoding/decoding with multiple secrets (multilevel XOR)
- Output formats: Base64 or Binary
- Interactive curses-style UI with:
  - Typewriter splash animation
  - Secret history loader
  - File save/load system
  - Light/dark themes
  - Magenta aesthetic 🌸🦊
- Fully offline & open source

---

## 🚀 Getting Started

### Requirements

- Python 3.6+
- `curses` (via `windows-curses` on Windows)

### 📦 Installation

Clone the repository or copy the script:

```bash
git clone https://github.com/yourname/cipherfox.git
cd cipherfox
python cipherfox.py
```

### 🪟 Windows Setup

If you're using Windows, you'll need to install a compatibility package:

```bash
pip install windows-curses
```

> 💡 You must run the script in a **real terminal** like CMD, PowerShell, or Windows Terminal (not IDLE or VSCode's internal terminal).

---

## 🛠️ How to Use

Run the script:

```bash
python cipherfox.py
```

Then use the keyboard-driven interface to:

- Switch between encode/decode mode
- Input your message
- Add one or more comma-separated secrets (keys)
- Choose output format (base64 or binary)
- View the result in real-time
- Save or load from files
- Toggle light/dark themes with `t`
- View previous secrets with `h`

Shortcuts:
```
↑ ↓ : Navigate fields
← → : Interact with history menu
s   : Save current result
l   : Load from file
t   : Toggle theme
h   : View secret history
Enter : Exit program
```

---

## 📝 License

This project is licensed under the **Creative Commons Zero v1.0 Universal** license.

> You can copy, modify, distribute and use the work, even for commercial purposes, all without asking permission.

For full legal text, see: [CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/)

---

## 🙌 Acknowledgments

- ASCII art powered by vibes
- UI powered by `curses`
- Created with curiosity and caffeine

---
