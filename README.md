# Sylphium
Sylphium eco laser driver


## Quickstart
1) Connect usb data cable to _Data in_ or _Data out_ port
2) Connect power adapter to Sylphium
3) Make sure that interlock connections are set correctly

```python
import libSylphium
import serial

# replace "COM3" with corresponding port on your computer
com = serial.Serial( "COM3", 460800, timeout = 10.0 )

# Connect to laser driver with address = 1 (default)
laser = libSylphium.Sylphium( com, 1 )
```

## Snippets

### Basic usage
```python
# Set limits and operating range
laser.write_float( libSylphium.PARAM_I_LIMIT, 0.2) # Set current limit to 0.2A
laser.write_float( libSylphium.PARAM_V_SET, 5.0 ) # Set diode supply voltage to 5V
laser.write_float( libSylphium.PARAM_TRIG_LVL, 0.025 ) # Set internal trigger level to 25mA
laser.write( libSylphium.PARAM_IRANGE, libSylphium.IRANGE_300mA ) # Set operating range to 300mA

# Enable main power supply and diode driver
laser.enable_main_power( True ) # enables main power supply but not the drive circuitry

# Enables both main power supply and the drive circuitry 
# (OBS! enable works only if interlock is ok)
laser.enable_output( True )  

laser.enable_main_power( False ) # Disables main power supply
laser.enable_output( False ) # Disables diode drive circuitry

# Modulation
laser.constant_current( 0.1 ) # Drive the diode with 0.1A constant current

laser.modulation( True ) # Turn on internal modulation
laser.modulation( False ) # Turn off the internal modulation

# Turn on the modulation for one modulation buffer round
laser.modulation( True, single_shot = True ) 

# note: Waveform buffer is 1000 samples long

# Fill waveform buffer with sine wave
# generate_sine( amplitude, offset, frequency, phase = 0, sample_period = 1000 )
# amplitude = amplitude of the sine wave (in amps)
# offset = dc current offset for the wave (in amps)
# frequency = how many periods will be generate to the waveform buffer 
# phase = phase offset of the sine wave (in radians)
# sample_period = duration of each sample (in µs)

laser.generate_sine( 0.1, 0.05, 1.0, sample_period = 1 )


# Fill waveform buffer with pulse wave
# generate_pulse( amplitude, offset, duty_cycle, sample_period = 1000 )
# amplitude = amplitude of the pulse (in amps)
# offset = dc current offset of the pulse (in amps)
# duty_cycle = relative pulse on time (0...1)
# sample_period = duration of each sample (in µs)

laser.generate_pulse( 0.1, 0.05, 0.15 )

```


### Parameters
```python

laser.read_float( libSylphium.PARAM_I_MEAS ) # -> Measured current [A]

laser.read_float( libSylphium.PARAM_VIN ) # Power supply input voltage [V]

laser.read_float( libSylphium.PARAM_V_MON_LP ) # Diode high side voltage [V]
laser.read_float( libSylphium.PARAM_V_MON_LM ) # Diode low side voltage [V]

laser.read_float( libSylphium.PARAM_EXT_PD ) # External photodiode control voltage [V]

laser.read_float( libSylphium.PARAM_EXT_MOD ) # External modulation control voltage [V]

laser.read_float( libSylphium.PARAM_PD_SIGNAL ) # Photodiode current [A]

laser.read( libSylphium.PARAM_OUTPUT_EN ) # 0 -> output disabled, 1 -> output enabled
laser.read( libSylphium.PARAM_POWER_OK ) # 0 -> main power not ok, 1 -> main power is ok

laser.read_float( libSylphium.PARAM_TEMP_0 ) # Internal temperature sensor reading [C]
laser.read_float( libSylphium.PARAM_TEMP_1 ) # Internal temperature sensor reading [C]
laser.read_float( libSylphium.PARAM_TEMP_2 ) # Internal temperature sensor reading [C]


# 0 -> interlock is not ok, 1 -> interlock is ok
laser.read( libSylphium.PARAM_INTERLOCK_OK )

# 0 -> laser cannot be enabled, 1 -> laser can be enabled 
laser.read( libSylphium.PARAM_LASER_OK ) 

laser.read( libSylphium.PARAM_TRIGGER_CNT ) # Counter for trigger events

laser.write_float( libSylphium.PARAM_V_SET, 10.0 ) # Set diode drive voltage, 3 .. Vin - 4 [V]

laser.write_float( libSylphium.PARAM_I_LIMIT 0.1 ) # Set current limit [A]

laser.write_float( libSylphium.PARAM_TRIG_LVL 0.025 ) # Set trigger level [A]

laser.write_float( libSylphium.PARAM_PD_THOLD, 1e-5 ) # Set photodiode control current threshold [A]

# set trigger output polarity
#  TRIGGER_POL_POS = positive
#  TRIGGER_POL_NEG = inverted
laser.write_float( libSylphium.PARAM_TRIG_POL, libSylphium.TRIGGER_POL_POS )  

# Set operating range ( IRANGE_3A or IRANGE_300mA )
laser.write_float( libSylphium.PARAM_IRANGE, libSylphium.IRANGE_3A ) 

# 0 -> photodiode amplifier is disabled, 1 -> amplifier is enabled
laser.write( libSylphium.PARAM_PD_EN, 0 ) 

# Set photodiode amplifier gain
#  PD_GAIN_1k
#  PD_GAIN_10k
#  PD_GAIN_100k
#  PD_GAIN_1M 
laser.write_float( libSylphium.PARAM_PD_GAIN, libSylphium.PD_GAIN_10k ) 

# Set photodiode bias voltage (PD_BIAS_0V or PD_BIAS_5V)
laser.write_float( libSylphium.PARAM_PD_BIAS, libSylphium.PD_BIAS_0V ) 

# 0 -> main power is not enabled, 1 -> main power is enabled
laser.read( libSylphium.PARAM_POWER_EN ) 


laser.read_float( libSylphium.PARAM_PD_AVG ) # Average photodiode current [A]
laser.read_float( libSylphium.PARAM_PD_RMS ) # Photodiode RMS current [A]

laser.read_float( libSylphium.PARAM_I_AVG ) # Average drive current [A]
laser.read_float( libSylphium.PARAM_I_RMS ) # RMS dririve current [A]

laser.read_float( libSylphium.PARAM_VD_AVG ) # Average voltage drop over diode [V]
laser.read_float( libSylphium.PARAM_VD_RMS ) # RMS voltage drop over diode [V]

laser.read_float( libSylphium.PARAM_P_AVG ) # Average electrical power delivered to diode [W]
laser.read_float( libSylphium.PARAM_P_RMS ) # RMS electrical power delivered to diode [W]


laser.read_float( libSylphium.PARAM_VDROP ) # Current voltage drop over diode [V]

# 0 -> disable photodiode regulation, 1 -> enable photodiode regulation
laser.write( libSylphium.PARAM_PD_CTRL, 0 ) 


# State of the digital input signal (secondary interlock input)
laser.read( libSylphium.PARAM_IO_IN )

# State of the optocoupled input signal (primary interlock input )
laser.read( libSylphium.PARAM_OPTO_IN ) 

laser.write( libSylphium.PARAM_IO_OUT, 0 ) # Set state of the digial output signal
laser.write( libSylphium.PARAM_OPTO_OUT, 0 ) # Set state of the optocoupler output signal

# Select interlock strategy
#  INTERLOCK_NORMAL = only primary
#  INTERLOCK_SECONDARY = require both primary and secondary interlock inputs,
#  INTERLOCK_SECONDARY_INV, same as INTERLOCK_SECONDARY but secondary input is inverted )
laser.write( libSylphium.PARAM_INTERLOCK_STRATEGY, libSylphium.INTERLOCK_NORMAL )

laser.write( libSylphium.PARAM_INTERLOCK_DELAY, 2000 ) # Interlock delay [ms]

laser.read( libSylphium.PARAM_SERIAL_NUMBER ) # Serial number of the device

laser.read( libSylphium.PARAM_FIRMWARE_VER ) # Firmware version of the device

laser.read( libSylphium.PARAM_UPTIME ) # Device uptime [ms]

```

