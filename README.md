# CISC3160-project

## Requirements
Python version **`3.10`** or **`higher`** installed

To run the interpreter, run the file **`main.py`** with python on a command line and pass in a file to interpret. In my case, I use the command:
> CISC3160 project> py .\main.py 'testfile.txt'

The Program will interpret the file and print the results

Currently, the interpreter supports variable assignments and reassignments and mathematical operations between variables and numbers:
* Addition
* Subtraction
* Multiply
* Unary Minus
* Unary Plus
* Parenthesis

## Examples:
---
Input 1

> x = 001;

Output 1

> Syntax Error on line 1 : x = 001;
---
Input 2

> x_2 = 0;

Output 2

> x_2 = 0
---
Input 3

> x = 0
>
> y = x;
> 
> z = ---(x+y);

Output 3

> Syntax Error on line 1 : x = 0
---
Input 4

> x = 1;
> 
> y = 2;
> 
> z = ---(x+y)*(x+-y);

Output 4

> x = 1
> 
> y = 2
> 
> z = 3
---
Input 5

> x = 0;
> 
> y = z;

Output 5
> x = 0
> 
> Uninitialized Error on line 2 : 'y = z;' : Variable: 'z' has not been initialized