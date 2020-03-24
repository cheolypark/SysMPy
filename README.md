# SysMPy
 
## About
SysMPy is an open-source library for System Modeling Runtime Environment (SMRE), an integrated software environment which offers several built-in libraries to support systems analysis and design, based on a convenient systems modeling script language, which forms a fundamental building block of SMRE.


### Install SysMPy via PIP
Example 1: Three action nodes 

```
pip install sysmpy
```

### Systems Modeling Script (SMS) Example
This tutorial walks you through how to run a simple SysMPy project. 
It will show you how to write a simple system modeling script and execute it.

#### Example 1: Three action nodes 

This tutorial uses a simple project named a simple action model. 
If you are unfamiliar with Python, take a time to study Python (https://www.python.org/).

SMS has a simple form as shown the following code. 
To define a process, a class Process(.) can be used. 
The return object from it provides a built-in function Action(.). 
By including the name of an Action, the Action node is defined along the process.  


```
from sysmpy import *
import asyncio

p = Process("Process")
act1 = p.Action("Action1")
act2 = p.Action("Action2")
act3 = p.Action("Action3")
```

The following figure shows an illustrative graph from the above code. 

```
                +---------------+
                |               |
                |     start     |
                |               |
                +---------------+
                        | Process
                        |
                +---------------+
                |               |
                |     Action1   |
                |               |        
                +---------------+        
                        |
                        |
                +---------------+
                |               |
                |     Action2   |
                |               |        
                +---------------+        
                        |
                        | 
                +---------------+
                |               |
                |      End      |
                |               |
                +---------------+
```

After writing the action model, we can run a simulation. 
To execute the simulation, asyncio.run(.) is used with the built-in function sim() of the process p.

```
asyncio.run(p.sim())
```

### Prerequisites for Matlab 
The following package would be needed to run some examples for Matlab. 
- Python for matlab:
https://www.mathworks.com/help/matlab/matlab_external/install-the-matlab-engine-for-python.html

### Members
Developers:

- Dr. Cheol Young Park
- Dr. Shou Matsumoto 
- Mr. DaePhil Han
- Mr. EunHak Lee 
- Mr. SeongRae Lim
- Mr. Hong Gyu Han

Advisers:

- Prof. Joongyoon Lee
- Dr. GwanTaik Lim
- Prof. YoungWon Park
