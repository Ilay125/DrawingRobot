import math
from consts import *


##
# @brief The inverse kinamtics function - converts (x,y)->(s1, s2)
# @param x - The x value of the end effector
# @param y - The y value of the end effector
# @return A tuple that represents the angle of the motors (s1, s2)
# #
def inv_kin(x, y):
    x -= motor_center[0]
    y -= motor_center[1]

    # Angle from left shoulder to end effector
    beta1 = math.atan2( y, (L0 + x) )

    # Angle from right shoulder to end effector
    beta2 = math.atan2( y, (L0 - x) )

    # Alpha angle pre-calculations
    alpha1_calc = (L1**2 + ( (L0 + x)**2 + y**2 ) - L2**2) / (2*L1*math.sqrt( (L0 + x)**2 + y**2 ))  
    alpha2_calc = (L1**2 + ( (L0 - x)**2 + y**2 ) - L2**2) / (2*L1*math.sqrt( (L0 - x)**2 + y**2 ))  

    # If calculations > 1, will fail acos function
    if alpha1_calc > 1 or alpha2_calc > 1:
        return -1, -1

    # Angle of left shoulder - beta1 and right shoulder - beta2
    alpha1 = math.acos(alpha1_calc)
    alpha2 = math.acos(alpha2_calc)

    # Angles of left and right shoulders
    shoulder1 = beta1 + alpha1
    shoulder2 = math.pi - beta2 - alpha2
    
    return shoulder1, shoulder2

##
# @brief The forward kinamtics function - converts (s1,s2)->(x, y)
# @param s1 - The angle of the right motor (1)
# @param y - The angel of the left motor (2)
# @return A tuple that represents the cooredinates of the end effector
# #
def forward_kin(theta1, theta2):
    # Elbows
    xL = -L0 + L1 * math.cos(theta1)
    yL = 0 + L1 * math.sin(theta1)
    xR =  L0 + L1 * math.cos(theta2)
    yR = 0 + L1 * math.sin(theta2)

    # Distance between elbows
    dx = xR - xL
    dy = yR - yL
    d = math.hypot(dx, dy)

    # midpoint along the line connecting elbows
    a = d / 2
    h = math.sqrt(max(L2**2 - a**2, 0))  # avoid domain error

    x0 = xL + a * dx / d
    y0 = yL + a * dy / d

    # pick the "lower" intersection (elbows down)
    x = x0 - h * dy / d
    y = y0 + h * dx / d

    # convert to screen coordinates
    return motor_center[0] + x, motor_center[1] + y

