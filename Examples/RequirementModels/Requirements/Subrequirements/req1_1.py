from entity import *

"""
+---------------------------------------------------------------------------+
--- Requirement template ---
id | category | who | auxv | how | howmuch | verb | what1 | what2 | where | why | when

--- Case 1 ---
Description: When constructing an architectural model, SAI should automatically optimize 
             the spatial arrangement of the boxes and lines that make up the model 
             in the modeling window by pressing the 'Model Space Optimization Button' 
             to improve readability.
              
ID:         1
Category:   Function
Who:        SAI
AuxV:       shall
How:        automatically
HowMuch:
Verb:       optimize
what1:      the spatial arrangement of the boxes and lines that make up the model 
what2:
where:      in the modeling window 
why:        to improve readability
when:       by pressing the 'Model Space Optimization Button‘, when constructing an architectural model

+---------------------------------------------------------------------------+
"""

###############################################
# 1 Define requirements

r1 = Requirement("Req 1.1.1",
                 des="The system shall fit into a volume not exceeding 1.0 m^3",
                 verb="fit into",
                 attribute="volume",
                 relation="<",
                 value="1",
                 unit="m^3"
                 )

r2 = Requirement("Req 1.1.2",
                 des="The system2 shall fit into a volume not exceeding 4.0 m^3",
                 verb="fit into",
                 attribute="volume",
                 relation="<",
                 value="4",
                 unit="m^3"
                 )
