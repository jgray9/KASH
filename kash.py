import pygame
import elements
import json

WINDOW_SIZE = (800, 600)

def create_scenes(screen: pygame.Surface):
    text = {}
    with open("text.json") as text_file:
        text = json.load(text_file)
    scenes = {}

    # create road scene
    scenes['road'] = elements.Scene([
        elements.ImageElement(screen, 0, 0, 800, 600, "images/road.png"),
        elements.ImageElement(screen, 200, 400, 86, 150, 'images/pin.png', 'vha'),
        elements.ImageElement(screen, 540, 190, 86, 150, 'images/pin.png', 'vba'),
        elements.ImageElement(screen, 180, 35, 86, 150, 'images/pin.png', 'nca')
    ])
    # create vha scene
    scenes['vha'] = elements.Scene([
        elements.TitleElement(screen, 100, 50, 600, 30, text['vha']['title'], 30),
        elements.ImageElement(screen, 10, 10, 50, 50, "images/back.png", "road"),
        elements.TextElement(screen, 50, 100, 700, 400, text['vha']['desc'], 18),
        elements.TextElement(screen, 50, 230, 700, 100, 'Phone Number: ' + text['vha']['phone'], 18),
        elements.TextElement(screen, 50, 248, 700, 100, 'Website: ' + text['vha']['website'], 18)
    ])
    # create vba scene
    scenes['vba'] = elements.Scene([
        elements.TitleElement(screen, 100, 50, 600, 30, text['vba']['title'], 30),
        elements.ImageElement(screen, 10, 10, 50, 50, "images/back.png", "road"),
        elements.TextElement(screen, 50, 100, 700, 400, text['vba']['desc'], 18),
        elements.TextElement(screen, 50, 230, 700, 100, 'Phone Number: ' + text['vba']['phone'], 18),
        elements.TextElement(screen, 50, 248, 700, 100, 'Website: ' + text['vba']['website'], 18)
    ])
    # create nca scene
    scenes['nca'] = elements.Scene([
        elements.TitleElement(screen, 100, 50, 600, 30, text['nca']['title'], 30),
        elements.ImageElement(screen, 10, 10, 50, 50, "images/back.png", "road"),
        elements.TextElement(screen, 50, 100, 700, 400, text['nca']['desc'], 18),
        elements.TextElement(screen, 50, 230, 700, 100, 'Phone Number: ' + text['nca']['phone'], 18),
        elements.TextElement(screen, 50, 248, 700, 100, 'Website: ' + text['nca']['website'], 18)
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