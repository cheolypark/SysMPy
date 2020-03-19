# 시스템 설명

### U2M 실행
U2G 컴포넌트는 U2M과 M2G 하부컴포넌트로 구성되어 있으며
U2M은 박박사 님이 M2G는 한대필이 작성하기로 하였다. 

- U2G 실행 순서
    1. code_gui 하위 mxgraph 하위 tornado_mx_server.py 파일 실행
        - 8080포트로 토네이도(웹서버) 실행하고 대기
    2. cmd 터미널 실행하고 NotebookExample 디렉토리로 이동
        - 예: D:\Git_Repogitory\SysMPy\Examples\NotebookExample
    3. cmd 터미널에서 jupyter lab 명령어 실행
        - 해당디렉토리를 기준으로 하는 주피터 랩 8888 포트로 실행 됨
    4. 주피터랩에서 5_Script_mxGraph_all.ipynb 열고 실행
        - 그래프 등 표현 됨

위 순서대로하면 U2G가 실행되고 주피터 랩 화면에 표현된다.
 

 
### 디렉토리 구성
```
SysMPy
  ├─ code_gui : 중심모듈
  │   ├─ mxgraph :   
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




### 흐름 설명
- 5_Script_mxGraph_all.ipynb
    - import gui_main
    - UnifiedCode 작성 ( 예: p_act1 = p3.Action("Action2") )
    - show( p )
- gui_main.py
    - import GuiMXGraphActionDiagram
    - show() 메소드 
        - iframe = "http://localhost:8080/AD/?g=" + GuiMXGraphActionDiagram().get_mxgraph(p)
        - display(HTML(iframe))
- GuiMXGraphActionDiagram.py
    - import GuiMXGraph
    - class GuiMXGraphActionDiagram(GuiMXGraph): 클래스 선언
        - 클래스 내의 get_mxgraph() 메소드
            - 각노드들 정리, 위치 등..
- GuiMXGraph.py
    
    
- 제어는 토네이도 서버로..
- 