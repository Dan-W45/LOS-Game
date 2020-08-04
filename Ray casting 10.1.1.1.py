import contextlib
with contextlib.redirect_stdout(None):
    import pygame, sys, random, math, time, ast, os, multiprocessing
    from pygame.locals import *
    from multiprocessing import Pool
    from itertools import product
    from contextlib import contextmanager

pool = Pool(os.cpu_count())



if __name__ == "__main__":
    pygame.init()
    canvas = pygame.display.set_mode([1280,720])
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
