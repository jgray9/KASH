import pygame
import func

WINDOW_SIZE = (800, 600)

pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
scene = "ROAD"
TITLE_FONT = pygame.font.Font(pygame.font.get_default_font(), 30)

class ImageButton:
    def __init__(self, filename, x, y, w, h, scene):
        # load image from file
        self.image = pygame.image.load(filename)
        # rescale image to size
        self.image = pygame.transform.scale(self.image, (w, h))
        # create shape to project image onto
        self.image_rect = pygame.Rect(x, y, w, h)
        # scene to transition to after image is clicked
        self.scene = scene
        # bool for if image is visible
        self.visible = False

    def draw(self):
        # dont draw if not visible
        if self.visible:
            # screen.blit adds an element to the screen
            screen.blit(self.image, self.image_rect)

    def click(self, mouse_pos):
        # Rect.collidepoint checks if a location is inside the rectangle
        if self.visible and self.image_rect.collidepoint(mouse_pos):
            change_scene(self.scene)

images = [
    ImageButton("pin.png", 200, 400, 86, 150, "VHA"),
    ImageButton("pin.png", 540, 190, 86, 150, "VBA"),
    ImageButton("pin.png", 180, 35, 86, 150, "NCA"),
    ImageButton("back.png", 10, 10, 50, 50, "ROAD")
]

def change_scene(new_scene):
    print("new scene = {}".format(new_scene))
    scene = new_scene

    # Clear screen
    screen.fill("white")

    # Show road & pins if scene is road
    for i in images:
        i.visible = scene == "ROAD"
    # Show back button only if scene is not road
    images[3].visible = scene != "ROAD"

    # Default screen
    if scene == "ROAD":
        func.draw_image(screen, "road.png", 0, 0, WINDOW_SIZE[0], WINDOW_SIZE[1])
    # Veterans Health Administration
    elif scene == "VHA":
        func.draw_text(screen, "Veterans Health Administration (VHA)", 30, WINDOW_SIZE[0] / 2, 50, True)
    # Veterans Benefits Administration
    elif scene == "VBA":
        func.draw_text(screen, "Veterans Benefits Administration (VBA)", 30, WINDOW_SIZE[0] / 2, 50, True)
    # National Cemetery Administration
    elif scene == "NCA":
        func.draw_text(screen, "National Cemetery Administration (NCA)", 30, WINDOW_SIZE[0] / 2, 50, True)

    # Draw all images
    for i in images: i.draw()
    # Update screen
    pygame.display.flip()

change_scene("ROAD")
running = True
while running:

    events = pygame.event.get() # all events that occured last frame
    for event in events:
        # user closes the window
        if event.type == pygame.QUIT:
            running = False
        # user clicks the mouse
        if event.type == pygame.MOUSEBUTTONDOWN:
            # coordinates of mouse
            mouse_pos = pygame.mouse.get_pos()
            print(mouse_pos)
            # [1:] starts at index one / road image is a background image and shouldnt be clicked
            for i in images:
                i.click(mouse_pos)


pygame.quit()