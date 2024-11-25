import pygame
import random
import sys
import threading
import time

pygame.init()
#Initialize Screen Sizing and Frames
SCREEN_WIDTH = 560
SCREEN_HEIGHT = 620
CELL_SIZE = 20
FPS = 10

#Create the color palette
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)


#Create Screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pac-Man")

font = pygame.font.SysFont('Arial', 18)
#Initialize Board
board = [
    list("############################"),
    list("#............##............#"),
    list("#.####.#####.##.#####.####.#"),
    list("#o####.#####.##.#####.####o#"),
    list("#.####.#####.##.#####.####.#"),
    list("#..........................#"),
    list("#.####.##.########.##.####.#"),
    list("#.####.##.########.##.####.#"),
    list("#......##....##....##......#"),
    list("######.##### ## #####.######"),
    list("######.##### ## #####.######"),
    list("######.##          ##.######"),
    list("######.## ###--### ##.######"),
    list("######.## #      # ##.######"),
    list("       ## #      # ##       "),
    list("######.## #      # ##.######"),
    list("######.## ######## ##.######"),
    list("######.##          ##.######"),
    list("######.## ######## ##.######"),
    list("######.## ######## ##.######"),
    list("#............##............#"),
    list("#.####.#####.##.#####.####.#"),
    list("#.####.#####.##.#####.####.#"),
    list("#o..##................##..o#"),
    list("###.##.##.########.##.##.###"),
    list("###.##.##.########.##.##.###"),
    list("#......##....##....##......#"),
    list("#.##########.##.##########.#"),
    list("#.##########.##.##########.#"),
    list("#..........................#"),
    list("############################")
]
#Initialize Assets
pacman_img = pygame.image.load('assets/pacman.png')
ghost_imgs = [
    pygame.image.load('assets/yellow.png'),
    pygame.image.load('assets/red.png'),
    pygame.image.load('assets/blue.png'),
    pygame.image.load('assets/green.png')
]
#Properly Size Objects
pacman_img = pygame.transform.scale(pacman_img, (CELL_SIZE, CELL_SIZE))
for i in range(len(ghost_imgs)):
    ghost_imgs[i] = pygame.transform.scale(ghost_imgs[i], (CELL_SIZE, CELL_SIZE))
#Initialize Pacman Data
pacman_x, pacman_y = 14, 23
pacman_direction = 'LEFT'
score = 0
#Initialize Ghost positions
ghost_positions = [
    {'x': 12, 'y': 14},
    {'x': 14, 'y': 14},
    {'x': 12, 'y': 16},
    {'x': 14, 'y': 16}
]

lock = threading.Lock()  #Create Lock
running = True

#Create a board using the board lists and replaceing each character with a rigidbody.
def draw_board():
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            if cell == '#':
                pygame.draw.rect(screen, BLUE, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            elif cell == '.':
                pygame.draw.circle(screen, WHITE, (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2), 3)
            elif cell == 'o':
                pygame.draw.circle(screen, WHITE, (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2), 7)

#Pacman rigidbody
def draw_pacman():
    screen.blit(pacman_img, (pacman_x * CELL_SIZE, pacman_y * CELL_SIZE))

#Ghost Rigidbody
def draw_ghosts():
    for i, ghost in enumerate(ghost_positions):
        screen.blit(ghost_imgs[i], (ghost['x'] * CELL_SIZE, ghost['y'] * CELL_SIZE))

#Pacman controls with lock
def move_pacman():
    global pacman_x, pacman_y, score
    with lock:
        if pacman_direction == 'LEFT' and board[pacman_y][pacman_x - 1] != '#':
            pacman_x -= 1
        elif pacman_direction == 'RIGHT' and board[pacman_y][pacman_x + 1] != '#':
            pacman_x += 1
        elif pacman_direction == 'UP' and board[pacman_y - 1][pacman_x] != '#':
            pacman_y -= 1
        elif pacman_direction == 'DOWN' and board[pacman_y + 1][pacman_x] != '#':
            pacman_y += 1

        if board[pacman_y][pacman_x] == '.':
            board[pacman_y][pacman_x] = ' '
            score += 10
        elif board[pacman_y][pacman_x] == 'o':
            board[pacman_y][pacman_x] = ' '
            score += 50

#Ghost Brain with lock
def move_ghosts():
    while running:
        with lock:
            for ghost in ghost_positions:
                direction = random.choice(['LEFT', 'RIGHT', 'UP', 'DOWN'])
                if direction == 'LEFT' and board[ghost['y']][ghost['x'] - 1] != '#':
                    ghost['x'] -= 1
                elif direction == 'RIGHT' and board[ghost['y']][ghost['x'] + 1] != '#':
                    ghost['x'] += 1
                elif direction == 'UP' and board[ghost['y'] - 1][ghost['x']] != '#':
                    ghost['y'] -= 1
                elif direction == 'DOWN' and board[ghost['y'] + 1][ghost['x']] != '#':
                    ghost['y'] += 1
        time.sleep(0.5)

#Check for ghost and pacman collision wiht lock
def check_collisions():
    with lock:
        for ghost in ghost_positions:
            if ghost['x'] == pacman_x and ghost['y'] == pacman_y:
                return True
    return False

#Create Ghost thread
ghost_thread = threading.Thread(target=move_ghosts, daemon=True) #daemon ends thread when main thread ends
#start ghost thread
ghost_thread.start()

clock = pygame.time.Clock()
#Game run properties
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                pacman_direction = 'LEFT'
            elif event.key == pygame.K_RIGHT:
                pacman_direction = 'RIGHT'
            elif event.key == pygame.K_UP:
                pacman_direction = 'UP'
            elif event.key == pygame.K_DOWN:
                pacman_direction = 'DOWN'

    move_pacman()

    if check_collisions():
        print("Game Over!")
        running = False

    if all(cell != '.' and cell != 'o' for row in board for cell in row):
        print("You Win!")
        running = False

    screen.fill(BLACK)
    draw_board()
    draw_pacman()
    draw_ghosts()

    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, SCREEN_HEIGHT - 30))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
