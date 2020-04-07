#============================================================================
# This is sample Script for digram
#============================================================================

from sysmpy import *

def getActionScript( ):
    p = Process("Root Process")
    p1, p2 = p.Condition("한글 컨디션 입니다. 이것은 테스트 ", "P1", "P2")
    p_act1 = p1.Action("Action1")
    p3, p4 = p1.Condition("Condition 2", "P3", "P4")
    p2_act1 = p2.Action("신규액션1")
    p_act1 = p3.Action("Action2")
    p_act2 = p4.Action("Action3")
    p.Action("Action4")
    p.Action("Action5")
    return p