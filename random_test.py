from random import random
from time import gmtime, strftime

f = open("random_test_output.txt", "a")

maxAngle = 420
minAngle = 69


f.write("%s\n" % strftime("%a, %d %b %Y %H:%M:%S", gmtime()))

for i in range(1,101):
	output = "%d: %f" % (i, random() * (maxAngle - minAngle) + minAngle)
	print output
	f.write("%s\n" % output)

f.write("\n")
f.close()