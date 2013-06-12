splay
=====

Python splay tree

Splay tree implemented in Python with the following dictionary interface:

insert()
find()
remove()

---
Development Notes:

Refactoring for better extensibility and modularity.
  Defining function binaryHelper()-changes policy on duplicate keys.
insertHelper() is now deprecated
Change TreeNode so that key and value are no longer private

When removing a node, is garbage collection considered?

Duplicate keys are not allowed
