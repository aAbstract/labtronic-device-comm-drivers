#include <assert.h>

#include "ltd_driver_0x87.h"

static MsgTypeConfig config_hash_map[MAX_MSG_TYPES];

MsgTypeConfig get_msg_type_config(uint8_t config_idx) {
  if (config_idx >= MAX_MSG_TYPES)
    return (MsgTypeConfig){.msg_type = 0, .data_type = 0, .size_bytes = 0};
  return config_hash_map[config_idx];
}

uint8_t init_ltd_driver_0x87(MsgTypeConfig* driver_config, uint8_t arr_size) {
  for (uint8_t i = 0; i < arr_size; i++) {
    MsgTypeConfig _config = driver_config[i];
    config_hash_map[_config.msg_type] = _config;
  }
  return OK_RC;
}

uint8_t encode_packet(uint16_t msg_seq_number, uint8_t msg_type, void* msg_value_ptr, uint8_t* out_packet) {
  // check if the msg_type exists in the config_hash_map
  if (msg_type > MAX_MSG_TYPES)
    return ERR_UNK_MSG_TYPE;
  MsgTypeConfig _config = config_hash_map[msg_type];
  if (_config.size_bytes == 0)
    return ERR_UNK_MSG_TYPE;

  return OK_RC;
}

uint8_t decode_packet(uint8_t* packet, DeviceMsg* out_device_msg) {
  return OK_RC;
}