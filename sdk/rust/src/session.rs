pub struct DSSXSession {

    pub running: bool
}

impl DSSXSession {

    pub fn start(&mut self) {

        self.running = true;
    }

    pub fn stop(&mut self) {

        self.running = false;
    }
}
