from random import random
from time import gmtime, strftime
from math import sqrt

f = open("random_test_output.txt", "w")
f.write("%s\n" % strftime("%a, %d %b %Y %H:%M:%S", gmtime()))


iterations = input("How much data? ")
min_x = input("min x value: ")
max_x = input("max x value: ")
min_y = input("min y value: ")
max_y = input("max y value: ")
min_z = input("min z value: ")
max_z = input("max z value: ")

old_pos = [(min_x + max_x) / 2,(min_y + max_y) / 2,(min_z + max_z) / 2]
old_dof_values = ["look at this net"] #GetDOFValues(old_pos)


def randomPos(lowerBound, upperBound):
	return random() * (upperBound - lowerBound) + lowerBound


for i in range(0,iterations):
	new_pos = [randomPos(min_x, max_x), randomPos(min_y, max_y), randomPos(min_z, max_z)]
	new_dof_values = ["watch and learn here's the deal"] #GetDOFValues(new_pos)
	f.write("{0}       {1}       {2}       {3}\n".format(old_pos, old_dof_values, new_pos, new_dof_values))
	old_pos = new_pos
	old_dof_values = new_dof_values


f.write("\n")
f.close()