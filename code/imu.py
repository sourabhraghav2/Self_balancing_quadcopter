import math

deltat =(0.01) #sampling period in seconds (shown as 1 ms)

gyroMeasError=float(3.14159265358979* (5.0 / 180.0)) # gyroscope measurement error in  /s (shown as 5 deg/s)
beta =float(math.sqrt(3.0/ 4.0) * gyroMeasError)

SEq_1 = 1.0
SEq_2 = 0.0
SEq_3 = 0.0
SEq_4 = 0.0 # estimated orientation quaternion elements with initial conditions
def  filterUpdate( w_x,  w_y,  w_z,  a_x,  a_y,  a_z):
	global SEq_1,SEq_2,SEq_3,SEq_4
	halfSEq_1 = float(0.5 * SEq_1)
	halfSEq_2 = float(0.5 * SEq_2)
	halfSEq_3 = float(0.5 * SEq_3)
	halfSEq_4 = float(0.5 * SEq_4)
	twoSEq_1 = float(2.0 * SEq_1)
	twoSEq_2 = float(2.0 * SEq_2)
	twoSEq_3 = float(2.0 * SEq_3)

	# Normalise the accelerometer measurement
	norm = math.sqrt(a_x * a_x + a_y * a_y + a_z * a_z)
	a_x /= norm
	a_y /= norm
	a_z /= norm
	# Compute the objective function and Jacobian
	f_1 = twoSEq_2 * SEq_4 - twoSEq_1 * SEq_3 - a_x
	f_2 = twoSEq_1 * SEq_2 + twoSEq_3 * SEq_4 - a_y
	f_3 = 1.0 - twoSEq_2 * SEq_2 - twoSEq_3 * SEq_3 - a_z
	J_11or24 = twoSEq_3 # J_11 negated in matrix multiplication
	J_12or23 = 2.0 * SEq_4
	J_13or22 = twoSEq_1 # J_12 negated in matrix multiplication
	J_14or21 = twoSEq_2
	J_32 = 2.0 * J_14or21 # negated in matrix multiplication
	J_33 = 2.0 * J_11or24 # negated in matrix multiplication
	# Compute the gradient (matrix multiplication)
	SEqHatDot_1 = J_14or21 * f_2 - J_11or24 * f_1
	SEqHatDot_2 = J_12or23 * f_1 + J_13or22 * f_2 - J_32 * f_3
	SEqHatDot_3 = J_12or23 * f_2 - J_33 * f_3 - J_13or22 * f_1
	SEqHatDot_4 = J_14or21 * f_1 + J_11or24 * f_2
	# Normalise the gradient
	norm = math.sqrt(SEqHatDot_1 * SEqHatDot_1 + SEqHatDot_2 * SEqHatDot_2 + SEqHatDot_3 * SEqHatDot_3 + SEqHatDot_4 * SEqHatDot_4)
	SEqHatDot_1 /= norm
	SEqHatDot_2 /= norm
	SEqHatDot_3 /= norm
	SEqHatDot_4 /= norm
	# Compute the quaternion derrivative measured by gyroscopes
	SEqDot_omega_1 = -halfSEq_2 * w_x - halfSEq_3 * w_y - halfSEq_4 * w_z
	SEqDot_omega_2 = halfSEq_1 * w_x + halfSEq_3 * w_z - halfSEq_4 * w_y
	SEqDot_omega_3 = halfSEq_1 * w_y - halfSEq_2 * w_z + halfSEq_4 * w_x
	SEqDot_omega_4 = halfSEq_1 * w_z + halfSEq_2 * w_y - halfSEq_3 * w_x
	# Compute then integrate the estimated quaternion derrivative
	SEq_1 += (SEqDot_omega_1 - (beta * SEqHatDot_1)) * deltat
	SEq_2 += (SEqDot_omega_2 - (beta * SEqHatDot_2)) * deltat
	SEq_3 += (SEqDot_omega_3 - (beta * SEqHatDot_3)) * deltat
	SEq_4 += (SEqDot_omega_4 - (beta * SEqHatDot_4)) * deltat
	# Normalise quaternion
	norm = math.sqrt(SEq_1 * SEq_1 + SEq_2 * SEq_2 + SEq_3 * SEq_3 + SEq_4 * SEq_4)
	SEq_1 /= norm
	SEq_2 /= norm
	SEq_3 /= norm
	SEq_4 /= norm

	return [SEq_1,SEq_2,SEq_3,SEq_4]
