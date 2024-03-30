import tkinter as tk
from tkinter import filedialog, messagebox
import json

class JsonEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Minecraft Stats Editor")
        try:
            self.root.iconbitmap("assets/MCJson.ico")
        except tk.TclError:
            pass

        self.root.geometry("550x100")
        self.root.configure(padx=10, pady=10)
        self.load_button = tk.Button(root, text="Open Stats JSON File (Located in: AppData\Roaming\.minecraft\saves\<world name>\stats)", command=self.open_file)
        self.load_button.pack()

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'r') as file:
                self.data = json.load(file)
            self.load_button.destroy()
            self.create_editor()

    def create_editor(self):
        self.root.geometry("400x400")
        self.stats_frame = tk.Frame(self.root)
        self.stats_frame.pack(fill=tk.BOTH, expand=True)
        self.canvas = tk.Canvas(self.stats_frame)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar = tk.Scrollbar(self.stats_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.inner_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor=tk.NW)

        for category, stats in self.data['stats'].items():
            category_label = tk.Label(self.inner_frame, text=category, font=("Arial", 12, "bold"), padx=10, pady=5)
            category_label.pack()
            for stat, value in stats.items():
                stat_frame = tk.Frame(self.inner_frame)
                stat_frame.pack()
                tk.Label(stat_frame, text=stat).pack(side=tk.LEFT)
                entry = tk.Entry(stat_frame)
                entry.insert(0, str(value))
                entry.pack(side=tk.LEFT)
                setattr(self, f"{category}_{stat}", entry)

        self.root.bind('<MouseWheel>', self.on_mousewheel)

        save_button = tk.Button(self.root, text="Save Changes", command=self.save_changes)
        save_button.pack()

    def save_changes(self):
        for category, stats in self.data['stats'].items():
            for stat, value in stats.items():
                entry = getattr(self, f"{category}_{stat}")
                self.data['stats'][category][stat] = int(entry.get())

        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'w') as file:
                json.dump(self.data, file, indent=4)
            messagebox.showinfo("Saved", "Changes Saved!")

    def on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

def main():
    root = tk.Tk()
    app = JsonEditorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
