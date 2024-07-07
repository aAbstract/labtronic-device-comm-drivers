# LabTronic Device Communications Drivers

## Usage
1. Create driver config list
```c
#include "ltd_driver.h"

MsgTypeConfig driver_config[5] = {
    {
        .msg_type = 0,
        .data_type = DATA_TYPE_UINT,
        .size_bytes = 4,
    },
    {
        .msg_type = 1,
        .data_type = DATA_TYPE_UINT,
        .size_bytes = 1,
    },
    {
        .msg_type = 2,
        .data_type = DATA_TYPE_FLOAT,
        .size_bytes = 4,
    },
    {
        .msg_type = 3,
        .data_type = DATA_TYPE_FLOAT,
        .size_bytes = 4,
    },
    {
        .msg_type = 4,
        .data_type = DATA_TYPE_FLOAT,
        .size_bytes = 4,
    },
};
```

2. Initialize driver using driver config list
```c
uint8_t init_driver_rc = init_ltd_driver(0x8787, driver_config, 5);
```

3. Encoding a packet
```c
float test_value = 2.254;
uint8_t packet[15];
encode_packet(15, _config.msg_type, (uint8_t*)&test_value, packet);
```

3. Decoding a packet
```c
DeviceMsg device_msg;
decode_packet(packet, &device_msg);
```

4. Parsing Msg Value Buffer
```c
float decoded_value = 0;
((uint8_t*)&decoded_value)[0] = device_msg.msg_value_buffer[0];
((uint8_t*)&decoded_value)[1] = device_msg.msg_value_buffer[1];
((uint8_t*)&decoded_value)[2] = device_msg.msg_value_buffer[2];
((uint8_t*)&decoded_value)[3] = device_msg.msg_value_buffer[3];
printf("OK | msg_value: %0.3f\n", decoded_value); // OK | msg_value: 2.254
```

## API Reference
```c
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
```

## Run Unit Tests - Unix
Unit tests are implemented using **Python + PyTest**.  
Python **ctypes** is also used as Foreign Function Interface (FFI) to the compiled ***.so** file.
1. Build ***.so** lib
```bash
$ python scripts/build.py driver_so
```
2. Install pytest
```bash
$ pip install pytest
```
3. Run unit tests
```bash
$ pytest
```

## Run Unit Tests - Windows
The current Foreign Function Interface (FFI) supports only Unix systems (Linux/MacOS).  
To run unit tests on windows, a win32 compatible FFI is required.  
**test/unix_ffi.py** can be used as a guide to implement the win32 port.