import random
import time

class PredefinedUpdater:

    def __init__(self, variant):
        if variant == 1:
            self.class_list = [2,2,2,2,1,2, #vpered
                               3,2,2,2,1,2,2,2,2,2,2,2,1,2,2, #vlevo
                               3,1,1,2,1,1,2,1,1,1,1,1, #vniz
                               3,2, #zahvat
                               3,2,2,1,2,2,2,1,2,2, #vverh
                               3,1,1,1,2,1,1,1,1,1,1,2,1,1,1,1,2,1,1,1,1, #vpravo
                               3,1,1,1,1,2,1,1,1,1,1,1,1, #nazad
                               3,1,1,1,2,1,1,1,1,1, #vpravo
                               3,1,1,1,1,1,1, #vniz
                               3,1, #otkryt'
                               3,2,2,2,2,2,2,2]
        self.index = -1
        self.last_action_is_motion = False


    def get_next(self):
        if self.last_action_is_motion:
            self.last_action_is_motion = False
            return 0
        self.last_action_is_motion = True
        time.sleep(random.randint(1, 5))
        # time.sleep(1)
        self.index += 1
        return self.class_list[self.index]
