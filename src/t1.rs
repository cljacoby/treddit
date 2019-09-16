extern crate serde;
extern crate serde_json;

use std::fmt::{self, Formatter, Display};
use serde::{Serialize, Deserialize};
use serde_json::{Value, Map};

use crate::listing::{Listing, deserialize_replies};


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
        #[serde(deserialize_with = "deserialize_replies")]
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
