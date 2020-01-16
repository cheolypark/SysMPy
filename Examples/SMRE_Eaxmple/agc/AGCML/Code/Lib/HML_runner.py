import subprocess
import os
import json
import sys


class HML_runner():
    def __init__(self, model_structure=None):
        self.model_structure = model_structure
        self.csv = ""
        self.output = ""

    def run(self, csv, output):
        self.csv = csv
        self.output = output

        # create a hybrid model
        # script to be executed in dmp.jar
        cwd = os.path.dirname(os.path.realpath(__file__))
        dmp_args = " -b "
        dmp_args += "\"" + self.model_structure + "\""
        dmp_args += " -c "
        dmp_args += "\"" + self.csv + "\""
        dmp_args += " -p "
        dmp_args += "\"" + self.output + "\""

        # supervisor call to HML (command line)
        # print("current working directory: " + cwd)
        proc = subprocess.Popen("java -jar " + cwd + "/HML.jar" + dmp_args)

        proc.wait()

        (stdout, stderr) = proc.communicate()

        if proc.returncode != 0:
            print(stderr)
            sys.exit()
        else:
            # print("success")
            with open(self.output, 'r') as file:
                self.model_learned = file.read()
            return self.model_learned

    def make_Model(self, child, parents):
        self.model_structure = ""
        for nodeName in parents:
            self.model_structure += self.creat_BN_parent_node(nodeName)
        self.model_structure += self.creat_BN_child_Node(child, parents)
        # print(self.model_structure)
        return self.model_structure

    def creat_BN_parent_node(self, nodeName):
        s = "defineNode({}, des);".format(nodeName)
        s += "{ defineState(Continuous);"
        s += "  p( {} ) = NormalDist(  0, 0.000001 );".format(nodeName)
        s += "}"
        return s

    def creat_BN_child_Node(self, nodeName, parents):
        p = ", ".join(parents)
        e = "+ ".join(parents)
        s = "defineNode({}, des);".format(nodeName)
        s += "{ defineState(Continuous);"
        s += "  p( {} | {} ) = {} + NormalDist(  0, 0.000001 );".format(nodeName, p, e)
        s += "}"
        return s

    # read output from DMP
    def read_results(self, data_file_name):
        with open(data_file_name) as json_file:
            net = json.load(json_file)
            for node in net:
                for obj, contents in node.items():
                    print('node: ' + obj)
                    for attr, values in contents.items():
                        print(" " + attr + ': ' + str(values))
