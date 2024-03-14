import pygame

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
    ImageButton("road.png", 0, 0, WINDOW_SIZE[0], WINDOW_SIZE[1], ""),
    ImageButton("pin.png", 200, 400, 86, 150, "VHA"),
    ImageButton("pin.png", 540, 190, 86, 150, "VBA"),
    ImageButton("pin.png", 180, 35, 86, 150, "NCA"),
    ImageButton("back.png", 10, 10, 50, 50, "ROAD")
]

def draw_title(title_text, x, y):
    text = TITLE_FONT.render(title_text, True, "black")
    # coordinates usually represent top-left of an object
    coords = (x - text.get_width() / 2, y)
    screen.blit(text, coords)

def change_scene(new_scene):
    print("new scene = {}".format(new_scene))
    scene = new_scene

    # Clear screen
    screen.fill("white")

    # Show road & pins if scene is road
    for i in images[0:4]:
        i.visible = scene == "ROAD"
    # Show back button only if scene is not road
    images[4].visible = scene != "ROAD"

    # Veterans Health Administration
    if scene == "VHA":
        draw_title("Veterans Health Administration (VHA)", WINDOW_SIZE[0] / 2, 50)
    # Veterans Benefits Administration
    elif scene == "VBA":
        draw_title("Veterans Benefits Administration (VBA)", WINDOW_SIZE[0] / 2, 50)
    # National Cemetery Administration
    elif scene == "NCA":
        draw_title("National Cemetery Administration (NCA)", WINDOW_SIZE[0] / 2, 50)

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
            for i in images[1:]:
                i.click(mouse_pos)


pygame.quit()