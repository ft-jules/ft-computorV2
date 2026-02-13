import tkinter as tk
from tkinter import scrolledtext
import sys
import io

from src.lexer.lexer import Lexer
from src.parser.parser import Parser

class ComputorGui:
    def __init__(self, context):
        self.ctx = context
        self.root = tk.Tk()
        self.root.title("ComputorV2 - Interactive Console")
        self.root.geometry("700x500")
        self.root.configure(bg="#1e1e1e") # fond sombre
        self.font = ("monospace", 12)
        self.build_ui()

    def build_ui(self):
        input_frame = tk.Frame(self.root, bg="#1e1e1e")
        input_frame.pack(side=tk.BOTTOM, fill='x', padx=10, pady=10)

        tk.Label(input_frame, text="> ", bg="#1e1e1e", fg="#569cd6", font=self.font).pack(side=tk.LEFT)

        self.input_entry = tk.Entry(
            input_frame,
            bg="#2d2d2d",
            fg="white",
            font=self.font,
            insertbackground="white",
            relief=tk.FLAT
        )
        self.input_entry.pack(side=tk.LEFT, expand=True, fill='x', padx=5, ipady=5)
        
        self.root.after(100, self.input_entry.focus)
        self.input_entry.bind("<Return>", self.process_input)

        self.output_area = scrolledtext.ScrolledText(
            self.root,
            wrap=tk.WORD,
            bg="#1e1e1e",
            fg="#d4d4d4",
            font=self.font,
            padx=10, pady=10,
            insertbackground="white"
        )
        self.output_area.pack(side=tk.TOP, expand=True, fill='both', padx=10, pady=(10, 0))
        self.output_area.insert(tk.END, "Welcome to ComputorV2 GUI!\nType your expression and press Enter.\n" + "="*40 + "\n\n")
        self.output_area.config(state=tk.DISABLED)

    def print_to_output(self, text, is_input=False):
        self.output_area.config(state=tk.NORMAL)
        if is_input:
            self.output_area.insert(tk.END, f"> {text}\n", "input")
            self.output_area.tag_config("input", foreground="#569cd6") # Bleu pour l'input
        else:
            self.output_area.insert(tk.END, f"{text}\n\n", "output")
            self.output_area.tag_config("output", foreground="#ce9178") # Orange pour le résultat
        
        self.output_area.see(tk.END)
        self.output_area.config(state=tk.DISABLED)

    def process_input(self, event=None):
        text = self.input_entry.get().strip()
        if not text:
            return

        if text.lower() in ['exit', 'quit']:
            self.root.destroy()
            return

        self.input_entry.delete(0, tk.END)
        self.print_to_output(text, is_input=True)

        # Redirection de print vers interface
        capture = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = capture

        try:
            import main 

            if '?' in text:
                main.handle_equation(text, self.ctx)
            else:
                lexer = Lexer(text)
                parser = Parser(lexer, self.ctx)
                result = parser.parse()
                if result is not None:
                    print(result)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            sys.stdout = old_stdout

        result_str = capture.getvalue().strip()
        if result_str:
            self.print_to_output(result_str)

    def run(self):
        self.root.mainloop()