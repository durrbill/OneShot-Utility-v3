# OneShot Utility V3
A utility for speedrunning OneShot. Features some code snippets from Firestrike and hunternet93.
Special thanks to Kazoeru and GIRakaCHEEZER <3

## Features

 - Reset button for Any% and NG+ categories
 - 10 prefab save states spanning Any% (including Tower puzzle saves) and NG+
 - Safe code reader
 - ______.exe checker (checks to see if the "clover program" is running
 - Player name editor
 - Ability to create up to 78 custom-named saves by importing valid .dat files
 - Ability to export sets of custom saves into a formatted .zip file for distribution
 - Ability to import sets of custom saves, enabling the distribution of custom "save packs" for specific purposes
 ## Using the Utility

 ### Prefab Saves
 The list of saves present by default in the program are an arrangement of saves spread throughout the Any% and NG+ categories. Clicking a button will set your OneShot save to the specified location.
 
 At the top of this list are "reset" buttons, which can bring your game to the start of either the Any% or NG+ routes, at the title screen.

### Custom Saves
To create a custom save point, click the "Custom Save" button, locate a valid ".dat" file, and enter a chosen nickname for the save.

The .dat file to use as a custom save would typically be located in *%appdata%\Roaming\Oneshot*, and be named "save.dat". However, you may rename the .dat file to anything you like prior to selection, so long as another custom save does not exist with that same name.

Custom saves may be deleted by pressing "Delete Save", and then clicking on the custom save you wish to remove. Deleting a save or clicking on "Delete Save" once more will return the user to default behavior.

Custom save names may **not** feature the following characters: **/ \ * ? < > : |**

Importing an "invalid" .dat file (one that was *not* created by OneShot as a save.dat) will create a new button for the .dat, but will not function for the purposes of loading OneShot saves.

Up to 78 custom saves may exist at one time.

### Exporting and Importing Custom "savepacks"
The "Export Saves" and "Import Saves" buttons, respectively, export your current list of custom saves, and import already created lists of custom saves.

Clicking "Export Saves" creates a .zip file in the same directory as the program. This .zip file may be renamed as the user sees fit, and is automatically formatted to be used later by:

Clicking "Import Saves" prompts the user to locate a valid .zip file previously created by the utility. This will remove all current custom saves, and replace them with those present in the selected savepack.

Custom savepacks can be shared and distributed, allowing for pre-made sets of saves for different categories, run types, practice modes, etc.

### Changing Player Name
To change your player's "name" in OneShot, simply type the desired name into the textbox to the right of the "Set Player Name" button, then press said button.
## Installation/Necessary Files
OneShot Utility V3 will create up to three files/folders in the directory of the .exe. If one wishes to keep these out of sight, creating a shortcut to the program is recommended. No installation is required to run the utility, simply run the downloaded .exe file in the .zip. 

The files created by the .exe should not be tampered with manually. The program's functionality relies on only the program itself making the proper reads/writes from these files and folders, and modifying them manually **will** break the program. Only do so if you know what you're doing. The exception to this rule is if you wish to "clean reset" your utility's settings, which can be done by deleting "customsaves.ini", "safepath.ini", and the "customsaves" folder.

## Special Thanks
Thank you to Kazoeru for consistently bug testing <3
and GIRakaCHEEZER with help on setting up Tower saves!
