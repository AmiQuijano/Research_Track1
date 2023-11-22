# Python Robot Simulator
Assignment 1 for Research Track 1 Course
MSc Robotics Engineering at University of Genova
-------------------

## Simulator description
This is a simple, portable simulator developed by [Student Robotics](https://studentrobotics.org/).
The arena was modified to suit the particular objective of this exercise.

The simulator, in this particular project, provides one **Holonomic robot** and 6 equidistant **golden tokens** which are placed around a central gray square, as it can be observed in the image below.

![Alt Text](images/img2.png)

## Simulator Documentation
The API for controlling a simulated robot is designed to be as similar as possible to the [SR API][sr-api].

### Motors

The simulated robot has two motors configured for skid steering, connected to a two-output [Motor Board](https://studentrobotics.org/docs/kit/motor_board). The left motor is connected to output `0` and the right motor to output `1`.

The Motor Board API is identical to [that of the SR API](https://studentrobotics.org/docs/programming/sr/motors/), except that motor boards cannot be addressed by serial number. So, to turn on the spot at one quarter of full power, one might write the following:

```python
R.motors[0].m0.power = 25
R.motors[0].m1.power = -25
```

### The Grabber

The robot is equipped with a grabber, capable of picking up a token which is in front of the robot and within 0.4 metres of the robot's centre. To pick up a token, call the `R.grab` method:

```python
success = R.grab()
```

The `R.grab` function returns `True` if a token was successfully picked up, or `False` otherwise. If the robot is already holding a token, it will throw an `AlreadyHoldingSomethingException`.

To drop the token, call the `R.release` method.

Cable-tie flails are not implemented.

### Vision

To help the robot find tokens and navigate, each token has markers stuck to it, as does each wall. The `R.see` method returns a list of all the markers the robot can see, as `Marker` objects. The robot can only see markers which it is facing towards.

Each `Marker` object has the following attributes:

* `info`: a `MarkerInfo` object describing the marker itself. Has the following attributes:
  * `code`: the numeric code of the marker.
  * `marker_type`: the type of object the marker is attached to (either `MARKER_TOKEN_GOLD`, `MARKER_TOKEN_SILVER` or `MARKER_ARENA`).
  * `offset`: offset of the numeric code of the marker from the lowest numbered marker of its type. For example, token number 3 has the code 43, but offset 3.
  * `size`: the size that the marker would be in the real game, for compatibility with the SR API.
* `centre`: the location of the marker in polar coordinates, as a `PolarCoord` object. Has the following attributes:
  * `length`: the distance from the centre of the robot to the object (in metres).
  * `rot_y`: rotation about the Y axis in degrees.
* `dist`: an alias for `centre.length`
* `res`: the value of the `res` parameter of `R.see`, for compatibility with the SR API.
* `rot_y`: an alias for `centre.rot_y`
* `timestamp`: the time at which the marker was seen (when `R.see` was called).

For example, the following code lists all of the markers the robot can see:

```python
markers = R.see()
print "I can see", len(markers), "markers:"

for m in markers:
    if m.info.marker_type in (MARKER_TOKEN_GOLD, MARKER_TOKEN_SILVER):
        print " - Token {0} is {1} metres away".format( m.info.offset, m.dist )
    elif m.info.marker_type == MARKER_ARENA:
        print " - Arena marker {0} is {1} metres away".format( m.info.offset, m.dist )
```

[sr-api]: https://studentrobotics.org/docs/programming/sr/

# Installing and running 
The simulator was built and run with Ubuntu 22 and Python 3. Install them if it is not the case.
The simulator requires the [pygame](https://www.pygame.org/news) library, [PyPyBox2D](https://pypi.org/project/pypybox2d/2.1-r331/), and [PyYAML](https://pypi.org/project/PyYAML/). For installing them, run the following lines in the terminal.
```
$ sudo apt-get install python3-dev python3-pip python3-pygame python3-yaml
$ sudo pip3 install pypybox2d
$ cd /usr/local/lib/python3.8/dist-packages/pypybox2d
```
(check pypybox2d install directory since it might be different)

To download and run this simulator, install git and clone this repository. 
```
$ git clone https://github.com/AmiQuijano/Research_Track1.git
```

Once all the dependencies are installed, simply run the following line to test the simulator.
```
$ python3 run.py assignmentRobot.py
```

# Assignment
The project aims to make a holonomic robot move around the arena to find and grab all the golden tokens and collect them in a desired zone. For this assignment, the chosen dropp off zone was the central gray square of the arena. 

The result of the developed script is the following :D

![Alt Text](images/img1.png)

## Code Description: Pseudocode
The code in the file `assignmentRobot.py` contains the following functions and main explained with pseudocode as follows:

### drive(speed, seconds)
This function makes the robot move in a straight line forward or backwards (depending on `speed` sign) for a certain time given a desired speed. 

Arguments:
* `speed`: The velocity of the motors in this case equal on both motors in order to move straight.
* `seconds`:Time interval during which the robot will move straight.

```
Function drive(speed, seconds):
    Set power of Robot.motor.right to speed
    Set power of Robot.motor.left to speed
    Sleep for seconds
    Set power of Robot.motor.right to 0
    Set power of Robot.motor.left to 0
```
### turn(speed, seconds)
This function makes the robot turn either right or left (depending on `speed` sign) a certain time given a desired speed. 

Arguments:
* `speed`: The velocity of the motors in this case equal in magnitude on both motors but opposite in sign in order to make a turn.
* `seconds`:Time interval during which the robot will move straight.
  
```
Function turn(speed, seconds):
    Set power of Robot.motor.right to speed
    Set power of Robot.motor.left to -speed
    Sleep for seconds
    Set power of Robot.motor.right to 0
    Set power of Robot.motor.left to 0
```
### find_token(found_tokens)
This function finds the closest golden token identified by the robot with `R.see` within an initial maximum distance `dist` which have not yet been collected before. Keep in mind that `R.see` gives the distance `dist` and angle `rot_y` between the robot and the token seen. 

Arguments:
* `found_tokens`: List of token codes which have been collected

Returns:
* `dist`: distance of the closest token (-1 if no golden token is detected)
* `rot_y`: angle between the robot and the token (-1 if no golden token is detected)
* `num`: offset number or ID of the token (-1 if no golden token is detected)

```   
    FOR each token in R.see:
        If (token.dist < dist) and (token.type is MARKER_TOKEN_GOLD) and (token.ID not in found_tokens):
            Set dist to token.dist
            Set rot_y to token.rot_y
            Set num to token.ID
    END FOR
    
    IF dist is still 100:
        Return -1, -1, -1
    ELSE:
        Return dist, rot_y, num
```
### find_goal(goal_code)
This function finds the token assigned as the goal position (in this case, the center of the gray square in layout) identified by the robot with `R.see` within a maximum distance defined as `dist`. Keep in mind that `R.see` gives the distance `dist` and angle `rot_y` between the robot and the token seen. 

Arguments:
* `goal_code`: offset number of the token referenced as the goal

Returns:
* `dist`: distance to the goal token (-1 if no golden token is detected)
* `rot_y`: angle between the robot and the goal token (-1 if no golden token is detected)

```
Function find_goal(goal_code):
    FOR each goal in R.see:
        IF (goal.dist < dist) and (goal.ID is goal_code):
            Set dist to goal.dist
            Set rot_y to goal.rot_y
    END FOR
    
    IF dist is still 100:
        Return -1, -1
    ELSE:
        Return dist, rot_y
```

### move_token(found_tokens, goal_code, action, a_th, d_th_token, d_th_goal, grabbed_token)
This function moves the robot according to 3 cases:
* Case 1: Search for the first token, approach it, grab it, move it to center of arena and place it there. Make it the goal point for all future tokens found.
* Case 2: Search for a new token, approach it and grab it, only if it has not been already collected.
* Case 3: Move the grabbed token to the goal point once the goal has been found and place it there.

Arguments:
* `found_tokens`: List of token codes which have been collected
* `goal_code`: offset number of the token referenced as the goal
* `action`: Case number
* `a_th`: angle threshold
* `d_th_token`: distance threshold for approaching a token
* `d_th_goal`: distance threshold for approaching the goal token
* `grabbed_token`: Token that has been grabbed in Case 2`

Returns:
* `num`: The goal (for Case 1), the grabbed token (for Case 2) and the released token (for Case 3)

```
Function move_token(found_tokens, goal_code, action, a_th, d_th_token, d_th_goal, grabbed_token):

    WHILE condition is True:
        IF Case 1 or Case 2:
            distance_threshold = distance_threshold_for_approaching_token
            dist, rot_y, num = find_token

        ELSEIF Case 3:
            distance_threshold = distance_threshold_for_approaching_goal
            dist, rot_y = find_goal
            num = grabbed_token

        IF num is in found_tokens and num is not goal_code:
            print 'Token already collected. Searching...'
            turn_right
            record_motion

        ELIF dist is -1:
            print 'No token in sight! Searching...'
            turn_right
            record_motion

        ELIF dist is >= to distance_threshold:
            IF -angle_threshold <= rot_y <= angle_threshold:
                print 'Token detected! Approaching'
                drive_forward
                record_motion
                
            ELIF rot_y > angle_threshold:
                print 'Token detected! Turning right a bit'
                turn_right
                record_motion
                
            ElIf rot_y < -angle_threshold::
                print 'Token detected! Turning left a bit'
                turn_left
                record_motion

        ELIF dist < distance_threshold:
            IF Case 1:
                grab_token
                print 'Token ID grabbed'
                print 'Taking token to the collection area'
                For i in range of recorded_motions_list length:
                   take_last_recorded_motion_of_list

                    IF last_recorded_motion is drive:
                        drive_at_opposite_recorded_speed
  
                    ELSE:
                        turn_at_opposite_recorded_speed

                turn_left
                release_token
                drive_backwards
                print 'Token ID is the GOAL reference!'
                Set condition to False
                Return num

            ELIF Case 2:
                grab_token
                print 'Token ID grabbed'
                Set condition to False
                Return num

            ELIF Case 3:
                release_token
                print 'Token ID dropped at GOAL'
                drive_backwards
                turn_right
                Set condition to False
                Return num

```
### Main
```
Main function to move robot and tokens

Initialize needed variables and thresholds

print 'Moving to center of arena...'
turn_right
drive_forward
print 'This is the collection area!'
   
WHILE True:
    print 'RUNNING CASE #'
    print 'Goal is token ID_of_goal_token'
    print 'Collected tokens are found_tokens'
   
    IF Case 1:
        num = call move_token
        add token_ID to found_tokens
        Case = Case 2
        goal_code = num
           
    ELIF Case 2:
        num = call move_token
        print 'Searching for new token to grab'
        Case = Case 3
        
    ELIF Case 3:
        print 'Moving to GOAL token'
        num = call move_token
        Case = Case 2
        add token_ID to found_tokens
    
    IF all_tokens_collected
        print 'All tokens have been collected! GREAT JOB :D'
        exit
```

## Main encountered difficulties



## Possible improvements
The code works very smoothly in the current arena layout. Theredfore, it would be worthit to test the code in other arena layouts where the golden tokens are placed differently or where there are also other types of tokens such as silver ones.
