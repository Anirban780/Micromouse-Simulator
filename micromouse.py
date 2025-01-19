import pygame
import pygame_gui
import time
from collections import deque

# Constants
DEFAULT_CELL_SIZE = 50
DEFAULT_GRID_SIZE = 10
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800
INSTRUCTION_HEIGHT = 100
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Maze setup
def create_empty_maze(rows, cols):
    return [[0 for _ in range(cols)] for _ in range(rows)]


def flood_fill(maze, goal_x, goal_y):
    rows, cols = len(maze), len(maze[0])
    distances = [[-1 for _ in range(cols)] for _ in range(rows)]
    distances[goal_x][goal_y] = 0

    queue = deque([(goal_x, goal_y)])
    while queue:
        x, y = queue.popleft()
        current_distance = distances[x][y]

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] == 0 and distances[nx][ny] == -1:
                distances[nx][ny] = current_distance + 1
                queue.append((nx, ny))

    return distances


def next_move(mouse_x, mouse_y, distances):
    min_distance = float('inf')
    next_position = (mouse_x, mouse_y)

    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = mouse_x + dx, mouse_y + dy
        if 0 <= nx < len(distances) and 0 <= ny < len(distances[0]):
            if distances[nx][ny] != -1 and distances[nx][ny] < min_distance:
                min_distance = distances[nx][ny]
                next_position = (nx, ny)

    return next_position


def draw_maze(screen, maze, mouse_pos, goal_pos, cell_size, rows, cols, padding_x, padding_y):
    for i, row in enumerate(maze):
        for j, cell in enumerate(row):
            color = WHITE if cell == 0 else BLACK
            pygame.draw.rect(
                screen,
                color,
                (padding_x + j * cell_size, padding_y + i * cell_size, cell_size, cell_size),
            )
            pygame.draw.rect(
                screen,
                BLACK,
                (padding_x + j * cell_size, padding_y + i * cell_size, cell_size, cell_size),
                1,
            )

    if goal_pos:
        pygame.draw.rect(
            screen,
            GREEN,
            (
                padding_x + goal_pos[1] * cell_size,
                padding_y + goal_pos[0] * cell_size,
                cell_size,
                cell_size,
            ),
        )

    if mouse_pos:
        pygame.draw.circle(
            screen,
            RED,
            (
                padding_x + mouse_pos[1] * cell_size + cell_size // 2,
                padding_y + mouse_pos[0] * cell_size + cell_size // 2,
            ),
            cell_size // 3,
        )


def draw_instructions(screen, mode, font, message=None):
    """
    Draw the instructions text at the top of the screen.
    Optionally displays a custom message if provided.
    """
    instructions = ""
    
    if message:  # If a custom message is provided
        instructions = message
    elif mode == "obstacles":
        instructions = "Left-click to toggle obstacles. Press 'Shift+S' to set start position."
    elif mode == "start":
        instructions = "Left-click to set the start position. Press 'Shift+G' to set goal position."
    elif mode == "goal":
        instructions = "Left-click to set the goal position. Press 'Enter' to start simulation."
    elif mode == "simulate":
        instructions = "Simulation in progress..."
    elif mode == "complete":
        instructions = "Game Over! The Micromouse has reached the goal."

    # Render the instructions
    text = font.render(instructions, True, BLUE)
    screen.blit(text, (20, 20))



def main():
    pygame.init()
    clock = pygame.time.Clock()

    cell_size = DEFAULT_CELL_SIZE
    rows, cols = DEFAULT_GRID_SIZE, DEFAULT_GRID_SIZE
    maze = create_empty_maze(rows, cols)

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Micromouse Simulator")

    mouse_pos = None
    goal_pos = None
    running = True
    mode = "obstacles"
    font = pygame.font.SysFont("Arial", 24)

    manager = pygame_gui.UIManager((WINDOW_WIDTH, WINDOW_HEIGHT))
    grid_input_field = pygame_gui.elements.UITextEntryLine(
        pygame.Rect(20, 60, 200, 30), manager
    )
    grid_input_field.text_colour= WHITE
    grid_input_field.rebuild()
    grid_input_field.set_text(f"{rows}x{cols}")

    game_end_time = None

    # Initialize the restart button
    restart_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((20, 700), (120, 50)),
        text="Restart",
        manager=manager
    )
    restart_button.colours['normal_bg']= pygame.Color(255,255,255)
    restart_button.colours['normal_text']= pygame.Color(0,0,0)
    restart_button.colours['hovered_bg']= pygame.Color(195,209,210)
    restart_button.colours['hovered_text']= pygame.Color(247,34,34)
    restart_button.rebuild()
    

    while running:
        time_delta = clock.tick(30) / 1000.0
        screen.fill(WHITE)

        maze_width = cols * cell_size
        maze_height = rows * cell_size
        padding_x = max((WINDOW_WIDTH - maze_width) // 2, 0)
        padding_y = max((WINDOW_HEIGHT - maze_height - INSTRUCTION_HEIGHT) // 2, INSTRUCTION_HEIGHT)

        draw_instructions(screen, mode, font)
        draw_maze(screen, maze, mouse_pos, goal_pos, cell_size, rows, cols, padding_x, padding_y)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == restart_button:
                    # Reset game state
                    maze = create_empty_maze(rows, cols)
                    mouse_pos = None
                    goal_pos = None
                    mode = "obstacles"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    mode = "start"
                elif event.key == pygame.K_g and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    mode = "goal"
                elif mode == "goal" and event.key == pygame.K_RETURN:
                    mode = "simulate"

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if padding_y <= y < padding_y + maze_height and padding_x <= x < padding_x + maze_width:
                    grid_x = (y - padding_y) // cell_size
                    grid_y = (x - padding_x) // cell_size

                    if mode == "obstacles":
                        maze[grid_x][grid_y] = 1 - maze[grid_x][grid_y]
                    elif mode == "start":
                        mouse_pos = (grid_x, grid_y)
                    elif mode == "goal":
                        goal_pos = (grid_x, grid_y)

            if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_element == grid_input_field:
                grid_size_input = grid_input_field.get_text()
                if "x" in grid_size_input:
                    try:
                        rows, cols = map(int, grid_size_input.split("x"))
                        maze = create_empty_maze(rows, cols)
                    except ValueError:
                        print("Invalid grid size. Use 'NxM' format.")

            manager.process_events(event)

        if mode == "simulate" and mouse_pos and goal_pos:
            distances = flood_fill(maze, goal_pos[0], goal_pos[1])

            # Check if the goal is unreachable
            if distances[mouse_pos[0]][mouse_pos[1]] == -1:
                mode= "incomplete"
                game_end_time = pygame.time.get_ticks()
                no_path_message = "No valid path to the goal! Simulation terminated."
            else:
                no_path_message = None  # Clear previous message if path exists

                while mouse_pos != goal_pos:
                    time.sleep(0.3)
                    next_position = next_move(mouse_pos[0], mouse_pos[1], distances)

                    # Check if the micromouse is stuck
                    if next_position == mouse_pos:
                        mode = "complete"
                        game_end_time = pygame.time.get_ticks()
                        no_path_message = "Micromouse is stuck! Simulation terminated."
                        break

                    mouse_pos = next_position

                    # Render the game state during simulation
                    screen.fill(WHITE)
                    draw_instructions(screen, mode, font, no_path_message)  # Pass message dynamically
                    draw_maze(screen, maze, mouse_pos, goal_pos, cell_size, rows, cols, padding_x, padding_y)
                    manager.update(time_delta)
                    manager.draw_ui(screen)
                    pygame.display.flip()

                # End simulation when mouse reaches goal
                if mouse_pos == goal_pos:
                    mode = "complete"
                    game_end_time = pygame.time.get_ticks()

        # Handle the "complete" state with a possible custom message
        if mode == "complete" or mode == "incomplete" and game_end_time:
            elapsed_time = pygame.time.get_ticks() - game_end_time
            if elapsed_time >= 3000:  # Wait for 3 seconds before exiting
                running = False

            # Pass "no_path_message" or None to draw instructions
            draw_instructions(screen, mode, font, no_path_message)


        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
