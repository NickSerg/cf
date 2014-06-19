# Introduction

`cf.py` allows you:

 * download tests for all problems from a given contest
 * submit solution to a problem from a given contest
 * run your solution on all test cases for a given problem

You will need Python 2.7 to run this script.

# Configuration

Create a file named `.cfrc` in the same directory as `cf.py` with the following contents:

```
[cf]
handle =
password =
contest =
fileSolution =
.c = 10
.cpp = 16
.py = 7
.cs = 29
```
# Usage

Fill in your handle, password, the contest name and the file name with the solution for send in `.cfrc`.

## Download tests for all problems

```
./cf.py
```

This will create `a1.in`, `a2.in`,..., `e1.in`,... with inputs
and `a1.ans`, `a2.ans`,...,`e1.ans`,... with answers.

## Submit solution to a problem

```
./cf.py b
```

This will submit a solution to the problem *B* using C# as a compiler.

## Run solution on all test cases

```
./cf.py a t
```

This will run `./a` on all test cases for the problem `a`.
