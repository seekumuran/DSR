pub struct DSSXTransport {

    pub connected: bool
}

impl DSSXTransport {

    pub fn connect(&mut self) {

        self.connected = true;
    }

    pub fn disconnect(&mut self) {

        self.connected = false;
    }
}
