import pygame

# specifying variable types are only for readibility and dont really do anything code-wise
# centered=False just specifies the default value, so draw_text can be called without including the centered argument
def draw_text(surface: pygame.Surface, text: str, size: int, x: int, y: int, centered=False):
    # create new font with size size
    font = pygame.font.Font(pygame.font.get_default_font(), size)
    # pygame can only render one line at a time
    # iterate through each line in the text
    for line in text.split('\n'):
        # create a new surface object with text on it
        text_surface = font.render(line, True, "black")
        # subtract by width/2 to move object left to center of coords
        if centered:
            x = x - text_surface.get_width() / 2 
        # blit() draws one surface onto another surface
        surface.blit(text_surface, (x, y))
        # increase y by the text_height for the next line
        y += text_surface.get_height()


# def draw_title(title_text, x, y):
#     text = TITLE_FONT.render(title_text, True, "black")
#     # coordinates usually represent top-left of an object
#     # subtract by width/2 to move object to center of coords
#     coords = (x - text.get_width() / 2, y)
#     screen.blit(text, coords)