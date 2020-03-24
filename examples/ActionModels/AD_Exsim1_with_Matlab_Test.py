from entity import *
import asyncio

"""
                +---------------+
                |               |
                |     start     |
                |               |
                +---------------+
                        | process
                        |
                +---------------+
                |               |
     (Item1)--->|     Action1   |--->(Item2)
                |               |
                +---------------+
                        |
                        |
                +---------------+
                |               |
                |      End      |
                |               |
                +---------------+
"""
print('AD_Exsim_with_Matlab_Test')

###############################################
# 1 Define actions
p = Process("process 1")
act1 = p.Action("Action1")

i1 = Item("Item1")
i2 = Item("Item2")

pro1_1 = i1.Property("input", range=[1, 2, 3], value=1)
pro1_2 = i2.Property("output", range=[1, 2, 3], value=1)

# External SMRE_Eaxmple Script ######################################
def exsim_function(io):
    pro1_1, pro1_2 = io.get("Item1.input"), io.get("Item2.output")
    i1_value = pro1_1.get_random_value()

    # Setup matlab
    import matlab.engine
    eng = matlab.engine.start_matlab()
    eng.cd(r'.\ExSimCodes', nargout=0)

    # perform a simple calculation on Matlab
    pro1_2.value = eng.simple_cal_two_times(i1_value, nargout=1)

    print(f'input:{i1_value} -> output:{pro1_2.value}')

    eng.quit()


# Script end ##################################
act1.func(exsim_function)

###############################################
# 2 run simulation
asyncio.run(p.sim())