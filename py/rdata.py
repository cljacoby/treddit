#!/usr/bin/env python3

import json
import os
import requests

# debug imports. remove later.
from pprint import pprint
from types import SimpleNamespace


# List of TODO's:
#   * setup as actual python package
#   * update the test code
#   * (maybe) refactor data node of RNode to use attributes rather than dictionary keys
#   * consider a better way to do the iter_children/get_chilren and iter_replies/get_replies
#       * maybe render the child nodes at instantiation, but only one level down
#   * Write class or static func to make request to reddit and render comment tree as Thread
#   * Do this directly from .json URL, or using actual oauth api
#   * Expand the walk_dfs and walk_bfs allowing better callbacks on data RNodes
#   * Also add pre-order, in-order, and post-order traversal
#   * (maybe) add support for filling the More instaces in
#   * Add better __str__ and __repr__ methods to make terminal data analysis qucicker/easier
#   * double check the schema definitions
#   * (maybe) convert the schema confs to JSON config files and read that way 
#   * (maybe) rather than walk_dfs taking a callback, its just an iterable. or both methods are offered


# ===============================================================
# === util ======================================================
# ===============================================================

# TODO: At some point, create an actual package structure and turn
# this into a module.

class util(object):
    """Defined as class of staticmethods. Later, consider replacing
    this with a seperate py module of utility functions.
    """

    @staticmethod
    def load_json(path):
        with open(path) as f:
            d = json.load(f)
        return d

    @staticmethod
    def is_iterable(i):
        try:
            g = iter(i)
            return True
        except TypeError as te:
            return False

    @staticmethod
    def read_json(path):
        with open(path) as f:
            d = json.load(f)
            return d

# ===============================================================
# ===  exceptions  ==============================================
# ===============================================================
class RDataError(Exception):
    def __init__(self, msg=None, code=None):
        super().__init__(msg)
        self.msg = msg
        self.code = code

class RSchemaError(Exception):
    def __init__(self, msg=None, code=None):
        super().__init__(msg)
        self.msg = msg
        self.code = set()

class RSchematicError(Exception):
    def __init__(self, msg=None, code=None):
        super().__init__(msg)
        self.msg = msg
        self.code = code

# ===============================================================
# ===  RSchematic ===============================================
# ===============================================================
class RSchematic(object):
    """A single Schema instance for an RNode schema. For example, in a `Listing`,
    there is a field named `modhash` which is of the single type `str` and is
    nullable.
    """

    def __init__(self, name, types, nullable):
        # init proxy'd inner properties
        self._name = "_old_no_name_"
        self._types = set()
        self._nullable = False
        # set initial values via setters
        self.name = name
        self.types = types
        self.nullable = nullable

    """name getter/setted/validation
    """
    
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        self.validate_name(new_name)
        self._name = new_name

    def validate_name(self, name):
        if type(name) != str:
            raise RSchematicError("name must be string")

    """types getter/setter/validation
    """

    @property
    def types(self):
        return self._types

    # TODO: Is this is_iterable use actually kosher? What if its a custom class?
    @types.setter
    def types(self, new_types):
        if util.is_iterable(new_types):
            new_types = set(new_types)
        else:
            new_types = set([new_types])
        self.validate_types(new_types)
        self._types = new_types

    def validate_types(self, types):
        for t in types:
            if type(t) != type:
                raise RSchematicError("types must be iterable of type instances")

    """nullable getter/setter/validation
    """

    @property
    def nullable(self):
        return self._nullable

    @nullable.setter
    def nullable(self, new_nullable):
        self.validate_nullable(new_nullable)
        self._nullable = new_nullable

    def validate_nullable(self, nullable):
        if type(nullable) != bool:
            raise RSchematicError("nullable must be bool type")

    def __str__(self):
        s = "RNodeSchematic: {" \
            + f"name: '{self.name}', types: {self.types}, nullable: {self.nullable}" \
            + "}"
        return s

    def __repr__(self):
        return self.__str__() 
    
    # this might be un-kosher
    @classmethod
    def is_type(cls, x):
        """Indicate whether argument `x` is the type of this class.
        """
        return type(x) == cls

# ===============================================================
# ===  RSchema ==================================================
# ===============================================================

# This class is basically just a dict. I'm not sure if it actually
# provides extended value over just using an actual dict literal
# instead of an RSchema instance.

class RSchema(object):
    """A schema for an RNode subclass. Defines the expected keys, their types, and if they are nullable.
    """
    # TODO: Make the __key_transform__ function  not generate a new list each call

    def __init__(self):
        # TODO: Add ability to pass inital values
        self.store = {}

    def __len__(self):
        """Length of RSchematic definitions in the RSchema.
        """
        return len(self.store)

    def __getitem__(self, key):
        """Retrieve an RSchematic from the Rschema by the RSchematic name.
        """
        return self.store[key]

    def __iter__(self):
        """Iterate over the RSchema instance by the RSchematic keys.
        """
        return ( key for key in self.store.keys() )

    def __str__(self):
        s = f"RNodeSchemad: {str(self.store)}"
        # s = "[" + ",".join([ str(i)  for i in self.values() ]) + "]"
        return s

    def __contains__(self, x):
        """Indicate if internal RSchematic store has schemtic by key `x`.
        """
        return self.store.get(x) != None

    def __repr__(self):
        return self.__str__()
    
    def add(self, name, types, nullable):
        """Add a Rschematic to the RSchema.
        """
        if name in self.store:
            raise ValueError(f"RnodeSchemaD already containes schematic for `{name}`")
        schematic = RSchematic(name, types, nullable)
        self.store[schematic.name] = schematic

    def remove(self, name):
        """Remove an RSchematic from the RSchema.
        """
        if name not in self.store:
            raise KeyError(f"RNodeSchema has no schematic by name `{name}`")
        del self.store

    def get(self, key, default=None):
        return self.store.get(key, default)
    
    def values(self):
        """Analagous to dict.valeus()
        """
        return ( self.__getitem__(key) for key in self.__iter__() )

    def items(self):
        """Analagous to dict.items()
        """
        return ( (key, self.__getitem__(key)) for key in self.__iter__() )
    
    @staticmethod
    def from_conf(path):
        raise NotImplementedError("from_conf isn't implemented")

    @staticmethod
    def from_dict(d):
        schema = RSchema()
        for name, (types, nullable) in d.items():
            # schematic = RSchematic(name, types, nullable)
            schema.add(name, types, nullable)
        return schema


# ===============================================================
# ===  RNode ====================================================
# ===============================================================

class RNode(object):
    """Base class for all RNodes. Not init'd directly, only via sub-classes.
    """

    #TODO: Maybe define self.data as SimpleNamespace so you can use attrs rather than keys
    # refactor notes:
    #   - would still want to store the original input dict
    #   - maybe rather than SimpleNampespace proxy attributs to dict?
    #   - seems complicated and im not really sure what the benefit is, just sounds cool
    # touches:
    #   - RNode.validate
    #   - Lisitng.children 
    #   - T1.replies
    #   - str and repr methods
    #   - maybe the half implemented methods i started
    # since we're doing the valdiation on the dict input, it kind of makes sense to use attrs
    # because we can succesfully no in the subclass if we'll be able to access the attrs we
    # expect to be there

    # Override this in sub-class with actual value
    KIND =  None
    
    # Schema
    # A list of tuples, each defining a data key.
    # { name: (type, nullable), ... }
    SCHEMA = None

    def __init__(self, _d):
        
        # Set kind with respect to KIND class property 
        kind = _d.get("kind")
        if kind != self.KIND:
            raise ValueError(f"kind should be `{self.KIND}` but got `{kind}`.")
        self.kind = kind
        
        # Make sure `data` dict exists
        data = _d.get("data")
        if data == None:
            raise RDataError("RNode got dict without `data` key")
        self.data = data
        self._data = SimpleNamespace(**self.data) 
        self._d = _d

        # Validate against the class's schema property
        if self.SCHEMA != None:
            self.validate()
            
    def validate(self):
        """Iterate over data values, and check if all key value pairs agree with the schema.
        """
        for key, val in self.data.items():
            schematic = self.SCHEMA.get(key)
            if schematic == None:
                raise RNodeSchemaError(f"RNode got key `{key}` not in schema, or is duplicate key")
            if schematic.nullable and val == None:
                return
            t = type(val)
            if not t in schematic.types:
                raise RSchemaError(f"RNode got val `{val}` for key `{key}` which was not in types `{schematic.types}`")
            return

    def __str__(self):
        s = f"RNode<{self.KIND}>"
        return s

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def resolve(d):
        """Resolve a dictionary to an RNode instance.
        """
        if type(d) != dict:
            raise RDataError("input was not dict")
        data = d.get("data")
        if data == None:
            raise RDataError("input dict did not have `data` key")
        kind = d.get("kind")
        if kind == None:
            raise RDataError("input dict did not have `kind` key")
        if kind == "Listing":
            return Listing(d)
        if kind == "t1":
            return T1(d)
        if kind == "t3":
            return T3(d)
        if kind == "more":
            return More(d)
        raise ValueError("")


    @classmethod
    def from_path(cls, path):
        """Instantiate an RNode sub-class instance from a JSON file path.
        """
        if cls == RNode:
            raise NotImplementedError("from_path must be called on RNode subclass")
        d = util.read_json(path)
        inst = cls(d)
        return inst

# ===============================================================
# ===  Listing ==================================================
# ===============================================================

class Listing(RNode):
    """Internal RNode used for linkage of data structure.
    """
    
    KIND = "Listing"

    SCHEMA = RSchema.from_dict({
        "modhash": (str, True),
        "dist": (str, True),
        "children": (list, False),
        "after": (str, True),
        "before": (str, True),
    })

    def __init__(self, _d):
        super().__init__(_d)

    
    def iter_children(self, no_more=False):
        """Iterate over the Listing's children as generator. 
        """
        d_children = self.data.get("children")
        children = ( RNode.resolve(i) for i in d_children )
        include = lambda node: True
        if no_more:
            include = lambda node: type(node) != More
        return ( child for child in children if include(child) )

    def get_children(self):
        """Get Listing's children as list.
        """
        children = list(self.iter_children())
        return children

# ===============================================================
# ===  T1 =======================================================
# ===============================================================

class T1(RNode):
    """Comment post.
    """

    KIND = "t1"

    SCHEMA = RSchema.from_dict({
        'subreddit_id': (str, True),
        # Not sure on type
        'approved_at_utc': (bool, True),
        'mod_reason_by': (str, True),
        'banned_by': (str, True),
        'author_flair_type': (str, True),
        'removal_reason': (str, True),
        'link_id': (str, False),
        # Not sure on type
        'author_flair_template_id': (str, True),
        # Not sure on type
        'likes': (str, True),
        'no_follow': (bool, False),
        'replies': (dict, False),
        'user_reports': (list, False),
        'saved': (bool, False),
        'id': (str, False),
        # Not sure on type
        'banned_at_utc': (str, True),
        'mod_reason_title': (str, True),
        'gilded': (int, False),
        'archived': (bool, False),
        # Not sure on type
        'report_reasons': (str, True),
        'author': (str, False),
        'can_mod_post': (bool, False),
        'created_utc': (int, False),
        'send_replies': (bool, False),
        'parent_id': (str, False),
        'score': (int, False),
        'author_fullname': (str, False),
        # Not sure on type
        'approved_by': (str, True),
        'controversiality': (int, False),
        'body': (str, False),
        'edited': (bool, False),
        'author_flair_css_class': (str, True),
        'is_submitter': (bool, False),
        'downs': (int, False),
        'author_flair_richtext': (list, False),
        'author_patreon_flair': (bool, False),
        # Not sure on type
        'collapsed_reason': (str, True),
        'body_html': (str, False),
        'stickied': (bool, False),
        'subreddit_type': (str, False),
        'can_gild': (bool, False),
        'gildings': (dict, False),
        # Not sure on type
        'author_flair_text_color': (str, True),
        'score_hidden': (bool, False),
        'permalink': (str, False),
        'num_reports': (int, True),
        'name': (str, False),
        'created': (int, False),
        'subreddit': (str, False),
        'author_flair_text': (str, True),
        'collapsed': (bool, False),
        'subreddit_name_prefixed': (str, False),
        'ups': (int, False),
        'depth': (int, False),
        # Not sure on type
        'author_flair_background_color': (int, True),
        'mod_reports': (list, False),
        # Not sure on type
        'mod_note': (str, True),
        # Not sure on type
        'distinguished': (str, True),
    })

    def __init__(self, _d):
        super().__init__(_d)

    def __str__(self):
        s = "T1"
        # s = (f"author: {self.data.get('author')}\n\n"
        #     f"body: {self.data.get('body')}\n\n"
        #     f"score: {self.data.get('score')}")
        return s

    def __repr__(self):
        return self.__str__()

    def iter_replies(self, no_more=False):
        d_replies = self.data.get("replies")
        # TODO: Determine if there is a better way to handle when replies is ""
        if d_replies == "":
            return ()
        listing = Listing(d_replies)
        include = lambda node: True
        if no_more:
            include = lambda reply: not isinstance(reply, More)
        replies = ( i for i in listing.iter_children() if include(i) )
        return replies

    def get_replies(self, no_more=False):
        replies = list(self.iter_replies(no_more = no_more))
        return replies


# ===============================================================
# ===  RNode ====================================================
# ===============================================================

class T3(RNode):
    """Submission post.
    """

    KIND = "t3"

    SCHEMA = RSchema.from_dict({
        "approved_at_utc": (bool, True),
        "subreddit": (str, False),
        "selftext": (str, False),
        "user_reports": (list, False),
        "saved": (bool, True),
        "mod_reason_title": (bool, True),
        "gilded": (int, False),
        "clicked": (bool, False),
        "title": (str, False),
        "link_flair_richtext": (str, False),
        "subreddit_name_prefixed": (str, False),
        "hidden": (str, False),
        "pwls": (int, False),
        "link_flair_css_class": (str, False),
        "downs": (int, False),
        "parent_whitelist_status": (str, False),
        "hide_score": (bool, False),
        "name": (str, False),
        "quarantine": (bool, False),
        "link_flair_text_color": (str, False),
        "upvote_ratio": (float, False),
        "author_flair_background_color": (str, True),
        "subreddit_type": (str, False),
        "ups": (int, False),
        "domain": (str, False),
        "media_embed": (dict, False),
        "author_flair_template_id": (str, True),
        "is_original_content": (bool, True),
        "author_fullname": (str, False),
        "secure_media": (str, True),
        "is_reddit_media_domain": (bool, True),
        "is_meta": (bool, False),
        "category": (str, True),
        "secure_media_embed": (dict, False),
        "link_flair_text": (str, False),
        "can_mod_post": (bool, False),
        "score": (int, False),
        "approved_by": (str, True),
        "thumbnail": (str, False),
        "edited": (bool, False),
        "author_flair_css_class": (str, False),
        "author_flair_richtext": (list, False),
        "gildings": (dict, False),
        "content_categories": (str, False),
        "is_self": (bool, False),
        "mod_note": (str, True),
        "created": (int, False),
        "link_flair_type": (int, False),
        "wls": (int, False),
        "banned_by": (str, True),
        "author_flair_type": (str, False),
        "contest_mode": (bool, False),
        "selftext_html": (str, True),
        "likes": (int, True),
        "suggested_sort": (str, True),
        "banned_at_utc": (bool, True),
        "view_count": (int, True),
        "archived": (bool, False),
        "no_follow": (bool, False),
        "is_crosspostable": (bool, False),
        "pinned": (bool, False),
        "over_18": (bool, False),
        "media": (str, True),
        "media_only": (bool, False),
        "link_flair_template_id": (str, False), 
        "can_gild": (bool, False),
        "spoiler": (bool, False),
        "locked": (bool, False),
        "author_flair_text": (str, True),
        "visited": (bool, False),
        "num_reports": (int, True),
        "distinguished": (bool, True),
        "subreddit_id": (str, False),
        "mod_reason_by": (str, True),
        "removal_reason": (str, True),
        "link_flair_background_color": (str, False),
        "id": (str, False),
        "is_robot_indexable": (bool, False),
        "report_reasons": (str, True),
        "author": (str, False),
        "num_crossposts": (int, False),
        "num_comments": (int, False),
        "send_replies": (bool, False),
        "author_patreon_flair": (bool, False),
        "author_flair_text_color": (str, False),
        "permalink": (str, False),
        "whitelist_status": (str, False),
        "stickied": (bool, False),
        "url": (str, False),
        "subreddit_subscribers": (int, False),
        "created_utc": (int, False),
        "mod_reports": (list, False),
        "is_video": (bool, False),
    })

    def __init__(self, _d):
        super().__init__(_d)

    def __str__(self):
        s = "T3"
        # s = (f"author: {self.data.get('author')}\n\n"
        #         f"body: {self.data.get('body')}\n\n"
        #         f"score: {self.data.get('score')}")
        return s

    def __repr__(self):
        return self.__str__()

# ===============================================================
# ===  More =====================================================
# ===============================================================

class More(RNode):
    """More filler post.
    """

    KIND = "more"

    def __init__(self, _d):
        super().__init__(_d)

# ===============================================================
# ===  Thread ===================================================
# ===============================================================



def walk_dfs(self, visit=lambda x: x):
    """The top level depth-first-search walk function on the comment tree.
    """
    for child in self.t1_listing.iter_children(no_more=True):
        self._walk_dfs(child, visit)

def _walk_dfs(self, node, visit=lambda x: x):
    """The interior depth-first-search traversal method.
    """
    if type(node) == More:
        # TODO: Maybe eventually do something with these
        return
    elif type(node) != T1:
        msg = f"Got node that wasn't type `{T1.__name__}, or type `{More.__name__}`"
        raise ValueError(msg)
    else:
        # pre-order traversal only
        visit(node)
        for reply in node.iter_replies():
            self._walk_dfs(reply, visit)


class Thread(object):
    def __init__(self, arr):
        if len(arr) != 2:
            raise RDataError("Thread recieved list not length 2")
        # TODO: Is the order of t3 node and comment thread node gaurenteed?
        self.t3_listing = Listing(arr[0])
        self.t1_listing = Listing(arr[1])


    def walk_dfs(self):
        """
        """
        for child in self.t1_listing.iter_children(no_more=True):
            yield from self._traverse_dfs(child)

    def _traverse_dfs(self, node):
        yield node
        for reply in node.iter_replies(no_more=True):
            yield from self._traverse_dfs(reply)

    def walk_bfs(self):
        raise NotImplementedError("")

    @staticmethod
    def from_path(path):
        arr = util.read_json(path)
        thread = Thread(arr)
        return thread
   
    # TODO: This needs to be more mature:
    #  - Do actual oauth2 API process
    #  - Set user agent
    #  - Handle request timing
    #  - (maybe) basic validation logic, or try-catch to handle unexecpted API data
    @staticmethod
    def from_url(url):
        resp = requests.get(url)
        d = json.loads(resp.text)
        print(f"request data: {d}")
        thread = Thread(d)
        return thread

# =================================================
# ==== main =======================================
# =================================================

if __name__ == "__main__":
    # thread = Thread("/Users/chris/rust-req/data/api.json")
    # print(thread._d)
    s_t1 = open("./data/t1.json").read()
    d_t1 = json.loads(s_t1)
    t1 = T1(d_t1)
    
    s_t3 = open("./data/t3.json").read()
    d_t3 = json.loads(s_t3)
    t3 = T3(d_t3)

    s_listing = open("./data/listing.json").read()
    d_listing = json.loads(s_listing)
    listing = Listing(d_listing)
    
    thread = Thread.from_path("./data/api.json")
    for i, comment in enumerate(thread.walk_dfs()):
        print(i, comment)

    thread2 = Thread.from_url("https://www.reddit.com/r/worldnews/comments/bhuwat/saudi_arabia_has_repeatedly_helped_saudi_citizens/.json")
    print(thread2)


