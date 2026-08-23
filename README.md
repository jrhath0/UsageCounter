# UsageCounter
**Simple CPU and RAM Usage Monitoring Widget**

A lightweight, borderless system resource monitor built with Python and Tkinter.  Displays real-time CPU and RAM usage with live updating graphs.

```!(UsageCounter.png)```

**Features**
- Real-time Monitoring - Updates every second with current CPU and RAM usage
- Live Graphs - Visual representation of usage history for CPU and RAM
- Borderless Window - Clean and minimal interface
- Always On Top - Toggle-able option to keep window above other applications
- Resizable - Drag from the bottom-right corner to resize the window
- Draggable - Click and drag anywhere within the window to reposition it

**Requirements**
- Python 3.6+
- psutil Library
- tkinter Library
- logging Library

**Usage**
- Click and drag anywhere on the window to move it
- Use the bottom-right corner to resize the window
- Click the '✕' button in the top-right to close the application
- Toggle "Always on Top" to keep the window above other applications

**Other Infor**
- Current update interval is 1 second
- Graph history contains 50 data points
