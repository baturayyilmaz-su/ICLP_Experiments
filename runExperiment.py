import os
import subprocess
import multiprocessing
from abc import ABC, abstractmethod
import argparse


class CommandExecutor(ABC):
    def __init__(self):
        self.TIMEOUT_VALUE = 200  # in seconds

    def timeout(self, func, command, timeoutValue):
        manager = multiprocessing.Manager()
        return_dict = manager.dict()
        process = multiprocessing.Process(target=func, args=[command, return_dict])
        process.start()
        process.join(timeout=timeoutValue)

        if process.is_alive():  # TIMEOUT VALUE IS REACHED AND PROCESS IS STILL WORKING
            process.terminate()
            return False
        else:  # PROCESS IS FINISHED
            return return_dict.values()[0]

    def runProcess(self, command, return_dict):
        subPro = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return_dict[0] = subPro

    @abstractmethod
    def _getCommandString(self):
        pass

    def runCommand(self):
        command = self._getCommandString()

        subPro = self.timeout(func=self.runProcess, command=command, timeoutValue=self.TIMEOUT_VALUE)
        if subPro is False:  # then the process terminated because timeout is being reached
            return None
        # Process is finished. subPro has a value (which has the stdout of the process)
        else:
            processOutput = subPro.stdout.decode('utf-8')
            return processOutput



class Executor01(CommandExecutor):  # Executor for experiment 1
    def __init__(self, directoryOfInstances, inputSize, directoryOfOutputs):
        super().__init__()
        self.instanceDirectory = directoryOfInstances
        self.fileNameToSolve = ""
        self.inputSize = inputSize
        self.outputDirectory = directoryOfOutputs
    
    def _getCommandString(self):
        pathToInstance = os.path.join(self.instanceDirectory, self.inputSize, self.fileNameToSolve)
        pathToChocoJar = os.path.join("Solvers", "ChocoSolver", "distribution", "choco", "choco-solver-2.1.5.jar")
        pathToJavaMain = os.path.join("Solvers", "ChocoSolver", "distribution", "code20160401")
        return f"java -cp \".:{pathToChocoJar}:{pathToJavaMain}\" SRNary {pathToInstance} count" # for Windows use ";" as seperator, for Linux use ":" as seperator
    
    def writeOutputToFile(self, content, oFileName):
        with open(os.path.join(self.outputDirectory, "RES_"+self.inputSize, oFileName), "w") as oFile:
            oFile.write(content)

    def solveInstances(self):
        for root,dirs,files in os.walk(os.path.join(self.instanceDirectory, self.inputSize)):
            for inputFile in files:
                self.fileNameToSolve = inputFile
                print(f"Solving file: {self.instanceDirectory} - {self.inputSize} - {inputFile}!")

                output = self.runCommand()

                if output is None:
                    print(f"Command could not be executed in {self.TIMEOUT_VALUE}.")
                else:
                    oFileName = inputFile.replace("instance", "output")
                    self.writeOutputToFile(output, oFileName)


class Executor02(CommandExecutor): # Executor for experiment 2
    def __init__(self, directoryOfInstances, inputSize, directoryOfOutputs):
        super().__init__()
        self.instanceDirectory = directoryOfInstances
        self.fileNameToSolve = ""
        self.inputSize = inputSize
        self.outputDirectory = directoryOfOutputs
    
    def _getCommandString(self):
        pathToInstance = os.path.join(self.instanceDirectory, self.inputSize, self.fileNameToSolve)
        pathToEgalLP = os.path.join("Solvers", "EgalitarianSRTISolver", "egal.lp")
        pathToSRTILP = os.path.join("Solvers", "EgalitarianSRTISolver", "SRTISolver.lp")
        print(f"clingo {pathToSRTILP} {pathToEgalLP} {pathToInstance}")
        return f"clingo {pathToSRTILP} {pathToEgalLP} {pathToInstance}"
    
    def writeOutputToFile(self, content, oFileName):
        with open(os.path.join(self.outputDirectory, oFileName), "w") as oFile:
            oFile.write(content)

    def solveInstances(self):
        for root,dirs,files in os.walk(os.path.join(self.instanceDirectory, self.inputSize)):
            for inputFile in files:
                self.fileNameToSolve = inputFile
                print(f"Solving file: {self.instanceDirectory} - {self.inputSize} - {inputFile}!")

                output = self.runCommand()

                if output is None:
                    print(f"Command could not be executed in {self.TIMEOUT_VALUE}.")
                else:
                    oFileName = inputFile.replace("instance", "output")
                    self.writeOutputToFile(output, oFileName)

def runExperiment01():
    for inputSize in [20,40,60,80,100]:
        exec01 = Executor01(os.path.join("Benchmarks", "txtFormat", "ExistingBenchmark"), str(inputSize), os.path.join("Results", "Experiment 1 Results", "Existing Benchmark"))
        exec01.solveInstances()
        exec01 = Executor01(os.path.join("Benchmarks", "txtFormat", "NewBenchmark"), str(inputSize), os.path.join("Results", "Experiment 1 Results", "New Benchmark"))
        exec01.solveInstances()

def runExperiment02():
    for inputSize in [20,40,60,80,100]:
        exec02 = Executor02(os.path.join("Benchmarks", "lpFormat", "ExistingBenchmark"), str(inputSize), os.path.join("Results", "Experiment 2 Results", "Existing Benchmark"))
        exec02.solveInstances()
        exec02 = Executor02(os.path.join("Benchmarks", "lpFormat", "NewBenchmark"), str(inputSize), os.path.join("Results", "Experiment 2 Results", "New Benchmark"))
        exec02.solveInstances()

def main(experiment=0):
    if experiment == 1:
        runExperiment01()
    elif experiment == 2:
        runExperiment02()
    else:
        print("Please specify a valid experiment number (either 1 or 2)!")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", type=int, help="Experiment number to run (1 or 2)", required=True, default=0)
    args = parser.parse_args()
    
    main(experiment=args.e)