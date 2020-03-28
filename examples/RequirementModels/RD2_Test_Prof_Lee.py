import req1
from entity import *

"""
+---------------------------------------------------------------------------+
--- Requirement template ---
UUID | id | category | who | auxv | how | howmuch | verb | what | towhat | where | why | when

--- Case 1 ---
Description: When constructing an architectural model, SAI should automatically optimize 
             the spatial arrangement of the boxes and lines that make up the model 
             in the modeling window by pressing the 'Model Space Optimization Button' 
             to improve readability.
             
UUID:       A.T1.S1
ID:         1
Category:   Function
Who:        SAI
AuxV:       shall
How:        automatically
HowMuch:
Verb:       optimize
what:      the spatial arrangement of the boxes and lines that make up the model 
towhat:
where:      in the modeling window 
why:        to improve readability
when:       by pressing the 'Model Space Optimization Button‘, when constructing an architectural model

+---------------------------------------------------------------------------+
"""

###############################################
# 1 Define requirements
r1 = Requirement("Functional Req'",
                 category="Function",
                 who="SAI",
                 auxv="shall",
                 how="automatically",
                 verb="optimize",
                 what1="the spatial arrangement of the boxes and lines that make up the model",
                 where="in the modeling window",
                 why="to improve readability",
                 when="by pressing the 'Model Space Optimization Button‘, when constructing an architectural model")

r2 = Requirement("2",
                 category="Function",
                 who="SAI")

print(req1.r1)
