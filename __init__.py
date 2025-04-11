import requests, json, sys, numpy
from .DeviceParameters import DEVICE_IP, PORT, ApiKey
from .SensorParameters import SensorParams

TCHANNELS = ['', 't50k', 't4k', 'tmagnet', '', 'tstill', 'tmixing', '', 'tfse']
SENSORNAME = ['', '', '', '', '', '', 'R10482340', '', '']
PCHANNELS = ["can", "p2", "p3", "p4", "tank", "p6"]

class DR:

    def __init__(self, ADDR=DEVICE_IP, timeout=10):
        print(f"Opening API at {ADDR}")
        req=requests.get(f'https://{ADDR}:{PORT}/system?key={ApiKey}', timeout=timeout)
        if req.status_code==200:
            self.DEVICE_IP=DEVICE_IP
            self.PORT=PORT
            self.ApiKey=ApiKey
            self.timeout=timeout
            print(req.json()['data']['system_name'], req.json()['data']['system_version'])
        else:
            raise f"Initial HTTP request failed. Status Code:{req.stats_code}"

    def Help(self, Func=''):
        
        methods_list = [method for method in vars(DR) if callable(
                getattr(DR, method)) and not method.startswith("__")]
        
        if Func not in methods_list[1:]:
            if Func!='' and Func!='Help':
                print("Invalid Method")

            methods_list = [method for method in vars(DR) if callable(
                getattr(DR, method)) and not method.startswith("__")]

            print("Help(str method). Returns info on method")
            print("Methods:", methods_list)
            return 0
        
        FuncHelp = {
            'Get': "Get(str node). Return HTTP get data in Node (dict)", 

            'Post': "Post(str node, dict data). HTTP post data in Node",

            'Idn': "Idn(). Return system ID and version (str tuple)",

            'GetT': "GetT(str Name). Return temperature (float or nan) for Name",

            'GetTCh': "GetTCh(str n). Return temperature (float or nan)  for Channel n",

            'GetPCh': "GetPCh(str n). Return pressure (float or nan) for Channel n",

            'GetAirPressOk': "GetAirPressOk(). Return compressed air pressure ok (bool)",

            'GetFlow': "GetFlow(). Return He Flow (float)",

            'GetPulseTubeStatus': "GetPulseTubeStatus(). Return PT status (bool)"}
        
        print(FuncHelp[Func])
        return 0        

    def Get(self, node):
        req=requests.get(f"https://{self.DEVICE_IP}:{self.PORT}/{node}?key={self.ApiKey}", timeout=self.timeout)
        return req

    def Post(self, node, data):
        req = requests.post(f"https://{self.DEVICE_IP}:{self.PORT}/{node}?key={self.ApiKey}", json=data, timeout=self.rimeout)
        return req

    def Idn(self):
        req=requests.get(f'https://{DEVICE_IP}:{PORT}/system?key={ApiKey}', timeout=self.timeout)
        return req.json()['data']['system_name'], req.json()['data']['system_version']

    def GetT(self, name):
        if name not in TCHANNELS:
            return "Invalid channel"
        
        req=self.Get(f"values/mapper/bf/temperatures/{name}")
        if req.status_code != 200:
            return f"Comm failed. Status Code {req.status_code}"
         
        out=float(req.json()['data'][f'mapper.bf.temperatures.{name}']['content']['latest_value']['value'])
        if out>0:
            return out
        try:
            out=10**np.polyval(SensorParams[SENSORNAME[TCHANNELS.index(name)]], self.GetTR(name))
            return f"*{format(out, '.3e')}"
        except:
            return numpy.nan
        

    def GetTCh(self, Chn):
        return self.GetT(TCHANNELS[Chn])

    def GetTRCh(self, Chn):
        req=self.Get(f"values/mapper/temperature_control/sensors/t{Chn}/resistance")
        if req.status_code != 200:
            return f"Comm failed. Status Code {req.status_code}"
         
        try:
            out=float(req.json()['data'][f'mapper.temperature_control.sensors.t{Chn}.resistance']['content']['latest_value']['value'])
            if out>0:
                return out
        except:
            pass
        return float('NaN') 
        
    def GetTR(self, name):
        return self.GetTRCh(TCHANNELS.index(name))

    def GetPCh(self, Chn):
        if Chn not in range(1, 7):
            return "Invalid channel"
        
        req=self.Get(f"values/mapper/bf/pressures/p{Chn}")
        if req.status_code != 200:
            return f"Comm failed. Status Code {req.status_code}"
        
        try: 
            out=float(req.json()['data'][f'mapper.bf.pressures.p{Chn}']['content']['latest_value']['value'])
            if out>0:
                return out
        except:
            pass
        return float('NaN')

    def GetAirPressOk(self):
        req=self.Get("values/driver.vc.pressure_ok")

        if req.status_code != 200:
            return f"Comm failed. Status Code {req.status_code}"
        
        return bool(req.json()['data']['driver.vc.pressure_ok']['content']['latest_value']['value'])

    def GetFlow(self):
        req=self.Get(f"values/mapper/bf/flow")
        if req.status_code != 200:
            return f"Comm failed. Status Code {req.status_code}"
        
        try:
            out=float(req.json()['data']['mapper.bf.flow']['content']['latest_value']['value'])
            if out>0:
                return out
        except:
            pass
        return float('NaN')

    def GetPulseTubeStatus(self):
        req=self.Get(f"values/mapper/bf/pulsetube")
        if req.status_code != 200:
            return f"Comm failed. Status Code {req.status_code}"

        return int(req.json()['data']['mapper.bf.pulsetube']['content']['latest_value']['value'])
            
            
            
