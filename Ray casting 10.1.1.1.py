import contextlib
with contextlib.redirect_stdout(None):
    import pygame, sys, random, math, time, ast, os
    from pygame.locals import *
    from multiprocessing import Pool


pool = Pool(os.cpu_count())



def events(segments):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONUP:
            Mouse = pygame.mouse.get_pos()
            segments.append([[Mouse[0]-25, Mouse[1]-25], [Mouse[0]+25, Mouse[1]-25]])
            segments.append([[Mouse[0]+25, Mouse[1]-25], [Mouse[0]+25, Mouse[1]+25]])
            segments.append([[Mouse[0]+25, Mouse[1]+25], [Mouse[0]-25, Mouse[1]+25]])
            segments.append([[Mouse[0]-25, Mouse[1]+25], [Mouse[0]-25, Mouse[1]-25]])
            return segments

        elif event.type == pygame.KEYDOWN and pygame.key == k_F5:
            print("F5")

    return segments


def draw(screen, clock, segments):
    for seg in segments:
        pygame.draw.line(screen, [0,0,255], [seg[0][0], seg[0][1]],[seg[1][0], seg[1][1]],1)
    fps = font.render(str(int(clock.get_fps()))+" FPS", True, pygame.Color('Green'))
    screen.blit(fps, [0,0])


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
        screen.fill([0,0,0])
        segments = events(segments)

        draw(screen, clock, segments)

        pygame.display.flip()
        clock.tick()
