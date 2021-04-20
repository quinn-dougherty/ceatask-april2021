# JOURNAL

## 15:42, 90 minutes remaining

- solved all unit tests **but balancing** with my first (naive) iteration of `split_at`, that always returns a perfectly balanced tree by always returning a tree with three nodes. For large strings and restrictions on size per node, this would be a nonstarter, so I should keep iterating until I get the correct implementation
- A couple bugs in the starter code are fixed-- namely `this.text.length` where it should have been `len(self.text)` on line 40
- added some tests for my helper functions
- I forget why I implemented `fmap_rope`, I think I had an idea for doing concatenation with it but I didn't write it down so I forgot by the time I finished implementing fmap. Test case is there.
- **Part of me wants to switch out `.to_string` for `__str__`, etc**, in general make the starter code more pythonic, but it's a low priority. I'm also tempted to run the Black autoformatter on this to make it easier to read, but I haven't yet. 


## 

