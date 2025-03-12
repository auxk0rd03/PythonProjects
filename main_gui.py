import tkinter as tk
from tkinter import filedialog, scrolledtext
import subprocess
import threading
import os

class PythonScriptLauncher:
    def __init__(self, root, bg_color="#282c34", text_color="#ffffff"):  # Default colors
        self.root = root
        self.root.title("Python Script Launcher")
        self.process = None
        self.bg_color = bg_color
        self.text_color = text_color
        
        self.root.configure(bg=self.bg_color)
        
        # UI Elements
        self.run_button = tk.Button(root, text="Run Script", command=self.run_script, bg=self.bg_color, fg=self.text_color)
        self.run_button.pack(pady=5)
        
        self.stop_button = tk.Button(root, text="Stop Script", command=self.stop_script, state=tk.DISABLED, bg=self.bg_color, fg=self.text_color)
        self.stop_button.pack(pady=5)
        
        self.terminal = scrolledtext.ScrolledText(root, height=15, width=80, state=tk.DISABLED, bg="#1e1e1e", fg=self.text_color, insertbackground=self.text_color)
        self.terminal.pack(padx=10, pady=10)
    
    def run_script(self):
        file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
        if not file_path:
            return
        
        if self.process:
            self.append_terminal("Another script is already running. Stop it first.\n")
            return
        
        self.append_terminal(f"Running: {file_path}\n")
        self.stop_button.config(state=tk.NORMAL)
        
        def target():
            self.process = subprocess.Popen(
                ["python", file_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            for line in iter(self.process.stdout.readline, ''):
                self.append_terminal(line)
            self.process.stdout.close()
            self.process.wait()
            self.process = None
            self.stop_button.config(state=tk.DISABLED)
        
        threading.Thread(target=target, daemon=True).start()
    
    def stop_script(self):
        if self.process:
            self.process.terminate()
            self.append_terminal("Script terminated.\n")
            self.process = None
            self.stop_button.config(state=tk.DISABLED)
    
    def append_terminal(self, text):
        self.terminal.config(state=tk.NORMAL)
        self.terminal.insert(tk.END, text)
        self.terminal.config(state=tk.DISABLED)
        self.terminal.yview(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = PythonScriptLauncher(root)
    root.mainloop()
