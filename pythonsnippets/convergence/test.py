#test script for code in convergence.py
import convergence
import numpy
import unittest

#example data:
posn1 = (0,0)
posn2 = (2,3)
posn3 = (-1, 20)
posn4 = (4,20)
posn5 = (1,0)
posn6 = (1,1)
posn7 = (2,2)

array1 = numpy.array([[4,5,6], [1,2,3]])
array2 = numpy.array([[2,1,5],[7,10,3],[3,4,0]])


class Test(unittest.TestCase):
    def test_posn_inside_huh1(self):
        self.assertTrue(convergence.posn_inside_huh(array1, posn1, array1.shape))
    def test_posn_inside_huh2(self):
        self.assertFalse(convergence.posn_inside_huh(array1, posn2, array1.shape))
    def test_posn_inside_huh3(self):
        self.assertFalse(convergence.posn_inside_huh(array1, posn3, array1.shape))
    def test_posn_inside_huh4(self):
        self.assertFalse(convergence.posn_inside_huh(array1, posn4, array1.shape))

    def test_posn_sum1(self):
        self.assertEqual(convergence.posn_sum(array1, posn1), (6,2))
    def test_posn_sum2(self):
        self.assertEqual(convergence.posn_sum(array1, posn2), (0,0))
    def test_posn_sum3(self):
        self.assertEqual(convergence.posn_sum(array1, posn5), (6,2))
    def test_posn_sum4(self):
        self.assertEqual(convergence.posn_sum(array1, posn6), (9,3))
    def test_posn_sum5(self):
        self.assertEqual(convergence.posn_sum(array1, posn7), (3,1))
    def test_posn_sum6(self):
        self.assertEqual(convergence.posn_sum(array2, posn1), (8,2))
    def test_posn_sum7(self):
        self.assertEqual(convergence.posn_sum(array2, posn2), (0,1))
    def test_posn_sum8(self):
        self.assertEqual(convergence.posn_sum(array2, posn6), (15,4))
    def test_posn_sum9(self):
        self.assertEqual(convergence.posn_sum(array2, posn3), (0,0))
    def test_posn_sum10(self):
        self.assertEqual(convergence.posn_sum(array2, posn4), (0,0))

    def test_posn_average1(self):
        self.assertEqual(convergence.posn_average(array1, posn1), 3)
    def test_posn_average2(self):
        self.assertEqual(convergence.posn_average(array1, posn2), 0)
    def test_posn_average3(self):
        self.assertEqual(convergence.posn_average(array1, posn5), 3)
    def test_posn_average4(self):
        self.assertEqual(convergence.posn_average(array1, posn6), 3)
    def test_posn_average5(self):
        self.assertEqual(convergence.posn_average(array1, posn1), 3)
    def test_posn_average6(self):
        self.assertEqual(convergence.posn_average(array2, posn1), 4)
    def test_posn_average7(self):
        self.assertEqual(convergence.posn_average(array2, posn5), 5)
    def test_posn_average8(self):
        self.assertEqual(convergence.posn_average(array2, posn6), 3.75)
    def test_posn_average9(self):
        self.assertEqual(convergence.posn_average(array2, posn7), 3.5)

















unittest.main()
