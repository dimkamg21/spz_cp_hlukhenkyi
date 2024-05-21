import os
import tkinter as tk
from tkinter import ttk
from helpers.network_monitor import NetworkMonitor

def main():
    app = tk.Tk()
    app.title("Network Monitor")
    app.geometry('1000x460+300+200')
    app.configure(bg="gray63")

    style = ttk.Style(app)
    style.theme_use("clam")

    img_path = os.path.dirname(__file__)
    app.iconbitmap(os.path.join(img_path, 'speedtest.ico'))

    network_monitor = NetworkMonitor(app)
    gui = NetworkGUI(app, network_monitor)

    app.mainloop()

if __name__ == "__main__":
    main()
