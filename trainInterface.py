import time
import pickle
import datetime
import os
import pygame
from BCI import BCI
from deleteModule import delete_module
from PygameButton import PygameButton
from ClassUpdater import ClassUpdater
from BatyaGGPreprocessor import BatyaGGPreprocessor
from BatyaGGClassifier import BatyaGGClassifier

pygame.init()
game_display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
info_object = pygame.display.Info()
width = info_object.current_w
height = info_object.current_h
pygame.display.set_caption("Train frame")
clock = pygame.time.Clock()
left_arm_position = (0.2*width, 0.3*height, 0.1*width, 0.1*height)
right_arm_position = (0.7*width, 0.3*height, 0.1*width, 0.1*height)
legs_position = (0.45*width, 0.6*height, 0.1*width, 0.1*height)
pause_button_position = (0.05*width, 0.9*height, 0.1*width, 0.05*height)
finish_button_position = (0.85*width, 0.9*height, 0.1*width, 0.05*height)
font = pygame.font.SysFont('Comic Sans MS', 30)
PygameButton(game_display, left_arm_position, (0, 0, 255), font, "Left Hand", (255, 255, 255))
PygameButton(game_display, right_arm_position, (0, 0, 255), font, "Right Hand", (255, 255, 255))
PygameButton(game_display, legs_position, (0, 0, 255), font, "Legs", (255, 255, 255))
pause_button = PygameButton(game_display, pause_button_position, (255, 0, 0), font, "Pause", (255, 255, 255))
finish_button = PygameButton(game_display, finish_button_position, (255, 0, 0), font, "Finish", (255, 255, 255))
crashed = False
# home = False

class_updater = ClassUpdater(4)
current_class = class_updater.get_next()
window_duration = 1000
bci = BCI()
start_time = time.time()

while not crashed:
    if current_class == 0:
        PygameButton(game_display, left_arm_position, (0, 0, 255), font, "Left Hand", (255, 255, 255))
        PygameButton(game_display, right_arm_position, (0, 0, 255), font, "Right Hand", (255, 255, 255))
        PygameButton(game_display, legs_position, (0, 0, 255), font, "Legs", (255, 255, 255))
    elif current_class == 1:
        PygameButton(game_display, left_arm_position, (0, 255, 0), font, "Left Hand", (255, 255, 255))
        PygameButton(game_display, right_arm_position, (0, 0, 255), font, "Right Hand", (255, 255, 255))
        PygameButton(game_display, legs_position, (0, 0, 255), font, "Legs", (255, 255, 255))
    elif current_class == 2:
        PygameButton(game_display, left_arm_position, (0, 0, 255), font, "Left Hand", (255, 255, 255))
        PygameButton(game_display, right_arm_position, (0, 255, 0), font, "Right Hand", (255, 255, 255))
        PygameButton(game_display, legs_position, (0, 0, 255), font, "Legs", (255, 255, 255))
    elif current_class == 3:
        PygameButton(game_display, left_arm_position, (0, 0, 255), font, "Left Hand", (255, 255, 255))
        PygameButton(game_display, right_arm_position, (0, 0, 255), font, "Right Hand", (255, 255, 255))
        PygameButton(game_display, legs_position, (0, 255, 0), font, "Legs", (255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            if pause_button.is_pushed():
                bci.set_new_class(None)
                continue_button = PygameButton(game_display, pause_button_position, (255, 0, 0), font,
                                               "Continue", (255, 255, 255))
                pygame.display.update()
                pause = True
                while pause:
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONUP:
                            if continue_button.is_pushed():
                                pause = False
                pause_button = PygameButton(game_display, pause_button_position, (255, 0, 0), font, "Pause",
                                            (255, 255, 255))
                pygame.display.update()
                bci.restart()
                start_time = time.time()
                continue
            if finish_button.is_pushed():
                bci.set_new_class(None)
                crashed = True
                # home = True
    pygame.display.update()
    clock.tick(30)
    if (time.time() - start_time) * 1000 >= window_duration:
        bci.set_new_class(current_class)
        current_class = class_updater.get_next()
        start_time = time.time()

data_x, data_y = bci.get_data()
date_time = datetime.datetime.now().strftime("%b_%d_%Y_%H%M")
directory = date_time
if not os.path.exists(directory):
    os.makedirs(directory)
data = {'X': data_x, 'Y': data_y}
with open(directory + "/Data.pickle", 'wb') as handle:
    pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
preprocessor = BatyaGGPreprocessor(data_x.shape[0], bands=[8, 28])
data_x, data_y = preprocessor.fit_train(data_x, data_y)
clf = BatyaGGClassifier(zero_thresh=0.4)
clf.fit(data_x, data_y)
results_position = (0.2*width, 0.4*height, 0.6*width, 0.1*height)
with open(directory + "/Model.pickle", 'wb') as handle:
    pickle.dump(clf, handle, protocol=pickle.HIGHEST_PROTOCOL)
accur = clf.score(data_x, data_y);
print "Accuracy: "+ str(accur);
PygameButton(game_display, results_position, (0, 0, 0), font, "Accuracy: " + str(accur), (255, 255, 255))
time.sleep(1)
pygame.display.update()
time.sleep(10)
pygame.quit()
try:
    delete_module("mainInterface")
    import mainInterface
except:
    import mainInterface