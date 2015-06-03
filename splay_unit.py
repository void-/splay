import unittest
import pdb
from random import randint
from splay_tree import SplayTree

class TestSplayBasic(unittest.TestCase):

  def setUp(self):
    self.s = SplayTree()
    #self.mockSplay()

  def mockSplay(self):
    self.s.splay = lambda a : None

  def testConstructor(self):
    """Test if SplayTree can be constructed without raising an exception."""

    SplayTree()
    self.assertIsNotNone(self.s)
    self.assertIsInstance(self.s, SplayTree)

  def testInsert(self):
    """Test if SplayTree can be inserted into without raising an exception."""

    for i in xrange(randint(50,150)):
      self.s.insert(i, None)

  def testInsertLength(self):
    """Test if insertions into a splay tree result in the correct length."""

    num = randint(60,180)
    for i in xrange(num):
      self.s.insert(i, None)
    self.assertEqual(len(self.s), num)

    #try to insert duplicates
    for i in xrange(num):
      self.s.insert(i, None)
    self.assertEqual(len(self.s), num)

  def testRemove(self):
    """Test if a splay tree can be inserted into and removed without error."""

    numIns = randint(70,200)

    for i in xrange(numIns):
      self.s.insert(i, None)
    for i in xrange(numIns):
      self.s.remove(i)

  def testRemoveLengthSimple(self):
    """Test if a simple, insertion and removal result in the correct length."""

    a = randint(-2147483648,2147483647)
    self.s.insert(a, True)
    self.assertEqual(len(self.s), 1)
    self.s.remove(a)
    self.assertEqual(len(self.s), 0)

  def testRemoveLength(self):
    """Test if insertions into a splay tree result in the correct length.

    Use a python set to deal with duplicate insertions.

    """
    numIns = randint(60, 180)
    numRem = (numIns/2) + randint(0, numIns/2)
    ref = set()
    refStatic = set()

    for i in xrange(numIns):
      a = randint(-2147483648,2147483647)
      ref.add(a)
      refStatic.add(a)
      self.s.insert(a,True)

    self.assertEqual(len(self.s), len(ref))
    refLength = len(self.s)
    #pdb.set_trace()
    for i in xrange(numRem):
      self.assertEqual(len(self.s), refLength)
      refLength -=1
      self.s.remove(ref.pop())

    self.assertNotEqual(len(self.s), numIns)
    self.assertEqual(len(self.s), len(ref))

    for i in xrange(numRem): #try to re-remove items
      self.s.remove(refStatic.pop())

  def testFind(self):
    """Test if items inserted into the splay tree can be found again."""

    N = randint(20,150)
    s = SplayTree()
    for i in xrange(N):
      self.s.insert(i,1)
    for i in xrange(N):
      a = self.s.find(i)
      self.assertTrue(a)
      N-=a

    self.assertEqual(N, 0)

  def testContains(self):
    """Test if the number of items inserted into the tree can be re-found."""

    N = randint(20,100)
    for i in xrange(N):
      self.s.insert(i,True)
      N-=(i in self.s)

    self.assertEqual(N,0)

class TestSplayDeep(TestSplayBasic):
  """Test some of the internal features of the splay tree.

  This requires internal access to the members of SplayTree.

  """

  def testMin(self):
    """Test the correctness of SplayTree.minNode."""

    n = randint(50, 170)
    l = []
    for i in xrange(n):
      a = randint(-2147483648,2147483647)
      self.s.insert(a, a)
      l.append(a)

    self.assertIsNotNone(self.s.minNode(self.s._root))
    self.assertEqual(min(l), self.s.minNode(self.s._root).value)

  def testMax(self):
    """Test the correctness of SplayTree.maxNode."""

    n = randint(50, 170)
    l = []
    for i in xrange(n):
      a = randint(-2147483648,2147483647)
      self.s.insert(a, a)
      l.append(a)

    self.assertIsNotNone(self.s.maxNode(self.s._root))
    self.assertEqual(max(l), self.s.maxNode(self.s._root).value)

  def testBinaryHelper(self):
    """Test the correctness of SplayTree.binaryHelper."""

    self.mockSplay() #disable splaying

    #test base-case empty
    self.assertIsNone(self.s.binaryHelper(None, None))
    self.assertIsNone(self.s.binaryHelper(None, self.s._root))

    #test base-case
    self.s.insert(0, None)
    self.assertIsNotNone(self.s.binaryHelper(0, self.s._root))

    #note: binary helper does not splay, but insert does
    n = randint(2,2147483647)
    self.s.insert(n, None)
    self.s.insert(-n, None)

    #find a node that is in the tree
    self.assertIsNotNone(self.s.binaryHelper(n, self.s._root))
    self.assertIsNotNone(self.s.binaryHelper(-n, self.s._root))
    #find the exact node
    self.assertEqual(self.s.binaryHelper(n, self.s._root), self.s._root.right)
    self.assertEqual(self.s.binaryHelper(-n, self.s._root), self.s._root.left)
    #find the parent of a non-existant node
    #pdb.set_trace()
    self.assertEqual(self.s.binaryHelper(-1, self.s._root), self.s._root.left)
    self.assertEqual(self.s.binaryHelper(n-1, self.s._root), \
      self.s._root.right)
    #recursively find the parent of a non-existant node
    self.assertEqual(self.s.binaryHelper(n+1, self.s._root), \
      self.s._root.right)
    self.assertEqual(self.s.binaryHelper(-n+1, self.s._root), \
      self.s._root.left)

  def testRemoveDeep(self):
    """Test if removing an item from the tree updates it correctly.

    Do several rounds of inserts and removes and make sure that there are no
    inconsistancies between a splay tree and a python set.

    """
    ref = set()
    #pdb.set_trace()
    for j in xrange(randint(5, 50)):
      N = randint(60, 170)
      R = N/2 + randint(0, N/2) #remove over half the entries
      for i in xrange(N): #add
        a = randint(-2147483648,2147483647)
        self.s.insert(a, True)
        ref.add(a)
        self.assertTrue(a in self.s)
        self.assertTrue(a in ref)
      #ensure both contain equal number of elements
      #self.assertEqual(len(ref), len(self.s))
      for i in xrange(R): #remove
        a = ref.pop()
        self.s.remove(a)
        self.assertFalse(a in self.s)
        self.assertFalse(a in ref)
        #check no extra elements were accidentially deleted
        for j in ref:
          try:
            self.assertTrue(j in self.s)
          except Exception as e:
            print "missing:", j
            print self.s
            print ref
            raise e
      #check consistancy twice
      self.assertEqual(len(ref), len(self.s))
      for i in ref:
        self.assertIsNotNone(self.s.find(i))
      self.assertEqual(len(ref), len(self.s))
      for i in ref:
        self.assertIsNotNone(self.s.find(i))

  def testInsertDeep(self):
    """Test if parent/child relationships in the tree 'seem' ok."""

    #insert
    for i in xrange(randint(50, 180)):
      self.s.insert(randint(-2147483648,2147483647), i)

    #walk through the tree
    self.assertIsNotNone(self.s._root)
    self.assertIsNone(self.s._root.parent)
    self.assertIsNotNone(self.s._root.left)
    self.assertIsNotNone(self.s._root.right)

    def traversalHelper(n):
      if not n:
        return
      self.assertTrue((n.parent.left is n) or (n.parent.right is n))
      traversalHelper(n.left)
      traversalHelper(n.right)

    traversalHelper(self.s._root.left)
    traversalHelper(self.s._root.right)

if __name__ == "__main__":
  unittest.main()
