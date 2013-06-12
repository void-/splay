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
  #print "Run:",testsRun," Success:",successes," Failure:",(testsRun-successes)

def testInsert(N):
  """Test if SplayTree can be inserted into without raising an exception."""
  s = SplayTree()
  for i in range(N):
    s.insert(i,None)
  return True #No exceptions raised

def testInsertLength(N):
  s = SplayTree()
  for i in range(N):
    s.insert(i,None)
  return len(s) == N

def testRemoveLength(N,R):
  s = SplayTree()
  if R > N:
    raise ValueError("N must be greater than R")
  for i in range(N):
    s.insert(i,None)

  c = R
  for i in range(N):
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
  s = SplayTree()
  for i in range(N):
    s.insert(i,None)
  for i in range(N):
    s.remove(i)
  return True #No exceptions raised

def testFind(N):
  s = SplayTree()
  for i in range(N):
    s.insert(i,1)
  for i in range(N):
    a = s.find(i)
    if not a:
      print "Error: Key not found"
      return False
    N-=a
  return (N==0)

def testContains(N):
  """Known bug: If the value saved evaluates to False, the in operator always
  returns false.
  """
  s = SplayTree()
  for i in range(N):
    s.insert(i,True)
    N-=(i in s)
  return (N==0)

if __name__ == "__main__":
  testAll()

#Splay tree for manual tests
import random
s = SplayTree()
for i in range(10):
  s.insert(random.randint(0,100),i)
