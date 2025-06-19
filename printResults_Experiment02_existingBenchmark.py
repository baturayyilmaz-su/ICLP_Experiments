import os
import time
import math

def printTable(ROWS):
	oStr = ""

	oStr += "{:<5} {:<7} {:<18} {:<18}".format("n","p1","Avg Egal","Solved Egal")
	oStr += "\n----------------------------------------------------"


	counter = 0
	for row in ROWS:
		oStr += "\n{:<5} {:<7} {:<18} {:<18}".format(row["n"],row["p1"],round(row["AvgTimeEgal"],3),row["AmountOfSolvedFileEgal"])
		counter+=1
		if counter % 4 == 0 and counter < 20: oStr+="\n----------------------------------------------------"
	
	oStr += "\n----------------------------------------------------"

	print(oStr)
	return oStr


def handleOutputDir(outputDirEgal, n, p1):

	row = {"n": n, "p1" : p1, "AvgTimeEgal":0, "AmountOfSolvedFileEgal": 0}
	
	for root,dirs,files in os.walk(outputDirEgal): 
		for outputFile in files:
			
			p1_file = 1 - (int(outputFile.strip().split("-")[2].strip()) / 100)
			n_file = int(outputFile.strip().split("-")[1].strip())
			
			# print(f"Handling file: {outputFile}! - p1: {p1_file} - n:{n_file}")
			
			if n_file != n or p1_file != p1:
				continue

			cpuTime = 0
			isSat = True
			
			with open(os.path.join(outputDirEgal, outputFile), "r") as oFile:
				lines = oFile.readlines()

				for line in lines:
					if "UNSATISFIABLE" in line:
						isSat = False
						
					if "CPU Time" in line:
						cpuTime = float(line.strip().split(":")[1].strip().split("s")[0].strip())
		


			if isSat:
				row["AmountOfSolvedFileEgal"] += 1
				row["AvgTimeEgal"] += cpuTime

	
	if row["AmountOfSolvedFileEgal"] > 0: row["AvgTimeEgal"] /= row["AmountOfSolvedFileEgal"]
	
	
	return row

def main():
	
	dict_20_0 = handleOutputDir(os.path.join("Results", "Experiment 2 Results", "Existing Benchmark"), 20, 0.0)
	dict_40_0 = handleOutputDir(os.path.join("Results", "Experiment 2 Results", "Existing Benchmark"), 40, 0.0)
	dict_60_0 = handleOutputDir(os.path.join("Results", "Experiment 2 Results", "Existing Benchmark"), 60, 0.0)
	dict_80_0 = handleOutputDir(os.path.join("Results", "Experiment 2 Results", "Existing Benchmark"), 80, 0.0)
	dict_100_0 = handleOutputDir(os.path.join("Results", "Experiment 2 Results", "Existing Benchmark"), 100, 0.0)
	
	dict_20_25 = handleOutputDir(os.path.join("Results", "Experiment 2 Results", "Existing Benchmark"), 20, 0.25)
	dict_40_25 = handleOutputDir(os.path.join("Results", "Experiment 2 Results", "Existing Benchmark"), 40, 0.25)
	dict_60_25 = handleOutputDir(os.path.join("Results", "Experiment 2 Results", "Existing Benchmark"), 60, 0.25)
	dict_80_25 = handleOutputDir(os.path.join("Results", "Experiment 2 Results", "Existing Benchmark"), 80, 0.25)
	dict_100_25 = handleOutputDir(os.path.join("Results", "Experiment 2 Results", "Existing Benchmark"), 100, 0.25)
	
	dict_20_50 = handleOutputDir(os.path.join("Results", "Experiment 2 Results", "Existing Benchmark"), 20, 0.5)
	dict_40_50 = handleOutputDir(os.path.join("Results", "Experiment 2 Results", "Existing Benchmark"), 40, 0.5)
	dict_60_50 = handleOutputDir(os.path.join("Results", "Experiment 2 Results", "Existing Benchmark"), 60, 0.5)
	dict_80_50 = handleOutputDir(os.path.join("Results", "Experiment 2 Results", "Existing Benchmark"), 80, 0.5)
	dict_100_50 = handleOutputDir(os.path.join("Results", "Experiment 2 Results", "Existing Benchmark"), 100, 0.5)
	
	dict_20_75 = handleOutputDir(os.path.join("Results", "Experiment 2 Results", "Existing Benchmark"), 20, 0.75)
	dict_40_75 = handleOutputDir(os.path.join("Results", "Experiment 2 Results", "Existing Benchmark"), 40, 0.75)
	dict_60_75 = handleOutputDir(os.path.join("Results", "Experiment 2 Results", "Existing Benchmark"), 60, 0.75)
	dict_80_75 = handleOutputDir(os.path.join("Results", "Experiment 2 Results", "Existing Benchmark"), 80, 0.75)
	dict_100_75 = handleOutputDir(os.path.join("Results", "Experiment 2 Results", "Existing Benchmark"), 100, 0.75)
	
	rows = [dict_20_0, dict_20_25, dict_20_50, dict_20_75,
		dict_40_0, dict_40_25, dict_40_50, dict_40_75,
		dict_60_0, dict_60_25, dict_60_50, dict_60_75,
		dict_80_0, dict_80_25, dict_80_50, dict_80_75,
		dict_100_0, dict_100_25, dict_100_50, dict_100_75]
	
	table = printTable(rows)
	
	# with open(os.path.join("RESULT_TABLE", "table.txt"), "w+") as oFile:
	# 	oFile.write(table) 

if __name__ == '__main__':
	main()
