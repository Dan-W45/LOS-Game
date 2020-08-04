import contextlib
with contextlib.redirect_stdout(None):
    import pygame, sys, random, math
    from pygame.locals import *

pygame.init()
canvas = pygame.display.set_mode([1280,720])
pygame.display.set_caption("Ray casting Engine")
font=pygame.font.SysFont("Courier", 20, bold=True)
clock = pygame.time.Clock()

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


    ##Get all unique points
    points=[]
    for seg in segments:
        points.extend([seg[0],seg[1]])
    *uniquePoints,=map(list,{*map(tuple,points)})


    ##Get all angles
    uniqueAngles = []
    for j in range(len(uniquePoints)):
        uniquePoint = uniquePoints[j]
        angle = math.atan2(uniquePoint[1]-Mouse[1],uniquePoint[0]-Mouse[0])
        uniqueAngles.extend([angle-0.00001,angle,angle+0.00001])

    ##RAYS IN ALL DIRECTIONS
    intersects = []
    for j in range(len(uniqueAngles)):
        angle = uniqueAngles[j]

        ##Calculate dx & dy from angle
        dx = math.cos(angle)
        dy = math.sin(angle)

        ##Ray from center of screen to mouse
        ray = [Mouse,[dx, dy]]

        ##Find closest interaction
        closestIntersect = None
        for i in range(len(segments)):
            intersect = getIntersection(ray, segments[i])
            if intersect is None:
                continue
            if closestIntersect is None or intersect[2]<closestIntersect[2]:
                closestIntersect = list(intersect)


        ##Intersect angle
        if closestIntersect is None:
            continue
        closestIntersect.append(angle)
        
        ##Add to list of intersects
        intersects.append(closestIntersect)


    ##Sort intersects by angle
    intersects = sorted(intersects,key=lambda l:l[3])

    ##Draw as a polygon
    plot = []
    for intersect in intersects:
        plot.append([intersect[0],intersect[1]])
##    pygame.draw.polygon(canvas, [221,56,56], plot)
    pygame.draw.polygon(canvas, [238,238,238], plot)

    ##Draw debug lines
##    for intersect in intersects:
##        pygame.draw.line(canvas, [200,200,200], [Mouse[0], Mouse[1]], [intersect[0],intersect[1]])

    fps = font.render(str(int(clock.get_fps()))+" FPS", True, pygame.Color('Green'))
    canvas.blit(fps, [0,0])


##LINE SEGMENTS
segments = [
    ##Border
    [[-1,-1], [1280,-1]],
    [[1280,-1], [1280,720]],
    [[1280,720], [-1,720]],
    [[-1,720], [-1,-1]],

    ##Polygon #1
    [[100,150], [120,50]],
    [[120,50], [200,80]],
    [[200,80], [140,210]],
    [[140,210], [100,150]],

    ##Polygon #2
    [[100,200], [120,250]],
    [[120,250], [60,300]],
    [[60,300], [100,200]],

    ##Polygon #3
    [[200,260], [220,150]],
    [[220,150], [300,200]],
    [[300,200], [350,320]],
    [[350,320], [200,260]],

    ##Polygon #4
    [[340,60], [360,40]],
    [[360,40], [370,70]],
    [[370,70], [340,60]],

    ##Polygon #5
    [[450,190], [560,170]],
    [[560,170], [540,270]],
    [[540,270], [430,290]],
    [[430,290], [450,190]],

    ##Polygon #6
    [[400,95], [580,50]],
    [[580,50], [480,150]],
    [[480,150], [400,95]],

    ##Polygon #7
    [[880,160], [1060,200]],
    [[1060,200], [980, 390]],
    [[980, 390], [780,364]],
    [[780,364], [900, 250]],
    [[900, 250], [880,160]]
    ]

##DRAW LOOP
updateCanvas = True
def drawLoop(updateCanvas, canvas, segments, Mouse):
    if updateCanvas:
    	draw(canvas, segments, Mouse)
    	updateCanvas = False
    	pygame.display.flip()

##MOUSE	
Mouse = [canvas.get_width()/2, canvas.get_height()/2]
while True:
    clock.tick()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    Mouse = pygame.mouse.get_pos()
    updateCanvas = True
    drawLoop(updateCanvas, canvas, segments, Mouse)












