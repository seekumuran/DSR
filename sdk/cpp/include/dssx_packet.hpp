#pragma once

#include <cstdint>

struct DSSXPacket
{
    uint8_t sync;
    uint8_t version;
    uint8_t device;

    uint8_t buttons1;
    uint8_t buttons2;

    uint8_t lx;
    uint8_t ly;

    uint8_t rx;
    uint8_t ry;

    uint16_t crc;
};
