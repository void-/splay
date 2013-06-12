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

  def insert(self,key,value):
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

  def find(self,key):
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

  def __contains__(self,key):
    """Determine if a given key is within the tree. Wrapper for find()."""
    return bool(self.find(key))

  def remove(self,key):
    """Remove an item from the splay tree.

    Given a key, it will be removed in O(log(n)) amortized time and its parent 
    will be splayed to the root of the tree. If the operation is successful,
    the size of the tree will decrease be one and the value of the key will be 
    returned, otherwise, a value of None will be returned. Calling remove() on 
    a duplicate key will result in an arbitrary key being removed.

    """
    node = self.binaryHelper(key,self._root)
    n = node
    if not node:
      return
    elif node.key != key:#node is not actually in tree
      pass
    elif not node.left or not node.right:#node with single or no child
      if node == self._root:
        self._root = node.left if not node.right else node.right
      else:
        if node.parent.left == node:
          node.parent.left = (node.left if not node.right else node.right)
        else:
          node.parent.right = (node.left if not node.right else node.right)
      self._size-=1
    else:#node must have two children
      r = self.minNode(node.right)#r is guaranteed to be a node
      r.left = node.left
      node.left.parent = r

      if node.right != r:#general case for removing r
        r.parent.left = r.right
        if r.right: r.right.parent = r.parent
        n = r.parent#save as n
        r.right = node.right
        node.right.parent = r

      r.parent = node.parent
      if node == self._root:#link up parents
        self._root = node
      else:
        if node.parent.left == node:
          node.parent.left = r
        else:
          node.parent.right = r
      self._size-=1
    self.splay(n)

  def minNode(self,node):
    """Return the node that contains the minimum key.

    Helper function that returns the node with the minimum key in a tree given
    the root of that tree. If the given node is None, return None.

    """
    if not node or not node.left:
      return node
    return self.minNode(node.left)

  def maxNode(self,node):
    """Return the node that contains the maximum key.

    Helper function that returns the node with the maximum key in a tree given
    the root of that tree.

    """
    if not node or not node.right:
      return node
    return self.minNode(node.right)

  def binaryHelper(self,key,node):
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
    if node == self._root:
      return
    elif node.parent == self._root: #Zig
      if (node.parent).left == node:
        return self.rotateRight(node)
      elif (node.parent).right == node:
        return self.rotateLeft(node)
    #right left zig-zag
    elif (node.parent.right == node) and (node.parent.parent.left == node.parent):
      self.rotateLeft(node)
      self.rotateRight(node)
    #left right zig-zag
    elif (node.parent.left == node) and (node.parent.parent.right == node.parent):
      self.rotateRight(node)
      self.rotateLeft(node)
    #left zig-zig
    elif (node.parent.left == node) and (node.parent.parent.left == node.parent):
      self.rotateRight(node.parent)
      self.rotateRight(node)
      return self.splay(node)#recurse
    #right zig-zig
    elif (node.parent.right == node) and (node.parent.parent.right == node.parent):
      self.rotateLeft(node.parent)
      self.rotateLeft(node)
      return self.splay(node)#recurse

  def splay(self,node):
    """Mock out splay method: do nothing."""
    pass

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
    if node.right:node.right.parent = node.parent
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
    if node.left:node.left.parent = node.parent
    node.left = node.parent
    node.left.parent = node
    node.parent = node.parent.parent
    if node.parent: #If node's new parent is not None
      if node.parent.left == node.left:
        node.parent.left = node
      elif node.parent.right == node.left:
        node.parent.right = node

  def __str__(self):
    from collections import deque
    q = deque()
    n = lambda:None
    q.append(self._root)
    q.append(n)
    a = None
    result = ""
    while len(q) > 1:
      a = q.popleft()
      if a == n:
        result+="\n"
        q.append(a)
      elif a:
        q.append(a.left)
        q.append(a.right)
        result+="  "+str(a.key)+":"+str(a.value)
      else:
        result+="  "
    return result

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

  def __init__(self,key,value,parent=None,left=None,right=None):
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
