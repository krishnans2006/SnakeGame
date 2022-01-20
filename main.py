import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox

pygame.init()
width = 500
rows = 25
win = pygame.display.set_mode((width, width))
pygame.display.set_caption("Snake Game")
moved = False
end = False
score = 0

class Cube(object):
    rows = 25
    w = 500

    def __init__(self, start, dirnx=0, dirny=0, color=(255, 0, 0)):
        self.pos = start
        self.dirnx = dirnx
        self.dirny = dirny
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface, self.color, (i * dis, j * dis, dis, dis))
        if eyes:
            center = dis // 2
            radius = 3
            circleMiddle = (i * dis + center - radius, j * dis + 8)
            circle2Middle = (i * dis + dis - radius * 2, j * dis + 8)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circle2Middle, radius)


class Snake(object):
    body = []
    turns = {}

    def __init__(self, color, pos):
        self.color = color
        self.head = Cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1
        self.move_cnt = 0

    def move(self):
        global moved, end
        self.move_cnt += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end = True
                break
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT]:
                self.dirnx = 1
                self.dirny = 0
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                moved = True
            elif keys[pygame.K_LEFT]:
                self.dirnx = -1
                self.dirny = 0
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                moved = True
            elif keys[pygame.K_UP]:
                self.dirnx = 0
                self.dirny = -1
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                moved = True
            elif keys[pygame.K_DOWN]:
                self.dirnx = 0
                self.dirny = 1
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                moved = True
        if self.move_cnt % 5 == 0:
            for i, c in enumerate(self.body):
                p = c.pos[:]
                if p in self.turns:
                    turn = self.turns[p]
                    c.move(turn[0], turn[1])
                    if i == len(self.body) - 1: self.turns.pop(p)
                else:
                    if c.dirnx == -1 and c.pos[0] <= 0: c.pos = (c.rows - 1, c.pos[1])
                    elif c.dirnx == 1 and c.pos[0] >= c.rows - 1: c.pos = (0, c.pos[1])
                    elif c.dirny == -1 and c.pos[1] <= 0: c.pos = (c.pos[0], c.rows - 1)
                    elif c.dirny == 1 and c.pos[1] >= c.rows - 1: c.pos = (c.pos[0], 0)
                    else: c.move(c.dirnx, c.dirny)

    def reset(self, pos):
        self.head = Cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def addCube(self):
        global score
        tail = self.body[-1]
        dx = tail.dirnx
        dy = tail.dirny
        score += 1
        if dx == 1 and dy == 0:
            self.body.append(Cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(Cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] + 1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)


def redrawWindow(surface):
    global width, rows, moved, score
    surface.fill((0, 255, 0))
    s.draw(surface)
    snack.draw(surface)
    font = pygame.font.SysFont("timesnewroman", 25)
    if not moved:
        text = font.render("Press an arrow key to start moving!", 1, (50, 50, 50))
        surface.blit(text, (75, 100))
    else:
        surface.blit(font.render("Score: {0}".format(score), 1, (50, 50, 50)), (10, 10))
    pygame.display.update()


def randomSnack(rows, item):
    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            continue
        else:
            break

    return x, y


def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass


def main():
    global width, rows, win, s, snack, moved, end, score
    s = Snake((255, 0, 0), (rows // 2, rows // 2))
    snack = Cube(randomSnack(rows, s), 0, 0, color=(0, 0, 255))

    flag = True

    clock = pygame.time.Clock()

    win.fill((0, 255, 0))
    text = pygame.font.SysFont("timesnewroman", 75, True).render("Snake Game", 1, (255, 0, 0))
    win.blit(text, (50, 125))
    text = pygame.font.SysFont("timesnewroman", 25).render("Press C to Play or H to learn How to Play", 1, (0, 0, 255))
    win.blit(text, (45, 300))
    pygame.display.update()
    moveon = False
    howtoplay = False
    while not moveon:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                moveon = True
                end = True
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    moveon = True
                    howtoplay = True
                    break
                if event.key == pygame.K_c:
                    moveon = True
                    break

    if howtoplay and not end:
        win.fill((0, 255, 0))
        font = pygame.font.SysFont("timesnewroman", 25)
        text = font.render("Move around by using the arrow keys.", 1, (0, 0, 255))
        win.blit(text, (50, 100))
        text = font.render("Try to eat as many snacks as possible.", 1, (0, 0, 255))
        win.blit(text, (50, 150))
        text = font.render("You get longer after every snack you eat", 1, (0, 0, 255))
        win.blit(text, (50, 200))
        text = font.render("Hitting the sides of the game won't kill you.", 1, (0, 0, 255))
        win.blit(text, (50, 250))
        text = font.render("You only die by running into yourself.", 1, (0, 0, 255))
        win.blit(text, (50, 300))
        text = font.render("Good Luck! Press C to play the game...", 1, (0, 0, 255))
        win.blit(text, (50, 350))
        pygame.display.update()
        moveon = False
        while not moveon:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    end = True
                    moveon = True
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        moveon = True
                        break

    while flag and not end:
        clock.tick(30)
        s.move()
        if s.body[0].pos == snack.pos:
            s.addCube()
            snack = Cube(randomSnack(rows, s), color=(0, 0, 255))

        for i in range(len(s.body)):
            if s.body[i].pos in list(map(lambda z: z.pos, s.body[i + 1:])):
                message_box("You Lost!", "Well Done! Your score was: {0}. Play Again!".format(score))
                s.reset((rows // 2, rows // 2))
                moved = False
                score = 0
                break
        redrawWindow(win)


main()
