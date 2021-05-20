from scipy.ndimage import gaussian_filter
import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage.measurements import label
# a = [[0.8040218227309112, 1.8712801651400723, 2.4606905782074238], [0.8040218227309112, 1.8712801651400723, 2.4606905782074238], [0.8040218227309112, 1.8712801651400723, 2.4606905782074238], [0.8040218227309112, 1.8712801651400723, 2.4606905782074238], [0.8040218227309112, 1.8712801651400723, 2.4606905782074238], [0.8040218227309112, 1.8712801651400723, 2.4606905782074238], [0.8040218227309112,
#                                                                                                                                                                                                                                                                                                                                                                                           1.8712801651400723, 2.4606905782074238], [0.8040218227309112, 1.8712801651400723, 2.4606905782074238], [0.7930321869900006, 1.7079726660218904, 3.068526454665988], [0.7930321869900006, 1.7079726660218904, 3.068526454665988], [0.7930321869900006, 1.7079726660218904, 3.068526454665988], [0.7930321869900006, 1.7079726660218904, 3.068526454665988], [0.7930321869900006, 1.7079726660218904, 3.068526454665988]]
a = [3.34, 2.97]
gaus_a = gaussian_filter(a, 3)

a_mean = np.mean(a)
gaus_a_mean = np.mean(gaus_a)
print(f"original > {a} \n gaus >{list(gaus_a)} \n mean a > {a_mean} \n gaus mean > {gaus_a_mean}")
plt.plot(gaus_a, label= "gaus")
plt.plot(a, label= "original")
plt.legend()
plt.show()