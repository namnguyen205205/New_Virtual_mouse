import cv2
import tkinter as tk
from PIL import Image, ImageTk
import threading
import queue
import time

from logic_mouse import process


# ==========================================================
# CỬA SỔ CHÍNH
# ==========================================================
root = tk.Tk()
root.title("Virtual Mouse Control")
root.geometry("820x650")
root.resizable(False, False)

# Màu
BG = "#080c14"
HEADER = "#0f172a"
CARD = "#111827"
CARD2 = "#172033"

CYAN = "#22d3ee"
GREEN = "#22c55e"
PURPLE = "#c084fc"
RED = "#ef4444"
ORANGE = "#f97316"
BLUE = "#3b82f6"
YELLOW = "#facc15"

WHITE = "#f8fafc"
GRAY = "#94a3b8"

root.configure(bg=BG)


# ==========================================================
# HEADER
# ==========================================================
header = tk.Frame(
    root,
    bg=HEADER,
    height=65
)

header.pack(
    fill=tk.X
)

header.pack_propagate(False)


# Logo tròn
logo = tk.Canvas(
    header,
    width=30,
    height=30,
    bg=HEADER,
    highlightthickness=0
)

logo.pack(
    side=tk.LEFT,
    padx=(20, 8)
)

logo.create_oval(
    5,
    5,
    25,
    25,
    fill=CYAN,
    outline=""
)


# Tiêu đề
tk.Label(
    header,
    text="VIRTUAL MOUSE",
    font=("Consolas", 16, "bold"),
    bg=HEADER,
    fg=WHITE
).pack(
    side=tk.LEFT
)


tk.Label(
    header,
    text="HAND CONTROL SYSTEM",
    font=("Consolas", 8),
    bg=HEADER,
    fg=GRAY
).pack(
    side=tk.LEFT,
    padx=12
)


# FPS góc phải
fps_var = tk.StringVar(value="0.0")

fps_box = tk.Frame(
    header,
    bg=HEADER
)

fps_box.pack(
    side=tk.RIGHT,
    padx=20
)

tk.Label(
    fps_box,
    text="FPS",
    font=("Consolas", 8),
    bg=HEADER,
    fg=GRAY
).pack()

tk.Label(
    fps_box,
    textvariable=fps_var,
    font=("Consolas", 14, "bold"),
    bg=HEADER,
    fg=GREEN
).pack()


# ==========================================================
# CAMERA
# ==========================================================
camera_container = tk.Frame(
    root,
    bg=BG
)

camera_container.pack(
    pady=18
)


# Viền camera
camera_border = tk.Frame(
    camera_container,
    bg=CYAN,
    padx=2,
    pady=2
)

camera_border.pack()


canvas = tk.Canvas(
    camera_border,
    width=720,
    height=405,
    bg="black",
    highlightthickness=0
)

canvas.pack()


canvas_image = canvas.create_image(
    0,
    0,
    anchor=tk.NW
)


# ==========================================================
# DASHBOARD DƯỚI CAMERA
# ==========================================================
dashboard = tk.Frame(
    root,
    bg=BG
)

dashboard.pack(
    fill=tk.X,
    padx=30
)


# ==========================================================
# HÀM TẠO CARD
# ==========================================================
def create_card(parent, title, width=175):

    card = tk.Frame(
        parent,
        bg=CARD,
        width=width,
        height=105
    )

    card.pack(
        side=tk.LEFT,
        padx=5,
        expand=True,
        fill=tk.X
    )

    card.pack_propagate(False)

    tk.Label(
        card,
        text=title,
        font=("Consolas", 9, "bold"),
        bg=CARD,
        fg=CYAN
    ).pack(
        anchor="w",
        padx=12,
        pady=(10, 5)
    )

    return card


# ==========================================================
# CARD NGÓN CÁI
# ==========================================================
card_thumb = create_card(
    dashboard,
    "NGÓN CÁI"
)

cai_x = tk.StringVar(value="--")
cai_y = tk.StringVar(value="--")

tk.Label(
    card_thumb,
    textvariable=cai_x,
    font=("Consolas", 13, "bold"),
    bg=CARD,
    fg=WHITE
).pack()

tk.Label(
    card_thumb,
    textvariable=cai_y,
    font=("Consolas", 13, "bold"),
    bg=CARD,
    fg=WHITE
).pack()


# ==========================================================
# CARD NGÓN TRỎ
# ==========================================================
card_index = create_card(
    dashboard,
    "NGÓN TRỎ"
)

tro_x = tk.StringVar(value="--")
tro_y = tk.StringVar(value="--")

tk.Label(
    card_index,
    textvariable=tro_x,
    font=("Consolas", 13, "bold"),
    bg=CARD,
    fg=WHITE
).pack()

tk.Label(
    card_index,
    textvariable=tro_y,
    font=("Consolas", 13, "bold"),
    bg=CARD,
    fg=WHITE
).pack()


# ==========================================================
# CARD DISTANCE
# ==========================================================
card_dist = create_card(
    dashboard,
    "KHOẢNG CÁCH"
)

dist_var = tk.StringVar(value="--")

tk.Label(
    card_dist,
    textvariable=dist_var,
    font=("Consolas", 18, "bold"),
    bg=CARD,
    fg=PURPLE
).pack(
    pady=12
)


# ==========================================================
# CARD MODE
# ==========================================================
card_mode = create_card(
    dashboard,
    "TRẠNG THÁI"
)

mode_var = tk.StringVar(
    value="WAITING"
)

mode_label = tk.Label(
    card_mode,
    textvariable=mode_var,
    font=("Consolas", 12, "bold"),
    bg=CARD,
    fg=YELLOW
)

mode_label.pack(
    pady=15
)


MODE_COLOR = {

    "MOVING":
        GREEN,

    "LEFT CLICK":
        RED,

    "RIGHT CLICK":
        ORANGE,

    "SCROLL UP":
        CYAN,

    "SCROLL DOWN":
        BLUE,

    "WAITING":
        YELLOW
}


# ==========================================================
# FOOTER
# ==========================================================
footer = tk.Frame(
    root,
    bg=BG
)

footer.pack(
    fill=tk.X,
    padx=35,
    pady=15
)


status_canvas = tk.Canvas(
    footer,
    width=15,
    height=15,
    bg=BG,
    highlightthickness=0
)

status_canvas.pack(
    side=tk.LEFT
)

status_canvas.create_oval(
    3,
    3,
    12,
    12,
    fill=GREEN,
    outline=""
)


tk.Label(
    footer,
    text="CAMERA ACTIVE",
    font=("Consolas", 8, "bold"),
    bg=BG,
    fg=GREEN
).pack(
    side=tk.LEFT,
    padx=5
)


tk.Label(
    footer,
    text="Q  :  THOÁT",
    font=("Consolas", 8),
    bg=BG,
    fg=GRAY
).pack(
    side=tk.RIGHT
)


# ==========================================================
# QUEUE
# ==========================================================
frame_queue = queue.Queue(
    maxsize=1
)

running = True


# ==========================================================
# THREAD WEBCAM
# ==========================================================
def camera_loop():

    global running

    cap = cv2.VideoCapture(0)

    previous_time = time.time()

    while running:

        ret, frame = cap.read()

        if not ret:
            break


        # Lật camera
        frame = cv2.flip(
            frame,
            1
        )


        # -------------------------
        # FPS
        # -------------------------
        current_time = time.time()

        delta_time = (
            current_time
            - previous_time
        )

        if delta_time > 0:

            fps = (
                1
                /
                delta_time
            )

        else:

            fps = 0


        previous_time = (
            current_time
        )


        # -------------------------
        # LOGIC MOUSE
        # -------------------------
        frame, data = process(
            frame
        )


        # -------------------------
        # Đưa sang Queue
        # -------------------------
        if not frame_queue.full():

            frame_queue.put(
                (
                    frame,
                    data,
                    fps
                )
            )


    cap.release()


# ==========================================================
# REFRESH GIAO DIỆN
# ==========================================================
def refresh_ui():

    if not frame_queue.empty():

        frame, data, fps = (
            frame_queue.get()
        )


        # -------------------------
        # FPS
        # -------------------------
        fps_var.set(
            f"{fps:.1f}"
        )


        # -------------------------
        # DATA
        # -------------------------
        if data["found"]:

            cai_x.set(
                f"X : {data['lm4x']}"
            )

            cai_y.set(
                f"Y : {data['lm4y']}"
            )


            tro_x.set(
                f"X : {data['lm8x']}"
            )

            tro_y.set(
                f"Y : {data['lm8y']}"
            )


            dist_var.set(
                f"{data['dist']} px"
            )


            mode = data["mode"]

            mode_var.set(
                mode
            )

            mode_label.config(
                fg=MODE_COLOR.get(
                    mode,
                    YELLOW
                )
            )


        else:

            cai_x.set(
                "X : --"
            )

            cai_y.set(
                "Y : --"
            )

            tro_x.set(
                "X : --"
            )

            tro_y.set(
                "Y : --"
            )

            dist_var.set(
                "--"
            )

            mode_var.set(
                "WAITING"
            )

            mode_label.config(
                fg=YELLOW
            )


        # ==================================================
        # HIỂN THỊ CAMERA
        # ==================================================
        frame_rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )


        frame_rgb = cv2.resize(
            frame_rgb,
            (
                720,
                405
            )
        )


        image = Image.fromarray(
            frame_rgb
        )


        image_tk = (
            ImageTk.PhotoImage(
                image=image
            )
        )


        canvas.image_tk = (
            image_tk
        )


        canvas.itemconfig(
            canvas_image,
            image=image_tk
        )


    root.after(
        15,
        refresh_ui
    )


# ==========================================================
# ĐÓNG APP
# ==========================================================
def close_app():

    global running

    running = False

    root.destroy()


def keyboard(event):

    if (
        event.char.lower()
        == "q"
    ):

        close_app()


root.bind(
    "<Key>",
    keyboard
)


root.protocol(
    "WM_DELETE_WINDOW",
    close_app
)


# ==========================================================
# ĐƯA CỬA SỔ RA GIỮA MÀN HÌNH
# ==========================================================
root.update_idletasks()

screen_width = (
    root.winfo_screenwidth()
)

screen_height = (
    root.winfo_screenheight()
)

window_width = (
    root.winfo_width()
)

window_height = (
    root.winfo_height()
)


x = (
    screen_width
    // 2
    -
    window_width
    // 2
)

y = (
    screen_height
    // 2
    -
    window_height
    // 2
)


root.geometry(
    f"+{x}+{y}"
)


# ==========================================================
# THREAD CAMERA
# ==========================================================
camera_thread = (
    threading.Thread(
        target=camera_loop,
        daemon=True
    )
)

camera_thread.start()


# ==========================================================
# CHẠY
# ==========================================================
refresh_ui()

root.mainloop()