# CISC3160-project

## Requirements
Python version **`3.10`** or **`higher`** installed

To run the program, run the file **`toy_repl.py`** with python on a command line. In my case, I use the command:
> CISC3160 project> py .\toy_repl.py

This will bring you into the program REPL where you can enter statements
for the program to interpert
> toyREPL>

Currently, the interpreter supports variable assignments and reassignments and mathematical operations between variables and numbers:
* Addition
* Subtraction
* Multiply
* Unary Minus
* Unary Plus
* Parenthesis

## Examples:
Syntax Error
> toyREPL> x=001;
> 
> Syntax Error:

Variable names with digits and underscore
> toyREPL> x_2=0;
> 
> x_2 = 0

Uninitialized Variable Error
> toyREPL> x=3;
> 
> x = 3
> 
> toyREPL> y=x-z;
> 
> Uninitialized Error: Variable: 'z' has not been initialized

Complex Math Operations
> toyREPL> x=1;
> 
> x = 1
> 
> toyREPL> y=2;
> 
> y = 2
> 
> toyREPL> z=---(x+y)*(x+-y);
> 
> z = 3

Variable Reassignment
> toyREPL> x=2;  
> 
> x = 2
> 
> toyREPL> x=x*x;
> 
> x = 4