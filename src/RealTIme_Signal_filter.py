import collections
from collections import Counter
from scipy.ndimage import gaussian_filter
from uwb_subscriber import MqttSubscriber
import time
import numpy as np
# mqttSubscriber = MqttSubscriber("localhost", topic="top")
# mqttSubscriber.start()


class Signal_filter():
    def __init__(self):
        self.sample_size = None
        self.sigma = None
        self.deque_x = collections.deque([])
        self.deque_y = collections.deque([])
        self.deque_z = collections.deque([])
        self.final_pos = []
        self.mqttSubscriber = MqttSubscriber("localhost", topic="top")
        self.mqttSubscriber.start()

    def my_mode(self, sample):
        c = Counter(sample)
        return [k for k, v in c.items() if v == c.most_common(1)[0][1]]

    def plus_minus(self):
        value = np.random.random(1)[0]
        if value > 0.5:
            return 1
        return -1

    def mqtt_callback(self):
        raw_pos = self.mqttSubscriber.pos
        if raw_pos == []:
            time.sleep(0.5)
        time.sleep(0.08)
        return raw_pos

    def lauch_gauss_filter(self, sample_size, sigma):
        self.sample_size = sample_size
        self.sigma = sigma
        while len(self.deque_x) < self.sample_size:  # 15 was nice
            raw_pos = self.mqtt_callback()
            if raw_pos:
                self.deque_x.appendleft(raw_pos[0])  # works
                self.deque_y.appendleft(raw_pos[1])
                self.deque_z.appendleft(raw_pos[2])

                x_gaus = gaussian_filter(self.deque_x, self.sigma)
                y_gaus = gaussian_filter(self.deque_y, self.sigma)
                z_gaus = gaussian_filter(self.deque_z, self.sigma)

                deque_x_gaus = collections.deque(x_gaus)
                deque_y_gaus = collections.deque(y_gaus)
                deque_z_gaus = collections.deque(z_gaus)

                if len(deque_x_gaus) == self.sample_size:
                    self.deque_x.pop()
                    self.deque_y.pop()
                    self.deque_z.pop()
                    self.final_pos = [
                        deque_x_gaus.pop(), deque_y_gaus.pop(), deque_z_gaus.pop()]
                    return self.final_pos

    def lauch_mode_filter(self, sample_size):
        self.sample_size = sample_size
        while len(self.deque_x) < self.sample_size:
            raw_pos = self.mqtt_callback()
            if raw_pos:
                self.deque_x.appendleft(np.round(raw_pos[0], 2))
                self.deque_y.appendleft(np.round(raw_pos[1], 2))
                self.deque_z.appendleft(np.round(raw_pos[2], 2))

                x_mode = self.my_mode(self.deque_x)
                y_mode = self.my_mode(self.deque_y)
                z_mode = self.my_mode(self.deque_z)

                if len(self.deque_x) == self.sample_size:
                    self.deque_x.pop()
                    self.deque_y.pop()
                    self.deque_z.pop()
                    self.final_pos = [
                        np.mean(x_mode, axis=0), np.mean(y_mode, axis=0), np.mean(z_mode, axis=0)]
                    return self.final_pos

    def lauch_std_filter(self, sample_size, std_multiplier=1):
        self.sample_size = sample_size
        self.unlock = True
        self.pop_x = None
        self.pop_y = None
        self.pop_z = None
        while len(self.deque_x) < self.sample_size:  # 15 was nice
            raw_pos = self.mqtt_callback()
            if raw_pos:
                while len(self.deque_x) != self.sample_size-1 and self.unlock:
                    raw_pos_while = self.mqtt_callback()
                    self.deque_x.appendleft(raw_pos_while[0])
                    self.deque_y.appendleft(raw_pos_while[1])
                    self.deque_z.appendleft(raw_pos_while[2])
                self.unlock = False

                "getting first mean and std"
                self.mean_xyz = [np.mean(self.deque_x), np.mean(
                    self.deque_y), np.mean(self.deque_z)]

                self.std_xyz = [np.std(self.deque_x), np.std(
                    self.deque_y), np.std(self.deque_z)]

                "xyz standard deviation checker"
                # x
                if (self.mean_xyz[0]-std_multiplier*self.std_xyz[0]) < (raw_pos[0]) < (self.mean_xyz[0]+std_multiplier*self.std_xyz[0]):
                    self.deque_x.appendleft(raw_pos[0])
                else:
                    # continue
                    self.deque_x.appendleft(
                        np.mean(self.deque_x)+self.plus_minus()*np.std(self.deque_x))

                # y
                if (self.mean_xyz[1]-std_multiplier*self.std_xyz[1]) < (raw_pos[1]) < (self.mean_xyz[1]+std_multiplier*self.std_xyz[1]):
                    self.deque_y.appendleft(raw_pos[1])
                else:
                    self.deque_y.appendleft(
                        np.mean(self.deque_y)+self.plus_minus()*np.std(self.deque_y))

                # z
                if (self.mean_xyz[2]-std_multiplier*self.std_xyz[2]) < (raw_pos[2]) < (self.mean_xyz[2]+std_multiplier*self.std_xyz[2]):
                    self.deque_z.appendleft(raw_pos[2])
                else:
                    self.deque_z.appendleft(
                        np.mean(self.deque_z)+self.plus_minus()*np.std(self.deque_z))

                "popping"
                if len(self.deque_x) == self.sample_size:
                    self.pop_x = self.deque_x.pop()

                if len(self.deque_y) == self.sample_size:
                    self.pop_y = self.deque_y.pop()

                if len(self.deque_z) == self.sample_size:
                    self.pop_z = self.deque_z.pop()

                "final list"
                self.final_pos = [
                    self.pop_x,
                    self.pop_y,
                    self.pop_z
                ]
                return self.final_pos


if __name__ == "__main__":
    test = Signal_filter()
    while True:
        print(test.lauch_std_filter(15, 1))
        # print(test.lauch_gauss_filter(15, 5))
        # print(test.lauch_mode_filter(15))
