extern crate reqwest;
extern crate serde;
extern crate serde_json;

pub mod rdata;

// crate imports
use rdata::RNode; 
use rdata::Listing;

// external imports
use std::fs::File;
use serde_json::Value;
use std::io::prelude::*;

#[macro_use]
extern crate serde_derive;


// TODO: How to gracefully handle panic?
/// Reads the contents of file at path `path` to a String `contents`.
pub fn read_file(path: &str) -> String {
    let mut s = String::new();
    let mut file = File::open(path)
        .expect(&format!("Failed to open file at {}", path));
    file.read_to_string(&mut s)
        .expect(&format!("Failed to read data to String from {}", path));
    s
}
