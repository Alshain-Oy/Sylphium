#!/usr/bin/env python

import serial
import struct
from typing import Tuple

__version__ = '1.0.0'

OP_ERROR = 0x7f

OP_WRITE = 0x01
OP_READ = 0x02


OP_I2C_MEM_W = 0x19
OP_I2C_MEM_R = 0x20

OP_ICTRL = 0x03
OP_ENABLE = 0x04
OP_MODULATION = 0x05

# Parameters

PARAM_I_MEAS =      (0)
PARAM_VIN =         (1)
PARAM_I_MON_HS =    (2)
PARAM_V_MON_LP =    (3)
PARAM_V_MON_LM =    (4)
PARAM_EXT_PD =      (5)
PARAM_EXT_MOD =     (6)
PARAM_PD_SIGNAL =   (7)
PARAM_OUTPUT_EN =   (8)
PARAM_POWER_OK =    (9)
PARAM_TEMP_0 =     (10)
PARAM_TEMP_1 =     (11)
PARAM_TEMP_2 =     (12)
PARAM_TEMP_3 =     (13)

PARAM_INTERLOCK_OK =      (15)
PARAM_LASER_OK =          (16)

PARAM_TRIGGER_CNT =   (17)

PARAM_V_SET =       (20)
PARAM_I_LIMIT =     (21)
PARAM_TRIG_LVL =    (22)
PARAM_PD_THOLD =    (23)
PARAM_TRIG_POL =    (24)
PARAM_IRANGE =      (25)
PARAM_PD_EN =       (26)
PARAM_PD_GAIN =     (27)
PARAM_PD_BIAS =     (28)

PARAM_POWER_EN =    (29)


PARAM_PD_AVG =      (30)
PARAM_PD_RMS =      (31)

PARAM_I_AVG =      (32)
PARAM_I_RMS =      (33)

PARAM_VD_AVG =      (34)
PARAM_VD_RMS =      (35)

PARAM_P_AVG =      (36)
PARAM_P_RMS =      (37)


PARAM_VDROP =       (38)
PARAM_PD_CTRL =     (39)


PARAM_LSET_GAIN =     (40)
PARAM_LSET_OFFSET =   (41)
PARAM_DAC_OFFSET =    (42)
PARAM_CURRENT_GAIN =  (43)


PARAM_IO_IN =         (50)
PARAM_OPTO_IN =       (51)
PARAM_IO_OUT =        (52)
PARAM_OPTO_OUT =      (53)

PARAM_INTERLOCK_STRATEGY =  (55)
PARAM_INTERLOCK_DELAY =     (56)

PARAM_SERIAL_NUMBER =       (136)
PARAM_FIRMWARE_VER =		    (137)
PARAM_UPTIME =			        (138)


PARAM_MOD_PARAM0 =          (1010)
PARAM_MOD_PARAM1 =          (1011)
PARAM_MOD_PARAM2 =          (1012)
PARAM_MOD_PARAM3 =          (1013)

PARAM_MOD_LENGTH =          (1020)
PARAM_MOD_STATE =           (1021)
PARAM_MOD_REPEAT_PERIOD =   (1022)
PARAM_MOD_SAMPLERATE =      (1023)
PARAM_MOD_DATA_START =      (1024)

# Options
IRANGE_3A =          (0)
IRANGE_300mA =       (1)

TRIGGER_POL_POS =   (0)
TRIGGER_POL_NEG =   (1)

PD_GAIN_1k =        (0)
PD_GAIN_10k =       (1)
PD_GAIN_100k =      (2)
PD_GAIN_1M =        (3)

PD_BIAS_0V =        (0)
PD_BIAS_5V =        (1)


ENABLE_OUTPUT =     (0)
ENABLE_POWER =      (1)
ENABLE_PD =         (2)
ENABLE_PD_CTRL =    (3)

INTERLOCK_NORMAL =          (0)
INTERLOCK_SECONDARY =       (1)
INTERLOCK_SECONDARY_INV =   (2)

MOD_RUN =                (0)
MOD_FILL =               (1) 
MOD_SINGLE_SHOT =        (2)
MOD_PERIODC =            (3)

MOD_SHAPE_PULSE =   (0)
MOD_SHAPE_SINE =    (1)




# Functions to encode messages

def gen_write_msg( addr: int, key: int, value: int ) -> bytes:
    return struct.pack( ">BBIi", addr, OP_WRITE, key, value )

def gen_write_float_msg( addr: int, key: int, value: float ) -> bytes:
    return struct.pack( ">BBIf", addr, OP_WRITE, key, value )

def gen_read_msg( addr: int, key: int) -> bytes:
    return struct.pack( ">BBIi", addr, OP_READ, key, 0 )

def gen_action_msg( addr: int, action: int, key: int, value: int ) -> bytes:
    return struct.pack( ">BBIi", addr, action, key, value )

def gen_action_msg_float( addr: int, action: int, key: int, value: int ) -> bytes:
    return struct.pack( ">BBIf", addr, action, key, value )


def gen_action_msg( addr: int, action: int, key: int, value: int ) -> bytes:
    return struct.pack( ">BBIi", addr, action, key, value )
    
def gen_action_msg_mem( addr: int, action: int, key: int, value: int ) -> bytes:
    return struct.pack( ">BBII", addr, action, key, value )

def gen_action_msg_mem_float( addr: int, action: int, key: int, value: int ) -> bytes:
    return struct.pack( ">BBIf", addr, action, key, value )


# Functions to decode message

def decode_error( msg: bytes ) -> Tuple[int, int]:
    (addr, op, error, extra) = struct.unpack( ">BBIi", msg )
    return error, extra

def decode_read( msg: bytes ) -> Tuple[int, int]:
    (addr, op, key, value) = struct.unpack( ">BBIi", msg )
    return key, value

def decode_read_float( msg: bytes ) -> Tuple[int, float]:
    (addr, op, key, value) = struct.unpack( ">BBIf", msg )
    return key, value

def decode_action( msg: bytes ) -> Tuple[int, int]:
    (addr, op, key, value) = struct.unpack( ">BBIi", msg )
    return key, value

def decode_action_mem( msg: bytes ) -> Tuple[int, int]:
    (addr, op, key, value) = struct.unpack( ">BBII", msg )
    return key, value

def decode_action_mem_float( msg: bytes ) -> Tuple[int, float]:
    (addr, op, key, value) = struct.unpack( ">BBIf", msg )
    return key, value


def decode_header( msg: bytes ) -> Tuple[int, int]:
    (addr, op) = struct.unpack_from( ">BB", msg )
    
    return addr, op 


class MemoryMap( object ):
    def __init__( self, device: object ) -> None:
        self.device = device
    
    def __getitem__(self, addr: int) -> float:
        return self.device.read_float( PARAM_MOD_DATA_START + addr )
    
    def __setitem__(self, addr: int, value: float) -> float:
        return self.device.write_float( PARAM_MOD_DATA_START + addr, value )
    



class Sylphium( object ):
    def __init__( self, com: object, address: int ) -> None:
        self.com = com
        self.address = address
        self.arb = MemoryMap( self )
    

    def _clear_buffer( self ) -> None:
        if self.com.in_waiting > 0:
            self.com.read( self.com.in_waiting )

    def write( self, key: int, value: int ) -> None:
        self._clear_buffer()

        self.com.write( gen_write_msg( self.address, int(key), int(value) ) )
        response = self.com.read( 10 )
        addr, op = decode_header( response )
        if op == OP_ERROR:
            raise IndexError

    def write_float( self, key: int, value: float ) -> None:
        self._clear_buffer()
        
        self.com.write( gen_write_float_msg( self.address, int(key), value ) )
        response = self.com.read( 10 )
        addr, op = decode_header( response )
        if op == OP_ERROR:
            raise IndexError



    def read( self, key: int ) -> int:
        self._clear_buffer()
        
        self.com.write( gen_read_msg( self.address, int( key ) ) )
        response = self.com.read( 10 )
        
        addr, op = decode_header( response )
        if op == OP_ERROR:
            raise IndexError
        
        key, value = decode_read( response )
        return value

    def read_float( self, key: int ) -> float:
        self._clear_buffer()
        
        self.com.write( gen_read_msg( self.address, int( key ) ) )
        response = self.com.read( 10 )
        
        addr, op = decode_header( response )
        if op == OP_ERROR:
            raise IndexError
        
        key, value = decode_read_float( response )
        return value

    def mem_write( self, addr: int, value: int ) -> int:
        self._clear_buffer()
        
        self.com.write( gen_action_msg_mem( self.address, OP_I2C_MEM_W, addr, value ) )
        response = self.com.read( 10 )
        key, value = decode_action( response )
        return value 
    
    def mem_read( self, addr: int ) -> int:
        self._clear_buffer()
        
        self.com.write( gen_action_msg( self.address, OP_I2C_MEM_R, addr, 0 ) )
        response = self.com.read( 10 )
        key, value = decode_action_mem( response )
        return value 


    def mem_write_float( self, addr: int, value: float ) -> float:
        self._clear_buffer()
        
        self.com.write( gen_action_msg_mem_float( self.address, OP_I2C_MEM_W, addr, value ) )
        response = self.com.read( 10 )
        key, value = decode_action( response )
        return value 
    
    def mem_read_float( self, addr: int ) -> float:
        self._clear_buffer()
        
        self.com.write( gen_action_msg( self.address, OP_I2C_MEM_R, addr, 0 ) )
        response = self.com.read( 10 )
        key, value = decode_action_mem_float( response )
        return value 

    def enable_output( self, state ) -> None:
        self._clear_buffer()
        
        if state:
            self.com.write( gen_action_msg( self.address, OP_ENABLE, ENABLE_OUTPUT, 1 ) )
        else:
            self.com.write( gen_action_msg( self.address, OP_ENABLE, ENABLE_OUTPUT, 0 ) )
            
        response = self.com.read( 10 )


    def enable_main_power( self, state ) -> None:
        self._clear_buffer()
        
        if state:
            self.com.write( gen_action_msg( self.address, OP_ENABLE, ENABLE_POWER, 1 ) )
        else:
            self.com.write( gen_action_msg( self.address, OP_ENABLE, ENABLE_POWER, 0 ) )
        response = self.com.read( 10 )


    def constant_current( self, current ) -> None:
        self._clear_buffer()
        self.com.write( gen_action_msg_float( self.address, OP_ICTRL, 0, current ) )
        response = self.com.read( 10 )

    def modulation( self, state, single_shot = False, periodic = False ) -> None:
        self._clear_buffer()

        if not state:
            self.com.write( gen_action_msg( self.address, OP_MODULATION, MOD_RUN, 0 ) )
        else:
            if single_shot:
                   self.com.write( gen_action_msg( self.address, OP_MODULATION, MOD_SINGLE_SHOT, 1 ) )
            else:
                if periodic:
                    self.com.write( gen_action_msg( self.address, OP_MODULATION, MOD_PERIODC, 1 ) )
                else:
                    self.com.write( gen_action_msg( self.address, OP_MODULATION, MOD_RUN, 1 ) )

        #self.com.write( gen_action_msg( self.address, OP_MODULATION, key, value ) )
        response = self.com.read( 10 )
        #print( response )

    def generate_sine( self, amplitude, offset, frequency, phase = 0, sample_period = 1000 ):
        self.write_float( PARAM_MOD_PARAM0, amplitude )
        self.write_float( PARAM_MOD_PARAM1, offset )
        self.write_float( PARAM_MOD_PARAM2, frequency )
        self.write_float( PARAM_MOD_PARAM3, phase )
        self.write( PARAM_MOD_SAMPLERATE, sample_period )
        self.write( PARAM_MOD_LENGTH, 1000 )
        self.com.write( gen_action_msg( self.address, OP_MODULATION, MOD_FILL, MOD_SHAPE_SINE ) )
    
    def generate_pulse( self, amplitude, offset, duty_cycle, sample_period = 1000 ):
        self.write_float( PARAM_MOD_PARAM0, amplitude )
        self.write_float( PARAM_MOD_PARAM1, offset )
        self.write_float( PARAM_MOD_PARAM2, duty_cycle )
        self.write_float( PARAM_MOD_PARAM3, 0 )
        self.write( PARAM_MOD_SAMPLERATE, sample_period )
        self.write( PARAM_MOD_LENGTH, 1000 )
        self.com.write( gen_action_msg( self.address, OP_MODULATION, MOD_FILL, MOD_SHAPE_PULSE ) )
    
        
