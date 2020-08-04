import contextlib
with contextlib.redirect_stdout(None):
    import pygame, pygame.freetype, sys, random, math
    from pygame.locals import *
    from pygame.sprite import Sprite
    from pygame.sprite import RenderUpdates


def createSurfaceWithText(text, size, text_rgb, bg_rgb):
    Font=pygame.font.Font("Assets\emulogic.ttf", size)
    surface = Font.render(text, False, text_rgb, bg_rgb)
    return surface.convert_alpha()


class UITextElement(Sprite):
    def __init__(self, title, center_pos, text, size, bg_rgb, text_rgb, action=None):
        self.mouse_over = False
        self.action = action
        default_img = createSurfaceWithText(text, size, text_rgb, bg_rgb)
        if not title:
##            highlighted_img = createSurfaceWithText(text, size*1.2, text_rgb, bg_rgb)
            highlighted_img = createSurfaceWithText(text, size, (200,200,200), bg_rgb)
        else:
            highlighted_img = default_img
        self.images = [default_img, highlighted_img]
        self.rects = [default_img.get_rect(center=center_pos), highlighted_img.get_rect(center=center_pos)]
        super().__init__()

    @property
    def image(self):
        return self.images[1] if self.mouse_over else self.images[0]

    @property
    def rect(self):
        return self.rects[1] if self.mouse_over else self.rects[0]
    
    def update(self, mouse_pos, mouse_up, selected):
        if self.rect.collidepoint(mouse_pos) or selected:
            self.mouse_over = True
            if mouse_up:
                return self.action
        else:
            self.mouse_over = False

    def draw(self, surface):
        surface.blit(self.image, self.rect)


ALT, F4 = False, False
def menuEvents():
    global ALT, F4
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == 308:
                ALT = True
            if event.key == 285:
                F4 = True
        if event.type == pygame.KEYUP:
            if event.key == 308:
                ALT = False
            if event.key == 285:
                F4 = False
    if ALT and F4:
        pygame.quit()
        sys.exit()

def gameEvents(menu):
    global ALT, F4
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        #Escape key
        if event.type == pygame.KEYDOWN and event.key == 27:
            menu.ChangeLevel("Pause")

        if event.type == pygame.KEYDOWN:
            if event.key == 308:
                ALT = True
            if event.key == 285:
                F4 = True
        if event.type == pygame.KEYUP:
            if event.key == 308:
                ALT = False
            if event.key == 285:
                F4 = False
    if ALT and F4:
        pygame.quit()
        sys.exit()


class SFX:
    def __init__(self):
        pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512, devicename=None)
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512, allowedchanges=AUDIO_ALLOW_FREQUENCY_CHANGE | AUDIO_ALLOW_CHANNELS_CHANGE)

class MenuLevel:
    def __init__(self, level):
        self.level=[]
        self.level.append(level)
    def GetLevel(self):
        return self.level[-1]
    def ChangeLevel(self, level):
        if level != "Back":
            self.level.append(level)
        elif level == "Back":
            self.level.pop()
    def BackLevel(self):
        self.level.pop()


class Tiles(Sprite):
    def __init__(self):
        pass

    @property
    def image(self):
        pass

    @property
    def rect(self):
        return self.rects[0]

    def draw(self, screen):
        screen.blit(self.image, self.rect)


def game(screen, clock, menu):
    screen.fill([0,0,0])
    gameEvents(menu)
    pygame.display.flip()
    pygame.display.set_caption(str(int(clock.get_fps()))+"FPS")
    clock.tick()



'''
Menus
'''
def titleScreen(screen, clock, menu):
    title = UITextElement(True, [screen.get_width()/2, int(60*(screen.get_height()/720))], "Game", int(50*(screen.get_height()/720)), None, (255,255,255))
    play_button = UITextElement(False, [screen.get_width()/2, int(410*(screen.get_height()/720))], "Play", int(30*(screen.get_height()/720)), None, (255,255,255), "M.Game")
    options_button = UITextElement(False, [screen.get_width()/2, int(460*(screen.get_height()/720))], "Options", int(30*(screen.get_height()/720)), None, (255,255,255), "M.Options")
    quit_button = UITextElement(False, [screen.get_width()/2, int(510*(screen.get_height()/720))], "Quit", int(30*(screen.get_height()/720)), None, (255,255,255), "M.Quit")

    buttons = RenderUpdates(title, play_button, options_button, quit_button)
    ##buttons.add(new_button)
    return menuLoop(screen, clock, menu, buttons)

def pauseScreen(screen, clock, menu):
    title = UITextElement(True, [screen.get_width()/2, int(60*(screen.get_height()/720))], "Pause", int(50*(screen.get_height()/720)), None, (255,255,255))
    resume_button = UITextElement(False, [screen.get_width()/2, int(160*(screen.get_height()/720))], ("Resume"), int(30*(screen.get_height()/720)), None, (255,255,255), "M.Back")
    save_button = UITextElement(False, [screen.get_width()/2, int(210*(screen.get_height()/720))], ("Save"), int(30*(screen.get_height()/720)), None, (255,255,255), "S.Save")
    options_button = UITextElement(False, [screen.get_width()/2, int(260*(screen.get_height()/720))], ("Options"), int(30*(screen.get_height()/720)), None, (255,255,255), "M.Options")
    back_button = UITextElement(False, [screen.get_width()/2, int(660*(screen.get_height()/720))], "Exit to main menu", int(30*(screen.get_height()/720)), None, (255,255,255), "M.Main")

    buttons = RenderUpdates(title, resume_button, save_button, options_button, back_button)
    return menuLoop(screen, clock, menu, buttons)

def optionsScreen(screen, clock, menu):
    title = UITextElement(True, [screen.get_width()/2, int(60*(screen.get_height()/720))], "Options", int(50*(screen.get_height()/720)), None, (255,255,255))
##    language_button = UITextElement(False, [screen.get_width()/2, int(160*(screen.get_height()/720))], "Language", int(30*(screen.get_height()/720)), None, (255,255,255), "M.Language")
##    video_button = UITextElement(False, [screen.get_width()/2, int(210*(screen.get_height()/720))], "Video Settings", int(30*(screen.get_height()/720)), None, (255,255,255), "M.Video")
##    audio_button = UITextElement(False, [screen.get_width()/2, int(260*(screen.get_height()/720))], "Audio", int(30*(screen.get_height()/720)), None, (255,255,255), "M.Audio")
##    controls_button = UITextElement(False, [screen.get_width()/2, int(310*(screen.get_height()/720))], "Controls", int(30*(screen.get_height()/720)), None, (255,255,255), "M.Controls")
    back_button = UITextElement(False, [screen.get_width()/2, int(660*(screen.get_height()/720))], "Back", int(30*(screen.get_height()/720)), None, (255,255,255), "M.Back")

##    buttons = RenderUpdates(title, language_button, video_button, audio_button, controls_button, back_button)
    buttons = RenderUpdates(title, back_button)
    return menuLoop(screen, clock, menu, buttons)

def menuLoop(screen, clock, menu, buttons):
    selected = False
    mouse_down = False
    font1=pygame.font.SysFont("Courier", 20, bold=True)
    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == 27:
                if menu.GetLevel() != "Main":
                    menu.BackLevel()
                    return

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_down = True
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
                mouse_down = False

        screen.fill([106,159,181])

        for button in buttons:
            action = button.update(pygame.mouse.get_pos(), mouse_up, selected)
            if action is not None:
                if action[:1] == "M":
                    menu.ChangeLevel(action[2:])
                    return
##                if action[:1] == "S":
##                    value = eval(action[2:])()
##                    return

        buttons.draw(screen)

        pygame.display.set_caption(str(int(clock.get_fps()))+"FPS")
        pygame.display.flip()
        clock.tick()


def main():
    audio = SFX()
    pygame.init()
##    pygame.display.set_icon()
    screen = pygame.display.set_mode([1280, 720])
    clock = pygame.time.Clock()

    menu = MenuLevel("Main")

    while True:
        if menu.GetLevel() == "Game":
            game(screen, clock, menu)
        elif menu.GetLevel() == "Main":
            titleScreen(screen, clock, menu)
        elif menu.GetLevel() == "Pause":
            pauseScreen(screen, clock, menu)
        elif menu.GetLevel() == "Options":
            optionsScreen(screen, clock, menu)
        elif menu.GetLevel() == "Quit":
            pygame.quit()
            sys.exit()
            return



if __name__ == "__main__":
    main()























