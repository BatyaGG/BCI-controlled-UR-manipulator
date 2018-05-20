import time


class ControlUpdater:
    def __init__(self, variants, delay=3):
        self.variants = variants
        self.length = len(variants)
        self.index = -1
        self.asc = True
        self.delay = delay
        self.last_access = time.time() - delay

    def get_next(self):
        if time.time() - self.last_access < self.delay: return self.variants[self.index]
        if self.asc: self.index += 1
        else: self.index -= 1
        if self.index > self.length - 2: self.asc = False
        elif self.index < 1: self.asc = True
        self.last_access = time.time()
        return self.variants[self.index]

if __name__ == "__main__":
    var = ['l', 'r', 'leg', 'dig']
    CU = ControlUpdater(var)
    for i in range(15):
        print(CU.get_next())
