#include <stdio.h>

#include "lt_ch000.h"
#include "ltd_driver.h"

MsgTypeConfig get_msg_type_config(uint8_t config_idx);

int main() {
  uint8_t init_driver_rc = init_ltd_driver(0x8787, lt_ch000_driver_config, LT_CH000_DRIVER_CONFIG_SIZE);
  MsgTypeConfig _config = get_msg_type_config(WRITE_WEIGHT_MSG_TYPE);

  // encode_packet
  float test_value = 2.254;
  uint8_t packet[15];
  encode_packet(15, _config.msg_type, (uint8_t*)&test_value, packet);

  // decode_packet
  DeviceMsg device_msg;
  decode_packet(packet, &device_msg);

  // validation
  if (device_msg.seq_number != 15) {
    printf("Sequence number mismatch\n");
    return 1;
  }

  if (device_msg.config.msg_type != _config.msg_type ||
      device_msg.config.data_type != _config.data_type ||
      device_msg.config.size_bytes != _config.size_bytes ||
      device_msg.config.cfg2 != _config.cfg2) {
    printf("MsgTypeConfig mismatch\n");
    return 1;
  }

  float decoded_value = 0;
  ((uint8_t*)&decoded_value)[0] = device_msg.msg_value_buffer[0];
  ((uint8_t*)&decoded_value)[1] = device_msg.msg_value_buffer[1];
  ((uint8_t*)&decoded_value)[2] = device_msg.msg_value_buffer[2];
  ((uint8_t*)&decoded_value)[3] = device_msg.msg_value_buffer[3];
  float diff = test_value - decoded_value;
  if (diff >= 1e-4) {
    printf("Msg value mismatch\n");
    return 1;
  }

  printf("OK | msg_value: %0.3f\n", decoded_value);
  return 0;
}