import os, subprocess
import tkinter as tk
from tkinter import messagebox
import shutil

def convert_single_video(input_file, output_file=None):
    video_exts = ('.mp4', '.mkv', '.avi', '.mov', '.flv', '.wmv')
    ffmpeg_path = os.path.join(os.path.dirname(__file__), 'redist', 'ffmpeg.exe')

    if not input_file.lower().endswith(video_exts):
        print("Input file is not a supported video format.")
        return

    if not os.path.isfile(input_file):
        print("Input file does not exist.")
        return

    if output_file is None:
        output_dir = os.path.join(os.path.dirname(__file__), 'OUTPUT')
        os.makedirs(output_dir, exist_ok=True)
        base_name = os.path.splitext(os.path.basename(input_file))[0]
        output_file = os.path.join(output_dir, f"{base_name}.mp4")

    cmd = [
        ffmpeg_path,
        '-y',
        '-i', input_file,
        '-vf', 'scale=-1:1080',
        '-c:a', 'aac',
        '-c:v', 'libx264',
        '-profile:v', 'high',
        '-level:v', '4.2',
        '-r', '60',
        output_file
    ]

    subprocess.run(cmd, check=True)

def unite_videos_in_folder(folder_path, output_file=None):
    video_exts  = ('.mp4', '.mkv', '.avi', '.mov', '.flv', '.wmv')
    ffmpeg_path = os.path.join(os.path.dirname(__file__), 'redist', 'ffmpeg.exe')
    videos      = [f for f in os.listdir(folder_path) if f.lower().endswith(video_exts)]
    videos.sort()

    if not videos:
        print("No video files found in the folder.")
        return

    if output_file is None:
        folder_name = os.path.basename(os.path.normpath(folder_path))
        output_dir = os.path.join(os.path.dirname(__file__), 'OUTPUT')
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, f"{folder_name}.mp4")

    filelist_path = os.path.join(folder_path, 'filelist.txt')
    with open(filelist_path, 'w', encoding='utf-8') as f:
        for video in videos:
            f.write(f"file '{os.path.join(folder_path, video).replace("'", r'\'')}'\n")

    cmd = [
        ffmpeg_path,
        '-y',
        '-f', 'concat',
        '-safe', '0',
        '-i', filelist_path,
        '-vf', 'scale=-1:1080',
        '-c:a', 'aac',
        '-c:v', 'libx264',
        '-profile:v', 'high',
        '-level:v', '4.2',
        '-r', '60',
        output_file
    ]

    subprocess.run(cmd, check=True)
    os.remove(filelist_path)


def convert(root, listbox, obj_list):
    input_dir = os.path.join(os.path.dirname(__file__), 'INPUT')
    for i, obj in enumerate(os.listdir(input_dir)):
        obj_path = os.path.join(input_dir, obj)
        if os.path.isfile(obj_path):
            convert_single_video(obj_path)
        elif os.path.isdir(obj_path):
            unite_videos_in_folder(obj_path)
        update_listbox_status("✅", i, listbox, obj_list)
        root.update_idletasks()

def update_listbox_status(symbol, i, listbox, obj_list):
    listbox.delete(i)
    listbox.insert(i, f"{obj_list[i]} {symbol}")

def convert_with_status(root, listbox, obj_list):
    for i, obj in enumerate(obj_list):
        update_listbox_status("⏳", i, listbox, obj_list)
    root.update_idletasks()
    try:
        convert(root, listbox, obj_list)
        messagebox.showinfo("Success", "Conversion completed successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred:\n{e}")

def get_object_list():
    input_dir = os.path.join(os.path.dirname(__file__), 'INPUT')
    obj_list = os.listdir(input_dir) if os.path.exists(input_dir) else []
    return obj_list



if __name__ == "__main__":
    root = tk.Tk()
    root.title("Video Converter")


    label = tk.Label(root, text="Detected videos:", font=("Arial", 12))
    label.pack(padx=20, pady=(20, 0), anchor='w')
    obj_list = get_object_list()

    listbox = tk.Listbox(root, width=50, height=10)
    for obj in obj_list:
        listbox.insert(tk.END, obj)
    listbox.pack(padx=20, pady=(20, 0))

    def refresh_list():
        listbox.delete(0, tk.END)
        obj_list.clear()
        obj_list.extend(get_object_list())
        for obj in obj_list:
            listbox.insert(tk.END, obj)

    refresh_btn = tk.Button(
        root,
        text="Refresh",
        command=refresh_list,
        width=8,
        height=1
    )
    refresh_btn.pack(padx=20, pady=(10, 0), anchor='e')

    def get_free_space_gb(path):
        total, used, free = shutil.disk_usage(path)
        return free / (1024 * 1024 * 1024)

    free_space_gb = get_free_space_gb(os.path.dirname(__file__))
    free_space_label = tk.Label(root, text=f"Free space: {free_space_gb:.2f} GB", font=("Arial", 10))
    free_space_label.pack(padx=20, pady=(0, 10), anchor='w')

    convert_btn = tk.Button(
        root,
        text="Convert",
        command=lambda: convert_with_status(root, listbox, obj_list),
        width=20,
        height=2
    )
    convert_btn.pack(padx=20, pady=20)

    root.mainloop()
