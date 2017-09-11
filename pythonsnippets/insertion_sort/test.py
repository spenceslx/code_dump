import insertion_sort
import unittest

class InsertionSortTestCase(unittest.TestCase):
    def test_list1(self):
        self.assertEqual(insertion_sort.Insertion_Sort([2,1,10,5]), [1,2,5,10])

    def test_list2(self):
        self.assertEqual(insertion_sort.Insertion_Sort([0,0,0,0,0,0]), [0,0,0,0,0,0])
	
    def test_list3(self):
        self.assertEqual(insertion_sort.Insertion_Sort([-10,4,-2,7,9,7]), [-10,-2,4,7,7,9])



if __name__ == '__main__':
	#unittest.main()
	suite = unittest.TestLoader().loadTestsFromTestCase(InsertionSortTestCase)
	unittest.TextTestRunner(verbosity=2).run(suite)



