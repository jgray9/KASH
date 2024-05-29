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
    def __init__(self, screen, x, y, w, h, next_scene=None, a=256, bg_color=(0, 0, 0, 0)) -> None:
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
        # alpha of element
        self.a = a
        # set background color
        self.bg_surface = pygame.Surface((w, h))
        self.bg_surface.fill(bg_color)
        self.bg_surface.set_alpha(bg_color[3])
    
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
    def __init__(self, screen, x, y, w, h, filename, next_scene=None) -> None:
        # call super constructor
        super().__init__(screen, x, y, w, h, next_scene)
        # load image from file
        # loading an image automatically creates a surface with the image on it
        self.image_surface = pygame.image.load(filename)
        # rescale image to size
        self.image_surface = pygame.transform.scale(self.image_surface, (w, h))
        # set transparency
        self.image_surface.set_alpha(self.a)
    
    def draw(self):
        # blit() draws one surface onto another surface
        self.screen.blit(self.image_surface, (self.x, self.y))

class TextElement(SceneElement):
    def __init__(self, screen, x, y, w, h, text, text_size, next_scene=None, bg_color=(0,0,0,0), a=256) -> None:
        # call super constructor
        super().__init__(screen, x, y, w, h, next_scene, a, bg_color)
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
                curr_surface = font.render(word + ' ', True, "black")
                # if new x is out of bounds, increase y for a new line of text, and reset x
                if curr_x + curr_surface.get_width() >= x + w - self.padding:
                    curr_x = x + self.padding
                    curr_y += curr_surface.get_height()
                # add to list
                self.text_surfaces.append((curr_x, curr_y, curr_surface))
                curr_x += curr_surface.get_width()
            # reset x and increase y for new line
            curr_x = x + self.padding
            curr_y += curr_surface.get_height()
    
    def draw(self):
        self.screen.blit(self.bg_surface, (self.x, self.y))
        for x, y, text_surface in self.text_surfaces:
            self.screen.blit(text_surface, (x, y))

class TitleElement(SceneElement):
    def __init__(self, screen, x, y, w, h, text, text_size, next_scene=None, a=256, bg_color=(0, 0, 0, 0)) -> None:
        # call super constructor
        super().__init__(screen, x, y, w, h, next_scene, a, bg_color)
        # create new font with size size
        # no need for 'self.' since this wont be used outside of __init__
        font = pygame.font.Font(pygame.font.get_default_font(), text_size)
        # titles are only one line so one surface should suffice
        self.text_surface = font.render(text, True, "black")
    
    def draw(self):
        # center text in element
        # x coordinate specifies left of the object
        # move text right by element_width / 2 so text_x is at center of element
        # move text left by text_width / 2 so text is at center of the element
        centered_x = self.x + (self.w / 2) - (self.text_surface.get_width() / 2)
        # blit() draws one surface onto another surface
        self.screen.blit(self.text_surface, (centered_x, self.y))