import time
import pickle
import glob
import os
import pygame
from UR import UR
from BCI import BCI
from PygameButton import PygameButton
from deleteModule import delete_module
from ControlUpdater import ControlUpdater
from BatyaGGPreprocessor import BatyaGGPreprocessor
from pygame import mixer

mixer.init()
pygame.init()
game_display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) # full screen mode
# game_display = pygame.display.set_mode((800, 600)) # specified resolution mode
info_object = pygame.display.Info()
width = info_object.current_w
height = info_object.current_h
pygame.display.set_caption("Control frame")
clock = pygame.time.Clock()
left_arm_x = (0.35*width,0.15*height,0.1*width,0.1*height)
right_arm_x = (0.55*width,0.15*height,0.1*width,0.1*height)
leg_x = (0.35*width,0.26*height,0.3*width,0.02*height)
left_arm_y = (0.35*width,0.35*height,0.1*width,0.1*height)
right_arm_y = (0.55*width,0.35*height,0.1*width,0.1*height)
leg_y = (0.35*width,0.46*height,0.3*width,0.02*height)
left_arm_z = (0.35*width,0.55*height,0.1*width,0.1*height)
right_arm_z = (0.55*width,0.55*height,0.1*width,0.1*height)
leg_z = (0.35*width,0.66*height,0.3*width,0.02*height)
left_arm_g = (0.35*width,0.75*height,0.1*width,0.1*height)
right_arm_g = (0.55*width,0.75*height,0.1*width,0.1*height)
leg_g = (0.35*width,0.86*height,0.3*width,0.02*height)
finish_button_position = (0.85*width,0.9*height,0.1*width,0.05*height)
font = pygame.font.SysFont('Comic Sans MS', 30)
PygameButton(game_display, left_arm_x, (0, 0, 255), font, "    -", (255, 255, 255))
PygameButton(game_display, right_arm_x, (0, 0, 255), font, "    +", (255, 255, 255))
PygameButton(game_display, left_arm_y, (0, 0, 255), font, "    -", (255, 255, 255))
PygameButton(game_display, right_arm_y, (0, 0, 255), font, "    +", (255, 255, 255))
PygameButton(game_display, left_arm_z, (0, 0, 255), font, "    -", (255, 255, 255))
PygameButton(game_display, right_arm_z, (0, 0, 255), font, "    +", (255, 255, 255))
PygameButton(game_display, left_arm_g, (0, 0, 255), font, "    C", (255, 255, 255))
PygameButton(game_display, right_arm_g, (0, 0, 255), font, "    O", (255, 255, 255))
finish_button = PygameButton(game_display, finish_button_position, (255, 0, 0), font, "Finish", (255, 255, 255))
pygame.display.update()
crashed = False
# directory = max(glob.glob('*'), key=os.path.getctime) # path to last modified folder
directory = 'Your model directory name' # hard coded path to trained model
with open(directory + '/Data.pickle', 'rb') as handle:
    rows_per_epoch = pickle.load(handle)['X'].shape[0]
with open(directory + '/Model.pickle', 'rb') as handle:
    clf = pickle.load(handle)
# clf.zero_thresh = 0.5 # this classifier parameter can be changed during control stage
bci = BCI()
prp = BatyaGGPreprocessor(rows_per_epoch)
recent_data = prp.fit_test(bci.get_recent_data(rows_per_epoch))
current_class = clf.predict(recent_data)
control_updater = ControlUpdater(['x', 'y', 'z', 'g'])
current_control = control_updater.get_next()
ur = UR()
ur.go_home()
mixer.music.load('x_axis.mp3')
mixer.music.play()
while not crashed:
    if current_class == 3:
        current_control = control_updater.get_next()
        if current_control == 'x':
            mixer.music.load('x_axis.mp3')
            mixer.music.play()
        elif current_control == 'y':
            mixer.music.load('y_axis.mp3')
            mixer.music.play()
        elif current_control == 'z':
            mixer.music.load('z_axis.mp3')
            mixer.music.play()
        else:
            mixer.music.load('gripper.mp3')
            mixer.music.play()
    if current_control == 'x':
        PygameButton(game_display, leg_x, (0, 255, 0), font, "", (255, 255, 255))
        PygameButton(game_display, leg_y, (0, 0, 0), font, "", (255, 255, 255))
        PygameButton(game_display, leg_z, (0, 0, 0), font, "", (255, 255, 255))
        PygameButton(game_display, leg_g, (0, 0, 0), font, "", (255, 255, 255))
        if current_class == 0:
            PygameButton(game_display, left_arm_x, (0, 0, 255), font, "    -", (255, 255, 255))
            PygameButton(game_display, right_arm_x, (0, 0, 255), font, "    +", (255, 255, 255))
            PygameButton(game_display, left_arm_y, (0, 0, 255), font, "    -", (255, 255, 255))
            PygameButton(game_display, right_arm_y, (0, 0, 255), font, "    +", (255, 255, 255))
            PygameButton(game_display, left_arm_z, (0, 0, 255), font, "    -", (255, 255, 255))
            PygameButton(game_display, right_arm_z, (0, 0, 255), font, "    +", (255, 255, 255))
            PygameButton(game_display, left_arm_g, (0, 0, 255), font, "    C", (255, 255, 255))
            PygameButton(game_display, right_arm_g, (0, 0, 255), font, "    O", (255, 255, 255))
        elif current_class == 1:
            PygameButton(game_display, left_arm_x, (0, 255, 0), font, "    -", (255, 255, 255))
            PygameButton(game_display, right_arm_x, (0, 0, 255), font, "    +", (255, 255, 255))
            PygameButton(game_display, left_arm_y, (0, 0, 255), font, "    -", (255, 255, 255))
            PygameButton(game_display, right_arm_y, (0, 0, 255), font, "    +", (255, 255, 255))
            PygameButton(game_display, left_arm_z, (0, 0, 255), font, "    -", (255, 255, 255))
            PygameButton(game_display, right_arm_z, (0, 0, 255), font, "    +", (255, 255, 255))
            PygameButton(game_display, left_arm_g, (0, 0, 255), font, "    C", (255, 255, 255))
            PygameButton(game_display, right_arm_g, (0, 0, 255), font, "    O", (255, 255, 255))
        elif current_class == 2:
            PygameButton(game_display, left_arm_x, (0, 0, 255), font, "    -", (255, 255, 255))
            PygameButton(game_display, right_arm_x, (0, 255, 0), font, "    +", (255, 255, 255))
            PygameButton(game_display, left_arm_y, (0, 0, 255), font, "    -", (255, 255, 255))
            PygameButton(game_display, right_arm_y, (0, 0, 255), font, "    +", (255, 255, 255))
            PygameButton(game_display, left_arm_z, (0, 0, 255), font, "    -", (255, 255, 255))
            PygameButton(game_display, right_arm_z, (0, 0, 255), font, "    +", (255, 255, 255))
            PygameButton(game_display, left_arm_g, (0, 0, 255), font, "    C", (255, 255, 255))
            PygameButton(game_display, right_arm_g, (0, 0, 255), font, "    O", (255, 255, 255))
        else:
            PygameButton(game_display, left_arm_x, (0, 0, 255), font, "    -", (255, 255, 255))
            PygameButton(game_display, right_arm_x, (0, 0, 255), font, "    +", (255, 255, 255))
            PygameButton(game_display, left_arm_y, (0, 0, 255), font, "    -", (255, 255, 255))
            PygameButton(game_display, right_arm_y, (0, 0, 255), font, "    +", (255, 255, 255))
            PygameButton(game_display, left_arm_z, (0, 0, 255), font, "    -", (255, 255, 255))
            PygameButton(game_display, right_arm_z, (0, 0, 255), font, "    +", (255, 255, 255))
            PygameButton(game_display, left_arm_g, (0, 0, 255), font, "    C", (255, 255, 255))
            PygameButton(game_display, right_arm_g, (0, 0, 255), font, "    O", (255, 255, 255))
    elif current_control == 'y':
        PygameButton(game_display, leg_x, (0, 0, 0), font, "", (255, 255, 255))
        PygameButton(game_display, leg_y, (0, 255, 0), font, "", (255, 255, 255))
        PygameButton(game_display, leg_z, (0, 0, 0), font, "", (255, 255, 255))
        PygameButton(game_display, leg_g, (0, 0, 0), font, "", (255, 255, 255))
        if current_class == 0:
            PygameButton(game_display, left_arm_x, (0, 0, 255), font, "    -", (255, 255, 255))
            PygameButton(game_display, right_arm_x, (0, 0, 255), font, "    +", (255, 255, 255))
            PygameButton(game_display, left_arm_y, (0, 0, 255), font, "    -", (255, 255, 255))
            PygameButton(game_display, right_arm_y, (0, 0, 255), font, "    +", (255, 255, 255))
            PygameButton(game_display, left_arm_z, (0, 0, 255), font, "    -", (255, 255, 255))
            PygameButton(game_display, right_arm_z, (0, 0, 255), font, "    +", (255, 255, 255))
            PygameButton(game_display, left_arm_g, (0, 0, 255), font, "    C", (255, 255, 255))
            PygameButton(game_display, right_arm_g, (0, 0, 255), font, "    O", (255, 255, 255))
        elif current_class == 1:
            PygameButton(game_display, left_arm_x, (0, 0, 255), font, "    -", (255, 255, 255))
            PygameButton(game_display, right_arm_x, (0, 0, 255), font, "    +", (255, 255, 255))
            PygameButton(game_display, left_arm_y, (0, 255, 0), font, "    -", (255, 255, 255))
            PygameButton(game_display, right_arm_y, (0, 0, 255), font, "    +", (255, 255, 255))
            PygameButton(game_display, left_arm_z, (0, 0, 255), font, "    -", (255, 255, 255))
            PygameButton(game_display, right_arm_z, (0, 0, 255), font, "    +", (255, 255, 255))
            PygameButton(game_display, left_arm_g, (0, 0, 255), font, "    C", (255, 255, 255))
            PygameButton(game_display, right_arm_g, (0, 0, 255), font, "    O", (255, 255, 255))
        elif current_class == 2:
            PygameButton(game_display, left_arm_x, (0, 0, 255), font, "    -", (255, 255, 255))
            PygameButton(game_display, right_arm_x, (0, 0, 255), font, "    +", (255, 255, 255))
            PygameButton(game_display, left_arm_y, (0, 0, 255), font, "    -", (255, 255, 255))
            PygameButton(game_display, right_arm_y, (0, 255, 0), font, "    +", (255, 255, 255))
            PygameButton(game_display, left_arm_z, (0, 0, 255), font, "    -", (255, 255, 255))
            PygameButton(game_display, right_arm_z, (0, 0, 255), font, "    +", (255, 255, 255))
            PygameButton(game_display, left_arm_g, (0, 0, 255), font, "    C", (255, 255, 255))
            PygameButton(game_display, right_arm_g, (0, 0, 255), font, "    O", (255, 255, 255))
        else:
            PygameButton(game_display, left_arm_x, (0, 0, 255), font, "    -", (255, 255, 255))
            PygameButton(game_display, right_arm_x, (0, 0, 255), font, "    +", (255, 255, 255))
            PygameButton(game_display, left_arm_y, (0, 0, 255), font, "    -", (255, 255, 255))
            PygameButton(game_display, right_arm_y, (0, 0, 255), font, "    +", (255, 255, 255))
            PygameButton(game_display, left_arm_z, (0, 0, 255), font, "    -", (255, 255, 255))
            PygameButton(game_display, right_arm_z, (0, 0, 255), font, "    +", (255, 255, 255))
            PygameButton(game_display, left_arm_g, (0, 0, 255), font, "    C", (255, 255, 255))
            PygameButton(game_display, right_arm_g, (0, 0, 255), font, "    O", (255, 255, 255))
    elif current_control == 'z':
        PygameButton(game_display, leg_x, (0, 0, 0), font, "", (255, 255, 255))
        PygameButton(game_display, leg_y, (0, 0, 0), font, "", (255, 255, 255))
        PygameButton(game_display, leg_z, (0, 255, 0), font, "", (255, 255, 255))
        PygameButton(game_display, leg_g, (0, 0, 0), font, "", (255, 255, 255))
        if current_class == 0:
            PygameButton(game_display, left_arm_x, (0, 0, 255), font, "    -", (255, 255, 255))
            PygameButton(game_display, right_arm_x, (0, 0, 255), font, "    +", (255, 255, 255))
            PygameButton(game_display, left_arm_y, (0, 0, 255), font, "    -", (255, 255, 255))
            PygameButton(game_display, right_arm_y, (0, 0, 255), font, "    +", (255, 255, 255))
            PygameButton(game_display, left_arm_z, (0, 0, 255), font, "    -", (255, 255, 255))
            PygameButton(game_display, right_arm_z, (0, 0, 255), font, "    +", (255, 255, 255))
            PygameButton(game_display, left_arm_g, (0, 0, 255), font, "    C", (255, 255, 255))
            PygameButton(game_display, right_arm_g, (0, 0, 255), font, "    O", (255, 255, 255))
        elif current_class == 1:
            PygameButton(game_display, left_arm_x, (0, 0, 255), font, "    -", (255, 255, 255))
            PygameButton(game_display, right_arm_x, (0, 0, 255), font, "    +", (255, 255, 255))
            PygameButton(game_display, left_arm_y, (0, 0, 255), font, "    -", (255, 255, 255))
            PygameButton(game_display, right_arm_y, (0, 0, 255), font, "    +", (255, 255, 255))
            PygameButton(game_display, left_arm_z, (0, 255, 0), font, "    -", (255, 255, 255))
            PygameButton(game_display, right_arm_z, (0, 0, 255), font, "    +", (255, 255, 255))
            PygameButton(game_display, left_arm_g, (0, 0, 255), font, "    C", (255, 255, 255))
            PygameButton(game_display, right_arm_g, (0, 0, 255), font, "    O", (255, 255, 255))
        elif current_class == 2:
            PygameButton(game_display, left_arm_x, (0, 0, 255), font, "    -", (255, 255, 255))
            PygameButton(game_display, right_arm_x, (0, 0, 255), font, "    +", (255, 255, 255))
            PygameButton(game_display, left_arm_y, (0, 0, 255), font, "    -", (255, 255, 255))
            PygameButton(game_display, right_arm_y, (0, 0, 255), font, "    +", (255, 255, 255))
            PygameButton(game_display, left_arm_z, (0, 0, 255), font, "    -", (255, 255, 255))
            PygameButton(game_display, right_arm_z, (0, 255, 0), font, "    +", (255, 255, 255))
            PygameButton(game_display, left_arm_g, (0, 0, 255), font, "    C", (255, 255, 255))
            PygameButton(game_display, right_arm_g, (0, 0, 255), font, "    O", (255, 255, 255))
        else:
            PygameButton(game_display, left_arm_x, (0, 0, 255), font, "    -", (255, 255, 255))
            PygameButton(game_display, right_arm_x, (0, 0, 255), font, "    +", (255, 255, 255))
            PygameButton(game_display, left_arm_y, (0, 0, 255), font, "    -", (255, 255, 255))
            PygameButton(game_display, right_arm_y, (0, 0, 255), font, "    +", (255, 255, 255))
            PygameButton(game_display, left_arm_z, (0, 0, 255), font, "    -", (255, 255, 255))
            PygameButton(game_display, right_arm_z, (0, 0, 255), font, "    +", (255, 255, 255))
            PygameButton(game_display, left_arm_g, (0, 0, 255), font, "    C", (255, 255, 255))
            PygameButton(game_display, right_arm_g, (0, 0, 255), font, "    O", (255, 255, 255))
    elif current_control == 'g':
        PygameButton(game_display, leg_x, (0, 0, 0), font, "", (255, 255, 255))
        PygameButton(game_display, leg_y, (0, 0, 0), font, "", (255, 255, 255))
        PygameButton(game_display, leg_z, (0, 0, 0), font, "", (255, 255, 255))
        PygameButton(game_display, leg_g, (0, 255, 0), font, "", (255, 255, 255))
        if current_class == 0:
            PygameButton(game_display, left_arm_x, (0, 0, 255), font, "    -", (255, 255, 255))
            PygameButton(game_display, right_arm_x, (0, 0, 255), font, "    +", (255, 255, 255))
            PygameButton(game_display, left_arm_y, (0, 0, 255), font, "    -", (255, 255, 255))
            PygameButton(game_display, right_arm_y, (0, 0, 255), font, "    +", (255, 255, 255))
            PygameButton(game_display, left_arm_z, (0, 0, 255), font, "    -", (255, 255, 255))
            PygameButton(game_display, right_arm_z, (0, 0, 255), font, "    +", (255, 255, 255))
            PygameButton(game_display, left_arm_g, (0, 0, 255), font, "    C", (255, 255, 255))
            PygameButton(game_display, right_arm_g, (0, 0, 255), font, "    O", (255, 255, 255))
        elif current_class == 1:
            PygameButton(game_display, left_arm_x, (0, 0, 255), font, "    -", (255, 255, 255))
            PygameButton(game_display, right_arm_x, (0, 0, 255), font, "    +", (255, 255, 255))
            PygameButton(game_display, left_arm_y, (0, 0, 255), font, "    -", (255, 255, 255))
            PygameButton(game_display, right_arm_y, (0, 0, 255), font, "    +", (255, 255, 255))
            PygameButton(game_display, left_arm_z, (0, 0, 255), font, "    -", (255, 255, 255))
            PygameButton(game_display, right_arm_z, (0, 0, 255), font, "    +", (255, 255, 255))
            PygameButton(game_display, left_arm_g, (0, 255, 0), font, "    C", (255, 255, 255))
            PygameButton(game_display, right_arm_g, (0, 0, 255), font, "    O", (255, 255, 255))
        elif current_class == 2:
            PygameButton(game_display, left_arm_x, (0, 0, 255), font, "    -", (255, 255, 255))
            PygameButton(game_display, right_arm_x, (0, 0, 255), font, "    +", (255, 255, 255))
            PygameButton(game_display, left_arm_y, (0, 0, 255), font, "    -", (255, 255, 255))
            PygameButton(game_display, right_arm_y, (0, 0, 255), font, "    +", (255, 255, 255))
            PygameButton(game_display, left_arm_z, (0, 0, 255), font, "    -", (255, 255, 255))
            PygameButton(game_display, right_arm_z, (0, 0, 255), font, "    +", (255, 255, 255))
            PygameButton(game_display, left_arm_g, (0, 0, 255), font, "    C", (255, 255, 255))
            PygameButton(game_display, right_arm_g, (0, 255, 0), font, "    O", (255, 255, 255))
        else:
            PygameButton(game_display, left_arm_x, (0, 0, 255), font, "    -", (255, 255, 255))
            PygameButton(game_display, right_arm_x, (0, 0, 255), font, "    +", (255, 255, 255))
            PygameButton(game_display, left_arm_y, (0, 0, 255), font, "    -", (255, 255, 255))
            PygameButton(game_display, right_arm_y, (0, 0, 255), font, "    +", (255, 255, 255))
            PygameButton(game_display, left_arm_z, (0, 0, 255), font, "    -", (255, 255, 255))
            PygameButton(game_display, right_arm_z, (0, 0, 255), font, "    +", (255, 255, 255))
            PygameButton(game_display, left_arm_g, (0, 0, 255), font, "    C", (255, 255, 255))
            PygameButton(game_display, right_arm_g, (0, 0, 255), font, "    O", (255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            if finish_button.is_pushed():
                crashed = True
    pygame.display.update()
    clock.tick(30)
    if current_class == 1:
        ur.move_backward(current_control)
    elif current_class == 2:
        ur.move_forward(current_control)
    recent_data = prp.fit_test(bci.get_recent_data(rows_per_epoch))
    current_class = clf.predict(recent_data)
pygame.quit()
try:
    delete_module("mainInterface")
    import mainInterface
except:
    import mainInterface