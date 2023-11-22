# Python Robot Simulator
Assignment for Research Track 1 Course.

### Simulator description
This is a simple, portable simulator developed by [Student Robotics](https://studentrobotics.org/).
The arena was modified to suit the particular objective of this exercise.

The simulator, in this particular arena, provides one **Holonomic robot** and 6 equidistant **golden tokens** which are placed around a central gray square, as it can be observed in the image below.

### Installing and running 
The simulator was built and run with Ubuntu 22 and Python 3. Install them if it is not the case.
The simulator requires the [pygame](https://www.pygame.org/news) library, [PyPyBox2D](https://pypi.org/project/pypybox2d/2.1-r331/), and [PyYAML](https://pypi.org/project/PyYAML/). For installing them, run the following lines in the terminal.
```
$ sudo apt-get install python3-dev python3-pip python3-pygame python3-yaml
$ sudo pip3 install pypybox2d
$ cd /usr/local/lib/python3.8/dist-packages/pypybox2d
```
(check pypybox2d install directory since it might be different)

To download and run this simulator, install git and clone this repository. 

Once all the dependencies are installed, simply run the following line to test the simulator.
```
$ python3 run.py assignment.py
```
### Assignment description
The project aims to make a holonomic robot move around the arena to find and grab all the golden tokens and collect them in a desired zone.

## Code Description: Pseudocode
The code in the file `assignment.py` contains the following functions explained as pseudocode:

### drive(speed, seconds)
```
jkhjbw
```
