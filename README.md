# FZI Human Brain Project Praktikum 2018

## Installation

Simply clone this repo into your ~/.opt/nrpStorage folder.
Careful - as of now - a symlink instead of a copy won't work.

```bash
cd ~/.opt/nrpStorage
git clone git@github.com:HBPNeurorobotics/hbpprak_2018_throwing.git
```

## Challenge

The goal is to throw the cylinder as far as possible.
When the cylinder touches the ground, or after a time limit (in the state machine), a reward corresponding to the distance of the cylinder is published.
All the joints of the robot arm, including its hand, can be actuacted.
The provided transfer functions provide some helpers.
There is a camera on the table observing the cylinder and the arm.

### Going further

The task can easily be made more challenging.
Here are some ideas:
* the cylinder could pop at random locations on the table
* one could pop random objects instead of just a cylinder
* different types of camera systems could be used (DVS, stereo, ...)
