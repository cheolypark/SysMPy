import subprocess
import os
import json
import sys
import pandas as pd
import concurrent.futures
import time

class DMP_runner():
    def __init__(self, output):
        self.output = output
        self.my_df = pd.DataFrame()
        self.__model = ''
        self.__evidence = ''

    def setModel(self, sbn):
        with open(sbn, 'r') as file:
            self.__model += file.read()

    def addEvidence(self, nodeName, value):
        s = '\ndefineEvidence({}, {});'.format(nodeName, value)
        self.__evidence += s

    def runDMP(self):
        model = self.__model + self.__evidence + '\nrun(DMP);'
        self.run(model)
        self.__evidence = ''

    def saveResult(self):
        ###############################
        # Save reasoned results
        nodes = []
        with open(self.output) as json_file:
            net = json.load(json_file)
            for node in net:
                for obj, contents in node.items():
                    nodes.append(obj)

        df = pd.DataFrame(columns=nodes)

        row_data = {}
        with open(self.output) as json_file:
            net = json.load(json_file)
            for node in net:
                for obj, contents in node.items():
                    if 'marginal' in contents:
                        row_data[obj] = contents['marginal']['MU']
                    elif 'evidence' in contents:
                        row_data[obj] = contents['evidence']['mean']

        df = df.append(row_data, ignore_index=True)
        self.my_df = self.my_df.append(df, ignore_index=True)
        return self.my_df

    def run(self, model):
        # create a hybrid model script to be executed in dmp.jar
        cwd = os.path.dirname(os.path.realpath(__file__))
        dmp_args = " -b "
        dmp_args += "\"" + model + "\""
        dmp_args += " -p "
        dmp_args += "\"" + self.output + "\""

        # supervisor call to DMP (command line)
        proc = subprocess.Popen("java -jar " + cwd + "/dmp.jar" + dmp_args)

        proc.wait()

        (stdout, stderr) = proc.communicate()

        if proc.returncode != 0:
            print(stderr)
            sys.exit()
        else:
            # print("success")
            pass

    ##############################################################
    # sampling
    def sampling(self, sbn, size):
        time.sleep(0.1)
        model = ""

        with open(sbn, 'r') as file:
            model += file.read()
        model += " run(LW, arg(1,1));"

        for i in range(size):
            print("   Sampling {:f} % ********************************".format(100*i/size))

            # Run a BN once using LW
            self.run(model)

        return self.saveResult()

    def sampling_by_thread(self, sbn, size, size_thread=50):
        # size_thread = 4
        distributed_size = size
        ts = time.time()

        with concurrent.futures.ThreadPoolExecutor(max_workers=size_thread) as executor:
            executor.map(self.sampling(sbn, distributed_size), range(size_thread))

        # with concurrent.futures.ProcessPoolExecutor(max_workers=size_thread) as executor:
        #     executor.map(self.sampling(sbn, distributed_size), range(size_thread))

        print("== sampling_by_thread end: Time {} ==============================".format(time.time() - ts))

        return self.my_df

    ##############################################################
    # read output from DMP
    def read_results(self, data_file_name):
        with open(data_file_name) as json_file:
            net = json.load(json_file)
            for node in net:
                for obj, contents in node.items():
                    print('node: ' + obj)
                    for attr, values in contents.items():
                        print(" " + attr + ': ' + str(values))
