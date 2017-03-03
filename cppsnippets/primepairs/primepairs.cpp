/*************************************\
*Just some quick sample C++	     *
*primepairs.cpp : 	 	     *
*generates a list of prime pairs from*
*a minimum value to a maxiumum value *
\************************************/

#include <iostream>
#include <cmath>


using namespace std;

bool isa_prime_num (int num);

int main ()
{

	int range_min, range_max;

	cout << "Enter a minimum value: ";
	cin >> range_min;
	cout << "Enter a maximum value: ";
	cin >> range_max;


	for (int i=range_min; i<range_max ; i++)
	{
		if ((isa_prime_num (i)) && (isa_prime_num (i+2)))
		{
			cout << i << " " << (i+2) << "\n";
		}	
	}

}


//prime_num?: Int -> Boolean
//Is the number a prime number?
bool isa_prime_num (int num)
{
	for (int n=2; n<(num-1); n++)
	{
		if (!(num%n)) return false; 
	}

	return true;
}

