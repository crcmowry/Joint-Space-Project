import ast
import yaml

num_of_bins = int(input("How many bins? "))
joint_index = int(input("Which joint? ")) - 1
def f(x):
    return {
    	'x': 0,
        'y': 1,
        'z': 2,
    }[x]
dimension = f(input("x, y, or z? (enter in lowercase) "))

stream = file('data.yaml', 'r')    # 'document.yaml' contains a single YAML document.
data = yaml.load(stream)

min_DOF_value = data["DOF_limits"][0][joint_index]
max_DOF_value = data["DOF_limits"][1][joint_index]

increment = (max_DOF_value - min_DOF_value) / num_of_bins
ranges = [increment*(i+1) + min_DOF_value for i in range(num_of_bins)]
value = [0 for i in range(num_of_bins)]
count = [0 for i in range(num_of_bins)]



def modifiedBinarySearch(alist, item):
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


i = 0
for DOFs in data["DOFs"]:
	joint_value = DOFs[joint_index]
	bin_index = modifiedBinarySearch(ranges, joint_value)
	value[bin_index] += data["Transforms"][i][dimension][3]
	count[bin_index] += 1
	i += 1


average_value = list()
for i in range(num_of_bins):
	if count[i] != 0:
		average_value.append(value[i] / count[i])



with open("extracted_data.txt", "w") as data_file:
	for data in average_value:
		data_file.write("{0}\n".format(data))
	data_file.write("\n")
	for data in ranges:
		data_file.write("{0}\n".format(data))