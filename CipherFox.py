#!/usr/bin/python3

'''
CipherFox - Written by Alayna Ferdarko on 18 April, 2025
Xor based encryption and decryption tool.
'''

import curses
import time
import base64
import os

# === File Directory Setup ===
SAVE_DIR = "cipherfox_data"
os.makedirs(SAVE_DIR, exist_ok=True)

# --- Core Cipher Logic ---
def xor_data(data: bytes, key: str) -> bytes:
    key_bytes = key.encode()
    return bytes([b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(data)])

def multilevel_xor(data: bytes, keys: list, encode=True) -> bytes:
    if not encode:
        keys = keys[::-1]
    for key in keys:
        data = xor_data(data, key)
    return data

def to_binary(data: bytes) -> str:
    return ''.join(format(b, '08b') for b in data)

def from_binary(binary_str: str) -> bytes:
    return bytes(int(binary_str[i:i+8], 2) for i in range(0, len(binary_str), 8))

def encode_message(message: str, keys: list, to_format="base64") -> str:
    encoded = multilevel_xor(message.encode(), keys, encode=True)
    return to_binary(encoded) if to_format == "binary" else base64.urlsafe_b64encode(encoded).decode()

def decode_message(encoded_str: str, keys: list, input_format="base64") -> str:
    data = from_binary(encoded_str) if input_format == "binary" else base64.urlsafe_b64decode(encoded_str)
    decoded = multilevel_xor(data, keys, encode=False)
    return decoded.decode(errors="ignore")

# === ASCII Splash Screen ===
CIPHERFOX_ASCII = r"""
   _______       __              ______          
  / ____(_)___  / /_  ___  _____/ ____/___  _  __
 / /   / / __ \/ __ \/ _ \/ ___/ /_  / __ \| |/_/
/ /___/ / /_/ / / / /  __/ /  / __/ / /_/ />  <  
\____/_/ .___/_/ /_/\___/_/  /_/    \____/_/|_|  
     /_/        XOR | B64 |
                Terminal Encoding Tool
                Alayna Ferdarko
"""

# === Color Pairs Initialization ===
def init_colors():
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_MAGENTA, curses.COLOR_BLACK)  # Header text
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)  # Progress bar
    curses.init_pair(6, curses.COLOR_YELLOW, curses.COLOR_BLACK)   # Highlight

# === Typewriter Effect for Text ===
def typewriter_effect(stdscr, text, y, x, delay=0.02):
    for i in range(len(text)):
        stdscr.addstr(y, x + i, text[i], curses.color_pair(2) | curses.A_BOLD)
        stdscr.refresh()
        time.sleep(delay)

# === Boot Splash Screen ===
def splash_screen(stdscr):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    lines = CIPHERFOX_ASCII.strip("\n").split("\n")
    start_y = h // 2 - len(lines) // 2

    for i, line in enumerate(lines):
        x = w // 2 - len(line) // 2
        stdscr.addstr(start_y + i, x, line, curses.color_pair(2) | curses.A_BOLD)

    stdscr.refresh()
    time.sleep(2.5)

# === Progress Bar Function ===
def draw_progress_bar(stdscr, y, x, progress):
    max_width = 40
    bar = "#" * int(progress * max_width)
    stdscr.addstr(y, x, f"[{bar:<{max_width}}] {int(progress * 100)}%", curses.color_pair(5))
    stdscr.refresh()

# === Boot Sequence with Progress Bar ===
def boot_sequence(stdscr):
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    boot_lines = [
        ("[+] Initializing XOR core...", 1),
        ("[+] Loading secret modules...", 1),
        ("[+] Syncing message encoder...", 1),
        ("[!] CipherFox interface ready.", 3)
    ]

    y_start = h // 2 - len(boot_lines) // 2
    progress = 0.0

    for idx, (line, color) in enumerate(boot_lines):
        stdscr.attron(curses.color_pair(color))
        if line == "[+] Syncing message encoder...":
            typewriter_effect(stdscr, line, y_start + idx, w // 2 - len(line) // 2)
            stdscr.attroff(curses.color_pair(color))

            for i in range(101):
                draw_progress_bar(stdscr, y_start + idx + 1, w // 2 - 20, i / 100)
                time.sleep(0.02)
        else:
            typewriter_effect(stdscr, line, y_start + idx, w // 2 - len(line) // 2)
            stdscr.attroff(curses.color_pair(color))
        time.sleep(0.6)

    stdscr.refresh()
    time.sleep(1.5)

# === Popup for History Selection ===
def popup_history(stdscr, history):
    selected = 0
    while True:
        stdscr.clear()
        stdscr.addstr(1, 2, "Secret History (← to select, → to cancel):", curses.color_pair(2))
        for idx, item in enumerate(history):
            attr = curses.color_pair(6) | curses.A_REVERSE if idx == selected else curses.color_pair(1)
            stdscr.addstr(3 + idx, 4, item, attr)
        stdscr.refresh()
        key = stdscr.getch()
        if key == curses.KEY_DOWN and selected < len(history) - 1:
            selected += 1
        elif key == curses.KEY_UP and selected > 0:
            selected -= 1
        elif key == curses.KEY_LEFT:
            return history[selected]
        elif key == curses.KEY_RIGHT:
            return None

# === Popup for File Name Input ===
def popup_filename(stdscr):
    curses.echo()
    stdscr.addstr(14, 4, "Enter save file name: ")
    stdscr.refresh()
    filename = stdscr.getstr().decode()
    curses.noecho()
    return os.path.join(SAVE_DIR, filename if filename.endswith(".txt") else filename + ".txt")

# --- Main UI for CipherFox ---
def draw_ui(stdscr):
    curses.curs_set(1)
    stdscr.clear()

    theme = 'dark'
    def set_colors():
        if theme == 'dark':
            curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
            curses.init_pair(2, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        else:
            curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
            curses.init_pair(2, curses.COLOR_MAGENTA, curses.COLOR_WHITE)
    set_colors()

    mode = "encode"
    format_type = "base64"
    message = ""
    secrets = ""
    secret_history = []

    current_field = 0
    fields = ["Mode (encode/decode): ", "Message: ", "Secrets (comma-separated): ", "Format (base64/binary): "]
    inputs = [mode, message, secrets, format_type]

    is_in_navigation_mode = True
    while True:
        stdscr.clear()
        stdscr.attron(curses.color_pair(2))
        stdscr.addstr(0, 2, "CipherFox XOR Encoder/Decoder")
        stdscr.attroff(curses.color_pair(2))
        stdscr.addstr(1, 2, "-" * 60)

        mode_status = "Navigation Mode" if is_in_navigation_mode else "Shortcut Mode"
        stdscr.addstr(2, 2, f"Current Mode: {mode_status}")

        for i, field in enumerate(fields):
            attr = curses.A_REVERSE if i == current_field else curses.color_pair(1)
            stdscr.addstr(3 + i, 4, field + inputs[i], attr)

        try:
            if inputs[2].strip() and inputs[2] not in secret_history:
                secret_history.append(inputs[2].strip())
            if inputs[0] == "encode":
                preview = encode_message(inputs[1], [k.strip() for k in inputs[2].split(",")], inputs[3])
            else:
                preview = decode_message(inputs[1], [k.strip() for k in inputs[2].split(",")], inputs[3])
        except Exception as e:
            preview = f"[Error: {str(e)}]"

        stdscr.addstr(9, 2, "Result:")
        stdscr.addstr(10, 4, preview[:curses.COLS - 8], curses.color_pair(1))

        stdscr.addstr(12, 2, "Shortcuts: ↑↓ Navigate | Enter=Exit | s=Save | l=Load | t=Theme | h=History")

        stdscr.refresh()
        key = stdscr.getch()

        if is_in_navigation_mode:
            if key == curses.KEY_DOWN and current_field < len(fields) - 1:
                current_field += 1
            elif key == curses.KEY_UP and current_field > 0:
                current_field -= 1
            elif key in (curses.KEY_BACKSPACE, 127, 8):
                inputs[current_field] = inputs[current_field][:-1]
            elif key in (10, 13):
                break
            elif 32 <= key <= 126:
                inputs[current_field] += chr(key)
            elif key == 27:
                is_in_navigation_mode = False
        else:
            if key == 27:
                is_in_navigation_mode = True
            elif key == ord('s'):
                filename = popup_filename(stdscr)
                if filename:
                    with open(filename, "w") as f:
                        f.write("[Secrets]: " + inputs[2] + "\n")
                        f.write("[Result]:\n" + preview)
                    stdscr.addstr(13, 4, f"Saved to {filename}", curses.A_DIM)
                    stdscr.refresh()
                    curses.napms(1000)
            elif key == ord('l'):
                try:
                    filename = popup_filename(stdscr)
                    with open(filename, "r") as f:
                        lines = f.readlines()
                        inputs[2] = lines[0].replace("[Secrets]: ", "").strip()
                        inputs[1] = ''.join(lines[2:]).strip()
                    stdscr.addstr(13, 4, f"Loaded from {filename}", curses.A_DIM)
                except Exception as e:
                    stdscr.addstr(13, 4, f"[Load error: {e}]", curses.A_BOLD)
                stdscr.refresh()
                curses.napms(1000)
            elif key == ord('t'):
                theme = 'light' if theme == 'dark' else 'dark'
                set_colors()
            elif key == ord('h') and secret_history:
                chosen = popup_history(stdscr, secret_history)
                if chosen:
                    inputs[2] = chosen

def main():
    def wrapped(stdscr):
        curses.curs_set(0)
        init_colors()
        splash_screen(stdscr)
        boot_sequence(stdscr)
        draw_ui(stdscr)
    curses.wrapper(wrapped)

if __name__ == "__main__":
    main()
