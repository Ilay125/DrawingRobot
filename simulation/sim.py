import pygame
import numpy as np
import math
from consts import *
from kinematics import *

win = pygame.display.set_mode(win_res)
clock = pygame.time.Clock()


##
# @brief Drawing the arms
# @param s1 - The angle of the right motor
# @param s2 - The angle of the left motor
# #
def draw_arms(s1, s2):
    R = 10
    efx, efy = forward_kin(s1, s2)
    p1 = ( motor_center[0]-L0 + L1 *math.cos(s1), motor_center[1] + L1 * math.sin(s1)  )
    p2 = ( motor_center[0] + L0 + L1*math.cos(s2), motor_center[1] + L1 * math.sin(s2)  )

    # sanity check
    '''
    print(f"Left arm length = {math.hypot(p1[0] - (motor_center[0]-L0), p1[1] - motor_center[1])}")
    print(f"Right arm length = {math.hypot(p2[0] - (motor_center[0]+L0), p2[1] - motor_center[1])}\n\n")
    '''

    # L base arm
    pygame.draw.line(win, (255, 0, 0), (motor_center[0] - L0, motor_center[1]), p2, R//2)

    # R base arm
    pygame.draw.line(win, (255, 0, 0), (motor_center[0] + L0, motor_center[1]), p1, R//2)

    # L hold arm
    pygame.draw.line(win, (0, 0, 255), p2, (efx, efy), R//2)

    # R hold arm
    pygame.draw.line(win, (0, 0, 255), p1, (efx, efy), R//2)

    pygame.draw.circle(win, (0, 0, 0), (motor_center[0] - L0, motor_center[1]), R, 0) # LM
    pygame.draw.circle(win, (0, 0, 0), (motor_center[0] + L0, motor_center[1]), R, 0) # RM
    pygame.draw.circle(win, (0, 0, 0), p1, R, 0) # p1
    pygame.draw.circle(win, (0, 0, 0), p2, R, 0) # p2
    pygame.draw.circle(win, (0, 0, 0), (efx, efy), R, 0) # ef


##
# @brief Move each motor with his own constant angular velocity and sync them to
#        end on the same time
# @param win - The window to draw on
# @param org_s1 - The angel of the right motor from the src point
# @param org_s2 - The angel of the left motor from the src point
# @param new_s1 - The angel of the right motor from the dest point
# @param new_s2 - The angel of the left motor from the new point
# @param dots - The list of all visited dots to draw them later and show
#               the path moved
# #
def linear_move(win, org_s1, org_s2, new_s1, new_s2, dots):
    delta_s1 = new_s1 - org_s1
    delta_s2 = new_s2 - org_s2

    max_delta = max(abs(delta_s1), abs(delta_s2))
    n_steps = int(np.ceil(max_delta / MAX_OMEGA))

    s1_range = np.linspace(org_s1, new_s1, n_steps+1)
    s2_range = np.linspace(org_s2, new_s2, n_steps+1)

    for i in range(n_steps+1):
        s1_curr = s1_range[i]
        s2_curr = s2_range[i]
        efx, efy = forward_kin(s1_curr, s2_curr)

        dots.append((efx, efy))

        win.fill((255, 255, 255))
        for d in dots:
            pygame.draw.circle(win, (0, 0, 0), d, r_marker, 0)
        draw_arms(s1_curr, s2_curr)

        pygame.display.flip()
        clock.tick(FPS)

##
# @brief Moves the ef from src to dest in a straight line.
# @param win - The window to draw on
# @param efx_o - The x coordinate of the src end effector 
# @param efy_o - The y coordinate of the src end effector 
# @param efx_n - The x coordinate of the dest end effector 
# @param efx_n - The x coordinate of the dest end effector 
# @param dots - The list of all visited dots to draw them later and show
#               the path moved
# #
def straight_line(win, efx_o, efy_o, efx_n, efy_n, dots):
    n_steps = max(1, int(np.ceil(abs(efx_n - efx_o) / dx)))

    if efx_n == efx_o:
        # vertical line
        y_range = np.linspace(efy_o, efy_n, max(2, int(abs(efy_n - efy_o)/dx)+1))
        x_range = np.full_like(y_range, efx_o)
    else:
        slope = (efy_n - efy_o) / (efx_n - efx_o)
        inter = efy_o - slope * efx_o
        dist = abs(efx_n - efx_o)
        n_steps = max(1, int(np.ceil(dist / dx)))
        x_range = np.linspace(efx_o, efx_n, n_steps + 1)
        y_range = slope * x_range + inter

    x_range = np.linspace(efx_o, efx_n, n_steps + 1)
    y_range = slope * x_range + inter

    for i in range(n_steps):
        x_curr, y_curr = x_range[i], y_range[i]
        x_next, y_next = x_range[i+1], y_range[i+1]

        s1_curr, s2_curr = inv_kin(x_curr, y_curr)
        s1_next, s2_next = inv_kin(x_next, y_next)

        # skip unreachable points
        if s1_curr == -1 or s2_curr == -1 or s1_next == -1 or s2_next == -1:
            print("Unreachable coordinates here")
            continue
        linear_move(win, s1_curr, s2_curr, s1_next, s2_next, dots)

##
# @brief The main loop
# #
def main():
    # initial values
    efx, efy = 400, 400
    s1, s2 = inv_kin(efx, efy)
    click = False
    run = True
    dots = []

    # sanity check
    '''
    s1_t, s2_t = math.radians(20), math.radians(160)
    x_t, y_t = forward_kin(s1_t, s2_t)
    s1_tt, s2_tt = inv_kin(x_t, y_t)

    print(f"forward: ({x_t}, {y_t})\tbackwards:({math.degrees(s1_tt), math.degrees(s2_tt)})\n\n")
    '''

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            # Checking for click on screen
            if event.type == pygame.MOUSEBUTTONDOWN:
                tmp_efx, tmp_efy = event.pos
                click = True
        
        # Debouncer
        if click:   
            click = False

            tmp_s1, tmp_s2 = inv_kin(tmp_efx, tmp_efy) 
            if (tmp_s1 == -1 and tmp_s2 == -1):
                print("Unreachable coordinates")
                continue

            straight_line(win, efx, efy, tmp_efx, tmp_efy, dots)
            efx, efy = tmp_efx, tmp_efy
            s1, s2 = tmp_s1, tmp_s2 

        
        
        win.fill((255, 255, 255))

        # Drawing the path of the EF
        for d in dots:
            pygame.draw.circle(win, (0, 0, 0), d, r_marker, 0)

        draw_arms(s1, s2)

        pygame.display.flip()
        clock.tick(FPS)


    pygame.quit()

if __name__ == "__main__":
    main()
    exit()