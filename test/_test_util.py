from ctypes import CDLL, c_uint8
from unix_ffi import (
    MsgTypeConfig,
    FFIDefines,
    create_ltd_driver_0x87_ffi
)

MsgTypeConfigArr = MsgTypeConfig * FFIDefines.LT_CH000_DRIVER_CONFIG_SIZE
lt_ch000_driver_config = MsgTypeConfigArr(
    MsgTypeConfig(msg_type=FFIDefines.WRITE_PISTON_PUMP_MSG_TYPE, data_type=FFIDefines.DATA_TYPE_UINT, size_bytes=4),
    MsgTypeConfig(msg_type=FFIDefines.WRITE_PERISTALTIC_PUMP_MSG_TYPE, data_type=FFIDefines.DATA_TYPE_UINT, size_bytes=1),
    MsgTypeConfig(msg_type=FFIDefines.WRITE_WEIGHT_MSG_TYPE, data_type=FFIDefines.DATA_TYPE_FLOAT, size_bytes=4),
    MsgTypeConfig(msg_type=FFIDefines.WRITE_TEMPERATURE_MSG_TYPE, data_type=FFIDefines.DATA_TYPE_FLOAT, size_bytes=4),
    MsgTypeConfig(msg_type=FFIDefines.WRITE_PRESSURE_MSG_TYPE, data_type=FFIDefines.DATA_TYPE_FLOAT, size_bytes=4),
    MsgTypeConfig(msg_type=FFIDefines.WRITE_DEVICE_ERROR, data_type=FFIDefines.DATA_TYPE_UINT, size_bytes=1),
    MsgTypeConfig(msg_type=FFIDefines.READ_PISTON_PUMP_MSG_TYPE, data_type=FFIDefines.DATA_TYPE_UINT, size_bytes=4),
    MsgTypeConfig(msg_type=FFIDefines.READ_PERISTALTIC_PUMP_MSG_TYPE, data_type=FFIDefines.DATA_TYPE_UINT, size_bytes=1),
    MsgTypeConfig(msg_type=FFIDefines.READ_RESET_SCALE_MSG_TYPE, data_type=FFIDefines.DATA_TYPE_COMMAND, size_bytes=1),
)


def create_ltd_driver_0x87() -> CDLL:
    _ffi = create_ltd_driver_0x87_ffi()
    assert _ffi
    init_rc = _ffi.init_ltd_driver_0x87(lt_ch000_driver_config, c_uint8(FFIDefines.LT_CH000_DRIVER_CONFIG_SIZE))
    assert init_rc == 0
    return _ffi


def cmp_msg_type_config(config_1: MsgTypeConfig, config_2: MsgTypeConfig) -> bool:
    cmp_flag = True
    cmp_flag &= config_1.data_type == config_2.data_type
    cmp_flag &= config_1.msg_type == config_2.msg_type
    cmp_flag &= config_1.size_bytes == config_2.size_bytes
    return cmp_flag
