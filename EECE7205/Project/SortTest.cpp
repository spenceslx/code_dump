//C++ STL Run with g++ command

#include<random>
#include<vector>
#include<iostream>
#include<limits>
#include<fstream>
#include<string>
#include<unistd.h>

using namespace std;

//function declaration
void populateVector(vector <int> &A, double m, int size);
void insertionSort(vector <int> &A, long &numComparisons, clock_t &tempo);
void mergeSortA(vector <int> &A, int p, unsigned int r, long &numComparisons, clock_t &tempo);
void mergeA(vector <int> &A, int p, int q, int r, long &numComparisons);
void bubbleSort(vector <int> &A, long &numComparisons, clock_t &tempo);
void countingSort(vector <int> A, vector <int> &B, long &numComparisons, clock_t &tempo);
//might not need print vector
void printVector(vector<int> A);

//global variables
vector<int> vec (30000);
vector<int> B (1000000);

int main()
{
  long numComparisons = 0;
  int array_size[] = {5,20,50,100,200,500,1000,2000,5000,10000,20000,30000};
  int num_array_sizes = sizeof(array_size)/sizeof(array_size[0]);
  cout << "num of points: " << num_array_sizes <<endl;
  clock_t t;
  double rand_bounds[] = {10.0, 50.0, 100.0, 200.0, 1000.0, 10000.0, 100000.0, 1000000.0 };
  cout << "\n";
  int iterations;
  float averaged_time = 0;


  //insertionSort
  ofstream fs;
  ofstream comp;
  fs.open("insertionSort.csv");
  comp.open("insertionSortcomp.csv");
  for(int i=0; i<num_array_sizes; i++)
  {
    int iterations;
    float mean = 0;
    float stdev = 0;
    float times[10];
    for (int test=0; test<10; test++)
    {
      vec.resize(array_size[i]);
      populateVector(vec, rand_bounds[1], array_size[i]);
      t = clock();
      insertionSort(vec, numComparisons, t);
      vec.resize(0);
      times[test] = (1000.0 * float(t))/CLOCKS_PER_SEC;
      mean += times[test];
      numComparisons = 0;
    }
    mean = mean/10;
    for (int iter=0; iter<10; iter++) {stdev += pow(times[iter] - mean, 2.0);}
    stdev = sqrt( (1.0/9.0)* stdev);
    cout << "stdev is: " << stdev << endl;
    cout << "mean is: " << mean << endl;
    iterations = 1536.64*pow(stdev, 2.0)/pow(mean, 2.0);
    if (iterations < 5) iterations = 5;
    cout << "array_size of " << array_size[i] << " running for " << iterations << " iterations" <<endl;

    for(int j=0; j<iterations; j++)
    {
      numComparisons = 0;
      vec.resize(array_size[i]);
      populateVector(vec, rand_bounds[1], array_size[i]);
      t = clock();
      insertionSort(vec, numComparisons, t);
      vec.resize(0);
      cout << "numComparisons: " << numComparisons << endl;
      t = (1000.0 * float(t))/CLOCKS_PER_SEC;
      cout << "time: " << t << "ms" << endl << endl;
      averaged_time += (t/iterations);
     }
     fs << array_size[i] << "," << averaged_time << endl;
     comp << array_size[i] << "," << numComparisons << endl;
     averaged_time = 0;

  }
  fs.close();
  comp.close();

  //mergeSortA
  fs.open("mergeSortA.csv");
  comp.open("mergeSortAcomp.csv");
  for(int i=0; i<num_array_sizes; i++)
  {
    int iterations;
    float mean = 0;
    float stdev = 0;
    float times[10];
    for (int test=0; test<10; test++)
    {
      vec.resize(array_size[i]);
      populateVector(vec, rand_bounds[1], array_size[i]);
      t = clock();
      mergeSortA(vec, 0, array_size[i], numComparisons, t);
      vec.resize(0);
      times[test] = (1000.0 * float(t))/CLOCKS_PER_SEC;
      mean += times[test];
      numComparisons = 0;
    }
    mean = mean/10;
    for (int iter=0; iter<10; iter++) {stdev += pow(times[iter] - mean, 2.0);}
    stdev = sqrt( (1.0/9.0)* stdev);
    cout << "stdev is: " << stdev << endl;
    cout << "mean is: " << mean;
    iterations = 1536.64*pow(stdev, 2.0)/pow(mean, 2.0);
    if (iterations < 5) iterations = 5;
    cout << "running for " << iterations << " iterations" <<endl;

    for(int j=0; j<iterations; j++)
    {
      numComparisons = 0;
      vec.resize(array_size[i]);
      populateVector(vec, rand_bounds[1], array_size[i]);
      t = clock();
      mergeSortA(vec, 0, array_size[i], numComparisons, t);
      vec.resize(0);
      cout << "numComparisons: " << numComparisons << endl;
      t = (1000.0 * float(t))/CLOCKS_PER_SEC;
      cout << "time: " << t << "ms" << endl << endl;
      averaged_time += (t/iterations);
    }
    fs << array_size[i] << "," << averaged_time << endl;
    comp << array_size[i] << "," << numComparisons << endl;
    averaged_time = 0;
  }
  fs.close();
  comp.close();

  //bubbleSort
  fs.open("bubbleSort.csv");
  comp.open("bubbleSortcomp.csv");
  for(int i=0; i<num_array_sizes; i++)
  {
    int iterations;
    float mean = 0;
    float stdev = 0;
    float times[10];
    for (int test=0; test<10; test++)
    {
      vec.resize(array_size[i]);
      populateVector(vec, rand_bounds[1], array_size[i]);
      t = clock();
      bubbleSort(vec, numComparisons, t);
      vec.resize(0);
      times[test] = (1000.0 * float(t))/CLOCKS_PER_SEC;
      mean += times[test];
      numComparisons = 0;
    }
    mean = mean/10;
    for (int iter=0; iter<10; iter++) {stdev += pow(times[iter] - mean, 2.0);}
    stdev = sqrt( (1.0/9.0)* stdev);
    cout << "stdev is: " << stdev << endl;
    cout << "mean is: " << mean;
    iterations = 1536.64*pow(stdev, 2.0)/pow(mean, 2.0);
    if (iterations < 5) iterations = 5;
    cout << "running for " << iterations << " iterations" <<endl;

    for(int j=0; j<iterations; j++)
    {
      numComparisons = 0;
      vec.resize(array_size[i]);
      populateVector(vec, rand_bounds[1], array_size[i]);
      t = clock();
      bubbleSort(vec, numComparisons, t);
      vec.resize(0);
      cout << "numComparisons: " << numComparisons << endl;
      t = (1000.0 * float(t))/CLOCKS_PER_SEC;
      cout << "time: " << t << "ms" << endl << endl;
      averaged_time += (t/iterations);
    }
    fs << array_size[i] << "," << averaged_time << endl;
    comp << array_size[i] << "," << numComparisons << endl;
    averaged_time = 0;
  }
  fs.close();
  comp.close();

  //countingSort
  fs.open("countingSort.csv");
  comp.open("countingSortcomp.csv");
  for(int i=0; i<num_array_sizes; i++)
  {
    int iterations;
    float mean = 0;
    float stdev = 0;
    float times[10];
    for (int test=0; test<10; test++)
    {
      numComparisons = 0;
      vec.resize(array_size[i]);
      populateVector(vec, rand_bounds[1], array_size[i]);
      for (int k=0; k<vec.size(); k++) vec.at(k) = abs(vec.at(k));
      B.resize(array_size[i]);
      t = clock();
      countingSort(vec, B, numComparisons, t);
      vec.resize(0);
      B.resize(0);
      times[test] = (1000.0 * float(t))/CLOCKS_PER_SEC;
      mean += times[test];

    }
    mean = mean/10;
    if (mean > 0.01)
    {
      for (int iter=0; iter<10; iter++) {stdev += pow(times[iter] - mean, 2.0);}
      stdev = sqrt( (1.0/9.0)* stdev);
      cout << "stdev is: " << stdev << endl;
      cout << "mean is: " << mean;
      iterations = 1536.64*pow(stdev, 2.0)/pow(mean, 2.0);
    }
    else if (iterations < 5) iterations = 5;
    else iterations = 5;
    cout << "running for " << iterations << " iterations" <<endl;

    for(int j=0; j<iterations; j++)
    {
      numComparisons = 0;
      vec.resize(array_size[i]);
      populateVector(vec, rand_bounds[1], array_size[i]);
      for (int k=0; k<vec.size(); k++) vec.at(k) = abs(vec.at(k));
      B.resize(array_size[i]);
      t = clock();
      countingSort(vec, B, numComparisons, t);
      vec.resize(0);
      B.resize(0);
      cout << "numComparisons: " << numComparisons << endl;
      t = (1000.0 * float(t))/CLOCKS_PER_SEC;
      cout << "time: " << t << "ms" << endl << endl;
      averaged_time += (t/iterations);

    }
    fs << array_size[i] << "," << averaged_time << endl;
    comp << array_size[i] << "," << numComparisons << endl;
    averaged_time = 0;
  }
  fs.close();
  comp.close();

  //countingSort but varying by int size, on array size 500 elem
  fs.open("countingSortOverInts.csv");
  comp.open("countingSortOverIntscomp.csv");
  for(int i=0; i<8; i++)
  {
    int iterations = 0;
    float mean = 0;
    float stdev = 0;
    float times[10];
    for (int test=0; test<10; test++)
    {
      vec.resize(array_size[8]);
      populateVector(vec, rand_bounds[i], array_size[8]);
      for (int k=0; k<vec.size(); k++) vec.at(k) = abs(vec.at(k));
      B.resize(array_size[8]);
      t = clock();
      countingSort(vec, B, numComparisons, t);
      vec.resize(0);
      B.resize(0);
      times[test] = (1000.0 * float(t))/CLOCKS_PER_SEC;
      mean += times[test];
      numComparisons = 0;
    }
    mean = mean/10;
    if (mean > 0.01)
    {
      for (int iter=0; iter<10; iter++) {stdev += pow(times[iter] - mean, 2.0);}
      stdev = sqrt( (1.0/9.0)* stdev);
      cout << "stdev is: " << stdev << endl;
      cout << "mean is: " << mean;
      iterations = 1536.64*pow(stdev, 2.0)/pow(mean, 2.0);
    }
    else if (iterations < 5) iterations = 5;
    else iterations = 5;
    cout << "running for " << iterations << " iterations" <<endl;

    for(int j=0; j<iterations; j++)
    {
      vec.resize(array_size[8]);
      populateVector(vec, rand_bounds[i], array_size[8]);
      for (int k=0; k<vec.size(); k++) vec.at(k) = abs(vec.at(k));
      B.resize(array_size[8]);
      t = clock();
      countingSort(vec, B, numComparisons, t);
      vec.resize(0);
      B.resize(0);
      cout << "numComparisons: " << numComparisons << endl;
      numComparisons = 0;
      t = (1000.0 * float(t))/CLOCKS_PER_SEC;
      cout << "time: " << t << "ms" << endl << endl;
      averaged_time += (float(t)/float(iterations));
    }
    fs << rand_bounds[i] << "," << averaged_time << endl;
    comp << rand_bounds[i] << "," << numComparisons << endl;
    averaged_time = 0;
  }
  fs.close();
  comp.close();

  return 0;
}
// insertionSort: Vector -> Vector by ref
// Sorts the vector in Ascending Order
void insertionSort(std::vector<int> &A, long &numComparisons, clock_t &tempo)
{
  for (int j=1; j<A.size(); j++)
  {
    int key = A.at(j);
    int i = j-1;
    while(i>=0 && A.at(i)>key)
    {
      A.at(i+1) = A.at(i);
      i--;
      numComparisons++;
    }
    A.at(i+1) = key;
  }
  tempo = clock() - tempo;
}

//mergeSortA: Vector -> Vector by ref
// sorts the vector in Ascending Order
void mergeSortA(vector <int> &A, int p, unsigned int r, long &numComparisons, clock_t &tempo)
{
  if (p < r)
  {
    int q = (p+r)/2;
    mergeSortA(A, p, q, numComparisons, tempo);
    mergeSortA(A, q+1, r, numComparisons, tempo);
    mergeA(A, p, q, r, numComparisons);
  }
  tempo = clock() - tempo;
  //init call mergeSortA(A,1,n)
}

void mergeA(vector <int> &A, int p, int q, int r, long &numComparisons)
{
  int n1 = q-p+1;
  int n2 = r-q;
  int i, j, k;
  vector <int> L, R;
  L.resize(n1+1);
  R.resize(n2+1);
  L[n1] = 123456789;
  R[n2] = 123456789;
  for (i=0; i<n1; i++) L[i] = A[p+i];
  for (j=0; j<n2; j++) R[j] = A[q+j+1];
  //cout << "setting sentinels" << endl;
  //some sentinel thing
  //L.push_back(std::numeric_limits<int>::max());
  //R.push_back(std::numeric_limits<int>::max());
  //cout << "i,j = 0" << endl;
  i = 0;
  j = 0;
  for (k=p; k<=r; k++)
  {
    if (L[i]<=R[j])  //failing at this L[i]
    {
      A[k] = L[i];
      i++;
      //cout << "i = " << i << endl;
    }
    else
    {
      A[k] = R[j];
      j++;
      //cout << "j = " << j << endl;
    }
    numComparisons++;
  }
}

void bubbleSort(vector <int> &A, long &numComparisons, clock_t &tempo)
{
  int temp;
  int n = A.size();
  for (int i=0; i<n; i++)
  {
    for (int j=n-1; j>i; j--)
    {
      if (A.at(j) < A.at(j-1))
      { numComparisons++;
        temp = A[j];
        A.at(j) = A.at(j-1);
        A.at(j-1) = temp;
      }
    }
  }
  tempo = clock() - tempo;
}

void countingSort(vector <int> A, vector <int> &B, long &numComparisons, clock_t &tempo)
{
  vector <int> C;
  int n = A.size();
  int k = *max_element(A.begin(), A.end());
  for (int i=0; i<k+1; i++) C.push_back(0);
  for (int j=1; j<n; j++) C[A[j]] = C[A[j]] + 1;
  for (int i=1; i<k+1; i++) C[i] = C[i] + C[i-1];
  for (int j=n-1; j>=0; j--)
  {
    B[C[A[j]]] = A[j];
    C[A[j]] = C[A[j]] - 1;
  }
  numComparisons = 2*n + k;
  tempo = clock() - tempo;
}


// populateVector: Vector Double -> Vector by ref
// fills a vector with random integers uniformly distributed within the bounds
// of [-m,m]. array_size must be prespecified in global as it cannot be a param.
void populateVector(std::vector<int> &A, double m, int size)
{
  //from random.h, generator and distribution classes
  std::default_random_engine gener;
  //to limit the size of each integer
  std::uniform_int_distribution<int> dist(-m,m);
  //delcare iterator
  vector<int>::const_iterator i;
  for (int i=0; i<size; i++) A.insert(A.begin(),dist(gener));
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
