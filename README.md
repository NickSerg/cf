# Introduction

`cf.py` allows you:

 * download tests for all problems from a given contest
 * submit solution to a problem from a given contest

You will need Python 2.7 to run this script.

# Configuration

Create a file named `.cfrc` in the same directory as `cf.py` with the following contents:

```
[cf]
handle =
password =
contest =
.c = 10
.cpp = 1
.py = 7
.cs = 29
```
# Usage

Fill in your handle, password and the contest name in `.cfrc`.

## Download tests for all problems

```
./cf.py
```

This will create `a.1.in`, `a.2.in`,..., `e.1.in`,... with inputs
and `a.1.ans`, `a.2.ans`,...,`e.1.ans`,... with answers.

## Submit solution to a problem

```
./cf.py b.cpp
```

This will submit a solution to the problem *B* using GNU C++ as a compiler.

Also supported `.py` for Python and `.c` for GNU C.
