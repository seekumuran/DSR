pub struct DSSXPipeline {

    pub active: bool
}

impl DSSXPipeline {

    pub fn execute(&mut self) {

        self.active = true;
    }
}
