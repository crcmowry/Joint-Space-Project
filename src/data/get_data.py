from random import random
from math import sqrt
#import herbpy

import pr2py

import yaml
from yaml import CLoader as Loader, CDumper as Dumper


def random_dof_value(lowerBound, upperBound):
		return random() * (upperBound - lowerBound) + lowerBound

def get_transforms():
	links = ["r_shoulder_pan_link", "r_shoulder_lift_link", "r_upper_arm_roll_link", "r_elbow_flex_link", "r_forearm_roll_link", "r_wrist_flex_link", "r_wrist_roll_link",]
	link_transforms = list()
	for our_link in links:
		for k in range(len(robot.GetLinks())):
			if robot.GetLink(our_link) == robot.GetLinks()[k]:
				link_transforms.append(robot.GetLinkTransformations()[k].tolist())
	link_transforms.append(robot.right_arm.GetEndEffectorTransform().tolist())
	return link_transforms


iterations = input("How much data? ")


#env, robot = herbpy.initialize(sim = True)
env, robot = pr2py.initialize(sim = True)
robot.right_arm.SetActive()


limits = list(robot.GetActiveDOFLimits())
dof_values = robot.right_arm.GetDOFValues().tolist() 												# The DOF values at the starting position. Possibly all 0s.

for i in range(len(limits)):
	limits[i] = limits[i].tolist()

data = {"DOF_limits": limits, "DOFs": [dof_values], "Transforms": [get_transforms()]}



for i in range(iterations):
	#dof_values = [random_dof_value(limits[0][j],limits[1][j]) for j in range(7)]			# Generates the new random position within the range of the min and max
	print i
	dof_values_copy = list()
	for dof_value in dof_values:
		dof_values_copy.append(dof_value)
	dof_values = list()
	
	for j in range(7):
		if(j%2 == 0):
			dof_values.append(dof_values_copy[j])
		else:
			dof_values.append(random_dof_value(limits[0][j],limits[1][j]))


	"""for j in range(3):
		index = j * 2 + 1
		dof_values[index] = random_dof_value(limits[0][index],limits[1][index])"""


	robot.right_arm.SetDOFValues(dof_values)


	

	data["DOFs"].append(dof_values)
	data["Transforms"].append(get_transforms())

	


with file('data.yaml', 'w') as stream:
	dump = yaml.dump(data, stream, encoding='utf-8', default_flow_style=False, Dumper=Dumper)