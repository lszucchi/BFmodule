import requests, json, sys, numpy
sys.path.append('.')
from DeviceParameters import DEVICE_IP, PORT, ApiKey
sys.path.append('./bin')
from SensorParameters import SensorParams

TCHANNELS = ['', 't50k', 't4k', 'tmagnet', '', 'tstill', 'tmixing', '', 'tfse']
SENSORNAME = ['', '', '', '', '', '', 'R10482340', '', '']
PCHANNELS = ["can", "p2", "p3", "p4", "tank", "p6"]

class DR:

    def __init__(self, timeout=10):
        req=requests.get(f'https://{DEVICE_IP}:{PORT}/system?key={ApiKey}', timeout=timeout)
        if req.status_code==200:
            self.DEVICE_IP=DEVICE_IP
            self.PORT=PORT
            self.ApiKey=ApiKey
            self.timeout=timeout
            print(req.json()['data']['system_name'], req.json()['data']['system_version'])
        else:
            raise f"Initial HTTP request failed. Status Code:{req.stats_code}"

    def Get(self, node):
        req=requests.get(f"https://{self.DEVICE_IP}:{self.PORT}/{node}?key={self.ApiKey}", timeout=self.timeout)
        return req

    def Post(self, node, data):
        req = requests.post(f"https://{self.DEVICE_IP}:{self.PORT}/{node}?key={self.ApiKey}", json=data, timeout=self.rimeout)
        return req

    def Id(self):
        req=requests.get(f'https://{DEVICE_IP}:{PORT}/system?key={ApiKey}', timeout=self.timeout)
        return req.json()['data']['system_name'], req.json()['data']['system_version']

    def GetT(self, name):
        if name not in TCHANNELS:
            return "Invalid channel"
        
        req=self.Get(f"values/mapper/bf/temperatures/{name}")
        if req.status_code != 200:
            return f"Comm failed. Status Code {req.status_code}"
         
        try:
            out=float(req.json()['data'][f'mapper.bf.temperatures.{name}']['content']['latest_value']['value'])
            if out>0:
                return out
        except:
            pass

            numpy.polyval(SensorParams[SENSORNAME[TCHANNELS.index('tmixing')]], self.GetTR(name))
        
        return float('NaN')

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
            
            
            
