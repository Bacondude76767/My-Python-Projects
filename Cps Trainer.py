import tkinter as tk
import time

class ClickCounter:
    def __init__(self, use_unit="SECOND", bordered=False):
        self.root = tk.Tk()

        # Borderless or not
        if not bordered:
            self.root.overrideredirect(True)

        self.root.geometry("180x90+100+100")
        self.root.configure(bg="white")
        self.root.attributes("-topmost", True)

        self.unit_label = use_unit.upper()  # "MILLISECOND", "SECOND", "MINUTE", "HOUR"
        self.unit_time = {"MILLISECOND": 0.001, "SECOND": 1, "MINUTE": 60, "HOUR": 3600}[self.unit_label]

        # Dragging
        self.offset_x = 0
        self.offset_y = 0
        if not bordered:
            self.root.bind("<B1-Motion>", self.move_window)

        # Add small red X button to close
        self.close_btn = tk.Button(self.root, text="X", fg="white", bg="red",
                                   font=("Consolas", 10, "bold"), command=self.root.destroy,
                                   bd=0, relief="flat", highlightthickness=0)
        # Place it at top-right
        self.close_btn.place(x=160, y=0, width=20, height=20)

        # Label setup
        self.label = tk.Label(
            self.root,
            text="Click Me!",
            fg="black",
            bg="white",
            font=("Consolas", 16, "bold")
        )
        self.label.pack(expand=True, fill="both")

        # Click tracking
        self.click_times = []
        self.label.bind("<Button-1>", self.on_click)

        # Right-click closes the window
        self.root.bind("<Button-3>", lambda e: self.root.destroy())

        self.update_display()
        self.root.mainloop()

    def move_window(self, event):
        if self.root.overrideredirect():  # Only draggable if borderless
            x = self.root.winfo_pointerx() - self.offset_x
            y = self.root.winfo_pointery() - self.offset_y
            self.root.geometry(f"+{x}+{y}")

    def on_click(self, event):
        if not self.offset_x and not self.offset_y:
            self.offset_x = event.x
            self.offset_y = event.y
        self.click_times.append(time.time())

    def update_display(self):
        now = time.time()
        window = self.unit_time
        self.click_times = [t for t in self.click_times if now - t <= window]

        # Normalize rate
        if self.unit_label == "MILLISECOND":
            rate = len(self.click_times) * 1000
        else:
            rate = len(self.click_times)

        self.label.config(text=f"{self.unit_label}: {int(rate)}")
        self.root.after(100, self.update_display)


def mini_menu():
    menu = tk.Tk()
    menu.overrideredirect(True)
    menu.geometry("250x250+150+150")
    menu.configure(bg="white")
    menu.attributes("-topmost", True)

    # Dragging support
    offset_x = 0
    offset_y = 0

    def start_move(event):
        nonlocal offset_x, offset_y
        offset_x = event.x
        offset_y = event.y

    def do_move(event):
        x = menu.winfo_pointerx() - offset_x
        y = menu.winfo_pointery() - offset_y
        menu.geometry(f"+{x}+{y}")

    menu.bind("<Button-1>", start_move)
    menu.bind("<B1-Motion>", do_move)

    label = tk.Label(menu, text="Choose click unit:", fg="black", bg="white", font=("Consolas", 14, "bold"))
    label.pack(pady=10)

    def launch_counter(unit):
        menu.destroy()
        ClickCounter(use_unit=unit, bordered=False)

    options = ["MILLISECOND", "SECOND", "MINUTE", "HOUR"]
    for opt in options:
        btn = tk.Button(menu, text=opt.capitalize(), command=lambda u=opt: launch_counter(u),
                        font=("Consolas", 12), bg="white", fg="black")
        btn.pack(pady=5, fill="x", padx=20)

    menu.mainloop()


def main():
    choice = input("Do you want to change it to Clicks per Minute? (Y/N): ").strip().upper()
    use_minutes = (choice == "Y")

    border_choice = input("Do you want to make it have a border? (Y/N): ").strip().upper()
    bordered = (border_choice == "Y")

    extra = input(
        "Welcome to Click per Number, you can test your click per second or minute with this.\n"
        "If you want to explore more features, please type in (M) or enter anything else to dismiss: "
    ).strip().upper()

    if extra == "M":
        mini_menu()
    else:
        unit = "MINUTE" if use_minutes else "SECOND"
        ClickCounter(use_unit=unit, bordered=bordered)


if __name__ == "__main__":
    main()
