import requests, json
from DeviceParameters import DEVICE_IP, PORT, ApiKey

VALID_TCHANNELS = ['t50k', 't4k', 'tmagnet', 'tstill', 'tmixing', 'tfse']

class DR:

    def __init__(self, timeout=10):
        global DEVICE_IP, PORT, ApiKey
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

    def GetT(self, name, fstr=None):
        if name not in VALID_TCHANNELS:
            return "Invalid channel"
        
        req=self.Get(f"values/mapper/bf/temperatures/{name}")
        if req.status_code != 200:
            return f"Comm failed. Status Code {req.status_code}"

        return req.json()['data'][f'mapper.bf.temperatures.{name}']['content']['latest_value']['value']

    def GetP(self, Chn):
        if Chn not in range(1, 7):
            return "Invalid channel"
        
        req=self.Get(f"values/mapper/bf/pressures/p{Chn}")
        if req.status_code != 200:
            return f"Comm failed. Status Code {req.status_code}"

        return req.json()['data'][f'mapper.bf.pressures.p{Chn}']['content']['latest_value']['value']

    def GetFlow(self):
        req=self.Get(f"values/mapper/bf/flow")
        if req.status_code != 200:
            return f"Comm failed. Status Code {req.status_code}"

        return req.json()['data']['mapper.bf.flow']['content']['latest_value']['value']

    def GetPulseTubeStatus(self):
        req=self.Get(f"values/mapper/bf/pulsetube")
        if req.status_code != 200:
            return f"Comm failed. Status Code {req.status_code}"

        return int(req.json()['data']['mapper.bf.pulsetube']['content']['latest_value']['value'])
            
            
            
