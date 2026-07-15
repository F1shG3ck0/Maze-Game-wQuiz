**Cyber Maze Quiz**
**Requirements**

Python 3.10 (developed and tested with Python 3.10.11)

Python 3.12 may work, but Python 3.14 currently causes issues with some dependencies.

**Install Dependencies**

pip install pygame
pip install pygame-widgets
pip install pillow

or

pip install -r requirements.txt

**Project Structure**

Maze-Game-wQuiz/
│
├── interfaces.py
├── callbacks01.py
├── PlayGame01.py
├── LogOnDataBase.py
│
├── Images/
│   ├── Wall.png
│   ├── Clue.png
│   ├── Spy.png
│   ├── Avatar01.png
│   ├── Avatar02.png
│   ├── Avatar03.png
│   ├── Avatar04.png
│   └── ...
│
├── Game_text_files/
│   ├── Maze1.txt
│   ├── Cyber.txt
│   └── ...


**Running application**
python interfaces.py
or
py -3.10 interfaces.py
interfaces.py is the main entry point for the application.

**WARNING** - do not resize the simple GUI (It has not been designed for that as an A-Level project)


**Overview**

Cyber Maze Quiz is a maze-based educational game where players navigate mazes and answer quiz questions to progress. The application includes user management, score tracking, leaderboards, and administrative tools for managing game content.

**Technologies Used**

Python

Tkinter

SQLite

PIL (Pillow)

**Features**

User account management
Avatar selection
Maze-based gameplay
Question and clue system
Leaderboards and score tracking
Difficulty selection
Admin tools for managing game content
Local SQLite database storage

**Status**

This repository contains the original coursework submission and is no longer actively maintained. It is shared for educational and portfolio purposes.
