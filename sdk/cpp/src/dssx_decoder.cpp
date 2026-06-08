#include "../include/dssx_packet.hpp"

DSSXPacket decode_packet(uint8_t* raw)
{
    DXXSPacket p;

    p.sync = raw[0];
    p.version = raw[1];
    p.device = raw[2];

    p.buttons1 = raw[3];
    p.buttons2 = raw[4];

    p.lx = raw[5];
    p.ly = raw[6];

    p.rx = raw[7];
    p.ry = raw[8];

    p.crc = (raw[9] << 8) | raw[10];

    return p;
}
