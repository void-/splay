from splay_tree import SplayTree

def testAll():
  """Execute a series of tests, print out results, return success."""
  N = 100
  R = 30

  print "testInsert",testInsert(N)
  print "testInsertLength",testInsertLength(N)
  print "testRemove",testRemove(N)
  print "testRemoveLength",testRemoveLength(N,R)
  print "testFind",testFind(N)
  print "testContains",testContains(N)
  print "testRemoveDeep",testRemoveDeep(N,R)

  print "Tests Complete"

def testInsert(N):
  """Test if SplayTree can be inserted into without raising an exception."""

  s = SplayTree()
  for i in xrange(N):
    s.insert(i,None)
  return True #No exceptions raised

def testInsertLength(N):
  """Test if insertions into a splay tree result in the correct length."""

  s = SplayTree()
  for i in xrange(N):
    s.insert(i,None)
  return len(s) == N

def testRemoveLength(N,R):
  """Test if insertions into a splay tree result in the correct length."""

  s = SplayTree()
  if R > N:
    raise ValueError("N must be greater than R")
  for i in xrange(N):
    s.insert(i,None)

  c = R
  for i in xrange(N):
    if c <= 0:
      break
    s.remove(i)
    c-=1
  if not (len(s) == (N-R)):
    print "Error: Wrong Length"
    print "Tree is "+str(len(s))
    print "Tree should have: "+str(N-R)
  return (len(s) == (N-R))

def testRemove(N):
  """Test if a splay tree can be inserted into and removed without error."""

  s = SplayTree()
  for i in xrange(N):
    s.insert(i,None)
  for i in xrange(N):
    s.remove(i)
  return True #No exceptions raised

def testFind(N):
  """Test if items inserted into the splay tree can be found again."""

  s = SplayTree()
  for i in xrange(N):
    s.insert(i,1)
  for i in xrange(N):
    a = s.find(i)
    if not a:
      print "Error: Key not found"
      return False
    N-=a
  return (N==0)

def testContains(N):
  """Test if the number of items inserted into the tree can be found again."""

  s = SplayTree()
  for i in xrange(N):
    s.insert(i,True)
    N-=(i in s)
  return (N==0)

def testRemoveDeep(N,R):
  """Test if removing an item from the tree updates it correctly. 

  An error will occur if the internal structure of the tree is not the same
  before and after the insert/remove. If the tree splays, an error will occur.
  
  """
  s = SplayTree()
  treeStructure = ""
  for i in xrange(N):
    treeStructure = str(s)
    s.insert(i,1)
    s.remove(i)
    if treeStructure != str(s):
      print "Error: Key wasn't properly removed"
      return False
  return True

if __name__ == "__main__":
  testAll()

#Construct a splay tree for manual tests
import random
s = SplayTree()
for i in xrange(10):
  s.insert(random.randint(0,100),i)
