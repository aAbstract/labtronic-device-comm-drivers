#ifndef LTD_DRIVER_0x87_H
#define LTD_DRIVER_0x87_H

#include <stdint.h>

#define PROTOCOL_VERSION 0x87
#define PACKET_MIN_SIZE 11
#define PACKET_DATA_START 7
#define MAX_MSG_TYPES 16 // 4 msg_type bits

#define OK_RC 0
#define ERR_UNK_MSG_TYPE 1

#define DATA_TYPE_INT 0
#define DATA_TYPE_UINT 1
#define DATA_TYPE_FLOAT 2
#define DATA_TYPE_COMMAND 3

typedef struct MsgTypeConfig {
  uint8_t msg_type;
  uint8_t data_type;
  uint8_t size_bytes;
} MsgTypeConfig;

typedef struct DeviceMsg {
  MsgTypeConfig config;
  uint16_t seq_number;
  uint8_t msg_value_buffer[8];
} DeviceMsg;

uint8_t init_ltd_driver_0x87(const MsgTypeConfig* driver_config, uint8_t arr_size);
uint8_t encode_packet(uint16_t msg_seq_number, uint8_t msg_type, const uint8_t* msg_value_ptr, uint8_t* out_packet);
uint8_t decode_packet(const uint8_t* packet, DeviceMsg* out_device_msg);

#endif