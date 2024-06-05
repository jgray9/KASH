import pygame
import elements
import json
import os, sys

WINDOW_SIZE = (1000, 750)
DEPARTMENTS = {}

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
    scenes = {}

    # 
    # create road scene
    # 
    scenes['road'] = elements.Scene([
        elements.ImageElement(screen, get_file_path('images/background.png'), 0, 0),
        elements.ImageElement(screen, get_file_path('images/info_board.png'), x = 300, y = 10),
        elements.TitleElement(screen, DEPARTMENTS['VHA']['title'], 24, 'white', x = 310, y = 24, w = 660),
        elements.TextElement(screen, DEPARTMENTS['VHA']['desc'], 20, 'white', x = 315, y = 65, w = 650),
    ])
    # 16 elements each is 40 pixels tall
    # 17 empty spaces between each element (and edge of screen)
    # calculate the size of the empty spaces
    space_between_elements = (WINDOW_SIZE[1] - (16 * 40)) / 17
    y = space_between_elements
    for department in DEPARTMENTS:
        scenes['road'].elements.extend([
            elements.ImageElement(screen, get_file_path('images/sign.png'), x = 0, y = y, next_scene = department),
            elements.TitleElement(screen, department, 24, 'white', x = 129, y = y + 10, w = 140),
        ])
        y += space_between_elements + 40
    
    # 
    # create department info screens
    # 
    for department in DEPARTMENTS:
        scenes[department] = elements.Scene([
            elements.ImageElement(screen, get_file_path('images/background_2.png'), x = 0, y = 0),
            elements.ImageElement(screen, get_file_path('images/back.png'), x = 10, y = 10, next_scene='road'),
            elements.TitleElement(screen, department, 30, 'black', x = 0, y = 15, w = WINDOW_SIZE[0])
        ])

    return scenes

def program_loop(screen, scenes):
    # start on the road scene
    current_scene: elements.Scene = scenes['road']
    # loop until program closes
    while True:

        # HANDLE INPUT

        events = pygame.event.get() # all events that occured last frame
        for event in events:
            # user closes the window
            if event.type == pygame.QUIT:
                return
            # user moves the mouse
            if event.type == pygame.MOUSEMOTION:
                current_scene.check_hover(event.pos[0], event.pos[1])
            # user clicks the mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                current_scene.check_click(event.pos[0], event.pos[1])
                print(event.pos)
            # user hovers mouse of element
            if event.type == elements.ELEMENTHOVEREVENT:
                e: elements.SceneElement = event.element
                if current_scene == scenes['road'] and e.next_scene != None:
                    title_element: elements.TitleElement = current_scene.elements[2]
                    desc_element: elements.TextElement = current_scene.elements[3]
                    # reduce size if the department is OEDCA since the name is so long
                    title_font_size = 20 if e.next_scene == 'OEDCA' else 24
                    title_element.y = 26 if e.next_scene == 'OEDCA' else 24
                    # update text
                    title_element.set_text(DEPARTMENTS[e.next_scene]['title'], title_font_size, 'white')
                    desc_element.set_text(DEPARTMENTS[e.next_scene]['desc'], 20, 'white')

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
    with open(get_file_path("departments.json")) as text_file:
        DEPARTMENTS = json.load(text_file)
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    scenes = create_scenes(screen)
    program_loop(screen, scenes)

    pygame.quit()