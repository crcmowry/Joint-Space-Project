import math
import scipy.integrate as integrate
import pr2py

weights = list()

def get_weights(lengths,angles):
	if(len(lengths) == 1):
		weights.append(lengths[0])
		return weights
	else:
		l2 = lengths.pop()
		l1 = lengths.pop()
		a = angles.pop()

		f = lambda x: math.sqrt(l1**2 + l2**2 - 2*l1*l2*math.cos(x))
		average = abs(integrate.quad(f,a[0],a[1])[0]/(a[1]-a[0]))

		weights.append(l2)

		lengths.append(average)
		return get_weights(lengths,angles)


#lengths = input("Enter joint lengths as a list: ")
#angles = input("Enter joint angles as a list: ")

env, robot = pr2py.initialize(sim = True)


"""
def get_length():
	return 0
for index in robot.right_arm.GetArmJoints():
	print (robot.GetJoints()[index])
"""


"""
Upper Arm :: 400 mm
Forearm :: 321 mm
Wrist to Gripper Surface :: 120 to 200 mm
"""


lengths = [400,321,120]
angles = list()
for index in robot.right_arm.GetArmJoints():
	angles.append([robot.GetDOFLimits()[0][index],robot.GetDOFLimits()[1][index]])

print list(reversed(get_weights(lengths,angles)))