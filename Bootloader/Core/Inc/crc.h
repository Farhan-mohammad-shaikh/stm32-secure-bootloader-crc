#ifndef CRC_H
#define CRC_H

#include <stdint.h>

uint32_t crc32_calculate(uint8_t *data, uint32_t length);

#endif
