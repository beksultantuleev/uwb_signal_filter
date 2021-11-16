import numpy as np
from collections import Counter

from uwb_subscriber import MqttSubscriber
import time

class Mode_sample_filter():
    def __init__(self, sample_number, host, topic):
        self.sample_number = sample_number
        self.sample_list = []
        self.x_list = []
        self.y_list = []
        self.z_list = []
        self.host = host
        self.topic = topic
        self.mqttSubscriber = MqttSubscriber(self.host, topic=self.topic)
        self.mqttSubscriber.start()

    def my_mode(self, sample):
        c = Counter(sample)
        return [k for k, v in c.items() if v == c.most_common(1)[0][1]]
    
    def populate_sample_list(self):
        for i in range(self.sample_number):  # 15 was nice
            a = self.mqttSubscriber.pos
            if a == []:
                time.sleep(0.5)
            time.sleep(0.08)  # 0.08 is fine
            if a:
                self.sample_list.append(a)  # works

    def mode_filter(self):
        self.populate_sample_list()
        self.mqttSubscriber.stop()

        for i in self.sample_list:
            self.x_list.append(np.round(i[0], 2))
            self.y_list.append(np.round(i[1], 2))
            self.z_list.append(np.round(i[2], 2))
       
        self.get_filtered_position()
    
    def get_filtered_position(self):
        "avg mode value"
        filtered_x = np.mean(self.my_mode(self.x_list), axis=0)
        filtered_y = np.mean(self.my_mode(self.y_list), axis=0)
        filtered_z = np.mean(self.my_mode(self.z_list), axis=0)
        return [filtered_x, filtered_y, filtered_z]
    
    def get_mode_list(self):
        mode_x = self.my_mode(self.x_list)
        mode_y = self.my_mode(self.y_list)
        mode_z = self.my_mode(self.z_list)
        print(f"mode x > {mode_x} \n mode y > {mode_y} \n mode z > {mode_z}")

    def get_raw_list(self):
        raw_x = self.x_list
        raw_y = self.y_list
        raw_z = self.z_list
        print(f"raw x > {raw_x} \n raw y > {raw_y} \n raw z > {raw_z}")


if __name__ == '__main__':
    test = Mode_sample_filter(20, "localhost", "top")
    test.mode_filter()
    print(test.get_filtered_position())
    test.get_raw_list()
    "test"
    