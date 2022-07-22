import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
global GLOB
GLOB = True
# root window
root = tk.Tk()
root.geometry('300x220')
root.resizable(False, False)
root.title('Radio Button Demo')


def show_selected_size():
    showinfo(
        title='Result',
        message=selected_size.get()
    )


selected_size = tk.IntVar()


# label
label = ttk.Label(text="What's your t-shirt size?")
label.pack(fill='x', padx=5, pady=5)


yes = tk.Radiobutton(
        root,
        text='yes',
        value=1,
        variable=selected_size
    )
no = tk.Radiobutton(
        root,
        text='no',
        value=0,
        variable=selected_size
    )
# radio buttons
for r in (yes, no):
    r.pack(fill='x', padx=5, pady=5)



def f(event=None):
    global GLOB
    GLOB = not GLOB
    # if GLOB:
    #     yes.select()
    # else:
    #     no.select()
    selected_size.set(GLOB)

# button
button = ttk.Button(
    root,
    text="Get Selected Size",
    command=f)

button.pack(fill='x', padx=5, pady=5)


root.mainloop()