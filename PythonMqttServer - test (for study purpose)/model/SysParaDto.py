class SysParaDto:
    # System time
    SysTime = "1970-01-01T00:00:00"
    # Parameter time
    ParaTime = "1970-01-01T00:00:00"
    # Index interval
    IndexPeriod = 30*60
    # Process channel sampling interval
    TechPeriod = 30*60
    # Waveform interval
    WavePeriod = 60*60*2
    # Long waveform interval
    LongWavePeriod = 24*3600*3
    # Acquisition mode (continuous, discontinuous) 0-timed 1-continuous
    CollectType = 0
    # 485 output type 0-high frequency acceleration 1-low frequency acceleration 2-velocity
    OutType485 = 2
    # Rotational speed interval
    RpmPeriod = 30*60
    # RTU interval
    RtuPeriod = 30*60