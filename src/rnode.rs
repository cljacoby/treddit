extern crate serde;
extern crate serde_json;

use std::fmt::{self, Formatter, Display};
use serde::{Serialize, Deserialize};
use serde::de::{IntoDeserializer, Deserializer, Visitor};
use serde_json::{Value, Map};

use crate::t1::T1;
use crate::t3::T3;
use crate::more::More;
use crate::listing::Listing;

#[derive(Debug)]
#[derive(Serialize, Deserialize)]
#[serde(tag = "kind", content = "data")]
pub enum RNode { 
    Listing(Listing),
    
    #[serde(rename = "t3")]
    T3(T3),
    
    #[serde(rename = "t1")]
    T1(T1),
    
    #[serde(rename = "more")]
    More(More),
}

impl RNode {

    pub fn is_listing(rnode: RNode) -> bool {
        match rnode {
            RNode::Listing(listing) => true,
            _ => false,
        }
    }
    
    pub fn is_t1(rnode: RNode) -> bool {
        match rnode {
            RNode::T1(t1) => true,
            _ => false,
        }
    }
    
    pub fn is_t3(rnode: RNode) -> bool {
        match rnode {
            RNode::T3(t3) => true,
            _ => false,
        }
    }

    pub fn is_more(rnode: RNode) -> bool {
        match rnode {
            RNode::More(more) => true,
            _ => false,
        }
    }



}

mod test {

    use super::*;

    use serde::{Serialize, Deserialize};
    use serde_json::Value;

    #[test]
    fn _test() -> Result<(), Box<std::error::Error>> {

        assert!(true);
        Ok(())
    }

}

