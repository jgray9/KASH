import pygame
import elements

WINDOW_SIZE = (800, 600)

def create_scenes(screen: pygame.Surface):
    scenes = {}
    # create road scene
    scenes['road'] = elements.Scene([
        elements.ImageElement(screen, 0, 0, 800, 600, "road.png"),
        elements.ImageElement(screen, 200, 400, 86, 150, 'pin.png', 'vha'),
        elements.ImageElement(screen, 540, 190, 86, 150, 'pin.png', 'vba'),
        elements.ImageElement(screen, 180, 35, 86, 150, 'pin.png', 'nca')
    ])
    # create vha scene
    scenes['vha'] = elements.Scene([
        elements.TitleElement(screen, 100, 50, 600, 30, "Veterans Health Administration (VHA)", 30),
        elements.ImageElement(screen, 10, 10, 50, 50, "back.png", "road"),
        elements.TextElement(screen, 50, 100, 700, 400,
"""The Veterans Health Administration (VHA) provides healthcare
services to veterans, such as regular checkups with a primary care
provider or appointments with specialists (cardiologists, gynecologists, etc.)
Veterans are sorted into 8 priority groups, which determine the cost of
copayments as well as access to additional benefits such as dental care.

Website: https://www.va.gov/health/
Phone Number: 1-877-222-VETS (8387)""", 18)
    ])
    # create vba scene
    scenes['vba'] = elements.Scene([
        elements.TitleElement(screen, 100, 50, 600, 30, "Veterans Benefits Administration (VBA)", 30),
        elements.ImageElement(screen, 10, 10, 50, 50, "back.png", "road"),
        elements.TextElement(screen, 50, 100, 700, 400,
"""The Veterans Benefits Administration (VBA) provides many different
services to help veterans transition to civilian life. This includes
assistance with home loans, college tuition, and carrer counseling.
VBA is also responsible for pensions and monetary compensation for the
elderly and disabled. 

Website: https://benefits.va.gov/benefits/
Phone Number: 1-800-827-1000""", 18)
    ])
    # create nca scene
    scenes['nca'] = elements.Scene([
        elements.TitleElement(screen, 100, 50, 600, 30, "National Cemetery Administration (NCA)", 30),
        elements.ImageElement(screen, 10, 10, 50, 50, "back.png", "road"),
        elements.TextElement(screen, 50, 100, 700, 400,
"""The National Cemetery Administration (NCA) provides burial spaces
for veterans and maintains national cemetaries. NCA covers the cost
of the gravesite, grave liner, opening/closing of the grave, and U.S.
burial flag for free. Spouses, widows, and children of veterans are
also covered by the NCA, even if they die before the veteran themself.

Website: https://www.cem.va.gov/
Phone Number: 1-800-698-2411""", 18)
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
                # coordinates of mouse
                mouse_position = pygame.mouse.get_pos()
                # Scene.click() returns name of scene to transition to if a clickable element is clicked
                # click() returns None of no clickable element is clicked
                next_scene_name = current_scene.click(mouse_position[0], mouse_position[1])
                current_scene = scenes[next_scene_name] if next_scene_name != None else current_scene
        
        # HANDLE OUTPUT

        # Clear screen
        screen.fill("white")
        # Draw new elements
        current_scene.draw()
        # Update display
        pygame.display.flip()

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    scenes = create_scenes(screen)
    program_loop(screen, scenes)

    pygame.quit()