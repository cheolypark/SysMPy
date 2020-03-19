# 시스템 설명
 
### 디렉토리 구성
```
SysMPy
  ├─ code_gui : 
  │   ├─ mxgraph   
  │   └─ ...   
  ├─ core : 중심 모듈
  ├─ docs : 참고 문서
  ├─ Examples : 예제
  │   ├─ ActionModels   
  │   ├─ BlockModels   
  │   ├─ Gui   
  │   ├─ ...   
  │   └─ ...   
  └─ venv : 개발환경(파이참)
```

### 디렉토리별 파일
```
차후 정리
```
Example 1: Three action nodes 

SMS has a simple form as shown the following code. 
To define a process, a class Process(.) can be used. 
The return object from it provides a built-in function Action(.). 
By including the name of an Action, the Action node is defined along the process.  


```
from entity import *

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

After building the model, we can run a simulation. 
To execute the simulation, asyncio.run(.) is used with the built-in function sim() of the process p.

```
asyncio.run(p.sim())
```

### Prerequisites
The following pakages are needed to run the library.
- requests
- numpy
- tornado
- python for matlab 

### Members
Developers:

- Dr. Cheol Young Park
- Dr. Shou Matsumoto 
- Mr. DaePhil Han (minimal)
- Mr. EunHak Lee 
- Mr. SeongRae Lim
- Mr. Hong Gyu Han

Advisers:

- Prof. Joongyoon Lee
- Dr. GwanTaik Lim
- Prof. YoungWon Park
