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



### 디렉토리별 주요 파일
```
- core
  . entity.py : 모든 주요 엔티티 객체가 정의되어 있음  

나머지 차후 정리
```


### U2G 흐름 설명
- 5_Script_mxGraph_all.ipynb
    - import gui_main
    - UnifiedCode 작성 ( 예: p_act1 = p3.Action("Action2") )
    - show( p )
- gui_main.py
    - import gui_mxgraph_action_diagram
    - show() 메소드 
        - iframe = "http://localhost:8080/AD/?g=" + GuiMXGraphActionDiagram().get_mxgraph(p)
        - display(HTML(iframe))
- gui_mxgraph_action_diagram.py
    - import gui_mxgraph
    - class GuiMXGraphActionDiagram(GuiMXGraph): 클래스 선언
        - 클래스 내의 get_mxgraph() 메소드
            - 각노드들 정리, 위치 등이 담긴 str 반환
- gui_mxgraph.py
    - GuiMXGraph : 클래스 선언 - GuiMXGraphActionDiagram의 부모 클래스
    
- 제어는 토네이도 서버로..
    - get 으로 넘어가는 자료의 예
        - var A_Root_Process = graph.insertVertex(parent, 'A Root Process', '', 305.0, 42.0, 30, 30, 'Process')
        - var A_1_1_P1 = graph.insertVertex(parent, 'A.1.1 P1', '', 200.0, 141.0, 0, 0, 'Process')  

- tornado_mx_server.py
    - import ad_script
    - class ActionDiagramHandler(RequestHandler): 핸들러 클래스 선언
        - self.write(ad_script.mxGraph_start_nice_label + ad_script.mxGraph_styles + my_graph + ad_script.mxGraph_end)
            - my_graph 가 넘겨 받은 정보
        - self.render('simple_mx_web.html')

- ad_script.py
    - mxGraph_start_nice_label = ''' mxGraph 설정 및 스크립트 앞쪽 하드코딩 ''''
    - mxGraph_styles = ''' mxGraph 객체 스타일 하드코딩 ''''
    - mxGraph_end = ''' mxGraph 스크립트 뒤쪽 하드코딩 ''''
    - mxGraph_graph = ''' mxGraph 객체 하드코딩 ''''

- simple_mx_web.html
    - mxGraph가 표현될 html 
    
    
    