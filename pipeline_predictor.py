from decode1 import *
from error_handling import *
from execute1 import *
from execute2 import *
from fetch1 import *
from memoryaccess1 import *
from registerupdate1 import *


# print(lisss)
def b_predict(PC):  # change0
	# print("table is "+str(table))
	l = len(table)
	if (l < PC):
		# print("less")
		return -1  # no data found
	else:
		if (type(table[PC]) == list):
			# print("found")
			return table[PC][0]
		else:
			# print("not foung")
			return -1  # no data found


def b_update(PC, branch, p):
	# print("updating "+str(PC))
	list = [p, branch]  # p is 1 if taken else 0
	table[PC] = list


def new_branch(PC, branch, prediction):
	# print("given PC is"+str(PC))
	l = len(table)
	if (l < PC):
		for i in range(l, PC):
			table.append(0)
		list = [prediction, branch]
		table.append(list)
	else:
		list = [prediction, branch]
		table[PC] = list


# change0 ends

def pipeline_predictor_func():
	lisss = []
	ins_count = 0  # inst count
	data_count = 0  # number of data trasfer
	alu_count = 0  # no.of control inst
	control_count = 0
	data_hazard = 0
	control_hazard = 0
	data_stall = 0
	control_stall = 0
	d_stall = 0  # flag to data stall
	c_stall = 0  # flag to control stall
	cnt = 1
	oops = 0
	fl = open('machinecode.txt', 'r')
	file8 = open('Stats.txt', 'w')
	Lines = fl.readlines()
	for line in Lines:
		each = line.split()
		if cnt != 1: lisss.append(len(each))
		cnt = cnt - 1

	fl.close()
	lisss.append(0)

	assign_labelled_instruction()
	globalss.assign_register()
	a = error_handling()
	if a == 1:
		# print('not passed')
		sys.exit()
	# print('passed')
	convert_to_machinecode()
	globalss.assign_memory()
	globalss.assign_stack()

	pipeline = []
	parameter = []
	lii_list = []

	table = []  # branch prediction table change
	b = -2  # branch predictor -2 implies it is not branch instruction change
	offset = 0  # default offset change
	branch_miss = 0  # change
	cycle_count = 0
	stalls = 0
	control_hazard = 0
	data_hazard = 0
	file2 = open('machinecode.txt', 'r')
	file6 = open('Details.txt', 'w')
	i = 1
	each = str(linecache.getline('machinecode.txt', i))
	flag = 0
	flag1 = 0
	# mark=0 #if 1 means label instruction
	flag3 = 0  # indicates to flush or not
	flag4 = 0  # indicates to flush in decode
	j1 = 10  # to store j, j will not be 10
	temp = []  # to store temps
	change = 0
	while 1 == 1:
		change = 0
		global reg
		reg.clear()
		# print("i is "+str(i))
		if each != '':
			if flag == 0:
				each = each.split()
				if (len(each) == 1):
					# mark=1
					globalss.PC_execution = globalss.PC_execution + 4
					i = int(globalss.PC_execution / 4) + 1
					each = (linecache.getline('machinecode.txt', i))
					continue
				ins_count = ins_count + 1
				parameter.append(0)
				pipeline.append(list(reg))
				lii_list.append('')
		else:
			change = 1

		j = 0
		if len(parameter) > 0:
			cycle_count = cycle_count + 1
		if len(parameter) == 0:
			break
		flag = 0
		# print("flag3 is "+str(flag3))
		while (j < len(parameter)):

			reg.clear()

			if parameter[j] == 0:
				temp = lii_list[j]
				lii_list.pop(j)
				lii_list.insert(j, str(fetch(each)))
				# print ("j is "+str(j))
				parameter[j] = 1  # fetch has been done
				file6.write("F " + "Cycle:" + str(cycle_count) + " " + str(globalss.PC_execution) + " " + str(
					lii_list[j]) + "\n")
				if b != -2:
					# print("here3")
					j1 = j
					b = -2  # changing b
				if lii_list[j][25:32] == '1100011':
					# mark=0
					# print("j of list is"+str(j))
					b = b_predict(globalss.PC_execution)
					# print("predicted"+str(b))
					if b == 1:  # case no data found by default assume not taken
						offset = 2 * binary_2_decimal(
							lii_list[j][20:24] + lii_list[j][1:7] + lii_list[j][24:25] + lii_list[j][0:1])
						globalss.PC_execution = globalss.PC_execution + offset
						# print("b is 1")
						flag1 = 1  # change_1 ends
				# parameter[j]=4
				if lii_list[j][25:32] == '1100111' or lii_list[j][25:32] == '1100011' or lii_list[j][
																						 25:32] == '1101111':
					c_stall = 1
					control_hazard = control_hazard + 1
					flag = 1
				if flag3 == 1:
					# print("flush "+str(lii_list[j]))
					lii_list.pop(j)
					lii_list.insert(j, temp)
					lii_list.pop(j)
					inst = "00000000000000000000000000010011"
					lii_list.insert(j, inst)
					# cycle_count=cycle_count-4
					parameter[j] = 1
					oops = oops + 1
					# reg.clear()
					# j=j+1
					# i=i-1
					# flag1=1
					flag3 = 0

			elif parameter[j] == 1:
				temp2 = pipeline[j]
				pipeline.pop(j)
				reg = decode(lii_list[j])
				file6.write("D " + "Cycle:" + str(cycle_count) + " " + str(globalss.PC_execution) + " " + str(
					lii_list[j]) + "\n")
				pipeline.insert(j, list(determine_exact_instruction(lii_list[j], reg)))  # change_1

				if b != -2:  # this means branch instruction #change2
					# flag=1
					reg == pipeline[j]
					# print("here4")
					execute(reg)
					# print("reg is")
					# print(reg)
					u = reg[6]
					reg.pop()
					mark = lisss[int(globalss.PC_execution / 4)]
					# print("mark is "+str(mark))
					# print("u is "+str(u)) #contains T or NT
					if b == 1:

						if (mark == 1):

							b_update(globalss.PC_execution - offset, offset, u)
						else:
							b_update(globalss.PC_execution - offset, offset, u)  # if branch is taken PC is changed
					if b == 0:
						if (mark == 1):

							b_update(globalss.PC_execution, offset, u)
						else:
							b_update(globalss.PC_execution, offset, u)  # if branch is taken PC is changed
					if b == -1:
						# print("PC_u"+str(globalss.PC_execution))

						new_branch(globalss.PC_execution, offset, u)

					if b == 1 and u == 0:  # it should not be taken but it is taken
						branch_miss = branch_miss + 1
						# globalss.PC_execution=globalss.PC_execution-offset-4
						flag1 = 0
						# print("here1")
						flag3 = 1
					# parameter[j+1]=0 #marked next instruction which is fetched as not fetched...check it is j-1 or j+1
					if b != 1 and u == 1:  # it should be taken but it is not
						branch_miss = branch_miss + 1
						offset = 2 * binary_2_decimal(
							lii_list[j][20:24] + lii_list[j][1:7] + lii_list[j][24:25] + lii_list[j][0:1])
						# print("offset is "+str(offset))
						# print("PC_0 is"+str(globalss.PC_execution))

						globalss.PC_execution = globalss.PC_execution + offset - 4
						print("PC is" + str(globalss.PC_execution))
						flag1 = 1
						flag3 = 1
						print("here2")
					# print ("j is "+str(j))
					# print("j1 is"+str(j1))
					# print("m_code is")
					# print(lii_list[j1-1])

					# pipeline.pop(j1)

					offset = 0  # changing offset to default  change2 ends

				if pipeline[j][4] == 'SB' or pipeline[j][4] == 'UJ' or pipeline[j][4] == 'I_3':
					flag = 1
					if (pipeline[j][4] == 'SB'):
						c_stall = 1
					else:
						d_stall = 1
				parameter[j] = 2

			elif parameter[j] == 2:
				file6.write("E " + "Cycle:" + str(cycle_count) + " " + str(globalss.PC_execution) + " " + str(
					lii_list[j]) + "\n")
				# check if any resister is creatinh problem or not
				# reg[rd,rs1,rs2,imm,type,oriname,execute_result,memoryaccessreult]
				if j - 1 < 0:
					reg = pipeline[j]
					pipeline.pop(j)
					pipeline.insert(j, list(execute(reg)))

				else:
					if (pipeline[j - 1][0] == pipeline[j][1] and pipeline[j][1] != -1) or (
							pipeline[j - 1][0] == pipeline[j][2] and pipeline[j][2] != -1):
						data_hazard = data_hazard + 1
						if pipeline[j - 1][4] != 'I_2':
							globalss.register[pipeline[j - 1][0]] = int(pipeline[j - 1][6])
						else:
							globalss.register[pipeline[j - 1][0]] = int(pipeline[j - 1][7])
					reg = pipeline[j]
					pipeline.pop(j)
					pipeline.insert(j, list(execute(reg)))
				parameter[j] = 3
				if (pipeline[j][6] == 1 and pipeline[j][4] == 'SB') or (pipeline[j][4] == 'UJ') or (
						pipeline[j][4] == 'I_3'):
					change = 0
					if (pipeline[j][4] == 'SB'):
						c_stall = 1
					else:
						d_stall = 1

				if (pipeline[j][6] == 1 and pipeline[j][4] == 'SB') or (pipeline[j][4] == 'UJ') or (
						pipeline[j][4] == 'I_3'):
					flag1 = 1
				if pipeline[j][4] == 'SB':

					# print("u_SB is "+ str(u))
					# print("reg_e is"+str(reg))
					if (reg[6] != u):
						if (u == 1):
							globalss.PC_execution = globalss.PC_execution - offset

						else:
							globalss.PC_execution = globalss.PC_execution + offset - 4
						oops = oops + 1

						flag3 = 1
						flag4 = 1

			elif parameter[j] == 3:
				file6.write("M " + "Cycle:" + str(cycle_count) + " " + str(globalss.PC_execution) + " " + str(
					lii_list[j]) + "\n")
				reg = pipeline[j]
				pipeline.pop(j)
				pipeline.insert(j, list(memoryaccess(reg)))
				parameter[j] = 4
				if pipeline[j][4] == 'SB':

					# print("u_SB is "+ str(u))
					# print("reg_e is"+str(reg))
					if (reg[6] != u):
						if (u == 1):
							globalss.PC_execution = globalss.PC_execution - offset
						else:
							globalss.PC_execution = globalss.PC_execution + offset
						# print("oops")
						flag3 = 1
						# cycle_count=cycle_count-4
						flag4 = 1

			elif parameter[j] == 4:

				file6.write("W " + "Cycle:" + str(cycle_count) + " " + str(globalss.PC_execution) + " " + str(
					lii_list[j]) + "\n")
				reg = pipeline[j]
				if reg[4] == 'I_2' or reg[4] == 'S':
					data_count = data_count + 1
				elif reg[4] == 'I_3' or reg[4] == 'SB' or reg[4] == 'UJ':
					control_count = control_count + 1
				elif reg[4] == 'R' or reg[4] == 'I_1' or reg[4] == 'U_lui' or reg[4] == 'U_auipc':
					alu_count = alu_count + 1
				pipeline.pop(j)
				parameter.pop(j)
				lii_list.pop(j)
				registerupdate(reg)
				reg.clear()
				j = j - 1

			j = j + 1
		# print("end "+str(i))
		globalss.register[0] = 0

		for x in pipeline:
			print(x)
		print("done")

		if flag == 1 or change == 1:
			stalls = stalls + 1
			if (c_stall == 1):
				control_stall = control_stall + 1
				c_stall = 0
			if (d_stall == 1):
				data_stall = data_stall + 1
				d_stall = 0
			continue
		if flag1 == 0:
			globalss.PC_execution = globalss.PC_execution + 4
			i = int(globalss.PC_execution / 4) + 1
		else:
			i = int(globalss.PC_execution / 4) + 1
			flag1 = 0
		each = (linecache.getline('machinecode.txt', i))

	file2.close()
	file6.close()
	print(memory_array)
	print(register)
	cycle_count = cycle_count - 5 * oops
	ins_count = ins_count - oops
	alu_count = alu_count - oops
	# print("oops "+str(oops))
	print('\n')
	print(":: STATS ::")
	print('The number of cycles are ' + str(cycle_count))
	print('The number of instructions executed are ' + str(ins_count))
	cpi = cycle_count / ins_count
	print('The CPI of program is ' + str(cpi))
	print('The number of load and store instructions executed are ' + str(data_count))
	print('The number of ALU instructions executed are ' + str(alu_count))
	print('The number of control instructions exeucted are ' + str(control_count))
	print('The number of stalls/bubbles in pipeline are ' + str(stalls))
	print('The number of data hazards are ' + str(data_hazard))
	print('The number of control hazards are ' + str(control_hazard))
	print('The number of Branch mispredictions are: ' + str(branch_miss))
	print('The number of stalls due to data hazard are ' + str(data_stall))  # look
	print('The number of stalls due to control hazard are ' + str(control_stall))
	print("----------------------------------------------------------------------------")

	file8.write(":: STATS :: \n")
	file8.write('The number of cycles are ' + str(cycle_count) + ' \n')
	file8.write('The number of instructions executed are ' + str(ins_count) + ' \n')
	file8.write('The CPI of program is ' + str(cpi) + ' \n')
	file8.write('The number of load and store instructions executed are ' + str(data_count) + ' \n')
	file8.write('The number of ALU instructions executed are ' + str(alu_count) + ' \n')
	file8.write('The number of control instructions exeucted are ' + str(control_count) + ' \n')
	file8.write('The number of stalls/bubbles in pipeline are ' + str(stalls) + ' \n')
	file8.write('The number of data hazards are ' + str(data_hazard) + ' \n')
	file8.write('The number of control hazards are ' + str(control_hazard) + ' \n')
	file8.write('The number of Branch mispredictions are: ' + str(branch_miss) + ' \n')
	file8.write('The number of stalls due to data hazard are ' + str(data_stall) + ' \n')  # look
	file8.write('The number of stalls due to control hazard are ' + str(control_stall) + ' \n')
	file8.close()


if __name__ == '__main__':
	pipeline_predictor_func()
