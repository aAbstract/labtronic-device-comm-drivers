#include <stdio.h>

#include "lt_ch000.h"
#include "ltd_driver_0x87.h"

MsgTypeConfig get_msg_type_config(uint8_t config_idx);

int main() {
  uint8_t init_driver_rc = init_ltd_driver_0x87(lt_ch000_driver_config, LT_CH000_DRIVER_CONFIG_SIZE);
  MsgTypeConfig _config = get_msg_type_config(WRITE_WEIGHT_MSG_TYPE);

  // encode
  float test_value = 2.254;
  uint8_t packet[15];
  encode_packet(0, _config.msg_type, (uint8_t*)&test_value, packet);
}