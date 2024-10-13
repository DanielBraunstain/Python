#Alex

import unittest
import bst as b



class TestBST(unittest.TestCase):

    def setUp(self):

        def compare_func(x,y) -> int:
            if x < y:
                return -1
            elif x > y:
                return 1
            else:
                return 0

        self.bst = b.BST(compare = compare_func)

    def tearDown(self):
        pass

    def test_is_empty(self):
        self.assertTrue(self.bst.is_empty())
        self.bst.insert(10)
        self.assertFalse(self.bst.is_empty())
        self.bst.remove(10)
        self.assertTrue(self.bst.is_empty())

    def test_length(self):
        self.assertEqual(self.bst.length, 0)
        self.bst.insert(10)
        self.bst.insert(5)
        self.assertEqual(self.bst.length, 2)
        self.bst.remove(10)
        self.assertEqual(self.bst.length, 1)
        self.bst.remove(5)
        self.assertEqual(self.bst.length, 0)

    def test_insert(self):
        self.bst.insert(10)
        self.bst.insert(5)
        self.bst.insert(15)
        self.bst.insert(2)
        self.bst.insert(15)
        self.bst.insert(12)
        self.assertEqual(self.bst.root.value, 10)
        self.assertEqual(self.bst.root.right.value, 15)
        self.assertEqual(self.bst.root.right.left.value, 12)
        self.assertEqual(self.bst.root.right.right.value, 15)
        self.assertEqual(self.bst.root.left.value, 5)
        self.assertEqual(self.bst.root.left.left.value, 2)
        self.assertIsNone(self.bst.root.left.left.left) #checking 2 is a leaf
        self.assertIsNone(self.bst.root.left.left.right)



    def test_remove(self):
        self.assertFalse(self.bst.remove(3)) #remove from empty tree


        self.bst.insert(10)
        self.assertTrue(self.bst.remove(10)) #delete from a tree with only a root
        self.assertEqual(self.bst.root, None)

        self.bst.insert(10) #delete the root when it has 1 child only
        self.bst.insert(5)
        self.assertTrue(self.bst.remove(10))
        self.assertEqual(self.bst.root.value, 5)
        self.assertTrue(self.bst.remove(5))
        self.assertEqual(self.bst.root, None)

        self.bst.insert(10)
        self.bst.insert(5)
        self.bst.insert(15)
        self.bst.insert(2)
        self.bst.insert(15)
        self.bst.insert(12)
        self.bst.insert(14)

        self.assertFalse(self.bst.remove(7))# remove non existent node
        self.assertEqual(self.bst.length, 7) #checking length stayed the same
        self.assertTrue(self.bst.remove(10)) # delete node with 2 children
        self.assertEqual(self.bst.root.value, 12)
        self.assertEqual(self.bst.length, 6)

        self.assertTrue(self.bst.remove(5)) # delete node with left child only
        self.assertEqual(self.bst.root.left.value, 2)
        self.assertEqual(self.bst.length, 5)

        self.assertTrue(self.bst.remove(2)) # delete node with 0 children
        self.assertEqual(self.bst.root.left, None)
        self.assertEqual(self.bst.length, 4)

        self.assertTrue(self.bst.remove(12)) #delete node with right child only
        self.assertEqual(self.bst.root.value, 15)
        self.assertEqual(self.bst.length, 3)

        self.assertTrue(self.bst.remove(15))
        self.assertTrue(self.bst.remove(15))
        self.assertTrue(self.bst.remove(14))
        self.assertTrue(self.bst.is_empty())





    def test_for_each(self):
        self.bst.insert(10)
        self.bst.insert(5)
        self.bst.insert(15)
        self.bst.insert(2)

        data_of_nodes = []


        self.bst.for_each("in", lambda x: data_of_nodes.append(2*x))
        self.assertEqual([4,10,20,30],data_of_nodes)

        data_of_nodes.clear()

        self.bst.for_each("pre", lambda x: data_of_nodes.append(2*x))
        self.assertEqual([20, 10, 4, 30], data_of_nodes)

        data_of_nodes.clear()

        self.bst.for_each("post", lambda x: data_of_nodes.append(2*x))
        self.assertEqual([4, 10, 30, 20], data_of_nodes)


    def test_contain(self):
        self.bst.insert(10)
        self.bst.insert(5)
        self.bst.insert(2)
        self.assertTrue(5 in self.bst)
        self.assertFalse(15 in self.bst)


















if __name__ == '__main__':
    unittest.main()