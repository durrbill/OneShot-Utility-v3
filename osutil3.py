import shutil, sys, glob, tkinter, psutil, zipfile, signal, json, subprocess, winreg, os
from ast import Index
from os import listdir
from pathlib import Path
from zipfile import ZipFile
from os.path import isfile, join
from win32com.client import Dispatch
from tkinter import filedialog, ttk, simpledialog, Tk, END, Toplevel, StringVar
from rubymarshal.reader import load as rb_load
from rubymarshal.writer import write as rb_write
from tkinter.messagebox import showinfo as msgbox, showwarning as warnbox
from tkinter.filedialog import askopenfilename as openfile, asksaveasfilename as savefile

# Frame and variable assignments
root, delmode, autoload, autobutton, savesdict = Tk(), False, False, tkinter.IntVar(), {}
savepath = os.path.join(os.path.expanduser('~'), 'AppData', 'Roaming' '\\Oneshot')
root.resizable(False, False)
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
root.title("OneShot Utility v3.4")
customsavepath = savepath + "\\customsaves\\"
psettings_path = os.path.join(os.path.expanduser('~'), 'AppData', 'Roaming' '\Oneshot' '\p-settings.dat')
root.iconbitmap(os.path.join(getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__))), r"ico\icon.ico"))


mainframe = ttk.Frame(root, padding="3 3 3 3")
mainframe.grid(column=0, row=0, sticky="nsew")

saveframe = ttk.Frame(root, padding="3 3 3 3")
saveframe.grid(column=1, row=0, sticky="nsew")

infolabel = (ttk.Label(mainframe, relief='sunken', text="OneShot Utility v3.4", padding="4 3 3 3", width=24))
infolabel.grid(sticky="nsew", columnspan=2)

safecode = ttk.Label(mainframe, text="000000", font=('System', 40))
safecode.grid(row=7, column=0, columnspan=2, rowspan=2)

clovercheck = ttk.Label(mainframe, text="Clover: idk", font=('System', 20))
clovercheck.grid(row=9, column=0, columnspan=2, rowspan=1, sticky="n")

namebox = ttk.Entry(mainframe, width=16)
namebox.grid(row=4, column=1, columnspan=1, rowspan=1)


def check_psettings():  # Checks to see if p-settings.dat exists, which is required for the utility to function
    if not os.path.exists(os.path.join(os.path.expanduser('~'), 'AppData', 'Roaming', 'Oneshot', 'p-settings.dat')):
        warnbox("Error", "p-settings.dat not found. Ensure you have run OneShot at least once.")
        sys.exit()

def check_steamshim():  # Checks to see if steamshim.exe exists in expected path, prompts user for location otherwise
    if os.path.exists(r"C:\Program Files (x86)\Steam\steamapps\common\OneShot\steamshim.exe"):
        return r"C:\Program Files (x86)\Steam\steamapps\common\OneShot\steamshim.exe"
    elif os.path.exists(savepath + r"\steamshimlocation.txt"):
        return open(savepath + r"\steamshimlocation.txt", "r").readline()
    else:
        msgbox("Error",
               "steamshim.exe not found. Please locate steamshim.exe in your OneShot installation folder.\n\n"
               "Note that this is typically located in C:/Program Files (x86)/Steam/steamapps/common/OneShot")
        shorttargetbase = openfile(filetypes=[("Executable File", ".exe")])
        with open(savepath + r"\steamshimlocation.txt", "w+") as steamshimloc:
            steamshimloc.write(shorttargetbase)
            return steamshimloc.readline()


def autoload_toggle(change):  # When called, globally toggles the state of autoloading via checking for an empty .txt file
    if os.path.exists(savepath + r"\loadstate.txt"):
        if change == 1:
            os.remove(savepath + r"\loadstate.txt")
            infolabel["text"] = "Auto-load on save select: off"
            return
        return True
    else:
        if change == 1:
            open(savepath + r"\loadstate.txt", "x")
            infolabel["text"] = "Auto-load on save select: on"
            return
        return False

# Creates the autoload checkbox and checks its last known state
if autoload_toggle(0): autobutton.set(1)
elif not autoload_toggle(0): autobutton.set(0)
loadbtn = ttk.Checkbutton(mainframe, text="Close/Open game on save load?", command=lambda: autoload_toggle(1), onvalue=1, offvalue=0, padding="0 5 0 0", variable=autobutton)
loadbtn.grid(row=6, column=0, columnspan=2)


def make_basebutton(txt, cmd, clm, row):  # Creates buttons used for basic functions
    ttk.Button(mainframe, text=txt, command=cmd, width=16).grid(column=int(clm), row=int(row))


def set_psettings(pdata):  # Function to edit p-settings.dat
    with open(psettings_path, "wb") as psettings:
        for d in pdata:
            rb_write(psettings, d)


def get_psettings():  # Function to read p-settings.dat
    with open(psettings_path, 'rb') as psettings:
        s = [rb_load(psettings), rb_load(psettings), rb_load(psettings)]
        return s


def get_playername():  # Reads p-settings.dat for current player name
    name = get_psettings()[2]
    namebox.delete(0, END)
    namebox.insert(0, name)


def delete_mode(state):  # Toggles "delete mode" which determines if custom saves are loaded or deleted when clicked
    global delmode
    if not state:
        if delmode:
            infolabel["text"] = "Delete mode disabled"
        delmode = False
    elif delmode:
        infolabel["text"] = "Delete mode disabled"
        delmode = False
    else:
        infolabel["text"] = "Select a save to delete"
        delmode = True


def set_playername():  # Changes the player's name by editing p-settings.dat
    if check_program("oneshot.exe"):
        return
    name = namebox.get().strip()
    if len(name) == 0:
        warnbox("No name entered", "Please enter a player name.")
    data[2] = name
    set_psettings(data)
    delete_mode(False)
    infolabel["text"] = f"Player name set to: {name}"
    namebox.delete(0, END)
    namebox.insert(0, name)


def check_program(prog):  # Checks to see if the specified program (oneshot.exe or ______.exe) is running
    cmd = 'tasklist /fi "imagename eq {}"'.format(prog)
    output = subprocess.check_output(cmd, shell=True).decode('cp437')
    if prog.lower() in output.lower(): return True
    else: return False


def about():  # Displays info about the program
    msgbox("About", "OneShot Utility v3.4 by durrbill\nSome code from Firestrike and hunternet93\n\n"
                    "For help with utility, visit https://github.com/durrbill/OneShot-Utility-v3")
    delete_mode(False)


def restart_game():  # Force closes OneShot.exe and reopens it
    for pid in (process.pid for process in psutil.process_iter() if process.name() == "oneshot.exe"):
        os.kill(pid, signal.SIGABRT)
    os.chdir(str(check_steamshim().split("steamshim.exe")[0]))
    os.startfile(check_steamshim().split("steamshim.exe")[0] + r"\oscut.lnk")


def game_reset(reset_type):  # Resets the game to the specified state
    delete_mode(False)
    data[0][9] = False
    try: os.remove(savepath + r"\save.dat")
    except FileNotFoundError: pass

    if reset_type == "full":
        data[0][1] = False
        if not autoload_toggle(0):
            infolabel["text"] = "Game reset to Any%"
        else:
            infolabel["text"] = "Any% run reset"
            restart_game()
    elif reset_type == "sol":
        data[0][1] = True
        if not autoload_toggle(0):
            infolabel["text"] = "Game reset to NG+"
        else:
            infolabel["text"] = "NG+ run reset"
            restart_game()
    set_psettings(data)


def import_saves():  # Imports .zip savepacks created by the utility
    delete_mode(False)
    msgbox("Import Saves", "Please select a valid .zip file to import saves from.\n\n"
                           "Note that imported savepacks will replace all existing saves.\n\n"
                           "Export your current saves if you wish to use them later.")
    importfile = openfile(filetypes=[("Zip Archives", ".zip")])
    with zipfile.ZipFile(importfile, 'r') as zip_file:
        file_list = zip_file.namelist()
        if "customsaves.json" in file_list:
            try: shutil.rmtree(customsavepath)
            except FileNotFoundError: pass
            btnlist = saveframe.grid_slaves()
            for li in btnlist: li.destroy()
            with zipfile.ZipFile(importfile, 'r') as zip_ref:
                zip_ref.extract("customsaves.json", savepath)
                for file in zip_ref.namelist():
                    if file.startswith("customsaves"):
                        zip_ref.extract(file, savepath)
            check_for_saves()
            zipname = importfile.split("/")[-1]
            infolabel["text"] = f"Imported {zipname}"
        else:
            warnbox("Error", "Invalid .zip. Ensure the chosen .zip was created by OneShot Utility v3.4.")


def export_saves():  # Exports current saves into a .zip savepack which can be imported later
    delete_mode(False)
    if not len(os.listdir(customsavepath)) == 0:
        savepack_loc = savefile(filetypes=[("Zip Archives", ".zip")])
        with ZipFile(savepack_loc + ".zip", "w") as zip_obj:
            saveslist = glob.glob(f"{customsavepath}*")
            src = Path(savepath)
            file = Path(savepath + "\\customsaves.json")
            for i in saveslist:
                zip_obj.write(i, arcname=Path(i).relative_to(src))
            zip_obj.write(file, arcname=file.relative_to(src))
            infolabel["text"] = "Saves exported successfully"
    else:
        warnbox("Export Saves", r"Export failed. Ensure you have custom saves present in a customsaves folder.")


def new_custom_save():  # Creates a new custom save, creating pathing if necessary and placing its button in the grid
    delete_mode(False)
    msgbox("New Save", "Please select a valid .dat save file to use.\n\n"
                       "Note that invalid .dat files will be nonfunctional.")
    newsavepath = openfile(filetypes=[("Save Files", ".dat")])

    if not os.path.exists(customsavepath):
        os.makedirs(customsavepath)
    if os.path.exists(customsavepath + newsavepath.split("/")[-1]) and newsavepath.split("/")[-1].endswith(".dat"):
        warnbox("Error", "Custom saves folder already contains " +
                str(newsavepath.split("/")[-1]) + " Rename your chosen .dat file and retry.")
        return
    elif newsavepath != '':
        customname = tkinter.simpledialog.askstring("New Custom Save", "Enter a name for this custom save.")
    else:
        return

    illegal_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']

    if any(x in customname for x in illegal_chars):
        warnbox("Error", r"Name cannot contain the following characters: / \ * ? < > : |")
        return
    elif customname.startswith(' ') or customname.endswith(' ') or customname == "":
        warnbox("Error", "Custom name cannot begin or end with an empty character.")
        return
    elif os.path.exists(customsavepath + str(customname) + ".dat"):
        warnbox("Error", "Custom name is already in use.")
        return

    shutil.copy(newsavepath, customsavepath)
    os.rename(customsavepath + str(newsavepath.split("/")[-1]), customsavepath + customname + ".dat")
    column_override = str(f'{len(savesdict):02d}'[0])
    infolabel["text"] = f"New save created: {customname}"

    if len(savesdict) >= 10:
        row_override = len(savesdict) - (10 * int(str(len(savesdict))[0]))
    else:
        row_override = len(savesdict)

    savecount = str(len(savesdict) + 1)
    (ttk.Button(saveframe, text=str(customname), width=18, command=lambda: set_save(savesdict[savecount]))
     .grid(row=row_override, column=2 + int(column_override), sticky="nw"))

    savesdict[str(len(savesdict) + 1)] = customname
    with open(savepath + r'\customsaves.json', 'w') as savesdict_json:
        json.dump(savesdict, savesdict_json)


def set_save(newsave):  # Called when a save button is pressed, can either load or delete the chosen save from the list
    if not delmode:
        delete_mode(False)
        infolabel["text"] = f"Game save set to: {newsave}"
        shutil.copy(customsavepath + newsave + ".dat", savepath)
        if os.path.exists(savepath + "/" + "save.dat"):
            os.remove(savepath + "/save.dat")
        os.rename(savepath + "/" + newsave + ".dat", savepath + "/save.dat")
        if autoload_toggle(0):
            restart_game()

    else:
        infolabel["text"] = "DELETE MODE: Choose a save to remove"
        removed_key = list(savesdict.keys())[list(savesdict.values()).index(newsave)]
        saveslistcount = len(savesdict)

        for i in range(1, len(savesdict) + 1):
            if int(i) >= int(removed_key):
                if int(i) == int(saveslistcount):
                    savesdict.pop(str(i))
                else:
                    savesdict[str(int(i))] = savesdict[str(int(i) + 1)]

        os.remove(customsavepath + newsave + ".dat")
        if len(os.listdir(customsavepath)) == 0:
            savesdict.clear()

        def delete_all_saves():
            for btns in saveframe.grid_slaves():
                btns.destroy()
        with open(savepath + r'\customsaves.json', 'w') as savesdict_json:
            json.dump(savesdict, savesdict_json)

        delete_all_saves(), check_for_saves(), delete_mode(True)
        infolabel["text"] = f"Save '{newsave}' deleted"


def check_for_saves():  # Updates custom save list when the program is opened, or other relevant functions are called
    if os.path.exists(savepath + r'\customsaves.json'):
        if os.path.getsize(savepath + r'\customsaves.json') > 1:
            savesdict.clear()
            with open(savepath + r'\customsaves.json') as csjson:
                savesdict.update(json.load(csjson))

            for i in range(len(savesdict)):
                column_override = str(f'{int(i):02d}'[0])
                if int(i) >= 10:
                    row_override = int(i) - (10 * int(str(i)[0]))
                else:
                    row_override = int(i)
                ttk.Button(saveframe, text=str(savesdict[str(int(i) + 1)]), width=18,
                           command=lambda i = i: set_save(savesdict[str(int(i) + 1)])
                           ).grid(column=2 + int(column_override), row=row_override, sticky="nw")

def check_safe():  # Checks DOCUMENT.oneshot.txt every two seconds, located via windows registry entries
    try:
        reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders")
        documents_path = winreg.QueryValueEx(reg_key, "Personal")[0] + r"\DOCUMENT.oneshot.txt"
        winreg.CloseKey(reg_key)

        with open(documents_path, 'r', encoding='utf8') as safe_doc:
            safe_data = safe_doc.readlines()
            safecode["text"] = safe_data[len(safe_data)-1].split()[-1]
    except FileNotFoundError:
        safecode["text"] = "000000"

    if check_program("_______.exe"):
        clovercheck["text"] = "Clover: Yes"
    else:
        clovercheck["text"] = "Clover: No"

    root.after(2000, check_safe)


# Calls 'make_basebutton', passing each button's properties and position to the function
make_basebutton("Full Reset (Any%)", lambda: game_reset("full"), 0, 2)
make_basebutton("Full Reset (NG+)", lambda: game_reset("sol"), 1, 2)
make_basebutton("New Save", lambda: new_custom_save(), 0, 3)
make_basebutton("Delete Save", lambda: delete_mode(True), 1, 3)
make_basebutton("Set Player Name:", lambda: set_playername(), 0, 4)
make_basebutton("Import Saves", lambda: import_saves(), 0, 5)
make_basebutton("Export Saves", lambda: export_saves(), 1, 5)
aboutbtn = ttk.Button(mainframe, width=3, text="?", command=lambda: about())
aboutbtn.grid(row=0, column=1, sticky='e')


# Various function calls and variable assignments
shell = Dispatch('WScript.Shell')
shortcut = shell.CreateShortCut(check_steamshim().split("steamshim.exe")[0] + r"\oscut.lnk")
shortcut.Targetpath = check_steamshim()
shortcut.save()
data = get_psettings()
check_safe()
get_playername()
check_for_saves()
root.mainloop()
