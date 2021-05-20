import collections
from nodes import my_mode
from scipy.ndimage import gaussian_filter
from uwb_subscriber import MqttSubscriber
import time
from collections import Counter
import numpy as np


class Mode_realtime_filter():
    def __init__(self, sample_size=15, sigma=5):
        self.sample_size = sample_size
        self.sigma = sigma
        self.deque_x = collections.deque([])
        self.deque_y = collections.deque([])
        self.deque_z = collections.deque([])
        self.final_pos = []
        self.mqttSubscriber = MqttSubscriber("localhost", topic="top")
        self.mqttSubscriber.start()
    
    def my_mode(self, sample):
        c = Counter(sample)
        return [k for k, v in c.items() if v == c.most_common(1)[0][1]]
    
    def lauch_mode_filter(self):
        while len(self.deque_x) < self.sample_size:  # 15 was nice
            a = self.mqttSubscriber.pos
            if a == []:
                time.sleep(0.5)
            time.sleep(0.08)  # 0.08 is fine
            if a:
                self.deque_x.appendleft(np.round(a[0], 2))  # works
                self.deque_y.appendleft(np.round(a[1], 2))
                self.deque_z.appendleft(np.round(a[2], 2))

                x_mode = self.my_mode(self.deque_x)
                y_mode = self.my_mode(self.deque_y)
                z_mode = self.my_mode(self.deque_z)


                if len(self.deque_x) == 15:
                    self.deque_x.pop()
                    self.deque_y.pop()
                    self.deque_z.pop()
                    self.final_pos = [
                        np.mean(x_mode, axis=0), np.mean(y_mode, axis=0), np.mean(z_mode, axis=0)]
                    return self.final_pos


if __name__ == "__main__":
    test = Mode_realtime_filter()
    while True:
        print(test.lauch_mode_filter())


