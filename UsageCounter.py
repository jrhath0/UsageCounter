from logging import config, root
from tkinter import *
from tkinter import ttk
import psutil

# Data Storage
cpu_history = [0] * 50
ram_history = [0] * 50

def frequency_monitor():
    # Get CPU percentage
    cpu_percent = psutil.cpu_percent(interval=1)

    # Get RAM usage
    ram_percent = psutil.virtual_memory().percent
    ram_gb = round(psutil.virtual_memory().used / (1024 ** 3), 2)
    ram_total_gb = round(psutil.virtual_memory().total / (1024 ** 3), 2)

    # Update history lists
    cpu_history.append(cpu_percent)
    ram_history.append(ram_percent)
    if len(cpu_history) > 50:
        cpu_history.pop(0)
    if len(ram_history) > 50:
        ram_history.pop(0)

    #print(f"CPU Usage: {cpu_percent}% | RAM Usage: {ram_percent}% ({ram_gb}GB/{ram_total_gb}GB)")
    cpu_label.config(text=f"CPU Usage: {cpu_percent}%")
    ram_label.config(text=f"RAM Usage: {ram_percent}% ({ram_gb}GB/{ram_total_gb}GB)")

    draw_graphs(cpu_canvas, cpu_history, "blue")
    draw_graphs(ram_canvas, ram_history, "red")

    root.after(1000, frequency_monitor)  # Schedule the next update after 1 second

def draw_graphs(canvas, data, color):
    canvas.delete("all")  # Clear the canvas before drawing
    width = canvas.winfo_width()
    height = canvas.winfo_height()

    if width < 10 or height < 10:
        width, height = 200, 80 # default size if the canvas is too small

    # Add reference lines, 25, 50, 75 percent
    for ref_value in [0, 20, 40, 60, 80]:
        y = height - (ref_value / 100) * height
        canvas.create_line(0, y, width, y, fill="lightgray", dash=(2, 4))
        canvas.create_text(5, y - 10, text=f"{ref_value}%", anchor='w', fill="gray")

    #draw lines
    if len(data) > 1:
        points = []
        for i, value in enumerate(data):
            x = (i / len(data)) * width
            y = height - (value / 100) * height
            points.extend([x, y])
        canvas.create_line(points, fill=color, width=2)

    # draw border
    canvas.create_rectangle(0, 0, width, height, outline="gray", width=1)

# Custom close function
def close_app():
    root.destroy()

# Make window draggable
def start_move(event):
    # Don't start drag if clicking on the resize handle
    if hasattr(event.widget, 'name') and event.widget.name == "resize_frame":
        return
    
    # Also don't drag if clicking on the close button
    if hasattr(event.widget, 'name') and event.widget.name == "close_button":
        return
    
    root._drag_x = event.x_root
    root._drag_y = event.y_root
    root.resizable(False, False)

def do_move(event):
    if hasattr(root, '_drag_x'):
        dx = event.x_root - root._drag_x
        dy = event.y_root - root._drag_y
        x = root.winfo_x() + dx
        y = root.winfo_y() + dy
        root.wm_geometry(f"+{int(x)}+{int(y)}")
        root._drag_x = event.x_root
        root._drag_y = event.y_root

def stop_move(event):
    if hasattr(root, '_drag_x'):
        delattr(root, '_drag_x')
        root.resizable(True, True)

# Resizing functions
def start_resize(event):
    root._resize_x = event.x_root
    root._resize_y = event.y_root
    root._orig_width = root.winfo_width()
    root._orig_height = root.winfo_height()
    # Disable drag during resize
    if hasattr(root, '_drag_x'):
        delattr(root, '_drag_x')

def do_resize(event):
    if hasattr(root, '_resize_x'):
        dx = event.x_root - root._resize_x
        dy = event.y_root - root._resize_y
        
        new_width = max(300, root._orig_width + dx)
        new_height = max(350, root._orig_height + dy)
        
        root.wm_geometry(f"{new_width}x{new_height}")
        root._resize_x = event.x_root
        root._resize_y = event.y_root
        root._orig_width = new_width
        root._orig_height = new_height

def on_resize(event): #redraw graphs when window is resized
    draw_graphs(cpu_canvas, cpu_history, "blue")
    draw_graphs(ram_canvas, ram_history, "red")

def main():
    global root, cpu_label, ram_label, cpu_canvas, ram_canvas

    root = Tk()
    root.title("CPU/RAM Usage Monitor")

    root.overrideredirect(True)  # Removes title bar AND window borders
    root.attributes("-alpha", 0.99)  # Fixes a bug where the window becomes unresponsive on some systems
    root.wm_geometry("300x350")  # Set a default size for the window
    #root.attributes("-topmost", True)  # Keep the window on top
    root.resizable(True, True) # Allow resizing

    # gridweight configuration for resizing
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # Main Frame
    frm = ttk.Frame(root, padding=10)
    frm.grid(sticky="nsew")

    root.bind("<ButtonPress-1>", start_move)
    root.bind("<B1-Motion>", do_move)
    root.bind("<ButtonRelease-1>", stop_move)

    # Grid weights for frame resizing
    frm.grid_rowconfigure(0, weight=0)  # CPU label row + check box + Close button
    frm.grid_rowconfigure(1, weight=1)  # CPU graph row
    frm.grid_rowconfigure(2, weight=0)  # RAM label row
    frm.grid_rowconfigure(3, weight=1)  # RAM graph row
    frm.grid_rowconfigure(4, weight=0)  # Button row
    frm.grid_columnconfigure(0, weight=1)
    frm.grid_columnconfigure(1, weight=0)  # Close button column fixed
    frm.grid_columnconfigure(2, weight=0)  # Topmost button column fixed

    # Custom close button in title bar
    close_button = ttk.Button(frm, text='✕', width=2, command=close_app)
    close_button.grid(column=2, row=0, sticky='e', padx=5, pady=(5, 2))
    close_button.lift()  # Bring the close button to the front
    close_button.name = "close_button"  # Assign a name to the close button for identification

    # CPU Usage label & Graph
    cpu_label = ttk.Label(frm, text="CPU Usage: 0%", anchor='w')
    cpu_label.grid(column=0, row=0, sticky='w', pady=(5, 2))
    cpu_canvas = Canvas(frm, bg="white", highlightthickness=1, highlightbackground="gray")
    cpu_canvas.grid(column=0, row=1, columnspan=3, sticky='nsew', padx=5, pady=(0, 5))
    cpu_canvas.bind("<Configure>", on_resize)

    # RAM Usage label & Graph
    ram_label = ttk.Label(frm, text="RAM Usage: 0% (0GB/0GB)", anchor='w')
    ram_label.grid(column=0, row=2, columnspan=3, sticky='ew', pady=(5, 2))
    ram_canvas = Canvas(frm, bg="white", highlightthickness=1, highlightbackground="gray")
    ram_canvas.grid(column=0, row=3, columnspan=3, sticky='nsew', padx=5, pady=(0, 5))
    ram_canvas.bind("<Configure>", on_resize)

    # Always On Top Button
    topmost_button = IntVar(value=1) # 1 = always on top 🔝 ▲
    def toggle_topmost():
        root.attributes("-topmost", bool(topmost_button.get()))

    topmost_check = Checkbutton(frm, text="🔝", variable=topmost_button, command=toggle_topmost, font=('Segoe UI Emoji', 15))
    topmost_check.grid(column=1, row=0, sticky='w', padx=5, pady=(5, 2))

    # Add resizing handle at bottom right corner
    resize_frame = Frame(root, cursor="size_nw_se", bg="gray")
    resize_frame.name = 'resize_frame'  # Assign a name to the resize frame for identification
    resize_frame.place(relx=1.0, rely=1.0, anchor="se", width=15, height=15)
    resize_frame.bind("<ButtonPress-1>", start_resize)
    resize_frame.bind("<B1-Motion>", do_resize)
    resize_frame.bind("<ButtonRelease-1>", lambda e: root.configure(cursor=""))
    resize_frame.bind("<ButtonPress-1>", lambda e: "break", add="+")  # Prevent propagation to root for dragging

    frequency_monitor()  # Start monitoring in the background

    root.mainloop()
    

if __name__ == "__main__":
    main()