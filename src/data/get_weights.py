import math
import scipy.integrate as integrate
import pr2py
import pprint as pp

weights = list()

def get_weights(lengths,angles):
	if(len(lengths) == 1):
		weights.append(lengths[0])
		return weights
	else:
		l2 = lengths.pop()
		l1 = lengths.pop()
		a = angles.pop()

		f = lambda x: math.sqrt(l1**2 + l2**2 - l1*l2*math.cos(x))
		average = abs(integrate.quad(f,a[0],a[1])[0]/(a[1]-a[0]))

		weights.append(l2)

		lengths.append(average)
		return get_weights(lengths,angles)

def get_length(l1,l2):
	delta_x = l2[0][3] - l1[0][3]
	delta_y = l2[1][3] - l1[1][3]
	delta_z = l2[2][3] - l1[2][3]
	return (delta_x**2 + delta_y**2 + delta_z**2)**(1.0/2)


def get_transforms():
	links = ["r_shoulder_pan_link", "r_shoulder_lift_link", "r_upper_arm_roll_link", "r_elbow_flex_link", "r_forearm_roll_link", "r_wrist_flex_link", "r_wrist_roll_link",]
	link_transforms = list()
	for our_link in links:
		for k in range(len(robot.GetLinks())):
			if robot.GetLink(our_link) == robot.GetLinks()[k]:
				link_transforms.append(robot.GetLinkTransformations()[k].tolist())
	link_transforms.append(robot.right_arm.GetEndEffectorTransform().tolist())
	return link_transforms



env, robot = pr2py.initialize(sim = True)
robot.right_arm.SetActive()


link_transform = get_transforms()

lengths = list()
prev_index = 1
for i in range(3):
	index = i * 2 + 3
	lengths.append(get_length(link_transform[index],link_transform[prev_index]))
	prev_index = index



angles = list()
limits = list(robot.GetActiveDOFLimits())
for i in range(2):
	index = i * 2 + 3
	angles.append([limits[0][index]+math.pi,limits[1][index]+math.pi])

print limits
print angles
print lengths
print list(reversed(get_weights(lengths,angles)))








"""
Upper Arm :: 400 mm
Forearm :: 321 mm
Wrist to Gripper Surface :: 180 mm
"""

"""
<joint:r_shoulder_pan_joint (27), dof=27, parent=pr2>
<joint:r_shoulder_lift_joint (28), dof=28, parent=pr2>
<joint:r_upper_arm_roll_joint (29), dof=29, parent=pr2>
<joint:r_elbow_flex_joint (30), dof=30, parent=pr2>
<joint:r_forearm_roll_joint (31), dof=31, parent=pr2>
<joint:r_wrist_flex_joint (32), dof=32, parent=pr2>
<joint:r_wrist_roll_joint (33), dof=33, parent=pr2>
"""

"""
 RaveGetEnvironment(1).GetKinBody('pr2').GetLink('r_shoulder_pan_link'),
 RaveGetEnvironment(1).GetKinBody('pr2').GetLink('r_shoulder_lift_link'),
 RaveGetEnvironment(1).GetKinBody('pr2').GetLink('r_upper_arm_roll_link'),
 RaveGetEnvironment(1).GetKinBody('pr2').GetLink('r_upper_arm_link'),
 RaveGetEnvironment(1).GetKinBody('pr2').GetLink('r_elbow_flex_link'),
 RaveGetEnvironment(1).GetKinBody('pr2').GetLink('r_forearm_roll_link'),
 RaveGetEnvironment(1).GetKinBody('pr2').GetLink('r_forearm_cam_frame'),
 RaveGetEnvironment(1).GetKinBody('pr2').GetLink('r_forearm_cam_optical_frame'),
 RaveGetEnvironment(1).GetKinBody('pr2').GetLink('r_forearm_link'),
 RaveGetEnvironment(1).GetKinBody('pr2').GetLink('r_wrist_flex_link'),
 RaveGetEnvironment(1).GetKinBody('pr2').GetLink('r_wrist_roll_link'),
"""