//C++ STL Run with g++ command

#include<random>
#include<vector>
#include<iostream>

using namespace std;

//function declaration
void populateVector(vector <int> &A, double m);
void insertionSort(vector <int> &A, unsigned int &numComparisons, clock_t &tempo);
void mergeSortA(vector <int> &A, int p, unsigned int r, int &numComparisons, clock_t &tempo);
void radixSort(vector <int> &A, unsigned int &numComparisons, clock_t &tempo);
//might not need print vector
void printVector(vector<int> A);

//global variables
int array_size;
double rand_bounds;
vector<int> vec;

int main()
{
  cout << "Enter an integer for the size of vector to be sorted (n>1): ";
  cin >> array_size;
  cout << "Enter a real number to bound the random integers of the vector (m>1.0): ";
  cin >> rand_bounds;


  populateVector(vec, rand_bounds);
  cout << "Original vector: ";
  printVector(vec);
  insertionSort(vec);
  cout << "Sorted vector: ";
  printVector(vec);


  return 0;
}
// insertionSort: Vector -> Vector by ref
// Sorts the vector in Ascending Order
void insertionSort(std::vector<int> &A)
{
  for (int j=1; j<A.size(); j++)
  {
    int key = A[j];
    int i = j-1;
    while(i>=0 && A[i]>key)
    {
      A[i+1] = A[i];
      i--;
    }
    A[i+1] = key;
  }
}

// populateVector: Vector Double -> Vector by ref
// fills a vector with random integers uniformly distributed within the bounds
// of [-m,m]. array_size must be prespecified in global as it cannot be a param.
void populateVector(std::vector<int> &A, double m)
{
  //from random.h, generator and distribution classes
  std::default_random_engine gener;
  //to limit the size of each integer
  std::uniform_int_distribution<int> dist(-m,m);
  //delcare iterator
  vector<int>::const_iterator i;
  for (int i=0; i<array_size; i++) A.insert(A.begin(),dist(gener));
}

// printVector: Vector -> Vector
// prints a vector as text to the output stream
void printVector(vector<int> A)
{
  vector<int>::const_iterator ci;
  for (ci=A.begin(); ci != A.end(); ci++)
    cout << *ci << ' ';
  cout << endl;
}
