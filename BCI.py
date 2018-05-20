import sys
import time
import socket
import numpy as np
from FieldTrip import Client


class BCI:
    def __init__(self, hostname='localhost', port=1972, n_channels=16, window_delay=50):
        self.client = Client()
        self.n_channels = n_channels
        self.data_x = np.zeros((0, n_channels))
        self.data_y = []
        while not self.client.isConnected:
            try:
                self.client.connect(hostname, port)
            except socket.error:
                print("Failed to connect at " + hostname + ":" + str(port))
                time.sleep(1)
        self.buffer_start_index = self.client.poll()[0]
        self.transition_indexes = [self.client.poll()[0] - self.buffer_start_index]
        self.transition_classes = []
        self.min_rows_per_chunk = sys.float_info.max
        self.window_delay = window_delay

    def set_new_class(self, new_class):
        poll = self.client.poll()[0]
        self.transition_indexes += [poll - self.buffer_start_index]
        self.transition_classes += [new_class]
        if poll - self.buffer_start_index > 100000 or new_class is None:
            self.transition_indexes = self.transition_indexes[:-1]
            self.transition_classes = self.transition_classes[:-1]
            try:
                self.data_x = np.vstack((self.data_x, self.client.getData([self.buffer_start_index + self.window_delay,
                                                                           self.buffer_start_index +
                                                                           self.transition_indexes[-1] +
                                                                           self.window_delay])))
            except:
                time.sleep(1)
                self.data_x = np.vstack((self.data_x, self.client.getData([self.buffer_start_index + self.window_delay,
                                                                           self.buffer_start_index + 1 +
                                                                           self.transition_indexes[-1] +
                                                                           self.window_delay])))
            transition_indexes = [cur - prev for cur, prev in
                                  zip(self.transition_indexes[::-1], self.transition_indexes[::-1][1:])][::-1]
            min_rows_per_chunk = int(np.median(transition_indexes))
            if min_rows_per_chunk < self.min_rows_per_chunk: self.min_rows_per_chunk = min_rows_per_chunk
            data_y = [[val] * ind for val, ind in zip(self.transition_classes, transition_indexes)]
            self.data_y += [item for sublist in data_y for item in sublist]
            self.buffer_start_index = self.client.poll()[0]
            self.transition_indexes = [self.client.poll()[0] - self.buffer_start_index]
            self.transition_classes = []

    def restart(self):
        self.buffer_start_index = self.client.poll()[0]
        self.transition_indexes = [self.client.poll()[0] - self.buffer_start_index]
        self.transition_classes = []

    def get_data(self):
        segmented_x, segmented_y = self._segmentate(self.data_x, self.data_y, self.min_rows_per_chunk)
        return segmented_x, np.array(segmented_y)

    def get_recent_data(self, n_samples):
        last_sample_index = self.client.poll()[0]
        return self.client.getData([last_sample_index - n_samples, last_sample_index - 1]).reshape(n_samples, self.n_channels, 1)

    def _segmentate(self, data_x, data_y, rows_per_obs):
        cur_row = 0
        new_x = np.zeros((rows_per_obs, data_x.shape[1], 0))
        new_y = []
        while data_x.shape[0] - cur_row >= rows_per_obs:
            current_class = [data_y[cur_row]]
            current_window = np.zeros((0, data_x.shape[1]))
            counter = 0
            while counter < rows_per_obs and data_y[cur_row] == current_class[0]:
                current_window = np.vstack((current_window, data_x[cur_row, :].reshape((1, data_x.shape[1]))))
                cur_row += 1
                counter += 1
            if counter < rows_per_obs:
                current_window = np.zeros((rows_per_obs, data_x.shape[1], 0))
                current_class = []
            new_x = np.dstack((new_x, current_window))
            new_y += current_class
        return new_x, new_y

# if __name__ == '__main__':
#     bci = BCI()
#     print bci.get_recent_data(300).shape