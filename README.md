# DnD-Map-Assistant
Tool to show your maps and players during a DnD session. You are able to move the players, add enemies inside fighting areas, move them and kill them. This tool does not track player and enemy health, spell points or any other stat.  

# Setup

## Characters
To start playing you have to fill in the characters csv file in the characters folder, putting in the name of the character, its class and speed in the following format
- character name 1,character class 1,character speed 1
- character name 2,character class 2,character speed 2  

Please don't include any spaces before or after the commas or else the program won't run properly.

## Maps
Include all your map files in the Maps folder, you can name them in order of use, including their size in the name in case you reuse the map for other sessions.  
Some examples of naming schemes are:
- Map#_columnsxrows.png
- #_columnsxrows.png  

Please keep the same naming scheme for all the maps used in the same session.  

When you run the tool for the first time in a session it asks you what the dimensions for each map are. If the dimensions for a given map are 20 columns and 14 rows, write them with a space between them

When creating the maps, The best map designer for this tool is found in https://app.dungeonscrawl.com/. Remember, when cutting the map and downloading it as a png, cut an exact number of squares for the best experience. Any other tool which lets you download the map as an image and lets you cut the map to an exact number of squares is also usable.

# Example images
## Character movement example
![Image 1](./Markdown_Images/Image1.png)
## Distance measurement example
![Image 2](./Markdown_Images/Image2.png)

# Controls
- Left click: Select entity or activate function (create enemy, kill enemy, measure distance, change map)
- Right click: Reset all active selections
- M key: minimize window
- Double esc key: Close game

