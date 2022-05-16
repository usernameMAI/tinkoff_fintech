# BATTLESHIP

## Launching
First you need to install the required packages:
```
pip install -r requirements.txt
```
You need to go to repository and run:
```
python3 main.py n k
```
If you want to run the program with PyCharm, then you need to specify in the configuration:
1. write parameters: n k
2. click on the button emulate terminal in output console

Where n and k are sizes of game fields.

## Description
We have a main menu with 3 options:
1. launch game
2. load game
3. quit game

Also we have a game menu where we can play battleship. In this menu we can aim on points with 
WASD and shoot with 'p'. We can save the game by button 'l' and choose saving cell. 
Rules of game:
You need to hit all enemy ships. First player who do this is winner. Player can make one shot
for every move. Player can\`t shot in the same place two times. The placement of ships is random.
Ships can\`t stand close to each other by horizontal and vertical. When a ship is destroyed, the area around the ship is painted over, as no other ships can stand there. If the ship is hit, then its hit part is shown with 'X'. If it is destroyed, then 'd' is displayed. Water ingress is counted as '*'.

## Screenshots
![Alt text](screenshots/screenshot1.png?raw=true "screenshot1")
