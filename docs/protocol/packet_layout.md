# DSSX Packet Layout

```txt
+--------+---------+-----------+
| Byte   | Field   | Purpose   |
+--------+---------+-----------+
| 0      | SYNC    | Sync Byte |
| 1      | VERSION | Protocol  |
| 2      | DEVICE  | Device ID |
| 3      | BTN1    | Buttons A |
| 4      | BTN2    | Buttons B |
| 5      | LX      | Left X    |
| 6      | LY      | Left Y    |
| 7      | RX      | Right X   |
| 8      | RY      | Right Y   |
| 9      | CRC_H   | CRC High  |
| 10     | CRC_L   | CRC Low   |
+--------+---------+-----------+
```
