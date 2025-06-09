from model.SysParaDto import SysParaDto
from model.CollectPara import CollectPara
from model.CollectPara import VibChannalParaDto
from model.CollectPara import VibParaDto

import json
import time


def handel(topic, cmd, payload):
    respTopic = topic.replace("/Online", "")
    #===================================================================[Change 3]=================
    respTopic = "testbyrock/"+respTopic
    #==============================================================================================

    status = "1"  # default status = 1
    res = respDto(respTopic, "")
    try:
        res.payload = handels().case_to_function(cmd)(payload)
    #===================================================================[Change 4]=================
    except:
        status = "0"  # if failed, set status to 0
    # res.tpoic += "/"+status
    res.tpoic += "/"+status
    #==============================================================================================

    return res


class respDto:
    tpoic = ""
    payload = []
    isReplay = True

    def __init__(self, topic, payload) -> None:
        self.tpoic = topic
        self.payload = payload
        pass


class handels:
    def case_to_function(self, cmd):
        fun_name = "handel_" + str(cmd)
        method = getattr(self, fun_name)
        return method
    # Gateway register to network
    
    # Topic: Register
    def handel_Register(self, payload):
        return ""

    # Topic: SysPara
    def handel_SysPara(self, paylod):
        sysParaDto = SysParaDto()
        sysParaDto.SysTime = time.strftime(
            '%Y-%m-%dT%H:%M:%S', time.localtime(time.time()))
        sysParaDto.ParaTime = "2022-12-09T10:21:00"
        # Index interval
        sysParaDto.IndexPeriod =10 #30*60
        # Tech channel interval
        sysParaDto.TechPeriod = 30#*60
        # Waveform  interval
        sysParaDto.WavePeriod = 60#60*60*2
        # Long waveform interval
        sysParaDto.LongWavePeriod = 24*3600*3
        # Data collection mode(1: continuoius, 0: non-continuous, fixed interval)
        sysParaDto.CollectType = 0
        # 485 output types: 0 - high-frequency acceleration, 1 - low-frequency acceleration, 2 - velocity
        sysParaDto.OutType485 = 2
        # Rpm interval
        sysParaDto.RpmPeriod = 30*60
        # Rtu interval
        sysParaDto.RtuPeriod = 30*60
        result = json.dumps(sysParaDto.__dict__)
        #    dictStr = json.load(paylod.decode('utf-8'))
        #    sysParaDto.__dict__ = dictStr
        return result

    def handel_CollectPara(self, payload):

        isWired = True  # simulate wired parameters
        channels = 10  # ten channels
        collectPara = CollectPara([])
        if (isWired):
            allVibChannalParaDtos = []
            for i in range(channels):
                vibParaDtos = []
                vibParaDto = VibParaDto(20000, 32*1024, 11)
                vibParaDtos.append(vibParaDto)
                vibParaDto2 = VibParaDto(2000, 16*1024, 12)
                vibParaDtos.append(vibParaDto2)
                vibChannalParaDto = VibChannalParaDto(vibParaDtos)
                vibChannalParaDto.ChNo=i+1
                allVibChannalParaDtos.append(vibChannalParaDto)
                collectPara.VibChannelList = allVibChannalParaDtos
        else:
            # simulate wireless data
            allVibChannalParaDtos = []
            for i in range(channels):
                vibParaDtos = []
                
                vibParaDto = VibParaDto(20000, 32*1024, 11)
                vibParaDto.Dir = 1
                vibParaDtos.append(vibParaDto)
                
                vibParaDto2 = VibParaDto(2000, 16*1024, 12)
                vibParaDto2.Dir = 1
                vibParaDtos.append(vibParaDto2)

                vibParaDto3 = VibParaDto(2000, 32*1024, 12)
                vibParaDto3.Dir = 2
                vibParaDtos.append(vibParaDto3)
                
                vibParaDto4 = VibParaDto(2000, 32*1024, 12)
                vibParaDto4.Dir = 3
                vibParaDtos.append(vibParaDto4)
                
                vibChannalParaDto = VibChannalParaDto(vibParaDtos)
                vibChannalParaDto.ChNo=i+1
                allVibChannalParaDtos.append(vibChannalParaDto)
                collectPara.VibChannelList = allVibChannalParaDtos
        result = json.dumps(collectPara, default=lambda o: o.__dict__,indent=0)
        return result

    def handel_IndexData(self,payload):
        # Receive metric data
        print(payload)
        return ""

    def handel_TimeSeqData(self,payload):
        # Receive time-series data
        print(payload)
        return ""

    def handel_WaveData(self,payload):
        # Receive waveform data
        print(payload)
        return ""

    def handel_TimeMarkData(self,payload):
        # Receive time mark data
        print(payload)
        return ""

    def handel_CheckData(self,payload):
        # Receive self-diagnostic data
        print(payload)
        return ""

    def handel_SensorInfo(self,payload):
        # Receive sensor information data
        print(payload)
        return ""

    def handel_RtuData(self,payload):
        # Receive RTU channel data
        print(payload)
        return ""

    def handel_BatteryInfo(self,payload):
        # Receive battery information data
        print(payload)
        return ""

    def handel_LogFile(self,payload):
        # Receive log information data
        print(payload)
        return ""

    def handel_UpdateFileList(self,payload):
        # Receive upgrade file request
        print(payload)
        return "[]"

    def handel_Disconnect(self,payload):
        # Receive log information data
        print(payload)
        print("The lower computer is offline")
        return ""
    