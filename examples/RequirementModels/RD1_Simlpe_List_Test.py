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
r_sys = Requirement('System Requirement')
r_size = r_sys.Requirement('System Size',
                           des="The system shall fit into a volume not exceeding 1.0 m^3",
                           range=[1, 2, 3, 4],
                           unit="m^3")

r1_1 = r_size.Requirement('System Width',
                          des="The system width shall be between 0.5m and 1.0m",
                          range=[1, 2, 3, 4],
                          unit="m")

r2 = r_sys.Requirement('System Material',
                       des="The system shall be made entirely from Aluminum 6060 alloy",
                       type="alloy")

r2_1 = r2.Requirement('System Material Constraint',
                      des="The system shall not contain any internal voids or cavities")

r3 = r_sys.Requirement('System Shape',
                       des="The shape of the system must be a cube",
                       type="cube")

r4 = r_sys.Requirement('System Weight',
                       des="The mass of the system shall not exceed 2,700 kg",
                       range=[2600, 2700],
                       unit="kg")

print(r_sys)
