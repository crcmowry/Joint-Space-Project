from random import random
from math import sqrt
import herbpy
import yaml
from yaml import CLoader as Loader, CDumper as Dumper


def random_dof_values(lowerBound, upperBound):
		return random() * (upperBound - lowerBound) + lowerBound


iterations = input("How much data? ")


env, robot = herbpy.initialize(sim = True)
robot.right_arm.SetActive()


limits = list(robot.GetActiveDOFLimits())
pos = robot.right_arm.GetEndEffectorTransform().tolist() 												# This should be the starting position of the end effector.
old_dof_values = robot.right_arm.GetDOFValues().tolist() 												# The DOF values at the starting position. Possibly all 0s.

for i in range(len(limits)):
	limits[i] = limits[i].tolist()

data = {"DOF_limits": limits, "DOFs": [old_dof_values], "Transforms": [pos]}


for i in range(iterations):
	new_dof_values = [random_dof_values(limits[0][j],limits[1][j]) for j in range(7)]			# Generates the new random position within the range of the min and max
	
	robot.right_arm.SetDOFValues(new_dof_values)

	pos = robot.right_arm.GetEndEffectorTransform().tolist()												# Gets the pos at the new_dof_values.

	data["DOFs"].append(new_dof_values)
	data["Transforms"].append(pos)

	old_dof_values = new_dof_values


with file('data.yaml', 'w') as stream:
	dump = yaml.dump(data, stream, encoding='utf-8', default_flow_style=False, Dumper=Dumper)