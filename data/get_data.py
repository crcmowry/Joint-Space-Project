from random import random
from time import gmtime, strftime
from math import sqrt

DOF_values = open("DOF_values.txt", "w")														# r: read, w: write, a: append
x_y_z_position = open("x_y_z_position.txt", "w")

# Makes a time stamp at the top of each document.
# This is really only useful for when they
# (the documents) are being appended to instead
# of written to.
x_y_z_position.write("%s\n\n" % strftime("%a, %d %b %Y %H:%M:%S", gmtime()))
DOF_values.write("%s\n\n" % strftime("%a, %d %b %Y %H:%M:%S", gmtime()))


iterations = input("How much data? ")

# The following makes a cube that represents
# the task space of the robot. In reality,
# this won't be realistic because the joints
# will sweep in a fixed radius and cut out a
# semisphical shape.
min_x = input("min x value: ")
max_x = input("max x value: ")
min_y = input("min y value: ")
max_y = input("max y value: ")
min_z = input("min z value: ")
max_z = input("max z value: ")


# TODO: Implement old_pos to be the starting
# 		position of the end effector.
#			AND
#		Make dof_values the DOF values
#		at the starting position
old_pos = [(min_x + max_x) / 2,(min_y + max_y) / 2,(min_z + max_z) / 2] 						# This should be the starting position of the end effector.
dof_values = [0 for j in range(0,7)] 															# The DOF values at the starting position. Possibly all 0s.

x_y_z_position.write("{0}\n".format(old_pos))
DOF_values.write("{0}\n".format(dof_values))

def randomPos(lowerBound, upperBound):
	return random() * (upperBound - lowerBound) + lowerBound


for i in range(0,iterations):
	new_pos = [randomPos(min_x, max_x), randomPos(min_y, max_y), randomPos(min_z, max_z)]		# Generates the new random position within the range of the min and max

	# TODO: Move the end effector from old_pos to new_pos
	#
	#
	#
	#
	#
	#


	# TODO: Make dof_values the DOF values after the
	#		end effector moves from old_pos to new_pos.
	dof_values = [random() * 360 for j in range(0,7)] 											# Gets the DOF values at the new_pos.

	x_y_z_position.write("{0}\n".format(new_pos))
	DOF_values.write("{0}\n".format(dof_values))

	old_pos = new_pos


x_y_z_position.write("\n")
DOF_values.write("\n")
x_y_z_position.close()
DOF_values.close()