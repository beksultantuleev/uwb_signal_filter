import collections
from scipy.ndimage import gaussian_filter
from uwb_subscriber import MqttSubscriber
import time
# mqttSubscriber = MqttSubscriber("localhost", topic="top")
# mqttSubscriber.start()


class Gaussian_filter():
    def __init__(self, sample_size=15, sigma=5):
        self.sample_size = sample_size
        self.sigma = sigma
        self.deque_x = collections.deque([])
        self.deque_y = collections.deque([])
        self.deque_z = collections.deque([])
        self.final_pos = []
        self.mqttSubscriber = MqttSubscriber("localhost", topic="top")
        self.mqttSubscriber.start()

    def lauch_gauss_filter(self):
        while len(self.deque_x) < self.sample_size:  # 15 was nice
            a = self.mqttSubscriber.pos
            if a == []:
                time.sleep(0.5)
            time.sleep(0.08)  # 0.08 is fine
            if a:
                self.deque_x.appendleft(a[0])  # works
                self.deque_y.appendleft(a[1])
                self.deque_z.appendleft(a[2])

                x_gaus = gaussian_filter(self.deque_x, self.sigma)
                y_gaus = gaussian_filter(self.deque_y, self.sigma)
                z_gaus = gaussian_filter(self.deque_z, self.sigma)

                deque_x_gaus = collections.deque(x_gaus)
                deque_y_gaus = collections.deque(y_gaus)
                deque_z_gaus = collections.deque(z_gaus)

                if len(deque_x_gaus) == 15:
                    self.deque_x.pop()
                    self.deque_y.pop()
                    self.deque_z.pop()
                    self.final_pos = [
                        deque_x_gaus.pop(), deque_y_gaus.pop(), deque_z_gaus.pop()]
                    return self.final_pos


if __name__ == "__main__":
    test = Gaussian_filter()
    while True:
        print(test.lauch_gauss_filter())


