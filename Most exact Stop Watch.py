import tkinter as tk
import time
import winsound
import threading

running = False
start_time = 0
elapsed = 0
offset_x = 0
offset_y = 0
last_beep_second = 0

def play_beep(freq, duration=150):
    threading.Thread(target=lambda: winsound.Beep(freq, duration), daemon=True).start()

# sound presets
HIGH_BEEP = 1000   # every second
LOW_BEEP = 500     # start / stop / clear

def start():
    global running, start_time
    if not running:
        play_beep(LOW_BEEP)  # low beep on start
        running = True
        start_time = time.perf_counter_ns() - elapsed
        update_timer()

def stop():
    global running
    if running:
        play_beep(LOW_BEEP)  # low beep on stop
    running = False

def toggle_start_stop(event=None):
    if running:
        stop()
    else:
        start()

def clear(event=None):
    global elapsed, running, last_beep_second
    play_beep(LOW_BEEP)  # low beep on clear
    running = False
    elapsed = 0
    last_beep_second = 0
    label.config(text="0.000000000 s")

def update_timer():
    global elapsed, last_beep_second
    if running:
        elapsed = time.perf_counter_ns() - start_time
        seconds = elapsed / 1_000_000_000
        label.config(text=f"{seconds:.9f} s")

        whole_second = int(seconds)
        if whole_second > last_beep_second:
            play_beep(HIGH_BEEP)  # high beep every second
            last_beep_second = whole_second

        window.after(1, update_timer)

def close_window():
    window.destroy()

def click_window(event):
    global offset_x, offset_y
    offset_x = event.x
    offset_y = event.y

def drag_window(event):
    x = event.x_root - offset_x
    y = event.y_root - offset_y
    window.geometry(f"+{x}+{y}")

window = tk.Tk()
window.overrideredirect(True)
window.geometry("270x140")

border = tk.Frame(window, bg="black", highlightthickness=0)
border.pack(fill="both", expand=True)

app = tk.Frame(border, bg="#bfbfbf")
app.pack(fill="both", expand=True, padx=3, pady=3)

window.bind("<space>", toggle_start_stop)
window.bind("<Alt_L>", clear)
window.bind("<Alt_R>", clear)

window.bind("<Button-1>", click_window)
window.bind("<B1-Motion>", drag_window)

close_btn = tk.Button(app, text="X", command=close_window, bg="#ff4a4a", fg="white", bd=0, font=("Arial", 10))
close_btn.place(x=240, y=3, width=20, height=20)

label = tk.Label(app, text="0.000000000 s", font=("Arial", 16), bg="#bfbfbf", fg="black")
label.pack(pady=15)

btn_frame = tk.Frame(app, bg="#bfbfbf")
btn_frame.pack()

start_btn = tk.Button(btn_frame, text="Go", width=7, command=start)
start_btn.grid(row=0, column=0, padx=5)

clear_btn = tk.Button(btn_frame, text="Clear", width=7, command=clear)
clear_btn.grid(row=0, column=1, padx=5)

stop_btn = tk.Button(btn_frame, text="Stop", width=7, command=stop)
stop_btn.grid(row=0, column=2, padx=5)

window.mainloop()
