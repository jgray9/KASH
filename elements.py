import pygame

# ID for a custom pygame event for changing scenes
CHANGESCENEEVENT = pygame.USEREVENT + 1
SEARCHARTICLEEVENT = pygame.USEREVENT + 2

class Scene:
    def __init__(self, elements: list) -> None:
        self.elements: list[SceneElement] = elements

    def check_click(self, x: float, y: float):
        for e in self.elements:
            if e.check_position(x, y):
                e.click()
    
    def draw_all(self):
        for e in self.elements:
            if not e.hidden:
                e.draw()

class SceneElement:
    def __init__(self, screen: pygame.Surface,
                 x: float, y: float,
                 w: float, h: float,
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
        # when true, element is not drawn even when its current scene is active
        self.hidden = False
    
    def check_position(self, x: float, y: float) -> bool:
        # element hidden
        if self.hidden: return False
        # too far left
        if x < self.x: return False
        # too far right
        if x > self.x + self.w: return False
        # too far up
        if y < self.y: return False
        # too far down
        if y > self.y + self.h: return False
        return True
        
    def click(self):
        # element not clickable
        if self.next_scene == None: return
        # create a new change scene event
        event = pygame.event.Event(CHANGESCENEEVENT, {'scene': self.next_scene})
        # trigger the event
        pygame.event.post(event)
    
    def draw(self):
        pass

class ImageElement(SceneElement):
    def __init__(self, screen: pygame.Surface,
                 filename: str,
                 x: float, y: float,
                 opacity: int = 256,
                 next_scene: str = None) -> None:
        # call super constructor
        # width and height are set in set_image() function
        super().__init__(screen, x, y, 0, 0, opacity, next_scene)
        self.set_image(filename)
    
    def set_image(self, filename: str):
        # load image from file
        # loading an image automatically creates a surface with the image on it
        self.image_surface = pygame.image.load(filename)
        self.image_surface.set_alpha(self.opacity)
        # update width and height of element
        self.w = self.image_surface.get_width()
        self.h = self.image_surface.get_height()
    
    def draw(self):
        # blit() draws one surface onto another surface
        self.screen.blit(self.image_surface, (self.x, self.y))

class TextElement(SceneElement):
    def __init__(self, screen: pygame.Surface,
                 text: str, text_size: int, text_color: str,
                 x: float, y: float,
                 w: float,
                 opacity: int = 256) -> None:
        # call super constructor
        # width and height are used for click detection, not actual size of display
        # since text elements are never clickable, height does not matter
        # width matters since it is used to determine line breaks
        super().__init__(screen, x, y, w, 0, opacity)
        self.set_text(text, text_size, text_color)
    
    def set_text(self, text: str, text_size: int, text_color: str):
        # store text info so other parts of the program can look at it
        self.text = text
        self.text_size = text_size
        self.text_color = text_color
        # space between text and edges of element
        padding = 5
        # create new font with size text_size
        # no need for 'self.' since this wont be used outside of set_text()
        font = pygame.font.Font(pygame.font.get_default_font(), text_size)
        # pygame can only render one line at a time
        # text must be rendering using multiple surfaces
        self.text_surfaces = []
        # iterate through each word
        curr_x = self.x + padding
        curr_y = self.y + padding
        for line in text.split('\n'):
            for word in line.split(' '):
                # surface for current word
                curr_surface = font.render(word + ' ', True, text_color)
                # if new x is out of bounds, increase y for a new line of text, and reset x
                if curr_x + curr_surface.get_width() >= self.x + self.w - padding:
                    curr_x = self.x + padding
                    curr_y += curr_surface.get_height()
                # add to list
                curr_surface.set_alpha(self.opacity)
                self.text_surfaces.append((curr_x, curr_y, curr_surface))
                curr_x += curr_surface.get_width()
            # reset x and increase y for new line
            curr_x = self.x + padding
            curr_y += curr_surface.get_height()

    def draw(self):
        for x, y, text_surface in self.text_surfaces:
            self.screen.blit(text_surface, (x, y))

class TitleElement(SceneElement):
    def __init__(self, screen: pygame.Surface,
                 text: str, text_size: int, text_color: str,
                 x: float, y: float,
                 w: float,
                 opacity: int = 256) -> None:
        # call super constructor
        # width and height are used for click detection, not actual size of display
        # since title elements are never clickable, height does not matter
        # width matters since it is used to center text
        super().__init__(screen, x, y, w, 0, opacity=opacity)
        self.set_text(text, text_size, text_color)
    
    def set_text(self, text: str, text_size: int, text_color: str):
        # store text info so other parts of the program can look at it
        self.text = text
        self.text_size = text_size
        self.text_color = text_color
        # create new font with size text_size
        # no need for 'self.' since this wont be used outside of set_text()
        font = pygame.font.Font(pygame.font.get_default_font(), text_size)
        # titles are only one line so one surface should suffice
        self.text_surface = font.render(text, True, text_color)
        self.text_surface.set_alpha(self.opacity)

    def draw(self):
        # center text in element
        # text is left aligned by default -> left edge of textbox = left edge of element
        # add element_width / 2 to move the text right -> left edge of text = center of element
        # sub text_width / 2 to move text left -> center of text = center of element
        centered_x = self.x + (self.w / 2) - (self.text_surface.get_width() / 2)
        # blit() draws one surface onto another surface
        self.screen.blit(self.text_surface, (centered_x, self.y))