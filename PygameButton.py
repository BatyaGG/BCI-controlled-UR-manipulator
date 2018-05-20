import pygame


class PygameButton:
    def __init__(self, display, position, color, font, text, text_color):
        self.position = position
        pygame.draw.rect(display, color, (position[0],
                                                position[1],
                                                position[2],
                                                position[3]))
        display.blit(font.render(text, False, text_color),
                          (position[0], position[1]))

    def is_pushed(self):
        if pygame.mouse.get_pos()[0] >= self.position[0] and \
                        pygame.mouse.get_pos()[1] >= self.position[1]:
            if pygame.mouse.get_pos()[0] <= self.position[0] + self.position[2] and \
                            pygame.mouse.get_pos()[1] <= self.position[1] + self.position[3]:
                return True
        return False
