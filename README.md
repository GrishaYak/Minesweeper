Minesweeper
==
This is a minesweeper game written on python and running in terminal

Installation
--
Just download "minesweeper.py" and run it.

Usage
--
Firstly, it will ask you about the size of the field. Just type the amount of rows you want, then press the space bar and type the amount of columns you want.

Then, you will have to set the level of difficulty. The higher the difficulty, the more mines will be on a field. You can write "easy", "medium" or "hard" as well as just a number between 1 and 3.

So, after these steps you can actually start playing. Now you can write x and y (separated by space) coordinates of the cell you want to open. You can add "f" or "flag" at the end to place a flag there. Game won't let you open a cell with a flag. To get rid of flag, try to put there another one.

Rules of the game
--
You have a field with some mines and your work is to locate all of them. To do that, you have to open all cells without mines. If you open a cell with a mine, you will explode and, obviously, lose. A cell that does not contain a mine will show you a number of mines around it, or won't show anything if there are no mines near. For example:
```
_______
|1|1| |
|o|2|1|
|1|2|o|
-------
```
"o" is mine.