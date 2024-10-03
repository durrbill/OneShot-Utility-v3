# OneShot Utility V3
A utility for speedrunning OneShot. Features some code snippets from Firestrike and hunternet93.
Special thanks to Kazoeru and GIRakaCHEEZER <3

## Features

 - Reset button for Any% and NG+ categories
 - Safe code reader
 - ______.exe checker (checks to see if the "clover program" is running
 - Player name editor
 - Ability to create/delete custom-named saves by importing valid .dat files
 - Ability to toggle automatically closing/reopening the game upon loading any save or resetting the game, allowing for near-instant run resets or resetting a segment to practice
 - Ability to export sets of custom saves into a formatted .zip file for distribution
 - Ability to import sets of custom saves, enabling the distribution of custom "save packs" for specific purposes
 ## Using the Utility

### Setting Up Saves
 - To begin with a base list of saves to load from, open the program, select "Import Saves", then select the "anysaves.zip" file that was in the original .zip you downloaded. Your program will automatically load up a list of premade saves that cover both the Any% and NG+ routes.
 

### Custom Saves
 - To create a custom save point, click the "New Save" button, locate a valid ".dat" file, and enter a chosen nickname for the save.
 
 - The .dat file to use as a custom save would typically be located in *%appdata%\Roaming\Oneshot*, and be named "save.dat". However, you may rename the .dat file to anything you like prior to selection, so long as another custom save does not exist with that same name.

 - Custom saves may be deleted by pressing "Delete Save", and then clicking on the custom save you wish to remove. Deleting a save or clicking on "Delete Save" once more will return the user to default behavior.

 - Custom save names may **not** feature the following characters: **/ \ * ? < > : |**

 - Importing an "invalid" .dat file (one that was *not* created by OneShot as a save.dat) will create a new button for the .dat, but will not function for the purposes of loading OneShot saves.

 - Theoretically, an infinite number of custom saves may be created.


### Toggling the auto-load feature
 - Located above the safe code checker is a checkbox. If checked, the utility will automatically close OneShot (if open), and reopen OneShot, with the new custom save loaded. This allows for near uninterrupted repeated practice of difficult segments. This feature also enables the "Full Reset" buttons to close OneShot, wipe your save to Any% or NG+, and reopen to the title screen to reset a run quicky.


### Exporting and Importing Custom "savepacks"
 - The "Export Saves" and "Import Saves" buttons, respectively, export your current list of custom saves, and import already created lists of custom saves.

 - Clicking "Export Saves" creates a .zip file in the same directory as the program. This .zip file may be renamed as the user sees fit, and is automatically formatted to be used later by:

 - Clicking "Import Saves" prompts the user to locate a valid .zip file previously created by the utility. This will remove all current custom saves, and replace them with those present in the selected savepack.

 - Custom savepacks can be shared and distributed, allowing for pre-made sets of saves for different categories, run types, practice modes, etc.


### Changing Player Name
 - To change your player's "name" in OneShot, simply type the desired name into the textbox to the right of the "Set Player Name" button, then press said button.

## Installation/Necessary Files
OneShot Utility v3.3 will create up to three elements:
- A "customsaves" folder in the same directory as the .exe, which will store any created custom saves
- A "customsaves.json" file in OneShot's save directory (%appdata%\Roaming\Oneshot\), which stores relevant data for custom saves to function
- A "safepath.txt" file in OneShot's save directory, which stores the location of DOCUMENT.oneshot.txt, if said file does not exist in expected default locations
