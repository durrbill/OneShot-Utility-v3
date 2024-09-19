import os
import shutil
import sys
import glob
import time
import tkinter
import psutil
import zipfile
import configparser
import tkinter.simpledialog
from ast import Index
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from zipfile import ZipFile
from tkinter.filedialog import askopenfilename
from rubymarshal.reader import load as rb_load
from rubymarshal.writer import write as rb_write
from os import listdir
from os.path import isfile, join

root = Tk()
root.title("OneShot Utility V3.2")
root.resizable(False, False)
config = configparser.ConfigParser()


# Tkinter frame setup
mainFrame = ttk.Frame(root, padding="3 3 0 3")
mainFrame.grid(column=0, row=1, sticky="nsew")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1, pad=3)
safeFrame = ttk.Frame(mainFrame, width=200, height=35, borderwidth=2, relief='sunken')
safeFrame.grid(column=1, row=7, columnspan=2)
customFrame = ttk.Frame(root, padding="0 3 3 3")
customFrame.grid(column=1, row=1, sticky="nsew")
customSaveBorder = ttk.Separator(mainFrame, orient="vertical")
customSaveBorder.grid(row=0, column=3, rowspan=50, columnspan=3, sticky="ns", padx=7)
nameBox = ttk.Entry(mainFrame, width=10)
nameBox.grid(row=10, column=2, columnspan=1, sticky="w", padx=2, ipadx=4)


# Save paths and safe status setup
try:
    psettingsPath = os.path.join(os.path.expanduser('~'), 'AppData', 'Roaming' r'\Oneshot' r'\p-settings.dat')
except FileNotFoundError:
    tkinter.messagebox.showwarning("Error", "p-settings.dat not found. Ensure you have run OneShot at least once.")
    sys.exit()

savePath = os.path.join(os.path.expanduser('~'), 'AppData', 'Roaming' r'\Oneshot')
save = os.path.join(os.path.expanduser('~'), 'AppData', 'Roaming' r'\Oneshot' r'\save.dat')
status = ttk.Label(safeFrame, text="111111", font=("Calibri Bold", 40), padding="15 -5 15 -1")
status.grid(sticky="")

# Clover checker setup
cloverStatus = ttk.Label(safeFrame, text="Clover = ?", font=("Calibri Bold", 22), padding="15 -5 15 -1")
cloverStatus.grid(sticky="")

global deleteCustomSaveMode
deleteCustomSaveMode = False


def resource_path(relative_path):  # Defines the locations of each of the pre-set saves
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


# Prefab save paths (built into the .exe)
barrpath = resource_path(r"barrens\save.dat")
glenpath = resource_path(r"glen\save.dat")
refupath = resource_path(r"refuge\save.dat")
towepath = resource_path(r"tower\save.dat")
doorpath = resource_path(r"door\save.dat")
lghtpath = resource_path(r"lightbulb\save.dat")
solbpath = resource_path(r"solbarrens\save.dat")
solgpath = resource_path(r"solglen\save.dat")
solrpath = resource_path(r"solrefuge\save.dat")
solepath = resource_path(r"solend\save.dat")
iconpath = resource_path(r"ico\sub2.ico")


def get_psettings():  # Finds the current state of p-settings.dat
    with open(psettingsPath, 'rb') as psettings:
        s = [rb_load(psettings), rb_load(psettings), rb_load(psettings)]
        return s


def set_psettings(data):  # Changes the current state of p-settings.dat
    with open(psettingsPath, 'wb') as psettings:
        for d in data:
            rb_write(psettings, d)


def get_playername():  # Gets the player's current "name" - the name that OneShot reads from your operating system
    name = get_psettings()[2]
    nameBox.delete(0, END)
    nameBox.insert(0, name)


def set_playername():  # Sets the player's name to the value entered in textbox
    if checkoneshot():
        return

    name = nameBox.get().strip()

    if len(name) == 0:
        tkinter.messagebox.showwarning('No name entered', 'Please enter a name.')
        return

    data = get_psettings()
    data[2] = name
    set_psettings(data)
    tkinter.messagebox.showinfo('Name changed', 'Player name has been changed to {}.'.format(name))
    nameBox.delete(0, END)
    nameBox.insert(0, name)


def resetdefault():  # Resets your game to the title screen, with the Solstice route disabled
    data[0][1] = False
    data[0][9] = False
    set_psettings(data)
    os.remove(save)


def resetsolstice():  # Resets your game to the title screen, with the Solstice route enabled
    data[0][1] = True
    data[0][9] = False
    set_psettings(data)
    os.remove(save)


def setsave(slocation):  # Function for replacing your current save.dat with a pre-set list of saves in Any% and NG+
    shutil.copy(slocation, savePath)
    if slocation == barrpath or slocation == solbpath:
        if slocation == barrpath:
            data[0][1] = False
            set_psettings(data)
        elif slocation == solbpath:
            data[0][1] = True
            set_psettings(data)
        else:
            pass
    else:
        pass


def helpdialogue():  # Shows a dialoguebox with the following text
    tkinter.messagebox.showinfo("Help", "OneShotUtil V3.2 by durrbill \nSome code from Firestrike and hunternet93 \n"
                                        "Special thanks to Kazoeru and GIRakaCHEEZER <3 \n\n"
                                        "The Custom Save button prompts the user for a valid OneShot .dat save file. "
                                        "Even renamed save.dat files will function, so long as the content and .dat "
                                        "extension remain. If a valid .dat file is selected, the user can name this "
                                        "custom save.\n\n"
                                        "The Export and Import Saves buttons allow the user to either export their "
                                        "current list of custom saves as a .zip, or import .zip files that have been "
                                        "exported from this program. "
                                        "This means you can export your saves into a .zip, rename said file, and share "
                                        "it with anyone. This also allows you to import custom savepack .zip files "
                                        "from others. \n\n"
                                        "The Delete Save button toggles Delete Mode, which removes the next custom "
                                        "save you click on. Clicking on Delete Save again cancels the operation. \n\n"
                                        "The Set Player Name button sets the name that OneShot reads from your PC to "
                                        "whatever is entered into the textbox to the right of the button.")


def exportsaves():  # Exports the user's current set of custom saves as a .zip file, which can later be re-imported
    with ZipFile('exportedsaves.zip', 'w') as zip_object:
        zip_object.write('customsaves.ini')
        saveslist = glob.glob('customsaves/*.dat')
        for i in saveslist:
            zip_object.write(i)
    if os.path.exists('exportedsaves.zip'):
        tkinter.messagebox.showinfo("Export Saves", "Saves exported to exportedsaves.zip successfully. "
                                                    "\nRename the new .zip file if you plan on sharing your saves.")
    else:
        tkinter.messagebox.showwarning("Export Saves", "Export failed. Please ensure you have a 'customsaves' folder "
                                                       "and customsaves.ini present.")


def importsaves():  # Prompts the user to select a .zip archive to import properly formatted savepacks
    tkinter.messagebox.showinfo("Import Saves", "Please select a valid .zip file to import saves from.\n\n"
                                                "Note that imported savepacks will replace your existing saves. "
                                                "Export your current saves if you wish to use them later.")
    importpath = tkinter.filedialog.askopenfilename(filetypes=[("Zip Archives", ".zip")])
    with zipfile.ZipFile(importpath, 'r') as zip_file:
        config.read("customsaves.ini")
        file_list = zip_file.namelist()
        if 'customsaves.ini' in file_list:
            config.remove_section("SAVES")
            config.remove_section("SAVESCOUNT")
            with open("customsaves.ini", "w") as config_file:
                config.write(config_file)
            os.remove('customsaves.ini')
            btnlist = customFrame.grid_slaves()
            for li in btnlist:
                li.destroy()
            try:
                shutil.rmtree('customsaves')
            except FileNotFoundError:
                pass
            with zipfile.ZipFile(importpath, 'r') as zip_ref:
                zip_ref.extractall('')

            checkforsaves()
        else:
            tkinter.messagebox.showwarning("Error", "Invalid .zip. Ensure the chosen .zip was created by this utility.")


def savedeletemode():  # Triggers the "setCustomSave" function to instead delete the next button pressed
    global deleteCustomSaveMode
    if deleteCustomSaveMode:
        deleteCustomSaveMode = False
        checkclover()
    else:
        deleteCustomSaveMode = True
        checkclover()


def checkclover():  # Checks to see if ______.exe (the clover program) is running
    if "_______.exe" in (p.name() for p in psutil.process_iter()) and not deleteCustomSaveMode:
        cstatus = "Clover = Yes"
        cloverStatus["text"] = cstatus
    elif not deleteCustomSaveMode:
        cstatus = "Clover = No"
        cloverStatus["text"] = cstatus
    else:
        cstatus = "Delete Mode"
        cloverStatus["text"] = cstatus


def checkoneshot():  # Checks to see if OneShot.exe is running
    if "OneShot.exe" in (p.name() for p in psutil.process_iter()):
        return True
    else:
        return False


# Custom Save Functions
def customsavecreate():  # Creates a button and save.dat file which are named by the user
    tkinter.messagebox.showinfo("Custom Save", "Please select a save.dat file to use as a custom save point. \n\n"
                                               "Note that invalid .dat files will be nonfunctional.")
    custompath = tkinter.filedialog.askopenfilename(filetypes=[("Save Files", ".dat")])
    newpath = r'customsaves'
    if os.path.exists('customsaves' + "/" + custompath.split("/")[-1]) and custompath != '':
        tkinter.messagebox.showwarning("Error", "A .dat save file already exists with the name: "
                                       + str(custompath.split("/")[-1]) +
                                       "\nPlease rename your chosen .dat file and try again.")
        return
    elif not os.path.exists(newpath) and custompath != 'customsaves' and custompath.endswith(".dat"):
        os.makedirs(newpath)
        customname = tkinter.simpledialog.askstring("New Custom Save", "Enter a name for this custom save.")
    elif custompath != 'customsaves' and custompath.endswith(".dat"):
        customname = tkinter.simpledialog.askstring("New Custom Save", "Enter a name for this custom save.")
    else:
        return

    matches = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']

    if any(x in customname for x in matches):
        tkinter.messagebox.showwarning("Error", r"Custom name cannot contain the following characters: / \ * ? < > : |")
        return
    elif customname.startswith(' ') or customname.endswith(' ') or customname == '':
        tkinter.messagebox.showwarning("Error", "Custom save name cannot start or end with an empty character.")
        return
    else:
        pass

    shutil.copy(custompath, "customsaves/")

    newsavename = str(custompath.split("/")[-1])

    try:
        os.rename("customsaves/" + newsavename, "customsaves/" + customname + ".dat")
        customsavenum = os.listdir("customsaves/")
        customsavenumlen = len(customsavenum)
        config.set("SAVESCOUNT", "savescount2", str(customsavenumlen))
        config.set("SAVES", str(customsavenumlen), customname)
    except FileExistsError:
        tkinter.messagebox.showwarning("Error", "The chosen name " + str(customname) + " is already in use.")
        os.remove("customsaves/" + newsavename)
        return

    if customsavenumlen > 78:
        tkinter.messagebox.showwarning("Error", "Max number of saves reached.")
        return
    elif customsavenumlen + 1 > 66:
        columnoverride = 6
        saverow = customsavenumlen - 66
    elif customsavenumlen + 1 > 53:
        columnoverride = 5
        saverow = customsavenumlen - 53
    elif customsavenumlen + 1 > 40:
        columnoverride = 4
        saverow = customsavenumlen - 40
    elif customsavenumlen + 1 > 27:
        columnoverride = 3
        saverow = customsavenumlen - 27
    elif customsavenumlen + 1 > 14:
        columnoverride = 2
        saverow = customsavenumlen - 14
    else:
        columnoverride = 1
        saverow = customsavenumlen
    if saverow <= 0:
        saverow = 1

    with open("customsaves.ini", "w") as config_file:
        config.write(config_file)
        ttk.Button(customFrame, text=str(customname), 
                   command=lambda: customsaveset((config.get("SAVES", str(customsavenumlen)))), 
                   width=15).grid(column=3 + columnoverride, row=int(saverow), sticky=W)


def customsaveset(cslocation):  # Replaces OneShot's save.dat with a chosen custom save, or removes the chosen save
    global deleteCustomSaveMode
    if not deleteCustomSaveMode:
        try:
            shutil.copy("customsaves/" + cslocation + ".dat", savePath)
            try:
                os.remove(savePath + "/" + "save.dat")
            except:
                pass
            os.rename(savePath + "/" + cslocation + ".dat", savePath + "/" + "save.dat")
        except FileNotFoundError:
            pass
    else:
        config.read("customsaves.ini" 'r')
        saveslist = []
        savesdict = {}
        saveslistcount = int(len(config.options("SAVES")))

        def remove_items_by_value(dictionary, value_to_remove):
            keys_to_remove = [key for key, value in dictionary.items() if value == value_to_remove]
            for key in keys_to_remove:
                del dictionary[key]
            return dictionary

        for i in range(saveslistcount):
            savesdict[str(i + 1)] = str(config.get("SAVES", str(i + 1)))

        for i in range(saveslistcount):
            saveslist.append(i + 1)

        value_to_remove = cslocation
        remove_items_by_value(savesdict, value_to_remove)
        savesdict2 = dict(zip(saveslist, list(savesdict.values())))
        saveslistcount = saveslistcount - 1
        os.remove("customsaves/" + cslocation + ".dat")

        for i in range(saveslistcount):
            config.set("SAVES", str(i + 1), str(savesdict2.get(i + 1)))
        config.remove_option("SAVES", str(saveslistcount + 1))
        config.set("SAVESCOUNT", "savescount2", str(saveslistcount))

        with open("customsaves.ini", "w") as config_file:
            config.write(config_file)

        def deletesavebutton():
            delbtnlist = customFrame.grid_slaves()
            for li in delbtnlist:
                li.destroy()
        deletesavebutton()
        checkforsaves()
        deleteCustomSaveMode = False
        checkclover()


def checkforsaves():  # Checks for existing custom saves and loads them into the utility
    if os.path.isdir('customsaves'):
        config.read("customsaves.ini")
        try:
            savescountglobal = config.get("SAVESCOUNT", "savescount2")
        except configparser.NoOptionError:
            config.set("SAVESCOUNT", "savescount2", str(0))
            savescountglobal = 0
        remakesavecount = 0

        for savenum in range(int(savescountglobal)):  # Creates buttons for each existing custom save
            remakesavecount += 1
            if os.path.isfile('customsaves/' + config.get("SAVES", str(savenum + 1)) + '.dat'):
                if savenum + 1 > 65:
                    columnoverride = 6
                    saverow = savenum - 65
                elif savenum + 1 > 52:
                    columnoverride = 5
                    saverow = savenum - 52
                elif savenum + 1 > 39:
                    columnoverride = 4
                    saverow = savenum - 39
                elif savenum + 1 > 26:
                    columnoverride = 3
                    saverow = savenum - 26
                elif savenum + 1 > 13:
                    columnoverride = 2
                    saverow = savenum - 13
                else:
                    columnoverride = 1
                    saverow = savenum

                ttk.Button(customFrame, text=str(config.get("SAVES", str(savenum + 1))),
                           command=lambda remakesavecount=remakesavecount: customsaveset
                           ((config.get("SAVES", str(remakesavecount)))), width=15
                           ).grid(column=3 + columnoverride, row=int(saverow), sticky=W)
            else:
                config.set("SAVES", str(savenum + 1), str(savenum + 2))
                config.remove_option("SAVES", str(savenum + 2))
            if savenum == int(savescountglobal):
                break
            with open("customsaves.ini", "w") as config_file:
                config.write(config_file)

    else:  # Called if custom saves do not currently exist and creates a .ini file for their operation
        config.add_section("SAVES")
        config.add_section("SAVESCOUNT")
        with open("customsaves.ini", "w") as config_file:
            config.write(config_file)


# Safe Checking
def safestatus():  # Checks "\Users\[user]\Documents" and "\Users\[user]\OneDrive\Documents" for DOCUMENT.oneshot.txt
    checkclover()  # Calls the clover checking function once every two seconds
    try:
        if os.path.isfile(os.path.join(os.path.expanduser('~'), 'Documents', 'DOCUMENT.oneshot.txt')):
            safecodepath = os.path.join(os.path.expanduser('~'), 'Documents', 'DOCUMENT.oneshot.txt')
        else:
            safecodepath = os.path.join(os.path.expanduser('~'), 'OneDrive', 'Documents', 'DOCUMENT.oneshot.txt')
        passworddocument = open(safecodepath, 'r', encoding='utf8')
        readabledocument = passworddocument.readlines()
        passworddocument.close()

        currentsafestatus = readabledocument[int(len(readabledocument))-1].split()[-1]

    except FileNotFoundError:  # If DOCUMENT.oneshot.txt is not found, request the user locate it manually
        if not os.path.isfile("safepath.ini"):  # Create a safepath.ini which stores the new DOCUMENT.oneshot.txt path
            if not config.has_section("PATH"):
                tkinter.messagebox.showinfo("Help", "DOCUMENT.oneshot.txt not found. Please open your safe code document.")
                userpath = tkinter.filedialog.askopenfilename(filetypes=[("Text Files", ".txt")])
                config.add_section("PATH")
                config.set("PATH", "cpath", userpath)
            with open("safepath.ini", "w") as config_file:
                config.write(config_file)

            config.read("safepath.ini")
            safecodepath = config.get("PATH", "cpath")
            passworddocument = open(safecodepath, 'r', encoding='utf8')
            readabledocument = passworddocument.readlines()
            passworddocument.close()

            currentsafestatus = readabledocument[int(len(readabledocument)) - 1].split()[-1]
        else:  # If safepath.ini already exists, use that path from now on
            config.read("safepath.ini")
            safecodepath = config.get("PATH", "cpath")
            passworddocument = open(safecodepath, 'r', encoding='utf8')
            readabledocument = passworddocument.readlines()
            passworddocument.close()

            currentsafestatus = readabledocument[int(len(readabledocument)) - 1].split()[-1]
    except:
        currentsafestatus = ""

    status["text"] = currentsafestatus
    root.after(2000, safestatus)


# Various required functions, assignments, & buttons on startup
data = get_psettings()
get_playername()
checkforsaves()
root.iconbitmap(resource_path(iconpath))

namebutton = ttk.Button(mainFrame, text='Set Player Name', command=set_playername)
namebutton.grid(row=10, column=1, columnspan=1, sticky="ew")
helpbox = ttk.Button(mainFrame, width=2, text="?", command=lambda: helpdialogue())
helpbox.grid(row=10, column=2, columnspan=1, sticky='e')

ttk.Button(mainFrame, text="Full Reset", command=resetdefault, width=15).grid(column=1, row=1, sticky=W)
ttk.Button(mainFrame, text="Solstice", command=resetsolstice, width=15).grid(column=2, row=1, sticky=W)
ttk.Button(mainFrame, text="Barrens", command=lambda: setsave(barrpath), width=15).grid(column=1, row=2, sticky=W)
ttk.Button(mainFrame, text="Glen", command=lambda: setsave(glenpath), width=15).grid(column=1, row=3, sticky=W)
ttk.Button(mainFrame, text="Refuge", command=lambda: setsave(refupath), width=15).grid(column=1, row=4, sticky=W)
ttk.Button(mainFrame, text="Tower", command=lambda: setsave(towepath), width=15).grid(column=1, row=5, sticky=W)
ttk.Button(mainFrame, text="Door Puzzle", command=lambda: setsave(doorpath), width=15).grid(column=1, row=6, sticky=W)
ttk.Button(mainFrame, text="Lightbulb", command=lambda: setsave(lghtpath), width=15).grid(column=2, row=6, sticky=W)
ttk.Button(mainFrame, text="Barrens (NG+)", command=lambda: setsave(solbpath), width=15).grid(column=2, row=2, sticky=W)
ttk.Button(mainFrame, text="Glen (NG+)", command=lambda: setsave(solgpath), width=15).grid(column=2, row=3, sticky=W)
ttk.Button(mainFrame, text="Refuge (NG+)", command=lambda: setsave(solrpath), width=15).grid(column=2, row=4, sticky=W)
ttk.Button(mainFrame, text="Ending (NG+)", command=lambda: setsave(solepath), width=15).grid(column=2, row=5, sticky=W)
ttk.Button(mainFrame, text="Custom Save", command=customsavecreate, width=15).grid(column=1, row=8, sticky=W)
ttk.Button(mainFrame, text="Delete Save", command=lambda: savedeletemode(), width=15).grid(column=2, row=8, sticky=W)
ttk.Button(mainFrame, text="Import Saves", command=importsaves, width=15).grid(column=1, row=9, sticky=W)
ttk.Button(mainFrame, text="Export Saves", command=exportsaves, width=15).grid(column=2, row=9, sticky=W)

safestatus()
time.sleep(0.1)
root.mainloop()  # I know this program is a bit of a mess lmao, but it works despite my freshness to python. Thank u!!!
