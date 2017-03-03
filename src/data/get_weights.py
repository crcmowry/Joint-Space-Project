import math

weights = list()

def get_weights(lengths,angles):
	if(len(lengths) == 1):
		weights.append(lengths[0])
		return weights
	else:
		l2 = lengths.pop()
		l1 = lengths.pop()
		a2 = angles.pop()
		a1 = angles.pop()

		dx = l1 * math.sin(a1) - l2 * math.sin(a1 + a2)
		dy = l1 * math.cos(a1) - l2 * math.cos(a1 + a2)

		d = math.sqrt(dx**2 + dy**2)
		a = math.atan(dy/dx)
		
		print a

		weights.append(l2)

		lengths.append(d)
		angles.append(a)
		return get_weights(lengths,angles)

lengths = input("Enter joint lengths as a list: ")
angles = input("Enter joint angles as a list: ")
print list(reversed(get_weights(lengths,angles)))