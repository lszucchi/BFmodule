SensorParams = {'R10482340' : [-5.83,4.07036]}

#### Script to calculate sensor parameters, uncoment to use

##import numpy as np
##import pandas as pd
##import matplotlib.pyplot as plt
##
##df=pd.read_csv('R10482.340.csv')
##
##R=df['Units']
##T=df['Temperature']
##T1=T[-2:]
##R1=R[-2:]
##T2=np.concatenate((T1,[0.006, 0.005, 0.004, 0.003, 0.002, 0.001, 0]))
##
##p=np.polyfit(T1, R1, 1)
##
##plt.plot(T1, R1, 'xk')
##plt.plot(T2, np.polyval(p, T2))
##plt.show()
