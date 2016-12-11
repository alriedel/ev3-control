# ev3-control
Control your Lego Mindstorms EV3 with a ps3-controller, inspiered by http://www.ev3dev.org/docs/tutorials/using-ps3-sixaxis/. Can drive, reverse, turn and rotate using the joystick.

# Setup
## What you need (for this project)
* Lego Mindstorms EV3 Home edition (or similar)
* ev3dev installed and working (see http://www.ev3dev.org/docs/getting-started/)
* a ps3-controller
* a working python environment (usually pre-installed)

## EV3-motors connections
The program will assume the following:
* the left large motor is connected into port B
* the right large motor is connected into port C
* optional: a medium motor connected into port A
* inversed orientation of all motors

# How-to start
* boot up ev3dev
* make sure that all driving motors are connected and that the brick has paired with your ps3-controller
* navigate into the working directory and run ps3_control.py
* when the Leds turn yellow, the program is ready to listen for controller-events
* use the right stick to drive and the select-button to stop the program
* use the left upper button to control the medium-motor
