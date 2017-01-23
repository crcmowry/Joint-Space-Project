from random import random
from time import gmtime, strftime
from math import sqrt
import herbpy

DOF_values = open("DOF_values.txt", "a")														# r: read, w: write, a: append
x_y_z_position = open("x_y_z_position.txt", "a")

# Makes a time stamp at the top of each document.
# This is really only useful for when they
# (the documents) are being appended to instead
# of written to.
x_y_z_position.write("%s\n\n" % strftime("%a, %d %b %Y %H:%M:%S", gmtime()))
DOF_values.write("%s\n\n" % strftime("%a, %d %b %Y %H:%M:%S", gmtime()))


iterations = input("How much data? ")



env, robot = herbpy.initialize(sim = True)
robot.right_arm.SetActive()
limits = robot.GetActiveDOFLimits()

pos = robot.right_arm.GetEndEffectorTransform() 												# This should be the starting position of the end effector.
old_dof_values = robot.right_arm.GetDOFValues() 												# The DOF values at the starting position. Possibly all 0s.


x_y_z_position.write("{0}\n".format(pos))
DOF_values.write("{0}\n".format(old_dof_values))




def random_dof_values(lowerBound, upperBound):
	return random() * (upperBound - lowerBound) + lowerBound




for i in range(0,iterations):
	new_dof_values = [random_dof_values(limits[0][j],limits[1][j]) for j in range(0,7)]			# Generates the new random position within the range of the min and max
	
	robot.right_arm.SetDOFValues(new_dof_values)


	pos = robot.right_arm.GetEndEffectorTransform() 											# Gets the pos at the new_dof_values.

	x_y_z_position.write("{0}\n".format(pos))
	DOF_values.write("{0}\n".format(new_dof_values))

	old_dof_values = new_dof_values


x_y_z_position.write("\n")
DOF_values.write("\n")
x_y_z_position.close()
DOF_values.close()