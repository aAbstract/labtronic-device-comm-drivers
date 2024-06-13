#include <stdio.h>

#include "lt_ch000.h"
#include "ltd_driver_0x87.h"

MsgTypeConfig get_msg_type_config(uint8_t config_idx);

int main() {
  uint8_t init_driver_rc = init_ltd_driver_0x87(lt_ch000_driver_config, LT_CH000_DRIVER_CONFIG_SIZE);
  MsgTypeConfig _config = get_msg_type_config(WRITE_WEIGHT_MSG_TYPE);
  printf("msg_type: %d\n", _config.msg_type);
  printf("data_type: %d\n", _config.data_type);
  printf("size_bytes: %d\n", _config.size_bytes);
  // float test_value = 1.5;
  // uint8_t packet[16] = {0};
  // uint8_t encode_packet_rc = encode_packet(0, 5, &test_value, packet);
  // printf("encode_packet_rc=%d\n", encode_packet_rc);
}