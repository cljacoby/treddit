extern crate treddit;
use std::{fs,env};
use std::path::Path;

mod common;

use common::SUBMISSION_PATH;
use treddit::rnode::{RNode};
use treddit::listing::Listing;

#[test]
fn test() -> Result<(), Box<std::error::Error>> {

    let path = Path::new(SUBMISSION_PATH);
    println!("path.to_str() = {:?}", path.to_str());
    println!("env::current_dir() = {:?}", env::current_dir()?);
    println!("path.is_file() = {:?}", path.is_file());
    
    let s = fs::read_to_string(path)?;
    let submission: Vec<RNode> = serde_json::from_str(&s)?;
    
    let err_msg = "Submission json did not contain\
        second Listing node, which provides the comment tree.";
    let rnode = submission
        .get(1)
        .expect(err_msg);

    let listing = match rnode {
        RNode::Listing(listing) => listing,
        _ => { 
            panic!("expected Listing RNode, but got a different RNode variant.")
        }
    };

    for rnode in listing.iter() {
        match rnode {
            RNode::T1(t1) => {
                t1.walk()
            },
            _ => {},
        } 
    
    }
    

    Ok(())
}
