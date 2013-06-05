class SplayTree(object):
  """Splay Tree object.

  A splay tree is a self balancing binary search tree with operations that run 
  in O(log(n)) amortized time where n is the number of entries in the tree. 
  This particular implementation only holds keys, no associated values.

  Member Variables:
    _size the number of entries in this splay tree.
    _root the root of this tree; an empty tree has a value of None.

  """

  def __init__(self):
    """Initialize an empty splay tree object."""

    self._size = 0
    self._root = None

  def __len__(self):
    """Return the size(number of entries) of the splay tree."""

    return self._size

  def insert(self,key):
    """Insert an item into the splay tree, increasing its size.

    Keys will be inserted in O(log(n)) amortized time and then splayed to the
    root of the tree. Duplicates are allowed; find() will return an arbitrary
    entry.

    """
    if self._root:
      node = insertHelper(key,self._root)
      self.splay(node)
    else:
      self._root = TreeNode(key)
    self._size+=1

  def insertHelper(self,key,node):
    """Insert an item into the splay tree given a node.

    Recursive helper function that inserts keys into a binary tree. The node
    that the key is inserted to is returned.

    """
    if key < node.entry:
      if node.left:
        return self.insertHelper(key,node.left)
      else:
        node.left = TreeNode(key,parent=node)
        return node
    else:
      if node.right:
        return self.insertHelper(key,node.right)
      else:
        node.right = TreeNode(key,parent=node)
        return node

  def binaryHelper(self,key,node):
    """Find a node that is right for the given key.

    Recursive helper function that returns the node that suits the key.
    If the key is not currently in the tree, return the parent node. If the key
    is already in the tree, return the node that contains it.

    """
    if key < node.entry:
      if node.left:
        return self.binaryHelper(node.left)
      else:
        return node #Return the parent node
    else:
      if node.right:
        return self.binaryHelper(key,node.right)
      else:
        return node

  def find(self,key):
    

  def remove(self,key):
    """Remove an item from the splay tree.

    Given a key, it will be removed in O(log(n)) amortized time and its parent 
    will be splayed to the root of the tree. If the operation is successful,
    the value of the key will be returned, otherwise, a value of None will be
    returned. Calling remove() on a duplicate key will result in an arbitrary
    key being removed.

    """
    #TODO:Implement


  def splay(self,node):
    """Splay a node up to the root.

    Mutate this splay tree so that the given node becomes the root of the tree.
    There are three named cases:

    zig-zig:
      The node is a right child of a right child OR a left of a left.
      In this case, rotate up through the parent, then through the grandparent.
    zig-zag:
      The node is a right child of a left child OR a left of a right.
      In this case, rotate the parent up through the grandparent, then rotate
      the node up through the parent.
    zig(base-case):
      The node is either a right child or a left child of the root. Rotate up.

    When the given node is the root of the tree, stop recursion.

    """
    if node == self.root:
      return
    elif node.parent == self.root: #Zig
      if (node.parent).left == node:
        return rotateRight(node)
      elif (node.parent).right == node:
        return rotateLeft(node)
    #right left zig-zag
    elif (node.parent.right == node) and (node.parent.parent.left == node.parent):
      rotateLeft(node)
      rotateRight(node)
    #left right zig-zag
    elif (node.parent.left == node) and (node.parent.parent.right == node.parent):
      rotateRight(node)
      rotateLeft(node)
    #left zig-zig
    elif (node.parent.left == node) and (node.parent.parent.left == node.parent):
      rotateRight(node.parent)
      rotateRight(node)
      return splay(node)#recurse
    #right zig-zig
    elif (node.parent.right == node) and (node.parent.parent.right == node.parent):
      rotateLeft(node.parent)
      rotateLeft(node)
      return splay(node)#recurse

  def rotateRight(self,node):
    """Rotate a given node right in the tree.

          P                         n
         / \    rotateRight()      / \
        n   ^   ------------>     ^   P
       / \ /C\                   /A\ / \
      ^  ^                           ^  ^
     /A\/B\                         /B\/C\

    """
    node.parent.left = node.right
    node.right.parent = node.parent
    node.right = node.parent
    node.right.parent = node
    node.parent = node.parent.parent
    if node.parent: #If node's new parent is not None
      if node.parent.left == node.right:
        node.parent.left = node
      elif node.parent.right == node.right:
        node.parent.right = node

  def rotateLeft(self,node):
    """Rotate a given node left in the tree.
       P                           n
      / \        rotateLeft()     / \
     ^   n       ---------->     P   ^
    /A\ / \                     / \ /C\
        ^  ^                   ^  ^
       /B\/C\                 /A\/B\

    """
    node.parent.right = node.left
    node.left.parent = node.parent
    node.left = node.parent
    node.left.parent = node
    node.parent = node.parent.parent
    if node.parent: #If node's new parent is not None
      if node.parent.left == node.left:
        node.parent.left = node
      elif node.parent.right == node.left:
        node.parent.right = node

class TreeNode(object):
  """Tree Node object.

  A tree node is an entry within a binary tree. 

  Member Variables:
    entry the item that this node contains.
    parent the parent of this node.
    left the left child node which has an entry less than this node.
    right the right child node which has an entry less than this node.

  """

  def __init__(self,key,parent=None,left=None,right=None):
    self.entry = key
    self.parent = parent
    self.left = left
    self.right = right
