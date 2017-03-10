import math
import scipy.integrate as integrate

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
lengths = [100,200,10,1]
angles = [[0,3*math.pi/2],[0,math.pi],[math.pi/2,math.pi*3/2]]

print list(reversed(get_weights(lengths,angles)))