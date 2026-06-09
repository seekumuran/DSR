pub struct DSSXRuntime {

    pub active: bool
}

impl DSSXRuntime {

    pub fn start(&mut self) {

        self.active = true;
    }

    pub fn stop(&mut self) {

        self.active = false;
    }
}
