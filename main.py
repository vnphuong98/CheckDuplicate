# Author: Nam Phuong Van
# OS: Windows 10, Version 2004, OS Build 19041.508
# Time created: 2020/09/15 19:44

from __future__ import print_function
from collections import defaultdict
import hashlib
import os
import sys
import tkinter
from tkinter import filedialog, messagebox

# Vairables
sourceFolder = []

# Functions
def chunk_reader(fobj, chunk_size=1024):
    while True:
        chunk = fobj.read(chunk_size)
        if not chunk:
            return
        yield chunk

def get_hash(filename, first_chunk_only=False, hash=hashlib.sha1):
    hashobj = hash()
    file_object = open(filename, 'rb')

    if first_chunk_only:
        hashobj.update(file_object.read(1024))
    else:
        for chunk in chunk_reader(file_object):
            hashobj.update(chunk)
    hashed = hashobj.digest()

    file_object.close()
    return hashed

def check_for_duplicates(paths, hash=hashlib.sha1):
    hashes_by_size = defaultdict(list)
    hashes_on_1k = defaultdict(list)
    hashes_full = {}
    outputFile = open("DuplicateSource.txt", "w")
    for path in paths:
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                full_path = os.path.join(dirpath, filename)
                try:
                    full_path = os.path.realpath(full_path)
                    file_size = os.path.getsize(full_path)
                    hashes_by_size[file_size].append(full_path)
                except (OSError,):
                    continue
    for size_in_bytes, files in hashes_by_size.items():
        if len(files) < 2:
            continue

        for filename in files:
            try:
                small_hash = get_hash(filename, first_chunk_only=True)
                hashes_on_1k[(small_hash, size_in_bytes)].append(filename)
            except (OSError,):
                continue

    for __, files_list in hashes_on_1k.items():
        if len(files_list) < 2:
            continue

        for filename in files_list:
            try:
                full_hash = get_hash(filename, first_chunk_only=False)
                duplicate = hashes_full.get(full_hash)
                if duplicate:
                    outputFile.writelines("{}            {}\n".format(filename, duplicate))
                else:
                    hashes_full[full_hash] = filename
            except (OSError,):
                continue
    outputFile.close()
    messagebox.showinfo("Finish", "Finish check Duplicate file")

# def AddSourceFolder():
#     for widget in frame.winfo_children():
#        widget.destroy()
#     sourceFolder.clear()
#     folder = filedialog.askdirectory()
#     sourceFolder.append(folder)
#     label = tkinter.Label(frame, text=folder)
#     label.pack()

# def FindDuplicate():
#     if(len(sourceFolder) == 0):
#         messagebox.showerror("Error", "Please select root foler")
#     else:
#         folder = sourceFolder[0]
#         check_for_duplicates(folder)

# Main
# Create GUI
#root = tkinter.Tk()
#root.title("Find duplicate source")

# Create frame
#frame = tkinter.Frame()
#frame.pack();

# Create Button select folder
#selectFolder = tkinter.Button(root, text="Select folder", padx=10, command=lambda: AddSourceFolder())
#selectFolder.pack()

# Create Button find duplicate find
#findDuplicate = tkinter.Button(root, text="Find duplicate source", padx=10, command=lambda: FindDuplicate())
#findDuplicate.pack()

#root.mainloop()

if sys.argv[1:]:
  check_for_duplicates(sys.argv[1:])
else:
   print("Please input the path")