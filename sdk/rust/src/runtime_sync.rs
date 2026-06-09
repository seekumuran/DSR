pub struct RuntimeSync {

    pub synchronized: bool
}

impl RuntimeSync {

    pub fn synchronize(&mut self) {

        self.synchronized = true;
    }
}
