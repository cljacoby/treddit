extern crate serde;
extern crate serde_json;

use serde::{Serialize, Deserialize};
use crate::rnode::RNode;
use crate::t1::T1;
use crate::t3::T3;
use crate::more::More;

/// test

// TODO: Make the members private
#[derive(Debug)]
#[derive(Serialize, Deserialize)]
pub struct Listing {
    pub modhash: String,
    pub dist: Option<i64>,
    pub children: Vec<RNode>,
    pub after: Option<String>,
    pub before: Option<String>,
}

impl Listing {

    /// An empty Listing node. Replaces `replies` nodes equal to emptry strings
    pub fn empty() -> Listing {
        Listing {
            modhash: String::from(""),
            dist: None,
            children: Vec::<RNode>::new(),
            after: None,
            before: None,
        }
    }
    
    pub fn iter(&self) -> &Vec<RNode> {
        &self.children
    }

    // Problem with direct iter is that the childern vector is RNodes.
    // This means the calling level needs to have the match logic

    /*

    pub fn extract_t1s(&self) -> Vec<&T1> {
        let mut t1s = Vec::new();
        for child in self.children.iter() {
            match child {
                RNode::T1(t1) => { t1s.push(t1); },
                _ => {},
            }
        }
        t1s
    }
    */

}

/// Container structure used to deserialize Lisitng nodes. Needed in nempty_string_as_none.
#[derive(Debug)]
#[derive(Serialize, Deserialize)]
struct ListingContainer {
    kind: String,
    data: Listing,
} 


// I'm not sure about this implementation there's the assumption in the Err branch,
// and seems roundabout in general.
/// Provides special deserializtion logic for the Listing nodes. 
pub fn deserialize_replies<'de, D>(deserializer: D) -> Result<Box<Listing>, D::Error>
where
    D: serde::Deserializer<'de>,
{

    let result = Option::<ListingContainer>::deserialize(deserializer);
    match result {
        Ok(opt) => {
            let err_msg = "Succesfully deserialized ListingContainer, \
                           but failed to unwrap Option"; 
            let listing = opt.expect(err_msg).data;
            Ok(Box::new(listing))
        },
        Err(_) => {
            // Sssumption. All `replies` nodes that fail to deserialize to ListingContainer should
            // be replaced by an empty listing. This happens when `replies` is an empty string.
            Ok(Box::new(Listing::empty()))
        }
    }
    
}
