pub struct DSSXPacket {

    pub sync: u8,
    pub version: u8,
    pub device: u8,

    pub buttons1: u8,
    pub buttons2: u8,

    pub lx: u8,
    pub ly: u8,

    pub rx: u8,
    pub ry: u8,

    pub crc: u16
}
