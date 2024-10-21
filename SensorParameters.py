SensorParams = {'R10482340' : [-0.17152658662092587, 0.698174957118352]}

#### Script to calculate sensor parameters, uncoment to use
##
##import numpy as np
##import pandas as pd
##import matplotlib.pyplot as plt
##
##
##df=pd.read_csv('R10482.340.csv')
##
##R=df['Units']
##T=df['Temperature']
##T1=T[-2:].to_numpy()
##R1=R[-2:].to_numpy()
##T2=np.concatenate((T1,[0.006, 0.005, 0.004, 0.003, 0.002, 0.001, 0]))
##
##p=np.polyfit(R1, T1, 1)
##
##plt.plot(R1, T1*1e3, 'xk', label='Calibration data')
##plt.plot(np.linspace(-p[1]/p[0], R1[0]), np.polyval(p, np.linspace(-p[1]/p[0], R1[0]))*1e3, label='Linear extrapolation')
##plt.ylabel('Temperature (mK)')
##plt.xlabel('Units (Log Ohm)')
##plt.title('Calibration curve for the tmixing sensor (R10482340)')
##plt.legend()
##plt.show()
##
##print(f"'SensorName' : {[p[0], p[1]]}")  ### parameters for the dict
