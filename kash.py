import pygame
import elements
import json
import os, sys

WINDOW_SIZE = (1000, 750)

# filepath is different when program is in .exe form
def get_file_path(filename):
    # true if file is in .exe form
    if hasattr(sys, "_MEIPASS"):
        # in .exe form, all files are in a temp directory
        # only include parts of filename that come after the last /
        # ex. images/road.png becomes road.png
        filename = filename[ filename.rfind('/') + 1 : ]
        # and then add the path to the temp directory before the filename
        # ex. road.png becomes .../AppData/Local/Temp/.../road.png
        filename = os.path.join(sys._MEIPASS, filename)
    return filename

def create_scenes(screen: pygame.Surface):
    text = {}
    with open(get_file_path("text.json")) as text_file:
        text = json.load(text_file)
    scenes = {}

    # create road scene
    scenes['road'] = elements.Scene([
        elements.ImageElement(screen,   0,   0, 1000, 750, get_file_path('images/background.png')),
        elements.ImageElement(screen,  50, 305,  250, 250, get_file_path('images/building.png'), 'vha'),
        elements.ImageElement(screen, 375, 305,  250, 250, get_file_path('images/building.png'), 'vba'),
        elements.ImageElement(screen, 700, 305,  250, 250, get_file_path('images/building.png'), 'nca'),
    ])
    # create vha scene
    scenes['vha'] = elements.Scene([
        elements.ImageElement(screen,   0,   0, 1000, 750, get_file_path('images/background_2.png')),
        elements.TitleElement(screen, 250,  50, 600,  30, text['vha']['title'], 30, bg_color=(0,255,0,50)),
        elements.ImageElement(screen,  10,  10, 200, 100, get_file_path('images/back.png'), 'road'),
        elements.TextElement(screen,  115, 140, 500, 400, text['vha']['desc'], 18, bg_color=(0,255,0,50)),
        elements.TextElement(screen,  645, 140, 300, 50, 'Phone Number:\n' + text['vha']['phone'], 18, bg_color=(0,255,0,50)),
        elements.TextElement(screen,  645, 200, 300, 50, 'Website:\n' + text['vha']['website'], 18, bg_color=(0,255,0,50)),
    ])
    # create vba scene
    scenes['vba'] = elements.Scene([
        elements.ImageElement(screen,   0,   0, 1000, 750, get_file_path('images/background_2.png')),
        elements.TitleElement(screen, 250,  50, 600,  30, text['vba']['title'], 30),
        elements.ImageElement(screen,  10,  10, 200, 100, get_file_path('images/back.png'), 'road'),
        elements.TextElement(screen,  115, 140, 500, 400, text['vba']['desc'], 18),
        elements.TextElement(screen,  645, 140, 300, 50, 'Phone Number:\n' + text['vba']['phone'], 18),
        elements.TextElement(screen,  645, 200, 300, 50, 'Website:\n' + text['vba']['website'], 18),
    ])
    # create nca scene
    scenes['nca'] = elements.Scene([
        elements.ImageElement(screen,   0,   0, 1000, 750, get_file_path('images/background_2.png')),
        elements.TitleElement(screen, 250,  50, 600,  30, text['nca']['title'], 30),
        elements.ImageElement(screen,  10,  10, 200, 100, get_file_path('images/back.png'), 'road'),
        elements.TextElement(screen,  115, 140, 500, 400, text['nca']['desc'], 18),
        elements.TextElement(screen,  645, 140, 300, 50, 'Phone Number:\n' + text['nca']['phone'], 18),
        elements.TextElement(screen,  645, 200, 300, 50, 'Website:\n' + text['nca']['website'], 18),
    ])

    return scenes

def program_loop(screen, scenes):
    # start on the road scene
    current_scene = scenes['road']
    # loop until program closes
    while True:

        # HANDLE INPUT

        events = pygame.event.get() # all events that occured last frame
        for event in events:
            # user closes the window
            if event.type == pygame.QUIT:
                return
            # user clicks the mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                current_scene.click(event.pos[0], event.pos[1])
                print(event.pos)
            # scene changes
            if event.type == elements.CHANGESCENEEVENT:
                current_scene = scenes[event.scene]
        
        # HANDLE OUTPUT

        # Clear screen
        screen.fill("white")
        # Draw new elements
        current_scene.draw_all()
        # Update display
        pygame.display.flip()

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    scenes = create_scenes(screen)
    program_loop(screen, scenes)

    pygame.quit()