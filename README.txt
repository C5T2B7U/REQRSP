
------------------------------------------------------------------------------
REQRSP v1 [POOR MAN'S PORTLESS/CLIENTLESS VNC SERVER FOR DROPBOX FOR WINDOWS]:
------------------------------------------------------------------------------

1.  PRIME REQUEST FILE AUTOMATICALLY GENERATED 	=  .\RQ.txt
2.  INSERT COMMANDS INTO PRIME REQUEST FILE  	=  .\RQ.txt
3.  TO SEND REQUEST COMMANDS, SAVE FILE AS 	=  .\REQ.txt
4.  SERVER WILL PROCESS REQUEST FILE  		=  .\REQ.txt
5.  SERVER WILL SEND RESPONSE SCREENSHOT  	=  .\RSP\RSP.png
6.  WATCH RESPONSES PROPAGATE WITH IRFANVIEW WATCH HOTFOLDER FUNCTION
7.  CLICK MOUSE ON RESPONSE SCREENSHOT IN IRFANVIEW TO OBTAIN SCREEN COORDINATES 

---------------------
REQRSP COMMANDS LIST:
---------------------

?					=  display help text with notepad
/					=  close help text with key sequence = [Alt]+[F4], [N]
E {start} <cmdString>			=  execute windows command
M <x> <y>				=  move mouse to screen coordinates
L {<x> <y>}				=  leftclick here {or at screen coordinates}
D {<x> <y>}				=  left doubleclick here {or at screen coordinates}
R {<x> <y>}				=  rightclick here {or at screen coordinates}
G {<fromX> <toX>} <toX> <toY>		=  drag mouse {from coordinates} to coordinates
S [<distanceUp> | <-distanceDown>]	=  scroll [distance up | -distance down]
T <text>				=  typewrite text
N {<text>}				=  press enter {or typewrite text then insert newline}
K <key1> {<key2> <key...>}		=  press key {or press hotkey sequence}
A					=  select all: 	[Ctrl]+[A]
X					=  cut: 	[Ctrl]+[X]
C					=  copy: 	[Ctrl]+[C]
V					=  paste: 	[Ctrl]+[V]
Z					=  undo: 	[Ctrl]+[Z]
Y					=  redo: 	[Ctrl]+[Y]
AUTO [ON | OFF] {<seconds>}		=  set automatic response mode [on | off] {set rate}
DEBUG [ON | OFF]			=  set debug messages [off | on]
