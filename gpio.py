import RPi.GPIO as GPIO
from time import sleep
from os import system

'''
************************
**       NOTES        **
************************

Light on = GPIO.HIGH
Light off = GPIO.LOW

The unpressed button starts out as true, when pressed it becomes false and conditions are executed

- wait for network
- clear playlists just in case
- set play to random on
- gather all playlists and combine 
- start playing playlist
- enter control loop forever

'''



'''
************************
**     VARIABLES      **
************************
'''
# GPIO pin numbers
blue_pin 			= 17
green_pin 			= 27
prev_button_pin 	= 22
play_button_pin 	= 5
stop_button_pin 	= 6
next_button_pin 	= 13
pause_button_pin 	= 19

# Playback commands
# System(command) executes commands in python
random_on 	= 'sudo mpc random on'
random_off 	= 'sudo mpc random off'
repeat_on	= 'sudo mpc repeat on'
repeat_off 	= 'sudo mpc repeat off'
next 		= 'sudo mpc next'
prev 		= 'sudo mpc prev'
play 		= 'sudo mpc play'
pause 		= 'sudo mpc pause'
load 		= 'sudo mpc add'
stop 		= 'sudo mpc stop'
clear 		= 'sudo mpc clear'


# Playlist URIs
big_list = 'spotify:user:johndavidsimmons:playlist:1TYInycooWEdVcKpo0MvgE'
# big_list2 = 'spotify:user:johndavidsimmons:playlist:0fry73cbZ8yvkl6qlDUD2o'

'''
************************
** SETUP DECLARATIONS **
************************
'''

# Set numbering system and turn off warnings
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Set up for input/output
GPIO.setup(prev_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(play_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(stop_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(next_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(pause_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(blue_pin, GPIO.OUT)
GPIO.setup(green_pin, GPIO.OUT)


'''
************************
**     FUNCTIONS      **
************************
'''
def load_playlist(uri):
	return system('{} {}'.format(load, uri))


'''
************************
**        MAIN        **
************************
'''

# Wait for the network before trying to load playlists
sleep(60)

# clear anything in the playlist
# Load/build playlists
system(clear)
load_playlist(big_list)

# Set playlist to random
system(random_on)

#play playlist
system(play)

# Turn on green light to indicate controls are active, ensure blue light is off
GPIO.output(green_pin, GPIO.HIGH)
GPIO.output(blue_pin, GPIO.LOW)

try:

	# Control loop
	while True:

		# Variable equal to the button beginning state of True
		prev_button_input_state = GPIO.input(prev_button_pin)
		play_button_input_state = GPIO.input(play_button_pin)
		stop_button_input_state = GPIO.input(stop_button_pin)
		next_button_input_state = GPIO.input(next_button_pin)
		pause_button_input_state = GPIO.input(pause_button_pin)

		# If the button is false (its state when pressed)
		if prev_button_input_state == False:

			# Turn on the blue light
			GPIO.output(blue_pin, GPIO.HIGH)
			
			# Send the next song command
			system(prev)
			
			# sleep for 1/5 second then await more commands
			sleep(0.1)

			# Explicitly turn light off
			GPIO.output(blue_pin, GPIO.LOW)

		if play_button_input_state == False:
			GPIO.output(blue_pin, GPIO.HIGH)
			system(play)
			sleep(0.1)
			GPIO.output(blue_pin, GPIO.LOW)

		if stop_button_input_state == False:
			GPIO.output(blue_pin, GPIO.HIGH)
			system(stop)
			sleep(0.1)
			GPIO.output(blue_pin, GPIO.LOW)

		if next_button_input_state == False:
			GPIO.output(blue_pin, GPIO.HIGH)
			system(next)
			sleep(0.1)
			GPIO.output(blue_pin, GPIO.LOW)

		if pause_button_input_state == False:
			GPIO.output(blue_pin, GPIO.HIGH)
			system(pause)
			sleep(0.1)
			GPIO.output(blue_pin, GPIO.LOW)

except KeyboardInterrupt:

	# undo everything
	system(stop)
	system(clear)
	system(random_off)
	GPIO.output(blue_pin, GPIO.LOW)
	GPIO.output(blue_pin, GPIO.LOW)	
	GPIO.cleanup()

else:
	exit()