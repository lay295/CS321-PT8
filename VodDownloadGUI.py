import os.path
from tkinter import filedialog
from tkinter import *

def start():
    # Start downloading and everything else
    # Globals are printed below for debug and informational purposes.
    print(input_url.get())
    print(time_length.get())
    print(folder_path.get())
    print(save_name.get())


def start_button():
    #Saves all the globals that are currently in the fillable boxes
    clear_labels()
    global save_name
    save_name.set(SaveFileNameTxt.get())
    global folder_path
    folder_path.set(SaveDestTxt.get())
    global input_url
    input_url.set(URLtxt.get())
    global time_length
    safe = spinbox.get().isdecimal()
    if safe:
        time_length.set(spinbox.get())
    else:
        sanitize_time_length_failed()

    if safe and handle_folder_path_check() and handle_time_length_check() and handle_input_url_check() and handle_save_name_check():
        lbl5.config(text="Correct Settings: Starting")
        clear_labels()
        start()
    else:
        lbl5.config(text="Incorrect Settings")


def handle_folder_path_check():
    if os.path.isdir(folder_path.get()):
        lbl6.config(text="Correct Path")
        return True
    lbl6.config(text="Incorrect Path")
    return False


def handle_save_name_check():
    if len(save_name.get()) == 0:
        lbl7.config(text="Invalid Name")
        return False
    lbl7.config(text="Valid Name")
    return True


def sanitize_time_length_failed():
    lbl6.config(text="Length contains non-number")


def handle_time_length_check():
    if 0 < time_length.get() <= 30:
        lbl8.config(text="Valid Length")
        return True
    lbl8.config(text="Invalid Length")
    return False


def handle_input_url_check():
    lbl8.config(text="Valid URL")
    return True


def clear_labels():
    lbl6.config(text="")
    lbl7.config(text="")
    lbl8.config(text="")
    lbl9.config(text="")


def browse_button():
    # Allow user to select a directory and store it in global var called folder_path
    global folder_path
    filename = filedialog.askdirectory()
    folder_path.set(filename)
    set_text_input(filename)


def set_text_input(text):
    SaveDestTxt.delete(0, "end")
    SaveDestTxt.insert(0, text)


window = Tk()
window.title("Vod Downloader App")
window.geometry('500x300')

folder_path = StringVar()
save_name = StringVar()
input_url = StringVar()
time_length = IntVar()


lbl1 = Label(window, text="Input URL:", anchor="w", justify=LEFT, width=23)
lbl1.grid(row=0, column=0)
URLtxt = Entry(window,width=45)
URLtxt.grid(row=0, column=1)

lbl2 = Label(window, text="Target video length(minutes):", anchor="w", justify=LEFT, width=23)
lbl2.grid(row=1, column=0)
spinbox = Spinbox(window, from_=1, to=30, width=5)
spinbox.grid(row=1, column=1)

lbl3 = Label(window, text="Output Destination:", anchor="w", justify=LEFT, width=23)
lbl3.grid(row=2, column=0)
SaveDestTxt = Entry(window,width=45)
SaveDestTxt.grid(row=2, column=1)
SaveDestTxt.delete(0, "end")
SaveDestTxt.insert(0, "Click Browse to select a destination to save your file!")
browse = Button(text="Browse", command=browse_button)
browse.grid(row=2, column=2)

lbl4 = Label(window, text="File Name:", anchor="w", justify=LEFT, width=23)
lbl4.grid(row=3, column=0)
SaveFileNameTxt = Entry(window,width=45)
SaveFileNameTxt.grid(row=3, column=1)

lbl5 = Label(window, text="", width=23)
lbl5.grid(row=4, column=0)
StartButton = Button(text="Start", command=lambda: start_button())
StartButton.grid(row=4, column=1)

lbl6 = Label(window, text="", width=23)
lbl6.grid(row=5, column=0)

lbl7 = Label(window, text="", width=23)
lbl7.grid(row=6, column=0)

lbl8 = Label(window, text="", width=23)
lbl8.grid(row=7, column=0)

lbl9 = Label(window, text="", width=23)
lbl9.grid(row=7, column=0)

mainloop()

