import pygame
import random as rd
pygame.init()

WIDTH, HEIGHT = 1000, 1000
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mines by Arthur bg")

FPS = 60
GRAY, BLACK, WHITE, RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE = (180, 180, 180), (0, 0, 0), (255, 255, 255), (255, 0, 0), (255, 123, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255), (255, 0, 255)
LGBT = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]
SCORE_FONT = pygame.font.SysFont("comicsans", 50)

#   |‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾|
#   |         GRID CODE         |
#   |   1 to 8 : n mines nearby |
#   |   0      : nothing        |
#   |   -1     : mine           |
#   |   -2     : not searched   |
#   |   -3     : flag           |
#   |___________________________|


def grid_gen() :
    mines = set()
    for _ in range(10) :
        mine = (rd.randrange(0, 1000, 100), rd.randrange(0, 1000, 100))
        while mine in mines :
            mine = (rd.randrange(0, 1000, 100), rd.randrange(0, 1000, 100))
        mines.add(mine)
    grid = {}
    for x in range(0, 1000, 100) :
        for y in range(0, 1000, 100) :
            cell = (x, y)
            if cell in mines :
                grid[cell] = -1
            else :
                v = cell
                count = 0
                if (v[0] - 100, v[1] - 100) in mines :
                    count += 1
                if (v[0], v[1] - 100) in mines :
                    count += 1
                if (v[0] + 100, v[1] - 100) in mines :
                    count += 1
                if (v[0] - 100, v[1] + 100) in mines :
                    count += 1
                if (v[0], v[1] + 100) in mines :
                    count += 1
                if (v[0] + 100, v[1] + 100) in mines :
                    count += 1
                if (v[0] - 100, v[1]) in mines :
                    count += 1
                if (v[0] + 100, v[1]) in mines :
                    count += 1
                grid[cell] = count
    return(grid)
   
def draw(win, selected_cell, grid, discovered) :
    i = 0
    #for v in LGBT :
    #    pygame.draw.rect(win, v, (0, i, WIDTH, HEIGHT // 6))
    #    i += HEIGHT // 6
   
    pygame.draw.rect(win, GRAY, (0, 0, WIDTH, HEIGHT))
   
    for v in grid :
        if grid[v] == 0 :
            pygame.draw.rect(win, GRAY, (v[0], v[1], 100, 100))
        elif grid[v] == -1 :
            pygame.draw.circle(win, ORANGE, (v[0] + 50, v[1] + 50), 50)
        elif grid[v] == -2 :
            pygame.draw.rect(win, WHITE, (v[0], v[1], 100, 100))
        elif grid[v] == -3 :
            pygame.draw.rect(win, RED, (v[0] + 10, v[1] + 10, 80, 50))
            pygame.draw.rect(win, WHITE, (v[0] + 10, v[1] + 60, 10, 30))
        elif grid[v] > 0 :
            text = SCORE_FONT.render(str(grid[v]), 1, BLUE)
            win.blit(text, v)
   
    for x in range(100, 1000, 100):
        pygame.draw.rect(win, BLACK, (x, 0, 4, HEIGHT))
    for y in range(100, 1000, 100):
        pygame.draw.rect(win, BLACK, (0, y, WIDTH, 4))
   
    if selected_cell not in discovered :
        pygame.draw.rect(win, RED, (selected_cell[0], selected_cell[1], 100, 4))
        pygame.draw.rect(win, RED, (selected_cell[0], selected_cell[1] + 100, 100, 4))
        pygame.draw.rect(win, RED, (selected_cell[0], selected_cell[1], 4, 100))
        pygame.draw.rect(win, RED, (selected_cell[0] + 100, selected_cell[1], 4, 100))
   
    pygame.display.update()
   
def reveal(selected_cell, g1, g2, discovered) :
    content = g1[selected_cell]
    if content > 0 :
        g2[selected_cell] = g1[selected_cell]
        discovered.add(selected_cell)
        return 0
    elif content == 0 :
        revealed_cells = set()
        revealed_cells.add(selected_cell)
        tracing = set()
        tracing.add(selected_cell)
        while tracing != set() :
            tmp = set()
            for v in tracing :
                print(v)
                tmp.add((v[0] + 100, v[1]))
                tmp.add((v[0] - 100, v[1]))
                tmp.add((v[0], v[1] + 100))
                tmp.add((v[0], v[1] - 100))
                tmp.add((v[0] + 100, v[1] + 100))
                tmp.add((v[0] + 100, v[1] - 100))
                tmp.add((v[0] - 100, v[1] + 100))
                tmp.add((v[0] - 100, v[1] - 100))
            tracing = set()
            for v in tmp :
                if v[0] < 1000 and v[0] > - 100 :
                    if v[1] < 1000 and v[1] > -100 :
                        if v not in revealed_cells :
                            if g1[v] != -1 :
                                revealed_cells.add(v)
                                if g1[v] == 0 :
                                    tracing.add(v)
                      
        for cell in revealed_cells :
            g2[cell] = g1[cell]
            discovered.add(cell)
        return 0
    elif content == -1 :
        g2[selected_cell] = g1[selected_cell]
        discovered.add(selected_cell)
        return -1

def flag(cell, grid) :
    if grid[cell] == -3 :
        grid[cell] = -2
    else :
        grid[cell] = -3

def win() :
    pygame.time.delay(3000)
    running = False

def loss() :
    pygame.time.delay(3000)
    running = False

def main() :
    running = True
    clock = pygame.time.Clock()
    grid = grid_gen()
    discovered = set()
    discovered_g = {}
    for v in grid :
        discovered_g[v] = -2
    status = 0

    while running :
   
        mouse_state = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT :
                running = False
                break
            if event.type == pygame.MOUSEBUTTONUP :       
                if mouse_state[0] :
                    status = reveal(selected_cell, grid, discovered_g, discovered)
                if mouse_state[2] :
                    if selected_cell not in discovered :
                        flag(selected_cell, discovered_g)       
        
        selected_cell = (mouse_pos[0] // 100 * 100, mouse_pos[1] // 100 * 100)
       
        draw(WIN, selected_cell, discovered_g, discovered)
       
        print(len(discovered))
        if len(discovered) == 90 :
            status = 1
       
        if status == 1 :
            win()
            break
        elif status == -1 :
            loss()
            break

if __name__ == "__main__" :
    main()