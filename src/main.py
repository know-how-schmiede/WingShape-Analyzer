import os
import customtkinter as ctk
from tkinter import filedialog, messagebox

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from analyzer import AirfoilParser, AirfoilData
from version import VERSION


class WingShapeApp(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()

        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.title(f"WingShape-Analyzer v{VERSION}")
        self.geometry("1200x720")
        self.minsize(900, 600)

        self.current_data: AirfoilData | None = None

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = ctk.CTkFrame(self, width=200)
        self.sidebar.grid(row=0, column=0, sticky="nsw", padx=(12, 6), pady=12)
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=6, pady=12)
        self.status_frame = ctk.CTkFrame(self, width=220)
        self.status_frame.grid(row=0, column=2, sticky="nse", padx=(6, 12), pady=12)

        self._build_sidebar()
        self._build_plot()
        self._build_status_panel()

    def _build_sidebar(self) -> None:
        title = ctk.CTkLabel(
            self.sidebar,
            text="WingShape-Analyzer",
            font=ctk.CTkFont(size=18, weight="bold"),
        )
        title.pack(padx=16, pady=(16, 12), anchor="w")

        self.file_label = ctk.CTkLabel(
            self.sidebar,
            text="No file loaded",
            wraplength=180,
            justify="left",
        )
        self.file_label.pack(padx=16, pady=(0, 18), anchor="w")

        self.load_button = ctk.CTkButton(
            self.sidebar,
            text="Load Airfoil",
            command=self.load_file,
        )
        self.load_button.pack(padx=16, pady=(0, 10), fill="x")

        self.export_button = ctk.CTkButton(
            self.sidebar,
            text="Export CSV",
            command=self.export_csv,
            state="disabled",
        )
        self.export_button.pack(padx=16, pady=(0, 10), fill="x")

        hint = ctk.CTkLabel(
            self.sidebar,
            text="Supported: Selig, Lednicer, Paired-Coordinates",
            wraplength=180,
            justify="left",
        )
        hint.pack(padx=16, pady=(12, 16), anchor="w")

    def _build_plot(self) -> None:
        self.figure = Figure(figsize=(6, 5), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_aspect("equal", adjustable="box")
        self.ax.grid(True, alpha=0.3)
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        self.ax.set_title("Load an airfoil file to begin")

        self.canvas = FigureCanvasTkAgg(self.figure, master=self.main_frame)
        canvas_widget = self.canvas.get_tk_widget()
        canvas_widget.pack(fill="both", expand=True, padx=12, pady=12)

    def _build_status_panel(self) -> None:
        header = ctk.CTkLabel(
            self.status_frame,
            text="Format Detection",
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        header.pack(padx=16, pady=(16, 8), anchor="w")

        self.name_label = ctk.CTkLabel(self.status_frame, text="Name: --")
        self.name_label.pack(padx=16, pady=(4, 4), anchor="w")

        self.format_label = ctk.CTkLabel(self.status_frame, text="Format: --")
        self.format_label.pack(padx=16, pady=(4, 4), anchor="w")

        self.points_label = ctk.CTkLabel(self.status_frame, text="Points: --")
        self.points_label.pack(padx=16, pady=(4, 4), anchor="w")

    def load_file(self) -> None:
        filetypes = [
            ("Airfoil files", "*.dat *.txt *.csv"),
            ("All files", "*.*"),
        ]
        path = filedialog.askopenfilename(
            title="Open Airfoil File",
            initialdir="data",
            filetypes=filetypes,
        )
        if not path:
            return

        try:
            parser = AirfoilParser.from_file(path)
            data = parser.parse()
        except Exception as exc:
            messagebox.showerror("Parsing failed", str(exc))
            return

        self.current_data = data
        self.file_label.configure(text=os.path.basename(path))
        self.export_button.configure(state="normal")

        self._update_status(data)
        self._plot_data(data)

    def export_csv(self) -> None:
        if self.current_data is None:
            messagebox.showwarning("No data", "Load an airfoil file first.")
            return

        path = filedialog.asksaveasfilename(
            title="Export CSV",
            defaultextension=".csv",
            filetypes=[("CSV", "*.csv")],
        )
        if not path:
            return

        try:
            df = self.current_data.to_dataframe()
            df.to_csv(path, index=False)
        except Exception as exc:
            messagebox.showerror("Export failed", str(exc))
            return

        messagebox.showinfo("Export complete", "CSV saved successfully.")

    def _update_status(self, data: AirfoilData) -> None:
        fmt = data.source_format.replace("_", " ").title()
        self.name_label.configure(text=f"Name: {data.name}")
        self.format_label.configure(text=f"Format: {fmt}")
        self.points_label.configure(
            text=f"Points: upper {len(data.upper)} | lower {len(data.lower)}"
        )

    def _plot_data(self, data: AirfoilData) -> None:
        self.ax.clear()
        self.ax.plot(data.upper[:, 0], data.upper[:, 1], label="Upper", color="#1f77b4")
        self.ax.plot(data.lower[:, 0], data.lower[:, 1], label="Lower", color="#ff7f0e")
        self.ax.set_aspect("equal", adjustable="box")
        self.ax.grid(True, alpha=0.3)
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        self.ax.set_title(data.name)
        self.ax.legend()
        self.canvas.draw_idle()


if __name__ == "__main__":
    app = WingShapeApp()
    app.mainloop()
