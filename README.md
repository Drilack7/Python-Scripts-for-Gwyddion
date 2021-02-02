In this repository, you can find scripts written in Python that can be used through the software Gwyddion.

<font size="6"> Gwyddion overview</font>
Gwyddion is a Free and Open Source software for SPM (scanning probe microscopy) data visualization and analysis. It is a powerful, modular program that is very convenient for much of the data analysis we do. Gwyddion does not have all of the functionality someone may need but allows for python scripting to add additional features. More info in the website of [Gwyddion](http://gwyddion.net/) and its [Python Scripting](http://gwyddion.net/documentation/user-guide-en/pygwy.html) support.

<font size="6"> Installation</font>
In order to install Gwyddion and its Python console (pygwy) you need to follow the steps in the website found [here](http://gwyddion.net/documentation/user-guide-en/installation-ms-windows.html#installation-ms-windows-pygwy). After installing 32-bit version of Gwyddion, Python 2.7.16 and the three Python packages you're good to go.

<font size="6"> Info for 'Automated Analysis Script.py'</font>
For this script to work, the module called gwy is imported through the code (command 'import gwy') from Gwyddion's bin folder directory.
In my case it was "C:/Program Files (x86)/Gwyddion/bin".
There's a chance yours is different so in that case, please change manually the directory inside the code yourself (it's in the 11th line).
This script does a lot of things:
1) Asks the user to input the directory of the folder with the files to process.
2) Asks the user to input the morphology channel number and the channel of interest (in my case was Current) number.
3) Loads the images with largest scan size into gwyddion's data browser
4) Flattens them
5) Calculates and prints the mean depth of the image
6) Creates new files with different names in gwyddion format
7) Creates jpeg images of the channel of interest of all the small scan size images with the same scale (the min and max are the average min and max of the first half of the images)
8) Creates a collage of all these images with their names appearing too.
Python file named "collage_maker" must always be in the same folder as the script, because it is needed to create the collage of the images. (a Compiled Python File with the same name appears after first run).
Ignore the first 3 warnings (** (python.exe:13424): WARNING **, etc.), it is normal for them to appear and according to the developers they cannot be avoided. 

 <font size="6"> Info for 'Scripts run in pygwy' folder</font>
After installing Python Console (pygwy) in Gwyddion (see "Installation" section), you can start using commands and scripts in the software.
Open and use pygwy:
To open the console, after opened Gwyddion(32bit), go to Data Process → Pygwy Console. A window appears from which you can run Python commands. In this case the Python code can interact with the current Gwyddion instance in various ways.
The Command entry in the lower part of the console window allows executing simple individual commands. They are immediately executed when you press Enter and their output is printed in the log area above.
Longer scripts can be typed, pasted or loaded into the main area in the upper part. The button Execute (Ctrl-E) then runs the script. The output is again displayed in the log area, together with any error messages. The other control buttons enable saving (Ctrl-S) and loading (Ctrl-O) the scripts. Button Clear Log clears the log area.
About the scripts:
In the current folder, there are some scripts that can be run only in the pygwy console of gwyddion (load them from the pygwy console window).
There are some categorized folders for the scripts, depending on their application to one(the current active) file or all open files(first channel or all of them).
All of the scripts can and should be modified most of the times, depending on the occasion.
Read the first comment in the beggining of each script to understand what it does and what values should be changed if necessary (unfortunately, you cannot ask the user to input values in pygwy).