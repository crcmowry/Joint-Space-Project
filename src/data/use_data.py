import herbpy



DOF_values = open("DOF_values.txt", "r")														# r: read, w: write, a: append
x_y_z_position = open("x_y_z_position.txt", "r")

num_of_bins = input("How many bins? ")
joint_index = input("Which joint? ") - 1
dimension = input("x, y, or z? (enter in lowercase) ")


env, robot = herbpy.initialize(sim = True)
robot.right_arm.SetActive()
limits = robot.GetActiveDOFLimits()

min_DOF_value = limits[0][joint_index]
max_DOF_value = limits[1][joint_index]
increment = (max_DOF_value - min_DOF_value) / num_of_bins
ranges = [increment*(i+1) + min_DOF_value for i in range(0, num_of_bins)]
value = [0 for i in range(0,num_of_bins)]
count = [0 for i in range(0,num_of_bins)]



def binarySearch(alist, item):
    first = 0
    last = len(alist)-1
    found = False

    while first<=last and not found:
        midpoint = (first + last)//2
        if alist[midpoint] >= item and alist[midpoint]-increment <= item:
            found = True
        else:
            if item < alist[midpoint]:
                last = midpoint-1
            else:
                first = midpoint+1

    return midpoint




for line in DOF_values:
	split_line = line.split(",")
	print split_line
	if line != '' and line[0] == '[' and line[1] != ' ':
		#joint = float(line[1:line.index(",")])
		joint = float(split_line[joint_index])
		index = binarySearch(ranges, joint)
		value[index] += joint 																	#3d position
		count[index] += 1

for i in range(0, num_of_bins):
	if count[i] != 0:
		value[i] /= count[i]

print value
print count
print ranges