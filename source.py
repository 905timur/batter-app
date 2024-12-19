#!/usr/bin/env python3

import os
import subprocess
import tkinter as tk
from tkinter import messagebox

def show_about():
    messagebox.showinfo("About Batter", "Developer: Timur Gabaidulin\nEmail: timur.gab@gmail.com")

# Function to apply new TLP settings
def apply_settings(start_threshold, stop_threshold):
    try:
        # Path to the TLP config file
        tlp_config_path = "/etc/tlp.conf"

        # Check if the user has root permissions
        if os.geteuid() != 0:
            messagebox.showerror("Permission Error", "This program must be run as root.")
            return

        # Read the current TLP config file
        with open(tlp_config_path, "r") as f:
            lines = f.readlines()

        # Update the thresholds in the config file
        updated_lines = []
        for line in lines:
            if line.strip().startswith("START_CHARGE_THRESH_BAT0"):
                updated_lines.append(f"START_CHARGE_THRESH_BAT0={start_threshold}\n")
            elif line.strip().startswith("STOP_CHARGE_THRESH_BAT0"):
                updated_lines.append(f"STOP_CHARGE_THRESH_BAT0={stop_threshold}\n")
            else:
                updated_lines.append(line)

        # Write the updated configuration back to the file
        with open(tlp_config_path, "w") as f:
            f.writelines(updated_lines)

        # Restart TLP to apply the changes
        subprocess.run(["systemctl", "restart", "tlp"], check=True)

        # Show a success message
        messagebox.showinfo("Success", f"Settings applied successfully:\nStart: {start_threshold}%\nStop: {stop_threshold}%")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Create the GUI
def create_gui():
    # Main window
    root = tk.Tk()
    root.title("Batter")
    root.geometry("400x300")

    # Create menubar
    menubar = tk.Menu(root)
    root.config(menu=menubar)

    
    info_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Info", menu=info_menu)
    info_menu.add_command(label="About", command=show_about)

    
    tk.Label(root, text="Start Charging Threshold (%)", font=("Arial", 12)).pack(pady=10)
    start_var = tk.StringVar(value="20")  # Default value
    start_dropdown = tk.Spinbox(root, from_=0, to=100, textvariable=start_var, width=10, font=("Arial", 12))
    start_dropdown.pack()

    # Stop Threshold Label and Dropdown
    tk.Label(root, text="Stop Charging Threshold (%)", font=("Arial", 12)).pack(pady=10)
    stop_var = tk.StringVar(value="70")  # Default value
    stop_dropdown = tk.Spinbox(root, from_=0, to=100, textvariable=stop_var, width=10, font=("Arial", 12))
    stop_dropdown.pack()

    
    def on_apply():
        start = start_var.get()
        stop = stop_var.get()
        if not start.isdigit() or not stop.isdigit():
            messagebox.showerror("Input Error", "Please enter valid numeric thresholds.")
            return

        start = int(start)
        stop = int(stop)

        if start >= stop:
            messagebox.showerror("Input Error", "Start threshold must be less than stop threshold.")
            return

        apply_settings(start, stop)

    tk.Button(root, text="Apply Settings", command=on_apply, font=("Arial", 12), bg="green", fg="white").pack(pady=20)

    # Run the GUI loop
    root.mainloop()

# Run the program
if __name__ == "__main__":
    create_gui()
