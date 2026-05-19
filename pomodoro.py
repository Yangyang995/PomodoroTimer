import tkinter as tk
from tkinter import messagebox

FOCUS_SECONDS = 25 * 60
BREAK_SECONDS = 5 * 60

class PomodoroTimer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("番茄钟")
        self.root.geometry("360x420")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e1e2e")

        # 让窗口居中
        self.root.update_idletasks()
        w = self.root.winfo_width()
        h = self.root.winfo_height()
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        self.root.geometry(f"+{x}+{y}")

        self.remaining = FOCUS_SECONDS
        self.total = FOCUS_SECONDS
        self.phase = "focus"  # "focus" | "break"
        self.running = False
        self.after_id = None

        self._build_ui()
        self._update_display()

    def _build_ui(self):
        bg = "#1e1e2e"
        fg = "#cdd6f4"
        accent_focus = "#f38ba8"
        accent_break = "#a6e3a1"

        # 阶段标签
        self.phase_label = tk.Label(
            self.root, text="专注时间", font=("Microsoft YaHei", 18, "bold"),
            bg=bg, fg=accent_focus
        )
        self.phase_label.pack(pady=(30, 10))

        # 计时数字
        self.timer_label = tk.Label(
            self.root, text="25:00", font=("Consolas", 56, "bold"),
            bg=bg, fg=fg
        )
        self.timer_label.pack(pady=(0, 10))

        # 进度条（用 Canvas 画）
        self.canvas = tk.Canvas(self.root, width=280, height=8, bg="#313244", highlightthickness=0)
        self.canvas.pack(pady=(0, 30))
        self.progress_rect = self.canvas.create_rectangle(0, 0, 0, 8, fill=accent_focus, outline="")

        # 按钮区
        btn_frame = tk.Frame(self.root, bg=bg)
        btn_frame.pack()

        btn_style = {
            "font": ("Microsoft YaHei", 13),
            "width": 8,
            "height": 1,
            "border": 0,
            "relief": "flat",
        }

        self.start_btn = tk.Button(
            btn_frame, text="开始", command=self.start,
            bg="#a6e3a1", fg="#1e1e2e", activebackground="#89d68a", **btn_style
        )
        self.start_btn.pack(side="left", padx=6)

        self.pause_btn = tk.Button(
            btn_frame, text="暂停", command=self.pause,
            bg="#f9e2af", fg="#1e1e2e", activebackground="#f0d68a", state="disabled", **btn_style
        )
        self.pause_btn.pack(side="left", padx=6)

        self.reset_btn = tk.Button(
            btn_frame, text="重置", command=self.reset,
            bg="#f38ba8", fg="#1e1e2e", activebackground="#e07a98", **btn_style
        )
        self.reset_btn.pack(side="left", padx=6)

        # 番茄计数
        self.count_label = tk.Label(
            self.root, text="已完成: 0 个番茄", font=("Microsoft YaHei", 11),
            bg=bg, fg="#6c7086"
        )
        self.count_label.pack(pady=(25, 0))

        self.pomodoro_count = 0

    def start(self):
        if self.running:
            return
        self.running = True
        self.start_btn.config(state="disabled")
        self.pause_btn.config(state="normal")
        self._tick()

    def pause(self):
        self.running = False
        if self.after_id:
            self.root.after_cancel(self.after_id)
            self.after_id = None
        self.start_btn.config(state="normal")
        self.pause_btn.config(state="disabled")

    def reset(self):
        self.running = False
        if self.after_id:
            self.root.after_cancel(self.after_id)
            self.after_id = None
        self.phase = "focus"
        self.remaining = FOCUS_SECONDS
        self.total = FOCUS_SECONDS
        self.start_btn.config(state="normal")
        self.pause_btn.config(state="disabled")
        self._update_display()

    def _tick(self):
        if not self.running:
            return
        self.remaining -= 1
        self._update_display()

        if self.remaining <= 0:
            self._on_timer_end()
            return

        self.after_id = self.root.after(1000, self._tick)

    def _on_timer_end(self):
        self.running = False
        self.root.lift()
        self.root.focus_force()

        if self.phase == "focus":
            self.pomodoro_count += 1
            self.count_label.config(text=f"已完成: {self.pomodoro_count} 个番茄")
            messagebox.showinfo("番茄钟", "专注时间结束！休息一下吧 🍅")
            self.phase = "break"
            self.remaining = BREAK_SECONDS
            self.total = BREAK_SECONDS
        else:
            messagebox.showinfo("番茄钟", "休息结束！开始新的番茄吧 🚀")
            self.phase = "focus"
            self.remaining = FOCUS_SECONDS
            self.total = FOCUS_SECONDS

        self._update_display()
        self.start_btn.config(state="normal")
        self.pause_btn.config(state="disabled")

    def _update_display(self):
        minutes = self.remaining // 60
        seconds = self.remaining % 60
        self.timer_label.config(text=f"{minutes:02d}:{seconds:02d}")

        if self.phase == "focus":
            self.phase_label.config(text="专注时间", fg="#f38ba8")
            self.canvas.itemconfig(self.progress_rect, fill="#f38ba8")
        else:
            self.phase_label.config(text="休息时间", fg="#a6e3a1")
            self.canvas.itemconfig(self.progress_rect, fill="#a6e3a1")

        # 更新进度条
        ratio = 1 - (self.remaining / self.total)
        bar_width = int(280 * ratio)
        self.canvas.coords(self.progress_rect, 0, 0, bar_width, 8)

    def run(self):
        self.root.mainloop()

        
if __name__ == "__main__":
    app = PomodoroTimer()
    app.run()
