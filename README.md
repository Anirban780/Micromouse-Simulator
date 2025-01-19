# Micromouse-Simulator
## Project Overview
The Micromouse Simulator is a Python-based simulation program built using Pygame and pygame_gui libraries. This program simulates a micromouse navigating through a maze, with the goal of finding the shortest path to a specified destination. The user can define the maze by toggling obstacles and setting start and goal positions, after which the simulation will run, and the micromouse will try to navigate the maze to reach the goal.

![DALL·E-2025-01-19-21 14 36-Create-a-set-of-four-icons-for-a-Micromouse-game-simulation](https://github.com/user-attachments/assets/3735bfef-8a26-4b79-aaa6-e650deec8ae3)

## Features:
### 1. Maze Creation: 
Users can click on the grid to toggle obstacles and set start/goal positions.
### 2. Simulation: 
After setting the start and goal positions, users can start the simulation, where the micromouse will navigate through the maze.
### 3. Dynamic Grid: 
Supports grid resizing by entering the desired grid size in the format M x N.
### 4. Restart Button: 
Restart the simulation to begin with a new maze configuration.

## Project Requirements
Before running the program, ensure you have the following prerequisites installed:

1. **Python 3.6+**: Python should be installed on your system.
2. **Pygame**: The game development library used for rendering the maze and simulation. (*pip install pygame*)
3. **pygame_gui**: A GUI framework for creating the user interface (buttons, input fields, etc.). (*pip install pygame_gui*)

## How to Play:
Open VS Code. Download necessary extensions. Open this file and **run "micromouse.py"** and then the game terminal will open.

**1. Grid Size:** The grid size is displayed at the top of the window. You can change the size of the grid by typing a new size in the format M x N (e.g., 10x10 for a 10x10 grid).

**2. Toggle Obstacles:** Left-click on the grid to toggle obstacles.

**3. Set Start Position:** Press **Shift+S** to set the start position, then click on the grid to select a cell for the start position.

**4. Set Goal Position:** Press **Shift+G** to set the goal position, then click on the grid to select a cell for the goal.

**5. Start Simulation:** Press **Enter** to start the simulation after setting the start and goal positions.

**6. Restart Simulation:** Press the **Restart** button to reset the grid and start over.
