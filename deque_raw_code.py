import collections
from scipy.ndimage import gaussian_filter
from uwb_subscriber import MqttSubscriber
import time
mqttSubscriber = MqttSubscriber("localhost", topic="top")
mqttSubscriber.start()

sample_list = []
deque_x = collections.deque([])
deque_y = collections.deque([])
deque_z = collections.deque([])
while len(deque_x)<15:  # 15 was nice
    a = mqttSubscriber.pos
    if a == []:
        time.sleep(0.5)
    time.sleep(0.08)  # 0.08 is fine
    if a:
        deque_x.appendleft(a[0])  # works
        deque_y.appendleft(a[1])
        deque_z.appendleft(a[2])


        x_gaus = gaussian_filter(deque_x, 5)
        y_gaus = gaussian_filter(deque_y, 5)
        z_gaus = gaussian_filter(deque_z, 5)

        deque_x_gaus = collections.deque(x_gaus)
        deque_y_gaus = collections.deque(y_gaus)
        deque_z_gaus = collections.deque(z_gaus)
        # print(f"gaus>>{deque_x_gaus}")
        # print(f"original>>{deque_x}")
        if len(deque_x_gaus)==15:
            deque_x.pop()
            deque_y.pop()
            deque_z.pop()
            final_pos = [deque_x_gaus.pop(), deque_y_gaus.pop(), deque_z_gaus.pop()]
            # print(deque_x_gaus.pop())
            print(final_pos)

# print(deque_x)
# mqttSubscriber.stop()
# data_list = []
# my_deque = collections.deque(data_list)

# my_deque.append(1.3)
# my_deque.append(3.5)
# my_deque.append(1.1)
# print(my_deque)
# gaus_deque = gaussian_filter(my_deque, 3)
# print(gaus_deque)