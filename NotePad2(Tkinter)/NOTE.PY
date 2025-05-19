import tkinter as tk
from tkinter import colorchooser
import win32con
import win32gui
import os
import threading
import keyboard  # Global hotkey library

class FloatingNotepad:
    def __init__(self, root):
        self.root = root
        self.root.title("Floating Notepad")
        self.root.geometry("400x300+100+100")
        self.root.attributes('-topmost', True)
        self.root.attributes('-alpha', 1)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Start hidden
        self.root.withdraw()

        # Text box with cursor customization
        self.text = tk.Text(self.root, wrap="word", font=("Calibri", 12), fg="white", bg="black", insertbackground="white", insertwidth=2)
        self.text.pack(expand=True, fill="both")

        # Controls
        self.control_frame = tk.Frame(self.root)
        self.create_controls()

        self.load_saved_text()

        # Hide from taskbar
        hwnd = win32gui.FindWindow(None, "Floating Notepad")
        ex_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, ex_style | win32con.WS_EX_TOOLWINDOW)

        # Register global hotkeys in a thread
        threading.Thread(target=self.register_hotkeys, daemon=True).start()

        # Start custom blinking cursor
        self.cursor_visible = True
        self.blink_cursor()

    def create_controls(self):
        self.control_frame.pack(side="bottom", fill="x")

        tk.Label(self.control_frame, text="Opacity").pack(side="left")
        self.opacity_slider = tk.Scale(self.control_frame, from_=30, to=100, orient="horizontal", command=self.change_opacity)
        self.opacity_slider.set(100)
        self.opacity_slider.pack(side="left")

        tk.Label(self.control_frame, text="Font Size").pack(side="left")
        self.font_size = tk.Spinbox(self.control_frame, from_=8, to=48, command=self.change_font_size)
        self.font_size.pack(side="left")

        tk.Button(self.control_frame, text="BG Color", command=self.change_bg_color).pack(side="left")
        tk.Button(self.control_frame, text="Text Color", command=self.change_fg_color).pack(side="left")
        tk.Button(self.control_frame, text="Save Now", command=self.save_text).pack(side="left")

    def register_hotkeys(self):
        keyboard.add_hotkey('ctrl+shift+1', self.show_window)
        keyboard.add_hotkey('ctrl+shift+2', self.hide_window)
        keyboard.wait()

    def show_window(self):
        def bring_to_front():
            self.root.deiconify()
            self.root.lift()
            self.root.attributes('-topmost', True)
            self.text.focus_set()
        self.root.after(0, bring_to_front)

    def hide_window(self):
        self.root.after(0, self.root.withdraw)

    def blink_cursor(self):
        if self.text.focus_get() == self.text:
            if self.cursor_visible:
                self.text.config(insertontime=0)
            else:
                self.text.config(insertontime=600)
            self.cursor_visible = not self.cursor_visible
        else:
            self.cursor_visible = True
            self.text.config(insertontime=600)

        self.root.after(600, self.blink_cursor)  # Repeat

    def change_opacity(self, value):
        self.root.attributes('-alpha', int(value) / 100.0)

    def change_font_size(self):
        size = int(self.font_size.get())
        self.text.configure(font=("Calibri", size))

    def change_bg_color(self):
        color = colorchooser.askcolor(title="Choose Background Color")[1]
        if color:
            self.text.configure(bg=color)

    def change_fg_color(self):
        color = colorchooser.askcolor(title="Choose Text Color")[1]
        if color:
            self.text.configure(fg=color)

    def save_text(self):
        with open("autosave.txt", "w", encoding="utf-8") as f:
            f.write(self.text.get("1.0", tk.END))
        print("[Saved]")

    def load_saved_text(self):
        if os.path.exists("autosave.txt"):
            with open("autosave.txt", "r", encoding="utf-8") as f:
                self.text.insert("1.0", f.read())

    def on_close(self):
        self.save_text()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = FloatingNotepad(root)
    root.mainloop()
