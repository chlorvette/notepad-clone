from tkinter import *
from tkinter import ttk
from tkinter.filedialog import *
from tkinter.simpledialog import *
from tkinter.messagebox import *
from datetime import *
import pyperclip # type: ignore


filetypes = (('text files', '*.txt'), ('All files', '*.*')) # Defining filetypes

# Defining functions/commands
def openfile(event=None):
    file = askopenfile(filetypes=filetypes)
    if file != None:
        text.delete("1.0", END)
        text.insert('1.0', file.read())
        window.title(f"{file.name} - Notepad")
        file.close()


def saveas(event=None):
    file = asksaveasfile(mode="w", defaultextension=".txt", filetypes=filetypes)
    if file != None:
        window.title(f"{file.name} - Notepad")
        file.write(text.get("1.0", END))
        file.close()
        return True
    else:
        return False


def update(event):
    title = window.title()
    if title == "Untitled - Notepad":
        window.title("*Untitled - Notepad")
    elif title == "*Untitled - Notepad" and text.get("1.0", END) == "\n":
        window.title("Untitled - Notepad")
    elif title[0] != "*":
        window.title("*" + title)
    else:
        return


def new(event=None):
    window.title("Untitled - Notepad")
    text.delete("1.0", END)


def wordwrapon():
    text['wrap'] = 'word'


def wordwrapoff():
    text['wrap'] = 'none'


def get_selected():
    try:
        return text.selection_get()
    except TclError:
        return None

def cut():
    pyperclip.copy(get_selected())
    text.delete(SEL_FIRST, SEL_LAST)


def copy():
    pyperclip.copy(get_selected())
    root.update()


def paste():
    text.insert(text.index(INSERT), root.clipboard_get())


def timedate(event=None):
    date = datetime.now()
    insert_date = date.strftime("%I") + ":" + date.strftime("%M") + " " + date.strftime("%p") + " " + date.strftime("%m") + "/" + date.strftime("%d") + "/" + date.strftime("%Y")
    text.insert(text.index(INSERT), insert_date)


def onclose():
    if window.title()[0] == "*":
        prompt = askyesnocancel("Notepad", f"Do you want to save changes to {window.title()[1:len(window.title()) - 10]}?")
        if prompt:
            temp = saveas()
            if temp:
                root.destroy()
        elif prompt == False:
            root.destroy()
        else:
            return
    else:
        root.destroy()


def create_info_win():
    win = Tk()
    win.resizable(False, False)
    return win


def viewhelp():
    help = create_info_win()
    help.title("Help")
    label = Label(help, text="Here you would usually find help.")
    label.pack(padx=10, pady=20)


def about():
    about = create_info_win()
    about.title("About Notepad")
    label = Label(about, text="Here you would find information about this application.")
    label.pack(padx=10, pady=20)


def undo():
    text.edit_undo()


def select_all():
    text.tag_add(SEL, "1.0", END)
    text.mark_set(INSERT, "1.0")

# Initiating/creating window and root
root = Tk()
root.withdraw()
window = Toplevel(root)
window.title("Untitled - Notepad")
window.option_add('*tearOff', FALSE)

# Creating menubars
menubar = Menu(window)
window['menu'] = menubar
menu_file = Menu(menubar)
menu_edit = Menu(menubar)
menu_format = Menu(menubar)
menu_help = Menu(menubar)
menubar.add_cascade(menu=menu_file, label="File")
menubar.add_cascade(menu=menu_edit, label="Edit")
menubar.add_cascade(menu=menu_format, label="Format")
menubar.add_cascade(menu=menu_help, label="Help")
menu_file.add_command(label='New', command=new)
menu_file.add_command(label='Open', command=openfile)
menu_file.add_command(label="Save As", command=saveas)
menu_file.add_separator()
menu_file.add_command(label='Exit', command=root.destroy)
menu_edit.add_command(label="Cut", command=cut)
menu_edit.add_command(label="Copy", command=copy)
menu_edit.add_command(label="Paste", command=paste)
menu_edit.add_command(label="Undo", command=undo)
menu_edit.add_separator()
menu_edit.add_command(label="Select All", command=select_all)
menu_edit.add_command(label="Time/Date", command=timedate)
wordwrap = Menu(menu_format)
menu_format.add_cascade(menu=wordwrap, label="Word Wrap")
wordwrap.add_command(label="On", command=wordwrapon)
wordwrap.add_command(label="Off", command=wordwrapoff)
menu_help.add_command(label="View Help", command=viewhelp)
menu_help.add_separator()
menu_help.add_command(label="About Notepad", command=about)

# Creating text field/Defining Keyboard Shortcuts & Keybinds/Defining events
text = Text(window, wrap="none", undo=True, autoseparators=True, maxundo=100)
text.bind("<KeyRelease>", update)
text.bind("<F5>", timedate)
window.bind("<Control-o>", openfile)
window.bind("<Control-O>", openfile)
window.bind("<Control-n>", new)
window.bind("<Control-N>", new)
window.bind("<Control-Shift-s>", saveas)
window.bind("<Control-Shift-S>", saveas)
window.protocol("WM_DELETE_WINDOW", onclose)

# Scrollbars
scrolly = ttk.Scrollbar(window, orient = VERTICAL, command = text.yview)
scrollx = ttk.Scrollbar(window, orient = HORIZONTAL, command = text.xview)
text.grid(column = 0, row = 0, sticky = 'nwes')
scrollx.grid(column = 0, row = 1, sticky = 'we')
scrolly.grid(column = 1, row = 0, sticky = 'ns')
text['yscrollcommand'] = scrolly.set
text['xscrollcommand'] = scrollx.set

# Handling resize
window.columnconfigure(0, weight=1)
window.rowconfigure(0, weight=1)
text.columnconfigure(0, weight=3)

window.mainloop()