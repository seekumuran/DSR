def crc16(data):

    crc = 0xFFFF

    for byte in data:

        crc ^= byte

        for _ in range(8):

            if crc & 1:
                crc = (crc >> 1) ^ 0xA001
            else:
                crc >>= 1

    return crc


packet = bytes([0xAA] * 9)

print(hex(crc16(packet)))
