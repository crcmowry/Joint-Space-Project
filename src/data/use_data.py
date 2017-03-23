import yaml
from yaml import CLoader as Loader, CDumper as Dumper

import numpy as np
from scipy import stats
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D



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



def inputs():
	#return 100, 1, [0,2], 1

	num_of_bins = int(input("How many bins? "))
	joint_index = int(input("Which joint? ")) - 1
	num_of_dimensions = int(input("How many task space dimensions do you wish to plot? "))
	dimensions = list()
	for i in range(num_of_dimensions):
		dimensions.append({'x': 0,'y': 1,'z': 2}[input("x, y, or z? (enter in lowercase) ")])
	regression_type = {'s':0,'l':1}[input("What type of regression (s/l)? ")]
	return num_of_bins, joint_index, dimensions, regression_type



def linear_regression(x,y_list):
	try:

		if(len(y_list) == 1):
			y = y_list[0]

			slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
			predict_y = intercept + slope * x

			plt.xlabel("Joint Space")
			plt.ylabel("Task Space: {0}".format(['x','y','z'][dimensions[0]]))

			plt.plot(x, y, 'o')
			plt.plot(x, predict_y, 'k-')
			plt.show()



		elif(len(y_list) == 2):
			fig = plt.figure()
			ax = fig.add_subplot(111, projection='3d')

			predicts = list()
			for i in range(2):
				slope, intercept, r_value, p_value, std_err = stats.linregress(x,y_list[i])
				predicts.append(intercept + slope * x)

			plt.xlabel("Joint Space")
			plt.ylabel("Task Space: {0}".format(['x','y','z'][dimensions[0]]))
			ax.set_zlabel("Task Space: {0}".format(['x','y','z'][dimensions[1]]))

			ax.plot(x, predicts[0], predicts[1])
			ax.scatter(x, y_list[0], y_list[1])
			plt.show()

	except ValueError:
		print("Not all bins are full, Vikram.")



def display_sinusoidal_regression(x,y_list):
	try:
		if(len(y_list) == 1):
			plt.plot(x, y_list[0], '.')
			plt.plot(x, sinusoidal_regression(x,y_list[0]))
			plt.show()
		elif(len(y_list) == 2):
			fig = plt.figure()
			ax = fig.add_subplot(111, projection='3d')

			plt.xlabel("Joint Space")
			plt.ylabel("Task Space: {0}".format(['x','y','z'][dimensions[0]]))
			ax.set_zlabel("Task Space: {0}".format(['x','y','z'][dimensions[1]]))

			ax.plot(x,sinusoidal_regression(x,y_list[0]), sinusoidal_regression(x,y_list[1]))
			ax.scatter(x, y_list[0], y_list[1])
			plt.show()

	except ValueError:
		print("Not all bins are full, Vikram.")



def sinusoidal_regression(x,y):
	guess_freq = 1
	guess_amplitude = 1
	guess_phase = 1
	guess_offset = 1

	p0=[guess_freq, guess_amplitude,
	    guess_phase, guess_offset]

	# create the function we want to fit
	def my_sin(x, freq, amplitude, phase, offset):
	    return np.sin(x * freq + phase) * amplitude + offset

	# now do the fit
	fit = curve_fit(my_sin, x, y)


	# recreate the fitted curve using the optimized parameters
	data_fit = my_sin(x, *fit[0])
	return data_fit



num_of_bins, joint_index, dimensions, regression_type = inputs()

# Loads data from yaml
stream = file('data.yaml', 'r')
data = yaml.load(stream, Loader=Loader)


while True:

	# Variable Declaration
	min_DOF_value = data["DOF_limits"][0][joint_index]
	max_DOF_value = data["DOF_limits"][1][joint_index]
	increment = (max_DOF_value - min_DOF_value) / num_of_bins
	ranges = [increment*(i+1) + min_DOF_value for i in range(num_of_bins)]
	value = list()
	for j in range(len(dimensions)):
		value.append([0 for i in range(num_of_bins)])
	count = [0 for i in range(num_of_bins)]


	# Sorts data
	i = 0
	for DOFs in data["DOFs"]:
		joint_value = DOFs[joint_index]
		bin_index = modifiedBinarySearch(ranges, joint_value)
		for j in range(len(dimensions)):
			value[j][bin_index] += data["Transforms"][i][7][dimensions[j]][3]
		count[bin_index] += 1	
		i += 1


	# Creates average_value
	average_value = list()
	for num in dimensions:
		average_value.append(list())
	for i in range(num_of_bins):
		for j in range(len(dimensions)):
			if count[i] != 0:
				average_value[j].append(value[j][i] / count[i])
			else:
				average_value[j].append(0)


	# Displays data
	dep_vars = np.array(average_value)
	ind_var = np.array(ranges)
	if(regression_type == 0):
		display_sinusoidal_regression(ind_var,dep_vars)
	elif(regression_type == 1):
		linear_regression(ind_var,dep_vars)



	if not input("Continue? (1/0): "):
		break

	num_of_bins, joint_index, dimensions, regression_type = inputs()