pub struct RuntimeCore {

    pub active: bool
}

impl RuntimeCore {

    pub fn initialize(&mut self) {

        self.active = true;
    }

    pub fn shutdown(&mut self) {

        self.active = false;
    }
}
