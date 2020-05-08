import numpy as np

a = (2,3)
b = []
b = np.array(b)
b = np.append(b,np.array(a),axis=0)
print(b)
print(np.append(b,[a]))