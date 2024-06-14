import os
from ctypes import (
    Structure,
    c_uint8,
    c_uint16,
    CDLL,
    POINTER,
)


class MsgTypeConfig(Structure):
    _fields_ = [
        ('msg_type', c_uint8),
        ('data_type', c_uint8),
        ('size_bytes', c_uint8),
    ]


class DeviceMsg(Structure):
    _fields_ = [
        ('config', MsgTypeConfig),
        ('seq_number', c_uint16),
        ('msg_value_buffer', c_uint8 * 8),
    ]


class FFIDefines:
    PROTOCOL_VERSION = 0x87
    PACKET_MIN_SIZE = 11
    MAX_MSG_TYPES = 16

    PKT_OFST_PV = 0
    PKT_OFST_LEN = 2
    PKT_OFST_SN = 3
    PKT_OFST_CFG1 = 5
    PKT_OFST_CFG2 = 6
    PKT_OFST_DATA = 7

    RC_OK = 0
    RC_ERR_UNK_MSG_TYPE = 1
    RC_ERR_PKT_TOO_SMALL = 2
    RC_ERR_INV_CRC16 = 3
    RC_ERR_INV_PV = 4
    RC_ERR_INV_PKT_LEN = 5

    DATA_TYPE_INT = 0
    DATA_TYPE_UINT = 1
    DATA_TYPE_FLOAT = 2
    DATA_TYPE_COMMAND = 3

    LT_CH000_DRIVER_CONFIG_SIZE = 9

    WRITE_PISTON_PUMP_MSG_TYPE = 0
    WRITE_PERISTALTIC_PUMP_MSG_TYPE = 1
    WRITE_WEIGHT_MSG_TYPE = 2
    WRITE_TEMPERATURE_MSG_TYPE = 3
    WRITE_PRESSURE_MSG_TYPE = 4
    WRITE_DEVICE_ERROR = 14
    READ_PISTON_PUMP_MSG_TYPE = 12
    READ_PERISTALTIC_PUMP_MSG_TYPE = 13
    READ_RESET_SCALE_MSG_TYPE = 15


def create_ltd_driver_0x87_ffi() -> CDLL | None:
    ltd_driver_0x87_lib_path = 'build/ltd_driver_0x87.so'
    if not os.path.exists(ltd_driver_0x87_lib_path):
        return None
    ltd_driver_0x87 = CDLL(ltd_driver_0x87_lib_path)

    ltd_driver_0x87.init_ltd_driver_0x87.argtypes = [
        POINTER(MsgTypeConfig),  # driver_config
        c_uint8,  # arr_size
    ]
    ltd_driver_0x87.init_ltd_driver_0x87.restype = c_uint8

    ltd_driver_0x87.encode_packet.argtypes = [
        c_uint16,  # msg_seq_number
        c_uint8,  # msg_type
        POINTER(c_uint8),  # msg_value_ptr
        POINTER(c_uint8),  # out_packet
    ]
    ltd_driver_0x87.encode_packet.restype = c_uint8

    ltd_driver_0x87.decode_packet.argtypes = [
        POINTER(c_uint8),  # packet
        POINTER(DeviceMsg),  # out_device_msg
    ]
    ltd_driver_0x87.encode_packet.restype = c_uint8

    ltd_driver_0x87.get_msg_type_config.argtypes = [
        c_uint8,  # config_idx
    ]
    ltd_driver_0x87.get_msg_type_config.restype = MsgTypeConfig

    return ltd_driver_0x87
