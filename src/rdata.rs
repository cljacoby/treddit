extern crate serde;
extern crate serde_json;

use std::fmt::{self, Formatter, Display};
use serde::{Serialize, Deserialize};
use serde::de::{IntoDeserializer, Deserializer, Visitor};
use serde_json::{Value, Map};


#[derive(Debug)]
#[derive(Serialize, Deserialize)]

/// Container structure used to deserialize Lisitng nodes. Needed in nempty_string_as_none.
struct ListingContainer {
    kind: String,
    data: Listing,
} 


// I'm not sure about this implementation there's the assumption in the Err branch,
// and seems roundabout in general.
/// Provides special deserializtion logic for the Listing nodes. 
fn empty_string_as_none<'de, D>(deserializer: D) -> Result<Box<Listing>, D::Error>
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
            modhash: "".to_string(),
            dist: None,
            children: Vec::<RNode>::new(),
            after: None,
            before: None,
        }
    }

    // NOTE: This seems like a kludge
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

    pub fn iter_only<T>() -> Vec::<T> {
        let v: Vec<T> = Vec::new();
        v
    }

}

#[derive(Debug)]
#[derive(Serialize, Deserialize)]
pub struct T3 {
    total_awards_received: u32,
    approved_at_utc: Option<String>,
    ups: u32,
    mod_reason_by: Option<String>,
    banned_by: Option<String>,
    author_flair_type: Option<String>,
    removal_reason: Option<String>,
    author_flair_template_id: Option<String>,
    likes: Option<u32>,
    no_follow: bool,
    user_reports: Vec<String>,
    saved: bool,
    id: String,
    banned_at_utc: Option<u32>,
    mod_reason_title: Option<String>,
    gilded: u32,
    archived: bool,
    report_reasons: Option<String>,
    author: String,
    can_mod_post: bool,
    send_replies: bool,
    score: u32,
    author_fullname: String,
    approved_by: Option<String>,
    // TODO: Define strongly typed serde struct for all_awardings
    all_awardings: Value,
    subreddit_id: String,
    // edited: bool,
    author_flair_css_class: Option<String>,
    downs: u32,
    author_flair_richtext: Vec<String>,
    author_patreon_flair: bool,
    stickied: bool,
    subreddit_type: String,
    can_gild: bool,
    gildings: Map<String, Value>,
    author_flair_text_color: Option<String>,
    permalink: String,
    num_reports: Option<i32>,
    locked: bool,
    name: String,
    created: u32,
    subreddit: String,
    author_flair_text: Option<String>,
    created_utc: u32,
    subreddit_name_prefixed: String,
    author_flair_background_color: Option<String>,
    mod_reports: Vec<String>,
    mod_note: Option<String>,
    distinguished: Option<String>,
    clicked: bool,
    selftext: String,
    link_flair_type: String,
    over_18: bool,
    is_self: bool,
    parent_whitelist_status: String,
    spoiler: bool,
    link_flair_text_color: String,
    is_reddit_media_domain: bool,
    link_flair_text: Option<String>,
    whitelist_status: String,
    link_flair_background_color: String,
    is_meta: bool,
    thumbnail: String,
    content_categories: Option<String>,
    title: String,
    link_flair_richtext: Vec<String>,
    is_robot_indexable: bool,
    pwls: u32,
    suggested_sort: Option<String>,
    visited: bool,
    hide_score: bool,
    num_comments: u32,
    url: String,
    media: Option<String>,    
    category: Option<String>,
    discussion_type: Option<String>,
    wls: u32,
    is_original_content: bool,
    secure_media: Option<String>,
    subreddit_subscribers: u32,
    quarantine: bool,
    secure_media_embed: Value,
    hidden: bool,
    media_only: bool,
    pinned: bool,
    view_count: Option<String>,
    selftext_html: Option<String>,
    allow_live_comments: bool,
    media_embed: Value,
    num_crossposts: u32,
    is_crosspostable: bool,
    is_video: bool,
    domain: String,
    contest_mode: bool,
    link_flair_css_class: Option<String>,
    
}


#[derive(Debug)]
#[derive(Serialize, Deserialize)]
pub struct T1 {
        total_awards_received: u32,
        approved_at_utc: Option<String>,
        ups: u32,
        mod_reason_by: Option<String>,
        banned_by: Option<String>,
        author_flair_type: Option<String>,
        removal_reason: Option<String>,
        link_id: String,
        author_flair_template_id: Option<String>,
        likes: Option<u32>,
        no_follow: bool,
        #[serde(deserialize_with = "empty_string_as_none")]
        replies: Box<Listing>,
        user_reports: Vec<String>,
        saved: bool,
        id: String,
        banned_at_utc: Option<u32>,
        mod_reason_title: Option<String>,
        gilded: u32,
        archived: bool,
        report_reasons: Option<String>,
        author: String,
        can_mod_post: bool,
        send_replies: bool,
        parent_id: String,
        score: u32,
        author_fullname: String,
        approved_by: Option<String>,
        all_awardings: Value,
        subreddit_id: String,
        body: String,
        // urg, this can be bool or u32
        // edited: bool,
        author_flair_css_class: Option<String>,
        is_submitter: bool,
        downs: u32,
        author_flair_richtext: Vec<String>,
        author_patreon_flair: bool,
        collapsed_reason: Option<String>,
        body_html: String,
        stickied: bool,
        subreddit_type: String,
        can_gild: bool,
        gildings: Map<String, Value>,
        author_flair_text_color: Option<String>,
        score_hidden: bool,
        permalink: String,
        num_reports: Option<i32>,
        locked: bool,
        name: String,
        created: u32,
        subreddit: String,
        author_flair_text: Option<String>,
        collapsed: bool,
        created_utc: u32,
        subreddit_name_prefixed: String,
        controversiality: u32,
        depth: u32,
        author_flair_background_color: Option<String>,
        mod_reports: Vec<String>,
        mod_note: Option<String>,
        distinguished: Option<String>,
}

impl T1 {

    pub fn walk(&self) {
        self._walk(0);
    }

    // TODO: Make this yield references to instances
    fn _walk(&self, depth: u32) {
        println!("{}", self);
        for t1 in self.replies.extract_t1s().iter() {
            t1._walk(depth + 1);
        }
    }

}

impl Display for T1 {

    fn fmt(&self, f: &mut Formatter) -> fmt::Result {
        write!(f, "T1 {{\n\
            \tauthor {}\n\
            \tscore: {}\n\
            \tdepth: {}\n\
            \treplies count: {}\n}} ",
            self.author, self.score, self.depth, self.replies.children.len())
    }
}


#[derive(Debug)]
#[derive(Serialize, Deserialize)]
pub struct More {
    count: u32,
    name: String,
    id: String,
    parent_id: String,
    depth: u32,
    children: Vec<String>,
}


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
    fn test_parse() -> Result<(), Box<std::error::Error>> {

        assert!(true);
        Ok(())
    }

}

