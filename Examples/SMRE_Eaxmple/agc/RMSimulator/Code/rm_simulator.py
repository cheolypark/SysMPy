from DMP_runner import DMP_runner
import winsound
import numpy as np


class RollingMachineSimulator():
    """
        This class generates sample data using a simulation model

        1. Input simulation model will be located in:
        '../Data/RM_simulation_model_Modified.txt'

        2. Output simulation results will be located in:
        '../Data/temporary_reasoned_output_by_BN.json'

    """
    def __init__(self):
        sim_model = r'../Data/RM_simulation_model_Modified.txt'
        sim_output = r'../Data/temporary_reasoned_output_by_BN.json'
        self.dmp = DMP_runner(sim_output)
        self.dmp.setModel(sim_model)

    def random_normal(self, mean, var):
        return str(np.random.normal(mean, np.sqrt(var)))

    def run(self, rollgap):
        # Set evidence for variables
        # self.dmp.addEvidence('temp_pass_rc', self.random_normal(1072.443113772455, 6638.191257485027))
        # self.dmp.addEvidence('passreduction_th_rc_plan', self.random_normal(-13.590508982035884, 56.027468602419084))
        # self.dmp.addEvidence('passdiff_width_rc_plan', self.random_normal(56.88962075848274, 12076.328812055945))
        # self.dmp.addEvidence('strength_yp', self.random_normal(41.90299401197606, 314.0165710179644))
        # self.dmp.addEvidence('th_pass_plan', self.random_normal(108.61382235528903, 6367.260253938381))
        # self.dmp.addEvidence('width_pass_rc', self.random_normal(2857.2870259481115, 245233.8155313375))
        # self.dmp.addEvidence('acc_rolling_weight', self.random_normal(1.78, 4.84))
        # self.dmp.addEvidence('rolling_speed_rm', self.random_normal(9.1, 6.22))
        # self.dmp.addEvidence('pp_cr_r', self.random_normal(5.18, 10.34))

        self.dmp.addEvidence('temp_pass_rc', 1073)
        self.dmp.addEvidence('passreduction_th_rc_plan', -13)
        self.dmp.addEvidence('passdiff_width_rc_plan', 56)
        self.dmp.addEvidence('strength_yp', 41)
        self.dmp.addEvidence('th_pass_plan', 108)
        self.dmp.addEvidence('width_pass_rc', 2857)
        self.dmp.addEvidence('acc_rolling_weight', 2)
        self.dmp.addEvidence('rolling_speed_rm', 9)
        self.dmp.addEvidence('pp_cr_r', 5)

        #################################################
        # AGC roll gap setting (e.g., rollgap = 20.0)
        self.dmp.addEvidence('rollgap_plan', rollgap)
        #################################################

        # Run simulation
        self.dmp.runDMP()

        # Save results as csv, if needed
        df = self.dmp.saveResult()
        df.to_csv(r"../Data/simulated_data.csv", index=None)


sim = RollingMachineSimulator()
sim.run(rollgap=20)

sim_output = r'../Data/temporary_reasoned_output_by_BN.json'

winsound.Beep(1000, 440)
