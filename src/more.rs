
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

