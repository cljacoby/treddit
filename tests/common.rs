use std::path::Path;

// Paths are relative from the crate root
pub const SUBREDDIT_PATH: &str = "./tests/data/subreddit.json";
pub const SUBMISSION_PATH: &str = "./tests/data/submission.json";

pub fn setup() {
    // some setup code, like creating required files/directories, starting
    // servers, etc.
    // share this setup code between integration tests, if needed.
}
