
/-Read me for the ETGG 1802 Map Editor-/
by jason ashworth.

##The following is a list of key commands while inside the map editor.
## s - Saves the current working map file.
## l - loads a new map file without without saving any changes made to the current file.
## ESC - Quits the map editor without saving
## Mouse-Wheel (up/down) - scrolls the Pallette up and down.
## Left mousebutton - Used to select from the pallette, and place the tiles on the map.


##After the big wall tile codes, the map editor needs the following elements.  I will ##break them down one by one.


##ALL elements must be seperated by ":"'s.  That is how it is set up to be read in.



##These are the locations of the warp squares on the screen.  
##The format is as follows:

##		Y-cordinate : X-cordinate : map that it warps to
## The Y and X must be placed in this order.  They are the Tile co-ordinates of the warp
##tile.  The map that it warps to, is basically the name.map of the file.  There is no
##limit to the number of Warps that a single map can have.

warps = 31:18:level1.map
        7:20:level2.map



##This is the player's STARTING position when warped to this level.  it is X : Y
##This will obviously need to increase as we create different warp spots, and be ##integrated into the world.

pos = 300:300



##This is where the overlays will be placed. (hand placed) 
##The first element is the overlay tile code.  Second is the Left-Right tile number.
##Lastly is the Up-Down tile number.  This is the location of the top-left corner of the
##overlay image.  There is no limit to the number of overlays that we can have.

overlay =o00:5:5
        o00:20:10
        o01:20:20
        o00:20:90
        o01:20:50

