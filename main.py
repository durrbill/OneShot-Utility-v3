from tkinter import *
from tkinter import ttk
import os
import shutil
import sys
from rubymarshal.reader import load as rb_load
from rubymarshal.writer import write as rb_write

root = Tk()
root.title("OneShot Utility V1.5")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

safeframe = ttk.Frame(mainframe, width=200, height=35, borderwidth=2, relief='sunken')
safeframe.grid(column=1, row=6, columnspan=2)

psettingspath = os.path.join(os.path.expanduser('~'), 'AppData', 'Roaming' '\Oneshot' '\p-settings.dat')
savepath = os.path.join(os.path.expanduser('~'), 'AppData', 'Roaming' '\Oneshot')
save = os.path.join(os.path.expanduser('~'), 'AppData', 'Roaming' '\Oneshot' '\save.dat')

status = ttk.Label(safeframe, text="111111", font=("Calibri Bold", 40), padding=("15 0 15 0"))
status.grid(sticky="")


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def get_psettings():
    with open(psettingspath, 'rb') as psettings:
        s = [rb_load(psettings), rb_load(psettings), rb_load(psettings)]
        return s

def set_psettings(data):
    with open(psettingspath, 'wb') as psettings:
        for d in data: rb_write(psettings, d)

data = get_psettings()

def resetdefault():
    data[0][1] = False
    data[0][9] = False
    set_psettings(data)
    os.remove(save)
    if FileNotFoundError:
        pass

def resetsolstice():
    data[0][1] = True
    data[0][9] = False
    set_psettings(data)
    os.remove(save)
    if FileNotFoundError:
        pass

def setsave(slocation):
    shutil.copy((slocation), savepath)

def safestatus():

    try:
        filepath = os.path.join(os.path.expanduser('~'), 'Documents', 'DOCUMENT.oneshot.txt')
        passworddocument = open(filepath, 'r', encoding='utf8')
        readabledocument = passworddocument.readlines()
        passworddocument.close()

        current_status = status["text"]
        current_status = readabledocument[int(len(readabledocument))-1].split()[-1]

    except FileNotFoundError:
        filepath = os.path.join(os.path.expanduser('~'), 'OneDrive', 'Documents', 'DOCUMENT.oneshot.txt')
        passworddocument = open(filepath, 'r', encoding='utf8')
        readabledocument = passworddocument.readlines()
        passworddocument.close()

        current_status = status["text"]
        current_status = readabledocument[int(len(readabledocument))-1].split()[-1]
    except:
        current_status = ""

    status["text"] = current_status

    root.after(1000, safestatus)

barrpath = resource_path("barrens\save.dat")
glenpath = resource_path("glen\save.dat")
refupath = resource_path("refuge\save.dat")
towepath = resource_path("tower\save.dat")
solbpath = resource_path("solbarrens\save.dat")
solgpath = resource_path("solglen\save.dat")
solrpath = resource_path("solrefuge\save.dat")
solepath = resource_path("solend\save.dat")

ttk.Button(mainframe, text="Full Reset", command=resetdefault, width=15).grid(column=1, row=1, sticky=W)
ttk.Button(mainframe, text="Solstice", command=resetsolstice, width=15).grid(column=2, row=1, sticky=W)
ttk.Button(mainframe, text="Barrens", command=lambda: setsave(barrpath), width=15).grid(column=1, row=2, sticky=W)
ttk.Button(mainframe, text="Glen", command=lambda: setsave(glenpath), width=15).grid(column=1, row=3, sticky=W)
ttk.Button(mainframe, text="Refuge", command=lambda: setsave(refupath), width=15).grid(column=1, row=4, sticky=W)
ttk.Button(mainframe, text="Tower", command=lambda: setsave(towepath), width=15).grid(column=1, row=5, sticky=W)
ttk.Button(mainframe, text="Barrens (NG+)", command=lambda: setsave(solbpath), width=15).grid(column=2, row=2, sticky=W)
ttk.Button(mainframe, text="Glen (NG+)", command=lambda: setsave(solgpath), width=15).grid(column=2, row=3, sticky=W)
ttk.Button(mainframe, text="Refuge (NG+)", command=lambda: setsave(solrpath), width=15).grid(column=2, row=4, sticky=W)
ttk.Button(mainframe, text="Ending (NG+)", command=lambda: setsave(solepath), width=15).grid(column=2, row=5, sticky=W)

root.after(1, safestatus())
root.mainloop()
