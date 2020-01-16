from entity import *

###############################################
# 1 Define requirements
r1 = Requirement("Req 1.1",
                 des="The system shall fit into a volume not exceeding 1.0 m^3",
                 verb="fit into",
                 attribute="volume",
                 relation="<",
                 value="1",
                 unit="m^3"
                 )

r1_1 = r1.Requirement("Req 1.1.1",
                 des="The system shall fit into a volume not exceeding 1.0 m^3",
                 verb="fit into",
                 attribute="volume",
                 relation="<",
                 value="1",
                 unit="m^3"
                 )

r1_2 = r1.Requirement("Req 1.1.2",
                 des="The system2 shall fit into a volume not exceeding 4.0 m^3",
                 verb="fit into",
                 attribute="volume",
                 relation="<",
                 value="4",
                 unit="m^3"
                 )

print(r1)
