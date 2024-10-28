SensorParams = {'R10482340' : [-4.06298468e-04,  2.19415590e+00]}

#### Script to calculate sensor parameters, uncoment to use
##
##import numpy as np
##import pandas as pd
##import matplotlib.pyplot as plt
##
##
##df=pd.read_csv('R10482340.csv')
##
##R=10**df['Units']
##T=np.log10(df['Temp'])
##T1=T[-2:].to_numpy()
##R1=R[-2:].to_numpy()
##T2=np.concatenate((T1,np.log10([0.006, 0.005, 0.004, 0.003, 0.002, 0.001])))
##
##p=np.polyfit(R1, T1, 1)
##
##plt.plot(R1, T1, 'xk', label='Calibration data')
##plt.plot(np.linspace(R1[0], 13000), np.polyval(p, np.linspace(R1[0], 13000)),  label='Linear extrapolation')
##plt.ylabel('T (log K)')
##plt.xlabel('R (Ohm)')
##plt.title('Calibration curve for the tmixing sensor (R10482340)')
##plt.legend()
##plt.show()
##
##print(f"'SensorName' : {[p[0], p[1]]}")  ### parameters for the dict
