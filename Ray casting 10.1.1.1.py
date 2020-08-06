import contextlib
with contextlib.redirect_stdout(None):
    import pygame, sys, random, math, time, ast, os, multiprocessing
    from pygame.locals import *
    from multiprocessing import Pool
    from itertools import product
    from contextlib import contextmanager

pool = Pool(os.cpu_count())


def draw(screen, segments):
    for seg in segments:
        pygame.draw.line(screen, [0,0,255], [seg[0][0], seg[0][1]],[seg[1][0], seg[1][1]],1)

def events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONUP:
            return pygame.mouse.get_pos()
    return None


def addTile(segments, Mouse):
    segments.append([[Mouse[0]-25, Mouse[1]-25], [Mouse[0]+25, Mouse[1]-25]])
    segments.append([[Mouse[0]+25, Mouse[1]-25], [Mouse[0]+25, Mouse[1]+25]])
    segments.append([[Mouse[0]+25, Mouse[1]+25], [Mouse[0]-25, Mouse[1]+25]])
    segments.append([[Mouse[0]-25, Mouse[1]+25], [Mouse[0]-25, Mouse[1]-25]])
    return segments


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode([1280, 720])
    pygame.display.set_caption("Ray casting Engine")
    font=pygame.font.SysFont("Courier", 20, bold=True)
    clock = pygame.time.Clock()

    ##LINE SEGMENTS
    segments = [
        ##Border
        [[-1,-1], [1280,-1]],
        [[1280,-1], [1280,720]],
        [[1280,720], [-1,720]],
        [[-1,720], [-1,-1]]]

    while True:
        Mouse = events()
        if Mouse is not None:
            segments = addTile(segments, Mouse)

        draw(screen, segments)

        screen.fill([0,0,0])
        pygame.display.flip()
        clock.tick()
