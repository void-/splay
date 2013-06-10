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

Duplicate keys are not allowed

remove()
  open up Java implementation of remove() from lab; copy; add behavior for splaying

cases:
  remove from an empty tree:Do nothing
  remove an item thats not actually in the tree:splay the node that search ended on
  remove the root(no parent)
  remove an item that has no right subtree
  remove an item who's next largest item is its right item
