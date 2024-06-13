import _test_util
from unix_ffi import (
    MsgTypeConfig,
    FFIDefines,
)


def test_init_ltd_driver_0x87():
    _driver = _test_util.create_ltd_driver_0x87()

    # case: config_idx >= MAX_MSG_TYPES
    _config: MsgTypeConfig = _driver.get_msg_type_config(20)
    assert _test_util.cmp_msg_type_config(_config, _test_util.DEFAULT_MSG_TYPE_CONFIG)

    # case: valid config_idx
    write_weight_config: MsgTypeConfig = _driver.get_msg_type_config(FFIDefines.WRITE_WEIGHT_MSG_TYPE)
    target_config = _test_util.lt_ch000_driver_config[2]
    assert _test_util.cmp_msg_type_config(write_weight_config, target_config)
