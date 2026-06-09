pub struct DSSXDevice {

    pub connected: bool
}

impl DSSXDevice {

    pub fn connect(&mut self) {

        self.connected = true;
    }

    pub fn disconnect(&mut self) {

        self.connected = false;
    }
}
