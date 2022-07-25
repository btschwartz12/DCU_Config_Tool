import os
from tkinter import filedialog


def process_files():
    name = filedialog.asksaveasfile(mode='w', initialfile='piper').name
    os.makedirs(name)


process_files()