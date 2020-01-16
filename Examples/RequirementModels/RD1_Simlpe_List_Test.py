from entity import *
"""
+---------------------------------------------------------------------------+
R1.0 The system shall fit into a volume not exceeding 1.0 m^3
    R1.1 The system width shall be between 0.5m and 1.0m
    R1.2 The system height shall be between 0.5m and 1.0m
    R1.3 The system depth shall be between 0.5m and 1.0m

R2.0 The system shall be made entirely from Aluminum 6060 alloy
    R2.1 The system shall not contain any internal voids or cavities

R3.0 The shape of the system must be a cube
    R3.1 The angles between sides shall be 90 deg +/-1 deg

R4.0 The mass of the system shall not exceed 2,700 kg
    R4.1 The center of mass of the system must be located at least 0.25
         meters from the edge of its volumetric envelope
    R4.2 The mass of the system must be verified using a Mettler-Toledo XYZ
         Bench Scale
+---------------------------------------------------------------------------+
"""

###############################################
# 1 Define requirements

r1 = Requirement(id="1.0",
                 des="The system shall fit into a volume not exceeding 1.0 m^3",
                 verb="fit into",
                 attribute="volume",
                 relation="<",
                 value="1",
                 unit="m^3"
                 )

r1_1 = r1.Requirement(id="1.1",
                 des="The system width shall be between 0.5m and 1.0m",
                 verb="be",
                 attribute="width",
                 relation="<=, <",
                 value="0.5, 1.0",
                 unit="m"
                 )

r2 = Requirement(id="2.0",
                 des="The system shall be made entirely from Aluminum 6060 alloy",
                 # subj="The system",
                 verb="be made entirely from",
                 # obj="Aluminum 6060 alloy"
                 )

r2_1 = r2.Requirement(id="2.1",
                 des="The system shall not contain any internal voids or cavities",
                 verb="not contain",
                 )

r3 = Requirement(id="3.0",
                 des="The shape of the system must be a cube",
                 # subj="The shape of the system",
                 verb="be",
                 # obj="a cube"
                 )

r3_1 = r3.Requirement(id="3.1",
                   des="The angles between sides shall be 90 deg +/-1 deg",
                   # subj="The angles between sides",
                   verb="be",
                   # obj="volume",
                   attribute="The angles between sides",
                   relation="<, <",
                   value="89, 91",
                   unit="deg"
                   )

r4 = Requirement(id="4.0",
                 des="The mass of the system shall not exceed 2,700 kg",
                 # subj="The mass of the system",
                 attribute="The mass of the system",
                 relation="<",
                 value="2,700",
                 unit="kg"
                 )

r4_1 = r4.Requirement(id="4.1",
                 des="The center of mass of the system must be located at least 0.25"
                     "meters from the edge of its volumetric envelope",
                 # subj="The center of mass of the system ",
                 attribute="The center of mass of the system ",
                 relation="<",
                 value="0.25",
                 unit="meters"
                 )

r4_2 = r4.Requirement(id="4.2",
                   des="The mass of the system must be verified "
                       "using a Mettler-Toledo XYZ Bench Scale",
                   # subj="The mass of the system",
                   verb="be verified",
                   # obj="using a Mettler-Toledo XYZ Bench Scale"
                  )


print(r1)
print(r4)
