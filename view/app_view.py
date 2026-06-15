import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime


class AppView(tk.Tk):
    """All tkinter UI lives here."""

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("Smart File Organizer")
        self.geometry("600x450")
        self.resizable(False, False)
        self._build_ui()

    def _build_ui(self) -> None:
        self.configure(padx=20, pady=20)

        # Folder row
        folder_frame = ttk.Frame(self)
        folder_frame.pack(fill="x", pady=(0, 12))

        self.folder_var = tk.StringVar(value="No folder selected")
        ttk.Label(folder_frame, textvariable=self.folder_var,
                  foreground="gray").pack(side="left", fill="x", expand=True)
        ttk.Button(folder_frame, text="Browse…",
                   command=self._on_browse).pack(side="right")

        # Buttons
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill="x", pady=(0, 12))

        self.btn_start = ttk.Button(btn_frame, text="▶  Organize",
                                    command=self._on_organize, state="disabled")
        self.btn_start.pack(side="left", padx=(0, 8))

        self.btn_undo = ttk.Button(btn_frame, text="↩  Undo",
                                   command=self._on_undo, state="disabled")
        self.btn_undo.pack(side="left")

        # Log area
        ttk.Label(self, text="Activity log").pack(anchor="w")
        self.log_box = tk.Text(self, height=16, width=60,
                               state="disabled", relief="flat",
                               background="#f5f5f5", font=("Courier", 10))
        self.log_box.pack(fill="both", expand=True)

    def _on_browse(self) -> None:
        folder = filedialog.askdirectory(title="Select a folder to organize")
        if folder:
            self.controller.set_folder(folder)
            self.folder_var.set(folder)
            self.btn_start.config(state="normal")
            self._append_log(f"Folder selected: {folder}")

    def _on_organize(self) -> None:
        moved, error = self.controller.run_organize()
        if error:
            messagebox.showerror("Error", error)
            return
        for item in moved:
            filename = item.source.split("\\")[-1]
            self._append_log(f"Moved: {filename}  →  {item.category}/")
        self._append_log(f"--- Done: {len(moved)} file(s) moved ---")
        self.btn_undo.config(
            state="normal" if self.controller.has_history() else "disabled"
        )

    def _on_undo(self) -> None:
        undone, error = self.controller.run_undo()
        if error:
            messagebox.showinfo("Undo", error)
            return
        for item in undone:
            filename = item.source.split("\\")[-1]
            self._append_log(f"Restored: {filename}")
        self._append_log(f"--- Undo complete: {len(undone)} file(s) restored ---")
        self.btn_undo.config(state="disabled")

    def _append_log(self, message: str) -> None:
        ts = datetime.now().strftime("%H:%M:%S")
        self.log_box.config(state="normal")
        self.log_box.insert("end", f"[{ts}] {message}\n")
        self.log_box.see("end")
        self.log_box.config(state="disabled")
