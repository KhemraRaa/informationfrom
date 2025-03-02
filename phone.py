import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os

# Function to list connected ADB devices
def list_devices():
    output = os.popen("adb devices").read()
    text_output.insert(tk.END, output + "\n")

# Function to run a custom ADB shell command
def run_shell_command():
    command = command_entry.get()
    if command.strip():
        output = os.popen(f"adb shell {command}").read()
        text_output.insert(tk.END, f"$ {command}\n{output}\n")
    else:
        messagebox.showwarning("Warning", "Please enter a shell command.")

# Function to install an APK file
def install_apk():
    apk_path = filedialog.askopenfilename(filetypes=[("APK files", "*.apk")])
    if apk_path:
        os.system(f"adb install \"{apk_path}\"")
        text_output.insert(tk.END, f"Installed APK: {apk_path}\n")

# Function to uninstall an app by package name
def uninstall_app():
    package = package_entry.get()
    if package.strip():
        os.system(f"adb uninstall {package}")
        text_output.insert(tk.END, f"Uninstalled app: {package}\n")
    else:
        messagebox.showwarning("Warning", "Please enter a package name.")

# Function to pull a file from the device
def pull_file():
    remote_path = filedialog.askstring("Remote File", "Enter remote file path:")
    local_path = filedialog.askdirectory()
    if remote_path and local_path:
        os.system(f"adb pull \"{remote_path}\" \"{local_path}\"")
        text_output.insert(tk.END, f"Pulled file from {remote_path} to {local_path}\n")

# Function to push a file to the device
def push_file():
    local_path = filedialog.askopenfilename()
    remote_path = filedialog.askstring("Remote Path", "Enter remote destination path:")
    if local_path and remote_path:
        os.system(f"adb push \"{local_path}\" \"{remote_path}\"")
        text_output.insert(tk.END, f"Pushed file from {local_path} to {remote_path}\n")

# Function to take a screenshot
def take_screenshot():
    os.system("adb shell screencap -p /sdcard/screenshot.png")
    os.system("adb pull /sdcard/screenshot.png .")
    text_output.insert(tk.END, "Screenshot saved as screenshot.png\n")

# Function to show device information
def show_device_info():
    output = os.popen("adb shell getprop").read()
    text_output.insert(tk.END, "Device Info:\n" + output + "\n")

# GUI Setup
root = tk.Tk()
root.title("ADB Remote Control Tool")
root.geometry("600x500")

# Frame for command execution
frame_top = tk.Frame(root)
frame_top.pack(pady=5)

tk.Label(frame_top, text="ADB Shell Command:").grid(row=0, column=0, padx=5, pady=5)
command_entry = tk.Entry(frame_top, width=40)
command_entry.grid(row=0, column=1, padx=5, pady=5)
tk.Button(frame_top, text="Run", command=run_shell_command).grid(row=0, column=2, padx=5, pady=5)

# Frame for APK and File Management
frame_middle = tk.Frame(root)
frame_middle.pack(pady=5)

tk.Button(frame_middle, text="List Devices", command=list_devices).grid(row=0, column=0, padx=5, pady=5)
tk.Button(frame_middle, text="Install APK", command=install_apk).grid(row=0, column=1, padx=5, pady=5)
tk.Button(frame_middle, text="Uninstall App", command=uninstall_app).grid(row=0, column=2, padx=5, pady=5)

tk.Label(frame_middle, text="Package Name:").grid(row=1, column=0, padx=5, pady=5)
package_entry = tk.Entry(frame_middle, width=25)
package_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Button(frame_middle, text="Pull File", command=pull_file).grid(row=2, column=0, padx=5, pady=5)
tk.Button(frame_middle, text="Push File", command=push_file).grid(row=2, column=1, padx=5, pady=5)
tk.Button(frame_middle, text="Screenshot", command=take_screenshot).grid(row=2, column=2, padx=5, pady=5)
tk.Button(frame_middle, text="Device Info", command=show_device_info).grid(row=3, column=1, padx=5, pady=5)

# Text Output
text_output = scrolledtext.ScrolledText(root, height=15, width=70)
text_output.pack(pady=10)

# Start GUI loop
root.mainloop()
