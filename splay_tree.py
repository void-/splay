class SplayTree(object):
  """Splay Tree object.

  A splay tree is a self balancing binary search tree with operations that run 
  in O(log(n)) amortized time, where n is the number of entries in the tree. 
  This particular implementation uses a dictionary interface; it may be
  extended to use a key only interface however.

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

  def insert(self, key, value):
    """Insert an item into the splay tree, increasing its size.

    Keys will be inserted in O(log(n)) amortized time and then splayed to the
    root of the tree. Duplicates are **not** allowed in the sense that only
    one copy of a key is allowed in the tree at a time. Further insertions
    with that key will overwrite previous keys.

    """
    if self._root:
      node = self.binaryHelper(key,self._root)
      if key == node.key: #Replace a duplicate key
        node._key = key
        node._value = value
        return
      elif key < node.key:
        node.left = TreeNode(key,value,node)
        node = node.left
      elif key > node.key:
        node.right = TreeNode(key,value,node)
        node = node.right
      self.splay(node)
    else:
      self._root = TreeNode(key,value)
    self._size+=1

  def insertHelper(self, key, node):
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

  def find(self, key):
    """Return the value that corresponds to the given key.

    Search the tree for the given key and return its corresponding value in 
    O(log(n)) amortized time. If the key is not in this tree, return None. 
    The node that the search ends on is splayed to the root of the tree. No 
    duplicates are allowed in this implementation.

    """
    if self._root:
      node = self.binaryHelper(key,self._root)
      self.splay(node) #Splay the found node to the root
      if node.key == key:
        return node.value

  def __contains__(self, key):
    """Determine if a given key is within the tree. Wrapper for find().
    
    This function returns false negatives if the entries in the tree are None.
    """

    return (self.find(key) != None)

  def remove(self, key):
    """Remove an item from the splay tree.

    Given a key, it will be removed in O(log(n)) amortized time and its parent 
    will be splayed to the root of the tree. If the operation is successful,
    the size of the tree will decrease be one and the value of the key will be 
    returned, otherwise, a value of None will be returned. Calling remove() on 
    a duplicate key will result in an arbitrary key being removed.

    """

    if not self._root: #nothing to remove
      return
    remove = self.binaryHelper(key, self._root)
    splayMe = None
    #remove is not None
    if remove.key != key: #node is not in the tree
      splayMe = remove
    elif remove is self._root:
      assert not remove.parent
      if not remove.left and not remove.right: #0 children
        self._root = None
      elif remove.left and not remove.right: #left child only
        self._root = remove.left
        remove.left.parent = None
        remove.left = None
      elif remove.right and not remove.left: #right child only
        self._root = remove.right
        remove.right.parent = None
        remove.right = None
      elif remove.right and remove.left: #both children
        replace = self.minNode(remove.right)
        assert replace
        assert not replace.left

        if replace is remove.right:
          replace.left = remove.left
          replace.left.parent = replace
          remove.left = None
          replace.parent = None
          remove.right = None
          self._root = replace
        else:
          assert replace.isLeftChild
          replace.left = remove.left
          replace.left.parent = replace
          remove.left = None
          if replace.right:
            replace.right.parent = replace.parent
            replace.parent.left = replace.right
          else:
            replace.parent.left = None
          replace.parent = None
          remove.right.parent = replace
          replace.right = remove.right
          remove.right = None
          self._root = replace

    else: #handle not root
      assert remove.parent
      if not remove.left and not remove.right: #0 children
        if remove.isLeftChild:
          remove.parent.left = None
        elif remove.isRightChild:
          remove.parent.right = None
        splayMe = remove.parent
        remove.parent = None
      elif remove.left and not remove.right: #left child only
        if remove.isLeftChild:
          remove.parent.left = remove.left
          remove.left.parent = remove.parent
          remove.left = None
          splayMe = remove.parent
          remove.parent = None
        elif remove.isRightChild:
          remove.parent.right = remove.left
          remove.left.parent = remove.parent
          remove.left = None
          splayMe = remove.parent
          remove.parent = None
      elif remove.right and not remove.left: #right child only
        if remove.isLeftChild:
          remove.parent.left = remove.right
          remove.right.parent = remove.parent
          remove.right = None
          splayMe = remove.parent
          remove.parent = None
        elif remove.isRightChild:
          remove.parent.right = remove.right
          remove.right.parent = remove.parent
          remove.right = None
          splayMe = remove.parent
          remove.parent = None
      elif remove.left and remove.right: #both children
        splayMe = replace = self.minNode(remove.right)
        assert replace
        assert not replace.left

        if remove.isLeftChild:
          if replace is remove.right:
            replace.left = remove.left
            replace.left.parent = replace
            remove.left = None
            remove.parent.left = replace
            replace.parent = remove.parent
            remove.parent = None
          else:
            assert replace.isLeftChild
            replace.left = remove.left
            replace.left.parent = replace
            remove.left = None
            if replace.right:
              replace.parent.left = replace.right
              replace.right.parent = replace.parent
            else:
              replace.parent.left = None
            replace.right = remove.right
            replace.right.parent = replace
            remove.right = None
            replace.parent = remove.parent
            replace.parent.left = replace
            remove.parent = None
        elif remove.isRightChild:
          if replace is remove.right:
            replace.left = remove.left
            replace.left.parent = replace
            remove.left = None
            remove.parent.right = replace
            replace.parent = remove.parent
            remove.parent = None
          else:
            assert replace.isLeftChild
            replace.left = remove.left
            replace.left.parent = replace
            remove.left = None
            if replace.right:
              replace.right.parent = replace.parent
              replace.parent.left = replace.right
            else:
              replace.parent.left = None
            replace.right = remove.right
            replace.right.parent = replace
            remove.right = None
            replace.parent = remove.parent
            replace.parent.right = replace
            remove.parent = None
    self.splay(splayMe)
    self._size -= 1

  def _removeRoot():
    """Remove the root from the tree.

    Helper function that removes the root from the tree and links up its
    replacement.

    The root either has one or both children, but no parent
    
    """

  def _removeParented(remove):
    """Remove a node in the tree that has a parent.

    Helper function given a node that has a parent, removes the node from the
    tree regardless of how many children it has.

    """
    #remove has a parent
    #unknown what kind of child remove is
    c = self.minNode(remove.right)
    if not c: #no right child ; left child unknown
      remove.parent


  def minNode(self, node):
    """Return the node that contains the minimum key.

    Helper function that returns the node with the minimum key in a tree given
    the root of that tree. If the given node is None, return None.

    """
    if not node or not node.left:
      return node
    return self.minNode(node.left)

  def maxNode(self, node):
    """Return the node that contains the maximum key.

    Helper function that returns the node with the maximum key in a tree given
    the root of that tree.

    """
    if not node or not node.right:
      return node
    return self.maxNode(node.right)

  def binaryHelper(self, key, node):
    """Find a node that is *right* for the given key.

    Helper function that returns the node that suits the key. If the key is not 
    currently in the tree, return the parent node. If the key is already in the
    tree, return the node that contains it. This function returns None if the 
    given node is equal to None.

    """
    if not node or key == node.key:
      return node
    elif key < node.key:
      if node.left:
        return self.binaryHelper(key,node.left)
      else:
        return node #Return the parent node
    elif key > node.key:
      if node.right:
        return self.binaryHelper(key,node.right)
      else:
        return node

  def splay(self, node):
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

    When the given node is the root of the tree, stop recursion. If node is
    None, return.

    """
    if not node or node is self._root:
      return
    elif node.parent is self._root: #Zig
      if node.isLeftChild:
        return self.rotateRight(node)
      elif node.isRightChild:
        return self.rotateLeft(node)
    #right left zig-zag
    elif node.isRightChild and node.parent.isLeftChild:
      self.rotateLeft(node)
      self.rotateRight(node)
    #left right zig-zag
    elif node.isLeftChild and node.parent.isRightChild:
      self.rotateRight(node)
      self.rotateLeft(node)
    #left zig-zig
    elif node.isLeftChild and node.parent.isLeftChild:
      self.rotateRight(node.parent)
      self.rotateRight(node)
    #right zig-zig
    elif node.isRightChild and node.parent.isRightChild:
      self.rotateLeft(node.parent)
      self.rotateLeft(node)
    return self.splay(node)#recurse

  def rotateRight(self, node):
    """Rotate a given node right in the tree.

          P                         n
         / \    rotateRight()      / \
        n   ^   ------------>     ^   P
       / \ /C\                   /A\ / \
      ^  ^                           ^  ^
     /A\/B\                         /B\/C\

    >>> s = SplayTree()
    >>> a = TreeNode(3,0)
    >>> b = TreeNode(2,1)
    >>> b.parent = a
    >>> c = TreeNode(1,2)
    >>> c.parent = b
    >>> s._root = a
    >>> s._root.left = b
    >>> s._root.left.left = c
    >>> s.rotateRight(b)
    >>> s._root is b
    True
    >>> s._root.left is c
    True
    >>> s._root.right is a
    True

    """
    node.parent.left = node.right
    if node.right:node.right.parent = node.parent
    node.right = node.parent
    node.parent = node.parent.parent
    node.right.parent = node
    if node.parent: #If node's new parent is not None
      if node.parent.left is node.right:
        node.parent.left = node
      elif node.parent.right is node.right:
        node.parent.right = node
    else:
      self._root = node

  def rotateLeft(self, node):
    """Rotate a given node left in the tree.
       P                           n
      / \        rotateLeft()     / \
     ^   n       ---------->     P   ^
    /A\ / \                     / \ /C\
        ^  ^                   ^  ^
       /B\/C\                 /A\/B\

    """
    node.parent.right = node.left
    if node.left:node.left.parent = node.parent
    node.left = node.parent
    node.parent = node.parent.parent
    node.left.parent = node
    if node.parent: #If node's new parent is not None
      if node.parent.left is node.left:
        node.parent.left = node
      elif node.parent.right is node.left:
        node.parent.right = node
    else:
      self._root = node

  def __str__(self):
    """Return the string representation of the tree.
    
    Return a string representing the tree sideways.
    Left nodes are below its parent, right above. Each level is indented with
    two spaces.
    
    """
    q = []
    def traversalHelper(n, d=0):
      if not n:
        return
      traversalHelper(n.right, d+1)
      q.append((d, n))
      traversalHelper(n.left, d+1)
    traversalHelper(self._root)

    return "".join(p[0]*"  "+str(p[1].key)+":"+str(p[1].value)+"\n" for p in q)

class TreeNode(object):
  """Tree Node object.

  A tree node is an entry within a binary tree that holds a key value pair.

  Member Variables:
    _key the key that this node contains. TreeNodes are searched by key.
    _value the value that corresponds to the stored key.
    parent the parent of this node.
    left the left child node which has a key less than this node.
    right the right child node which has a key less than this node.

  """

  def __init__(self, key, value, parent=None, left=None, right=None):
    """Initialize a Tree Node object given certain values."""

    self._key = key
    self._value = value
    self.parent = parent
    self.left = left
    self.right = right

  @property
  def key(self):
    """Return the key stored by this tree node."""
    return self._key

  @property
  def value(self):
    """Return the value stored by this tree node."""
    return self._value

  @property
  def isLeftChild(self):
    """Return whether this node is a left child."""
    if self.parent:
      return (self.parent).left is self

  @property
  def isRightChild(self):
    """Return whether this node is a right child."""
    if self.parent:
      return (self.parent).right is self

if __name__ == "__main__":
  s = SplayTree()
  from random import randint
  r = set()
  #s.splay = lambda a: None
  for i in xrange(20):
    a = randint(-10000, 10000)
    r.add(a)
    s.insert(a, True)
