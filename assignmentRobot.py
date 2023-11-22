from __future__ import print_function

import time
from sr.robot import *


""" RESEARCH TRACK 1 - AMI SOFIA QUIJANO SHIMIZU

Assignment: Write a python code that controls the robot to collect all the golden tokens together
The gray central square on the layout was considered as the "collection area".

The following steps where carried out:
	1. Move the robot to the collection area.
	2. Search for the first golden token, move towards it and grab it.
	3. Take it back to the collection area, release it and reference this first
	token as the "GOAL" point.
	4. Iteratively, look for another golden token from the GOAL position, move 
	towards it, grab it, take it back to the GOAL and release it.
	5. When all golden tokens are collected, stop searching for more.

For this algorithm, the following assumptions were made:
* Initial position and orientation of the robot is always the same one and it is the one given at
the initialization of the program
* The velocity and time needed for arriving to the central gray square, given the fixed initial 
position and orientation, are known
* It is known that there are 6 tokens in total
* It is known that the tokens are placed around the central gray square"""


""" FUNCTIONS """

def drive(speed, seconds):
    """
    Function for setting a linear velocity

    Args: speed (float): the speed of the wheels
	  seconds (float): the time interval of the motion
    """
    # Equal velocity on both motors causes a linear motion
    R.motors[0].m0.power = speed 
    R.motors[0].m1.power = speed
    time.sleep(seconds) # Duration of motion
    # Stopping motors
    R.motors[0].m0.power = 0 
    R.motors[0].m1.power = 0


def turn(speed, seconds):
    """
    Function for setting an angular velocity
    
    Args: speed (float): the speed of the wheels
	  seconds (float): the time interval of the motion
    """
    # Opposite direction velocities between motors causes a rotational motion
    R.motors[0].m0.power = speed  
    R.motors[0].m1.power = -speed
    time.sleep(seconds) # Duration of motion
    # Stopping motors
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0


def find_token(found_tokens):
    """
    Function to find the closest golden token

    Inputs:
        found_tokens (list): List of token codes which have been collected
        
    Returns:
        dist (float): distance of the closest token (-1 if no golden token is detected)
        rot_y (float): angle between the robot and the token (-1 if no golden token is detected)
        num (int): offset number of the token (-1 if no golden token is detected)
    """
    dist = 100
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD and token.info.offset not in found_tokens:
            dist = token.dist
            rot_y = token.rot_y
            num = token.info.offset
     #   elif token.info.offset in found_tokens:
     #       num = token.info.offset
     #       print('Token {} already collected. Searching...'.format(num))
    if dist == 100:
        return -1, -1, -1
    else:
        return dist, rot_y, num
        

def find_goal(goal_code):
    """
    Function to find the GOAL
    
    Input: 
        goal_code: offset number of the token referenced as the GOAL
    
    Returns:
        dist (float): distance from robot to the GOAL (-1 if GOAL is not detected)
        rot_y (float): angle between the robot and GOAL (-1 if GOAL is not detected)
"""
    dist = 100
    for goal in R.see():
        if goal.dist < dist and goal.info.offset == goal_code:
            dist = goal.dist
            rot_y = goal.rot_y
    if dist == 100:
        return -1, -1
    else:
        return dist, rot_y
    
        
def move_token(found_tokens, goal_code, action, a_th, d_th_token, d_th_goal, grabbed_token):

    """
    Function to move robot and tokens
    
    Input: 
        found_tokens (vector): List of token codes which have been collected
        goal_code (int): offset number of the token referenced as the GOAL
        action (int): variable that indicates the action case
        a_th (float): angle threshold
        d_th_token (float): distance threshold for grabbing and searcginf for tokens
        d_th_goal (float): distance threshold for releasing token at goal
    
    Returns:
        dist (float): distance from robot to the GOAL (-1 if GOAL is not detected)
        rot_y (float): angle between the robot and GOAL (-1 if GOAL is not detected)
"""
    
    list_actions = []
    """ dictionary: Sequence of velocities and times, for both linear and rotational
    motion, taken by the robot to go from the collection area to the first token"""
  
    cond = True # Condition to continue while loop
    
    while cond:
         
        if action == 1 or action == 2: # Looking for the first token or another one 
     #   elif action == 2: # Looking for token to be grabbed
            d_th = d_th_token
            dist, rot_y, num = find_token(found_tokens)
        
        elif action == 3: # Looking for goal to release token
            d_th = d_th_goal
            dist, rot_y = find_goal(goal_code)
            num = grabbed_token
            
    
        if num in found_tokens and num != goal_code: # If token detected has already been collected, turn right
            print('Token already collected. Searching...')
            turn(2, 0.5)
            list_actions.append({'action': 'turn', 'speed': 10, 'time': 0.5})

        elif dist == -1: # If no token is detected, turn right  
            print('No token on the sight! Searching...')
            turn(2, 0.5) 
            list_actions.append({'action': 'turn', 'speed': 10, 'time': 0.5})
        
        elif dist >= d_th: # If token is aligned, check angle between robot and token
            if -a_th <= rot_y <= a_th: # If token is within range, move towards token
                print('Token detected! Approaching')
                drive(30, 0.5) 
                list_actions.append({'action': 'drive', 'speed': 30, 'time': 0.5})
        
            elif rot_y > a_th: # If token is on the left, turn right
                print('Token detected! Turning right a bit')
                turn(2, 0.5)
                list_actions.append({'action': 'turn', 'speed': 2, 'time': 0.5})
        
            elif rot_y < -a_th: # If token is on the right, turn left
                print('Token detected! Turning left a bit')
                turn(-2, 0.5)
                list_actions.append({'action': 'turn', 'speed': -2, 'time': 0.5})
    
        elif dist < d_th:
            if action == 1:
                R.grab()
                print('Token {} grabbed'.format(num))    
                print('Taking token to collection area')
                # Move back to collection area by backtracking stored motion
                for i in range(len(list_actions)):
                    move = list_actions[len(list_actions)-i-1]
                
                    if move['action'] == 'drive':
                        drive(-move['speed'], move['time'])
                
                    else:
                        turn(-move['speed'], move['time'])
            
                turn(-10,1) # Adjust placing position 
                R.release() # Release token  
                drive(-10,3) # Move away to allow some space
                #found_tokens.append(num) # Add token to the list of collected tokens
                print('Token {} is the GOAL reference!'.format(num))
                cond = False
                return num
     
            if action == 2: # If token needs to be grabbed and is close enough, 
                R.grab() # Grab token
                print('Token {} grabbed'.format(num)) 
                cond = False 
                return num
        
            elif action == 3: # If token needs to be released and GOAL is close enough 
                R.release() # Release token
                #found_tokens.append(num) # Add token to the list of collected tokens
                print('Token {} dropped at GOAL'.format(num))
                # Move away to allow some space
                drive(-15, 3)
                turn(10,3)
                cond = False
                return num


"""MAIN"""
        
a_th = 2.0
""" float: Threshold for the control of the orientation"""

d_th_token = 0.4
""" float: Threshold for the control of the linear distance when searching for a token"""

d_th_goal = 0.7
""" float: Threshold for the control of the linear distance when searching the GOAL"""

found_tokens = []
""" list: Empty list to be filled with the offset numbers of the found tokens"""

list_actions = []
""" dictionary: Sequence of velocities and times, for both linear and rotationak motion, taken 
by the robot to go from the collection area to the first token"""

goal_code = -1 

action = 1

R = Robot()
""" instance of the class Robot"""


print('Moving to center of arena...')
# Move to center of collection area 
turn(0.5, 0.5)
drive(43, 6.5) 
print('This is the collection area!')
   
while 1:
    print('RUNNING ACTION ', action)
    print(goal_code)
    print('Collected tokens are ', found_tokens)
   
    if action == 1:
        num = move_token(found_tokens, goal_code, action, a_th, d_th_token, d_th_goal, -1)
        found_tokens.append(num) # Add token to the list of collected tokens
        action = 2
        goal_code = num
           
    elif action == 2:
        num = move_token(found_tokens, goal_code, action, a_th, d_th_token, d_th_goal, -1) 
        print('Searching for new a token to grab')
        action = 3
        
        
    elif action == 3:
        print('Moving to GOAL token')
        num = move_token(found_tokens, goal_code, action, a_th, d_th_token, d_th_goal, num)
        action = 2
        found_tokens.append(num) # Add token to the list of collected tokens
    
    if len(found_tokens) == 6: # If all 6 tokens have been collected, exit loop
        print('All tokens {} have been collected! GREAT JOB :D'.format(found_tokens)) 
        exit() 
    
        
        
