from ctypes import (
    c_uint8,
    c_uint16,
    c_float,
    cast,
    POINTER,
    CDLL,
)
from unix_ffi import (
    MsgTypeConfig,
    FFIDefines,
    DeviceMsg,
    create_ltd_driver_ffi,
)

DEFAULT_MSG_TYPE_CONFIG = MsgTypeConfig(msg_type=0, data_type=0, size_bytes=0)
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


def create_ltd_driver() -> CDLL:
    _ffi = create_ltd_driver_ffi()
    assert _ffi
    init_rc = _ffi.init_ltd_driver(c_uint16(0x8787), lt_ch000_driver_config, c_uint8(FFIDefines.LT_CH000_DRIVER_CONFIG_SIZE))
    assert init_rc == 0
    return _ffi


def cmp_msg_type_config(config_1: MsgTypeConfig, config_2: MsgTypeConfig) -> bool:
    cmp_flag = True
    cmp_flag &= config_1.data_type == config_2.data_type
    cmp_flag &= config_1.msg_type == config_2.msg_type
    cmp_flag &= config_1.size_bytes == config_2.size_bytes
    return cmp_flag


def test_init_ltd_driver():
    _driver = create_ltd_driver()

    # case: config_idx >= MAX_MSG_TYPES
    _config: MsgTypeConfig = _driver.get_msg_type_config(20)
    assert cmp_msg_type_config(_config, DEFAULT_MSG_TYPE_CONFIG)

    # case: valid config_idx
    write_weight_config: MsgTypeConfig = _driver.get_msg_type_config(FFIDefines.WRITE_WEIGHT_MSG_TYPE)
    target_config = lt_ch000_driver_config[2]
    assert cmp_msg_type_config(write_weight_config, target_config)


def test_encode_packet_invalid_msg_type():
    _driver = create_ltd_driver()
    msg_value_ptr = POINTER(c_float)(c_float(2.254))
    packet = (c_uint8 * 15)()
    encode_rc = _driver.encode_packet(c_uint16(0), 5, cast(msg_value_ptr, POINTER(c_uint8)), packet)
    assert encode_rc == FFIDefines.RC_ERR_UNK_MSG_TYPE


def test_encode_packet_data_payload():
    _driver = create_ltd_driver()
    msg_value_ptr = POINTER(c_float)(c_float(2.254))
    packet = (c_uint8 * 15)()
    encode_rc = _driver.encode_packet(c_uint16(0), FFIDefines.WRITE_WEIGHT_MSG_TYPE, cast(msg_value_ptr, POINTER(c_uint8)), packet)
    assert encode_rc == 0
    assert list(packet) == [0x87, 0x87, 0x0F, 0x00, 0x00, 0xA2, 0x00, 0x89, 0x41, 0x10, 0x40, 0xA4, 0x1A, 0x0D, 0x0A]


def test_encode_packet_command_payload():
    _driver = create_ltd_driver()
    msg_value_ptr = POINTER(c_uint8)(c_uint8(0xFF))
    packet = (c_uint8 * 12)()
    encode_rc = _driver.encode_packet(c_uint16(0), FFIDefines.READ_RESET_SCALE_MSG_TYPE, msg_value_ptr, packet)
    assert encode_rc == 0
    assert list(packet) == [0x87, 0x87, 0x0C, 0x00, 0x00, 0xCF, 0x00, 0xFF, 0x4B, 0xEB, 0x0D, 0x0A]


def test_decode_packet_pv_mismatch():
    _driver = create_ltd_driver()
    packet = (c_uint8 * 15)(0x87, 0x88, 0x0F, 0x00, 0x00, 0xA2, 0x00, 0x89, 0x41, 0x10, 0x40, 0x78, 0xB7, 0x0D, 0x0A)
    decode_rc = _driver.decode_packet(packet, POINTER(DeviceMsg)(DeviceMsg()))
    assert decode_rc == FFIDefines.RC_ERR_INV_PV


def test_decode_packet_invalid_length():
    _driver = create_ltd_driver()
    packet = (c_uint8 * 2)(0x87, 0x87)
    decode_rc = _driver.decode_packet(packet, POINTER(DeviceMsg)(DeviceMsg()))
    assert decode_rc == FFIDefines.RC_ERR_INV_PKT_LEN


def test_decode_packet_invalid_msg_type():
    _driver = create_ltd_driver()
    packet = (c_uint8 * 15)(0x87, 0x87, 0x0F, 0x00, 0x00, 0x2A, 0x00, 0x89, 0x41, 0x10, 0x40, 0x5E, 0x3E, 0x0D, 0x0A)
    decode_rc = _driver.decode_packet(packet, POINTER(DeviceMsg)(DeviceMsg()))
    assert decode_rc == FFIDefines.RC_ERR_UNK_MSG_TYPE


def test_decode_packet_invalid_crc16():
    _driver = create_ltd_driver()
    packet = (c_uint8 * 15)(0x87, 0x87, 0x0F, 0x00, 0x00, 0xA2, 0x00, 0x89, 0x41, 0x10, 0x40, 0xA5, 0x1A, 0x0D, 0x0A)
    decode_rc = _driver.decode_packet(packet, POINTER(DeviceMsg)(DeviceMsg()))
    assert decode_rc == FFIDefines.RC_ERR_INV_CRC16


def test_decode_packet_data_payload():
    _driver = create_ltd_driver()
    packet = (c_uint8 * 15)(0x87, 0x87, 0x0F, 0x00, 0x00, 0xA2, 0x00, 0x89, 0x41, 0x10, 0x40, 0xA4, 0x1A, 0x0D, 0x0A)
    device_msg = DeviceMsg()
    decode_rc = _driver.decode_packet(packet, POINTER(DeviceMsg)(device_msg))
    assert decode_rc == FFIDefines.RC_OK
    assert device_msg.seq_number == 0
    target_config = lt_ch000_driver_config[2]
    assert cmp_msg_type_config(device_msg.config, target_config)
    assert list(device_msg.msg_value_buffer) == [0x89, 0x41, 0x10, 0x40, 0x00, 0x00, 0x00, 0x00]


def test_decode_packet_device_error_payload():
    _driver = create_ltd_driver()
    packet = (c_uint8 * 12)(0x87, 0x87, 0x0C, 0x00, 0x00, 0x4E, 0x00, 0xF0, 0x8C, 0x45, 0x0D, 0x0A)
    device_msg = DeviceMsg()
    decode_rc = _driver.decode_packet(packet, POINTER(DeviceMsg)(device_msg))
    assert decode_rc == FFIDefines.RC_OK
    assert device_msg.seq_number == 0
    target_config = lt_ch000_driver_config[5]
    assert cmp_msg_type_config(device_msg.config, target_config)
    assert list(device_msg.msg_value_buffer)[0] == 0xF0
