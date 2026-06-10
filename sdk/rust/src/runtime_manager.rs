pub struct RuntimeManager {

    pub active: bool
}

impl RuntimeManager {

    pub fn start(&mut self) {

        self.active = true;
    }

    pub fn stop(&mut self) {

        self.active = false;
    }
}
