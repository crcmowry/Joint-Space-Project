import yaml
from yaml import CLoader as Loader, CDumper as Dumper
import pprint as pp

stream = file('data.yaml', 'r')
data = yaml.load(stream, Loader=Loader)


def get_length(l1,l2):
	delta_x = l2[0][3] - l1[0][3]
	delta_y = l2[1][3] - l1[1][3]
	delta_z = l2[2][3] - l1[2][3]
	return (delta_x**2 + delta_y**2 + delta_z**2)**(1.0/2)


total_lengths = [0,0,0]


for transform in data["Transforms"]:
	for i in range(3):
		total_lengths[i] += get_length(transform[i*2+1],transform[7])


average_lengths = list()
for datum in total_lengths:
	average_lengths.append(datum/len(data["Transforms"]))


print average_lengths