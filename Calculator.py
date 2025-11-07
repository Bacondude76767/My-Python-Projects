import tkinter as tk
from tkinter import Toplevel, messagebox, ttk
import subprocess
import sys
import webbrowser

# ----------------- Ensure requests is installed -----------------
try:
    import requests
except ModuleNotFoundError:
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
        import requests
    except Exception as e:
        messagebox.showerror("Error", f"Failed to install 'requests': {e}")
        requests = None

REQUESTS_AVAILABLE = requests is not None

# ----------------- Calculator -----------------
class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.overrideredirect(True)
        self.configure(bg="#c0c0c0")
        self.window_width = 400
        self.window_height = 550
        self._center_window(self.window_width, self.window_height)

        self.last_results = []
        self.average_window_open = False
        self.offset_x = 0
        self.offset_y = 0

        self._build_ui()
        self.bind_all("<Key>", self._on_key)

    # ------------------- Utilities -------------------
    def _center_window(self, width, height):
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    # ------------------- Drag -------------------
    def _start_move(self, event, win=None):
        if win is None: win = self
        win.offset_x = event.x
        win.offset_y = event.y
    def _on_move(self, event, win=None):
        if win is None: win = self
        x = event.x_root - win.offset_x
        y = event.y_root - win.offset_y
        win.geometry(f"+{x}+{y}")

    # ------------------- Display -------------------
    def _set_display(self, text):
        self.display.config(state="normal")
        self.display.delete(0, tk.END)
        self.display.insert(0, text)
        self.display.config(state="readonly")
    def _reset_display(self):
        self._set_display("0")

    # ------------------- UI / Buttons -------------------
    def _build_ui(self):
        # Header
        self.header = tk.Frame(self, bg="#000080", height=30)
        self.header.pack(fill="x", side="top")
        self.header.bind("<Button-1>", lambda e: self._start_move(e))
        self.header.bind("<B1-Motion>", lambda e: self._on_move(e))

        # Header buttons
        for text, cmd, bg in [("X", self.destroy, "#ff0000"),
                               ("⋯", lambda: messagebox.showinfo("Placeholder", "This is a placeholder button"), "#c0c0c0"),
                               ("⚙️", self.open_settings, "#c0c0c0")]:
            b = tk.Button(self.header, text=text, bg=bg, fg="white" if bg=="#ff0000" else "black",
                          relief="raised", command=cmd)
            b.pack(side="right", padx=2, pady=2)

        title = tk.Label(self.header, text="Calculator", bg="#000080", fg="white",
                         font=("Segoe UI", 12, "bold"))
        title.pack(side="left", padx=10)

        # Display
        self.display = tk.Entry(self, font=("Consolas", 20), justify="right",
                                bd=2, relief="sunken", bg="#00ff00", fg="black",
                                insertbackground="black", state="readonly")
        self.display.pack(padx=10, pady=(10,0), fill="x")
        self._set_display("0")

        # Buttons
        btn_frame = tk.Frame(self, bg="#c0c0c0")
        btn_frame.pack(pady=10)

        buttons = [
            ('7','8','9','/'),
            ('4','5','6','*','$'),  # Added $ button
            ('1','2','3','-'),
            ('0','.','C','+')
        ]

        for r, row in enumerate(buttons):
            for c, char in enumerate(row):
                cmd = lambda ch=char: self._on_button(ch)
                tk.Button(btn_frame, text=char, width=6, height=2,
                          bg="#d9d9d9", fg="black", font=("Segoe UI",12),
                          relief="raised", activebackground="#e0e0e0",
                          command=cmd).grid(row=r, column=c, padx=4, pady=4)

        # Extra buttons
        extras = [("@", self._open_info_window, 2, 4, "#d9d9d9"),
                  ("Average", self._open_average_window, 4, 3, "#d9d9d9"),
                  ("DT", self._open_data_table, 4, 4, "#d9d9d9"),
                  ("=", self._evaluate, 4, 0, "#d9d9d9", 3)]

        for ex in extras:
            if len(ex)==6:
                tk.Button(btn_frame, text=ex[0], width=ex[5]*6, height=2, bg=ex[4], fg="black",
                          font=("Segoe UI",12), relief="raised", activebackground="#e0e0e0",
                          command=ex[1]).grid(row=ex[2], column=ex[3], columnspan=ex[5], padx=4, pady=4)
            else:
                tk.Button(btn_frame, text=ex[0], width=6, height=2, bg=ex[4], fg="black",
                          font=("Segoe UI",12), relief="raised", activebackground="#e0e0e0",
                          command=ex[1]).grid(row=ex[2], column=ex[3], padx=4, pady=4)

    # ------------------- Button Actions -------------------
    def _on_button(self, ch):
        if ch=="C":
            self._reset_display()
        elif ch=="$":
            self._open_currency_window()
        else:
            current = self.display.get()
            if current=="0":
                self._set_display(ch)
            else:
                self._set_display(current+ch)

    def _evaluate(self):
        try:
            expr = self.display.get()
            result = eval(expr, {"__builtins__": None}, {})
            self.last_results.append((expr,result))
            self._set_display(str(result))
        except:
            self._set_display("Error")
            self.after(1000, self._reset_display)

    # ------------------- Windows -------------------
    def _create_window(self, width=350, height=250):
        win = Toplevel(self)
        win.overrideredirect(True)
        win.geometry(f"{width}x{height}")
        win.configure(bg="#c0c0c0")
        # Top border
        top = tk.Frame(win, bg="#000080", height=30)
        top.pack(fill="x", side="top")
        top.bind("<Button-1>", lambda e: self._start_move(e, win))
        top.bind("<B1-Motion>", lambda e: self._on_move(e, win))
        # Close button
        tk.Button(top,text="X",bg="#ff0000",fg="white",relief="raised",
                  command=win.destroy).place(x=width-30,y=5,width=20,height=20)
        return win, top

    # ------------------- Info Window -------------------
    def _open_info_window(self):
        win, top = self._create_window(350, 180)
        tk.Label(win, text="Information", bg="#c0c0c0", fg="black", font=("Segoe UI",14,"bold")).pack(pady=10)
        tk.Label(win, text="Made by Bacondude76767", bg="#c0c0c0", fg="black", font=("Segoe UI",12)).pack(pady=5)
        tk.Label(win, text="Email: emmit.theodore@gmail.com", bg="#c0c0c0", fg="black", font=("Segoe UI",10)).pack(pady=5)
        tk.Label(win, text="Version 2.3.7", bg="#c0c0c0", fg="black", font=("Segoe UI",10,"italic")).pack(pady=5)

    # ------------------- Average Window -------------------
    def _open_average_window(self):
        if self.average_window_open: return
        self.average_window_open=True
        win, top = self._create_window(400, 220)
        tk.Label(win, text="Average Number Calculator", bg="#c0c0c0", font=("Segoe UI",14,"bold")).pack(pady=10)
        tk.Label(win, text="Enter numbers separated by commas:", bg="#c0c0c0", font=("Segoe UI",10)).pack(pady=5)
        entry = tk.Entry(win, width=40)
        entry.pack(pady=5)
        result_label = tk.Label(win, text="", bg="#c0c0c0", font=("Segoe UI",12))
        result_label.pack(pady=10)

        def calculate_average():
            nums_str = entry.get()
            try:
                numbers = [float(x.strip()) for x in nums_str.split(",") if x.strip()!=""]
                if numbers:
                    avg = sum(numbers)/len(numbers)
                    result_label.config(text=f"Average: {avg}")
                    self._set_display(str(avg))
                else:
                    result_label.config(text="No numbers entered")
            except:
                result_label.config(text="Invalid input")

        tk.Button(win, text="Calculate", bg="#00ff00", fg="black", font=("Segoe UI",10),
                  command=calculate_average).pack(pady=5)

    # ------------------- Data Table -------------------
    def _open_data_table(self):
        win, top = self._create_window(400, 350)
        tk.Label(win, text="Data Table", bg="#c0c0c0", fg="black", font=("Segoe UI",14,"bold")).pack(pady=10)
        frame = tk.Frame(win, bg="#c0c0c0")
        frame.pack(pady=10, fill="both", expand=True)
        if self.last_results:
            for expr,res in self.last_results:
                tk.Label(frame, text=f"{expr} = {res}", bg="#c0c0c0", fg="black", font=("Segoe UI",10)).pack()
        else:
            tk.Label(frame, text="No data available", bg="#c0c0c0", fg="black", font=("Segoe UI",10)).pack()

    # ------------------- Settings -------------------
    def open_settings(self):
        win, top = self._create_window(350, 200)
        tk.Label(win, text="Settings", bg="#c0c0c0", fg="black", font=("Segoe UI",14,"bold")).pack(pady=10)

        # Refresh button clears data table and resets display
        def refresh():
            self.last_results.clear()
            self._reset_display()
            messagebox.showinfo("Refreshed", "Calculator and Data Table cleared.")

        tk.Button(win, text="Refresh", bg="#00ff00", fg="black", font=("Segoe UI",12), command=refresh).pack(pady=10)

        # GitHub button opens browser
        def open_github():
            webbrowser.open("https://github.com/Bacondude76767")

        tk.Button(win, text="GitHub", bg="#1a1aff", fg="white", font=("Segoe UI",12), command=open_github).pack(pady=5)

    # ------------------- Currency Converter -------------------
    def _open_currency_window(self):
        win, top = self._create_window(450, 300)
        tk.Label(win, text="Money Converter", bg="#c0c0c0", font=("Segoe UI",14,"bold")).pack(pady=10)

        currencies = ["USD","EUR","GBP","JPY","AUD","CAD","CHF","CNY","SEK","NZD","MXN","SGD",
                      "HKD","NOK","KRW","TRY","INR","RUB","BRL","ZAR"]

        frame = tk.Frame(win, bg="#c0c0c0")
        frame.pack(pady=10)

        tk.Label(frame, text="From:", bg="#c0c0c0").grid(row=0,column=0,padx=5,pady=5)
        from_box = ttk.Combobox(frame, values=currencies, width=10)
        from_box.grid(row=0,column=1,padx=5,pady=5)
        from_box.set("USD")

        tk.Label(frame, text="To:", bg="#c0c0c0").grid(row=1,column=0,padx=5,pady=5)
        to_box = ttk.Combobox(frame, values=currencies, width=10)
        to_box.grid(row=1,column=1,padx=5,pady=5)
        to_box.set("EUR")

        tk.Label(frame, text="Amount:", bg="#c0c0c0").grid(row=2,column=0,padx=5,pady=5)
        amount_entry = tk.Entry(frame)
        amount_entry.grid(row=2,column=1,padx=5,pady=5)
        amount_entry.insert(0,"1")

        result_label = tk.Label(win, text="", bg="#c0c0c0", font=("Segoe UI",12))
        result_label.pack(pady=10)

        # Hardcoded fallback rates
        fallback_rates = {
            "USD":1,"EUR":0.92,"GBP":0.8,"JPY":145,"AUD":1.5,"CAD":1.35,
            "CHF":0.97,"CNY":7.2,"SEK":10.0,"NZD":1.6,"MXN":18.5,
            "SGD":1.35,"HKD":7.8,"NOK":11.0,"KRW":1380,"TRY":29,"INR":83,
            "RUB":77,"BRL":5.2,"ZAR":19.0
        }

        def convert():
            from_currency = from_box.get().upper()
            to_currency = to_box.get().upper()
            try:
                amount = float(amount_entry.get())
            except:
                result_label.config(text="Invalid amount")
                return
            # Try online API first
            converted = None
            if REQUESTS_AVAILABLE:
                try:
                    url = f"https://api.exchangerate.host/convert?from={from_currency}&to={to_currency}&amount={amount}"
                    data = requests.get(url).json()
                    if data.get("success"):
                        converted = data["result"]
                except:
                    converted = None
            # Fallback
            if converted is None:
                try:
                    rate_from = fallback_rates.get(from_currency,1)
                    rate_to = fallback_rates.get(to_currency,1)
                    converted = amount/rate_from*rate_to
                except:
                    result_label.config(text="Conversion failed")
                    return
            result_label.config(text=f"{amount} {from_currency} = {converted:.2f} {to_currency}")
            self._set_display(str(round(converted,2)))

        tk.Button(win, text="Convert", bg="#00ff00", fg="black", font=("Segoe UI",12), command=convert).pack(pady=5)

    # ------------------- Keyboard -------------------
    def _on_key(self,event):
        if self.average_window_open: return
        key = event.keysym
        if key in ("Return","KP_Enter"): self._evaluate()
        elif key=="BackSpace":
            cur = self.display.get()
            if len(cur)>1: self._set_display(cur[:-1])
            else: self._reset_display()
        elif key=="Escape": self._reset_display()
        else:
            ch = event.char
            if ch in "0123456789.+-*/":
                cur = self.display.get()
                if cur=="0": self._set_display(ch)
                else: self._set_display(cur+ch)

if __name__=="__main__":
    Calculator().mainloop()
