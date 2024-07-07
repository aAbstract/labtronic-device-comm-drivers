#ifndef LTD_DRIVER_H
#define LTD_DRIVER_H

#include <stdint.h>

#define PACKET_MIN_SIZE 11
#define MAX_MSG_TYPES 16 // 4 msg_type bits

#define PKT_OFST_PV 0
#define PKT_OFST_LEN 2
#define PKT_OFST_SN 3
#define PKT_OFST_CFG1 5
#define PKT_OFST_CFG2 6
#define PKT_OFST_DATA 7

#define RC_OK 0
#define RC_ERR_UNK_MSG_TYPE 1
#define RC_ERR_PKT_TOO_SMALL 2
#define RC_ERR_INV_CRC16 3
#define RC_ERR_INV_PV 4
#define RC_ERR_INV_PKT_LEN 5

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

uint8_t init_ltd_driver(uint16_t _protocol_version, const MsgTypeConfig* driver_config, uint8_t arr_size);
uint8_t encode_packet(uint16_t msg_seq_number, uint8_t msg_type, const uint8_t* msg_value_ptr, uint8_t* out_packet);
uint8_t decode_packet(const uint8_t* packet, DeviceMsg* out_device_msg);

#endif