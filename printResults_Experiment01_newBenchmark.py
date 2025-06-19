import os
import time
import math

def printTable(RESULT):
	oStr = ""
	keys = []
	for key in RESULT.keys():
		keys.append(key)
	oStr += "{:<5} {:<18} {:<18} {:<18} {:<18} {:<18} {:<18}".format(keys[0],keys[1],keys[2],keys[3],keys[4],keys[5],keys[6])
	oStr += "\n-----------------------------------------------------------------------------------------------------------------------------------------------"

	rows = []
	for valueList in RESULT.values():
		if len(valueList) > len(rows):
			for _ in range(len(valueList) - len(rows)):
				rows.append([])
		
		for i in range(len(valueList)):
			rows[i].append(valueList[i])

	for row in rows:
		oStr += "\n{:<5} {:<18} {:<18} {:<18} {:<18} {:<18} {:<18}".format(row[0],round(row[1] / 1000,3),round(row[2],3),round(row[3],3),row[4],row[5],row[6])
	oStr += "\n-----------------------------------------------------------------------------------------------------------------------------------------------"

	print(oStr)
	return oStr

def mergeDictsToTable(RESULTS_20, RESULTS_40, RESULTS_60, RESULTS_80, RESULTS_100):
	RESULT = {"n" : [], "Avg. CPU Time" : [], "Avg. Nodes" : [], "Avg. Models" : [], "Min Model" : [], "Max Model" : [], "Solved Instance Count" : []}

	for resDict in [RESULTS_20, RESULTS_40, RESULTS_60, RESULTS_80, RESULTS_100]:
		RESULT["n"].append(resDict["n"])
		RESULT["Avg. CPU Time"].append(resDict["avg_cpu"])
		RESULT["Avg. Nodes"].append(resDict["avg_nodes"])
		RESULT["Avg. Models"].append(resDict["avg_models"])
		RESULT["Min Model"].append(resDict["min_model"])
		RESULT["Max Model"].append(resDict["max_model"])
		RESULT["Solved Instance Count"].append(resDict["amount"])

	return RESULT

def handleOutputDir(outputDir, instSize):
	RESULTS_0  = {"n" : instSize, "avg_cpu" : 0, "avg_nodes" : 0, "avg_models" : 0, "max_model" : 0, "min_model" : float("inf"), "amount" : 0}
	RESULTS_25 = {"n" : instSize, "avg_cpu" : 0, "avg_nodes" : 0, "avg_models" : 0, "max_model" : 0, "min_model" : float("inf"), "amount" : 0}
	RESULTS_5  = {"n" : instSize, "avg_cpu" : 0, "avg_nodes" : 0, "avg_models" : 0, "max_model" : 0, "min_model" : float("inf"), "amount" : 0}
	RESULTS_75 = {"n" : instSize, "avg_cpu" : 0, "avg_nodes" : 0, "avg_models" : 0, "max_model" : 0, "min_model" : float("inf"), "amount" : 0}

	dictList = [RESULTS_0, RESULTS_25, RESULTS_5, RESULTS_75]

	for root,dirs,files in os.walk(outputDir):
		for outputFile in files:
			# print(f"Handling file: {outputFile}!")

			model = 0
			cpuTime = 0
			nodes = 0

			with open(os.path.join(outputDir, outputFile), "r") as oFile:
				lines = oFile.readlines()
				line = lines[0] # output files contain a single line

				tokens = line.strip().split(":")
				model = int(tokens[1].strip().split("n")[0].strip())
				cpuTime = int(tokens[4].strip().split("t")[0].strip())
				nodes = int(tokens[2].strip().split("m")[0].strip())
		


			p1 = float(outputFile.strip().split("_")[2].strip())
			dictIndex = int((p1 * 100) / 25)
			dictList[dictIndex]["avg_cpu"] += cpuTime
			dictList[dictIndex]["avg_nodes"] += nodes
			dictList[dictIndex]["avg_models"] += model
			dictList[dictIndex]["amount"] += 1

			if model < dictList[dictIndex]["min_model"]: dictList[dictIndex]["min_model"] = model
			if model > dictList[dictIndex]["max_model"]: dictList[dictIndex]["max_model"] = model

	for i in range(len(dictList)):
		if dictList[i]["amount"] != 0:
			dictList[i]["avg_cpu"] /= dictList[i]["amount"]
			dictList[i]["avg_nodes"] /= dictList[i]["amount"]
			dictList[i]["avg_models"] /= dictList[i]["amount"]

	return RESULTS_0, RESULTS_25, RESULTS_5, RESULTS_75


def main():
	
	dict_20_0, dict_20_25, dict_20_5, dict_20_75 = handleOutputDir(os.path.join("Results", "Experiment 1 Results", "New Benchmark", "RES_20"), 20)
	dict_40_0, dict_40_25, dict_40_5, dict_40_75 = handleOutputDir(os.path.join("Results", "Experiment 1 Results", "New Benchmark", "RES_40"), 40)
	dict_60_0, dict_60_25, dict_60_5, dict_60_75 = handleOutputDir(os.path.join("Results", "Experiment 1 Results", "New Benchmark", "RES_60"), 60)
	dict_80_0, dict_80_25, dict_80_5, dict_80_75 = handleOutputDir(os.path.join("Results", "Experiment 1 Results", "New Benchmark", "RES_80"), 80)
	dict_100_0, dict_100_25, dict_100_5, dict_100_75 = handleOutputDir(os.path.join("Results", "Experiment 1 Results", "New Benchmark", "RES_100"), 100)

	RESULT_0 = mergeDictsToTable(dict_20_0, dict_40_0, dict_60_0, dict_80_0, dict_100_0)
	RESULT_25 = mergeDictsToTable(dict_20_25, dict_40_25, dict_60_25, dict_80_25, dict_100_25)
	RESULT_5 = mergeDictsToTable(dict_20_5, dict_40_5, dict_60_5, dict_80_5, dict_100_5)
	RESULT_75 = mergeDictsToTable(dict_20_75, dict_40_75, dict_60_75, dict_80_75, dict_100_75)

	print("\n\n")
	table_0 = printTable(RESULT_0)
	print("\n\n")
	table_25 = printTable(RESULT_25)
	print("\n\n")
	table_5 = printTable(RESULT_5)
	print("\n\n")
	table_75 = printTable(RESULT_75)

	# with open(os.path.join("RESULTS", "RESULT_P1_0.txt"), "w+") as oFile:
	# 	oFile.write(table_0)
	
	# with open(os.path.join("RESULTS", "RESULT_P1_25.txt"), "w+") as oFile:
	# 	oFile.write(table_25)

	# with open(os.path.join("RESULTS", "RESULT_P1_50.txt"), "w+") as oFile:
	# 	oFile.write(table_5)

	# with open(os.path.join("RESULTS", "RESULT_P1_75.txt"), "w+") as oFile:
	# 	oFile.write(table_75)

if __name__ == '__main__':
	main()