import pygame

# ID for a custom pygame event for changing scenes
CHANGESCENEEVENT = pygame.USEREVENT + 1

class Scene:
    def __init__(self, elements: list) -> None:
        self.elements = elements
    
    def click(self, x, y):
        for e in self.elements:
            e.click(x, y)
    
    def draw_all(self):
        for e in self.elements:
            e.draw()

class SceneElement:
    def __init__(self, screen: pygame.Surface,
                 x: int | float, y: int | float,
                 w: int | float, h: int | float,
                 opacity: int = 256,
                 next_scene: str = None) -> None:
        self.screen = screen
        # position of element
        self.x = x
        self.y = y
        # size of element
        self.w = w
        self.h = h
        # scene to transition to when element is clicked
        # (none by default since most elements wont be clickable)
        self.next_scene = next_scene
        # transparency of element
        self.opacity = opacity
    
    def click(self, x, y):
        # element not clickable
        if self.next_scene == None: return
        # too far left
        if x < self.x: return
        # too far right
        if x > self.x + self.w: return
        # too far up
        if y < self.y: return
        # too far down
        if y > self.y + self.h: return
        # create a new change scene event
        event = pygame.event.Event(CHANGESCENEEVENT, {'scene': self.next_scene})
        # trigger the event
        pygame.event.post(event)
    
    def draw(self):
        pass

class ImageElement(SceneElement):
    def __init__(self, screen: pygame.Surface,
                 filename: str,
                 x: int | float, y: int | float,
                 opacity: int = 256,
                 next_scene: str = None) -> None:
        # load image from file
        # loading an image automatically creates a surface with the image on it
        self.image_surface = pygame.image.load(filename)
        # call super constructor
        super().__init__(screen, x, y, self.image_surface.get_width(), self.image_surface.get_height(), opacity, next_scene)
        # set transparency
        self.image_surface.set_alpha(self.opacity)
    
    def draw(self):
        # blit() draws one surface onto another surface
        self.screen.blit(self.image_surface, (self.x, self.y))

class TextElement(SceneElement):
    def __init__(self, screen: pygame.Surface,
                 text: str, text_size: int, text_color: str,
                 x: int | float, y: int | float,
                 w: int | float,
                 opacity: int = 256) -> None:
        # call super constructor
        # width and height are used for click detection, not actual size of display
        # since text elements are never clickable, height does not matter
        # width matters since it is used to determine line breaks
        super().__init__(screen, x, y, w, 0, opacity=opacity)
        self.padding = 5
        # create new font with size size
        # no need for 'self.' since this wont be used outside of __init__
        font = pygame.font.Font(pygame.font.get_default_font(), text_size)
        # pygame can only render one line at a time
        # text must be split into multiple surfaces
        self.text_surfaces = []
        curr_x = x + self.padding
        curr_y = y + self.padding
        # iterate through each word
        for line in text.split('\n'):
            for word in line.split(' '):
                # surface for current word
                curr_surface = font.render(word + ' ', True, text_color)
                # if new x is out of bounds, increase y for a new line of text, and reset x
                if curr_x + curr_surface.get_width() >= x + w - self.padding:
                    curr_x = x + self.padding
                    curr_y += curr_surface.get_height()
                # add to list
                curr_surface.set_alpha(self.opacity)
                self.text_surfaces.append((curr_x, curr_y, curr_surface))
                curr_x += curr_surface.get_width()
            # reset x and increase y for new line
            curr_x = x + self.padding
            curr_y += curr_surface.get_height()
    
    def draw(self):
        for x, y, text_surface in self.text_surfaces:
            self.screen.blit(text_surface, (x, y))

class TitleElement(SceneElement):
    def __init__(self, screen: pygame.Surface,
                 text: str, text_size: int, text_color: str,
                 x: int | float, y: int | float,
                 w: int | float,
                 opacity: int = 256) -> None:
        # call super constructor
        # width and height are used for click detection, not actual size of display
        # since title elements are never clickable, height does not matter
        # width matters since it is used to center text
        super().__init__(screen, x, y, w, 0, opacity=opacity)
        # create new font with size size
        # no need for 'self.' since this wont be used outside of __init__
        font = pygame.font.Font(pygame.font.get_default_font(), text_size)
        # titles are only one line so one surface should suffice
        self.text_surface = font.render(text, True, text_color)
        self.text_surface.set_alpha(opacity)
    
    def draw(self):
        # center text in element
        # text is left aligned by default -> left edge of textbox = left edge of element
        # add element_width / 2 to move the text right -> left edge of text = center of element
        # sub text_width / 2 to move text left -> center of text = center of element
        centered_x = self.x + (self.w / 2) - (self.text_surface.get_width() / 2)
        # blit() draws one surface onto another surface
        self.screen.blit(self.text_surface, (centered_x, self.y))