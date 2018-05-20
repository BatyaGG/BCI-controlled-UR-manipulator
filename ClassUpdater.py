import numpy as np

class ClassUpdater:
    def __init__(self, num_of_classes):
        self.classes = np.arange(num_of_classes)[1:]
        self.current = 1
        self.current_index = 0


    def get_next(self):
        if self.current == 0:
            self.current = self.classes[self.current_index]
            if self.current_index < self.classes.size - 1:
                self.current_index += 1
            else:
                self.current_index = 0
                np.random.shuffle(self.classes)
        else:
            self.current = 0
        return self.current
