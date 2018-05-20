import pygame
from deleteModule import delete_module
from PygameButton import PygameButton

pygame.init()
info_object = pygame.display.Info()
width = info_object.current_w
height = info_object.current_h
game_display = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption("Main frame")
clock = pygame.time.Clock()
train_button_position = (0.4*width,0.45*height,0.2*width,0.05*height)
control_button_position = (0.4*width,0.55*height,0.2*width,0.05*height)
quit_button_position = (0.4*width,0.65*height,0.2*width,0.05*height)
font = pygame.font.SysFont('Comic Sans MS', 30)
train_button = PygameButton(game_display, train_button_position, (0, 255, 0), font, "Train model", (255, 255, 255))
control_button = PygameButton(game_display, control_button_position, (0, 255, 0), font, "Control robot", (255, 255, 255))
quit_button = PygameButton(game_display, quit_button_position, (255, 0, 0), font, "Quit", (255, 255, 255))
crashed = False
train_phase = False
control_phase = False

while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        if event.type == pygame.MOUSEBUTTONUP:
            if train_button.is_pushed():
                crashed = True
                train_phase = True
            if control_button.is_pushed():
                crashed = True
                control_phase = True
            if quit_button.is_pushed():
                crashed = True
    pygame.display.update()
    clock.tick(30)
pygame.quit()
if train_phase:
    try:
        delete_module("trainInterface")
        import trainInterface
    except:
        import trainInterface
elif control_phase:
    try:
        delete_module("controlInterface")
        import controlInterface
    except:
        import controlInterface