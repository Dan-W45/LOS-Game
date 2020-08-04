import contextlib
with contextlib.redirect_stdout(None):
    import pygame, sys, random, math, time, ast, multiprocessing
    from pygame.locals import *
    from multiprocessing import Pool
    from itertools import product
    from contextlib import contextmanager


##Find intersection of RAY & SEGMENT
def getIntersection(ray,segment):
##  RAY in parametric: Point + Delta*T1
    r_px = ray[0][0]
    r_py = ray[0][1]
    r_dx = ray[1][0]
    r_dy = ray[1][1]

##  SEGMENT in parametric: Point + Delta*T2
    s_px = segment[0][0]
    s_py = segment[0][1]
    s_dx = segment[1][0]-segment[0][0]
    s_dy = segment[1][1]-segment[0][1]

##  Are they parallel? If so, no intersect
    r_mag = math.sqrt(r_dx*r_dx+r_dy*r_dy)
    s_mag = math.sqrt(s_dx*s_dx+s_dy*s_dy)
    if r_dx/r_mag==s_dx/s_mag and r_dy/r_mag==s_dy/s_mag:
##	Unit vectors are the same.
        return None

##  SOLVE FOR T1 & T2
##  r_px+r_dx*T1 = s_px+s_dx*T2 && r_py+r_dy*T1 = s_py+s_dy*T2
##  ==> T1 = (s_px+s_dx*T2-r_px)/r_dx = (s_py+s_dy*T2-r_py)/r_dy
##  ==> s_px*r_dy + s_dx*T2*r_dy - r_px*r_dy = s_py*r_dx + s_dy*T2*r_dx - r_py*r_dx
##  ==> T2 = (r_dx*(s_py-r_py) + r_dy*(r_px-s_px))/(s_dx*r_dy - s_dy*r_dx)

    T2 = ((r_dx*(s_py-r_py) + r_dy*(r_px-s_px))/(s_dx*r_dy - s_dy*r_dx)) if (s_dx*r_dy - s_dy*r_dx) != 0.0 else math.inf
    T1 = (s_px+s_dx*T2-r_px)/r_dx if r_dx != 0.0 else math.inf

##  Must be within parametic whatevers for RAY/SEGMENT
    if(T1<0): return None
    if(T2<0 or T2>1.0000001): return None

##  Return the POINT OF INTERSECTION
    return r_px+r_dx*T1, r_py+r_dy*T1, T1


##///////////////////////////////////////////////////////

##DRAWING
def draw(canvas, segments, Mouse):
    ##Clear canvas
##    canvas.fill([238,238,238])
    canvas.fill([0,0,0])

    ##Draw segments
    for seg in segments:
        pygame.draw.line(canvas, [0,0,255], [seg[0][0], seg[0][1]],[seg[1][0], seg[1][1]],1)

    getUniquePoints(canvas, segments, Mouse)

def getUniquePoints(canvas, segments, Mouse):
    ##Get all unique points
    points=[]
    for seg in segments:
        points.extend([seg[0],seg[1]])
    *uniquePoints,=map(list,{*map(tuple,points)})

    getAllAngles(canvas, segments, Mouse, uniquePoints)

def getAllAngles(canvas, segments, Mouse, uniquePoints):
    ##Get all angles
    uniqueAngles = []
    for uniquePoint in uniquePoints:
        angle = math.atan2(uniquePoint[1]-Mouse[1],uniquePoint[0]-Mouse[0])
        uniqueAngles.extend([angle-0.00001,angle,angle+0.00001])

    calcRays(canvas, segments, Mouse, uniqueAngles)

##    canvas, segments, Mouse, intersects, calcTime = calcRays(canvas, segments, Mouse, uniqueAngles)
##    sortByAngle(canvas, segments, Mouse, intersects, calcTime)


def calcRays(canvas, segments, Mouse, uniqueAngles):
    global pool
    ##RAYS IN ALL DIRECTIONS
    intersects = []
    closeTime = time.time()

    rays = []
    for angle in uniqueAngles:
        ##Calculate dx & dy from angle
        dx = math.cos(angle)
        dy = math.sin(angle)
        ##Ray from center of screen to mouse
        rays.append([Mouse,[dx, dy]])

    ##Find closest interaction
    intersects = pool.starmap(getIntersection, product(rays, segments))

    closestIntersect = None
    for intersect in intersects:
        if intersect is None:
            continue
        if closestIntersect is None or intersect[2]<closestIntersect[2]:
            closestIntersect = list(intersect)


    calcTime = time.time() - closeTime

##    return canvas, segments, Mouse, intersects, calcTime

    sortByAngle(canvas, segments, Mouse, intersects, calcTime)

def sortByAngle(canvas, segments, Mouse, intersects, calcTime):
    ##Sort intersects by angle
    try:
        intersects = sorted(intersects,key=lambda l:l[3])
        dsTime = time.time()
        drawPolygons(canvas, segments, Mouse, intersects, dsTime, calcTime)
    except Exception as e:
        dsTime = time.time()
        times(canvas, dsTime, calcTime)


def drawPolygons(canvas, segments, Mouse, intersects, calcTime):
    ##Draw as a polygon
    plot = []
    for intersect in intersects:
        plot.append([intersect[0],intersect[1]])
##    pygame.draw.polygon(canvas, [221,56,56], plot)    #Red
    pygame.draw.polygon(canvas, [238,238,238], plot)    #Off White

    ##Draw debug lines
##    for intersect in intersects:
##        pygame.draw.line(canvas, [200,200,200], [Mouse[0], Mouse[1]], [intersect[0],intersect[1]])
    times(canvas, dsTime, calcTime)


def times(canvas, dsTime, calcTime):
    calcTimeTXT = font.render("Calc time: "+str(calcTime), True, pygame.Color('Green'))
    canvas.blit(calcTimeTXT, [1000,0])

    drawTimeTXT = font.render("Draw time: "+str(time.time()-dsTime), True, pygame.Color('Green'))
    canvas.blit(drawTimeTXT, [1000,20])

    fps = font.render(str(int(clock.get_fps()))+" FPS", True, pygame.Color('Green'))
    canvas.blit(fps, [0,0])




##DRAW LOOP
def drawLoop(updateCanvas, canvas, segments, Mouse):
    if updateCanvas:
    	draw(canvas, segments, Mouse)
    	updateCanvas = False
    	pygame.display.flip()




if __name__ == "__main__":
    pygame.init()
    canvas = pygame.display.set_mode([1280,720])
    pygame.display.set_caption("Ray casting Engine")
    font=pygame.font.SysFont("Courier", 20, bold=True)
    clock = pygame.time.Clock()

    global pool
    pool = Pool(5)

    ##LINE SEGMENTS
    segments = [
        ##Border
        [[-1,-1], [1280,-1]],
        [[1280,-1], [1280,720]],
        [[1280,720], [-1,720]],
        [[-1,720], [-1,-1]]]

    updateCanvas = True

    ##MOUSE	
    Mouse = [canvas.get_width()/2, canvas.get_height()/2]
    while True:
        clock.tick()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONUP:
                segments.append([[pygame.mouse.get_pos()[0]-25, pygame.mouse.get_pos()[1]-25], [pygame.mouse.get_pos()[0]+25, pygame.mouse.get_pos()[1]-25]])
                segments.append([[pygame.mouse.get_pos()[0]+25, pygame.mouse.get_pos()[1]-25], [pygame.mouse.get_pos()[0]+25, pygame.mouse.get_pos()[1]+25]])
                segments.append([[pygame.mouse.get_pos()[0]+25, pygame.mouse.get_pos()[1]+25], [pygame.mouse.get_pos()[0]-25, pygame.mouse.get_pos()[1]+25]])
                segments.append([[pygame.mouse.get_pos()[0]-25, pygame.mouse.get_pos()[1]+25], [pygame.mouse.get_pos()[0]-25, pygame.mouse.get_pos()[1]-25]])

            if event.type == pygame.KEYDOWN:
                if event.key == K_F5:
                    segments = [[[-1,-1], [1280,-1]],
                                [[1280,-1], [1280,720]],
                                [[1280,720], [-1,720]],
                                [[-1,720], [-1,-1]]]

        Mouse = pygame.mouse.get_pos()
        updateCanvas = True
        drawLoop(updateCanvas, canvas, segments, Mouse)












