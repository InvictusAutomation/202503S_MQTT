class CollectPara:
    def __init__(self, VibChannalParaDtos) -> None:
        # Vibration channel parameters need to be assigned additionally
        self.VibChannelList = VibChannalParaDtos
        # Other channel parameters
        self.TechChannelList = []
        self.SpeedChannelList = []
        self.TriggerList = []
        self.RtuChannelList = []
        self.OutputChannelList = []
        self.StopLimitList = []
        pass


class VibChannalParaDto:
    def __init__(self, VibParaLists) -> None:
        # Vibration channel number
        self.ChNo = 1
        # Associated rotational speed channel number
        self.SpeedNo = 0
        # Sensor type, use this default value currently
        self.SensType = 0
        # Control constant current source status (0-off; 1-on)
        self.CnstCurSrcState = 0
        # Sensor coefficient, wireless ignores this parameter, wired can be set according to specific sensor parameters
        self.SensCoef = 10
        # Device ID, use this default value currently
        self.DevId = 1
        # Vibration parameters, assign values according to actual situation
        self.VibParaList = VibParaLists
        # Threshold parameters
        self.LimitParaList = []
        pass


class VibParaDto:
    def __init__(self, HighFreq, Length, Code=11) -> None:
        # Lower frequency limit (HZ)
        self.LowFreq = 0
        # Upper frequency limit (HZ)
        self.HighFreq = HighFreq
        # Acquisition length
        self.Length = Length
        # Engineering unit (m/s^2)
        self.Unit = "m/s^2"
        # Additional length
        self.PlusLength = 0
        # Direction (0-no direction; 1-X axis; 2-Y axis; 3-Z axis)
        self.Dir = 0
        # Index type (1-long waveform; 11-high frequency acceleration; 12-low frequency acceleration; 15-velocity waveform)
        self.Code = Code
        pass