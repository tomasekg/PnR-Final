import pigo
import time  # import just in case students need
import random

# setup logs
import logging
LOG_LEVEL = logging.INFO
LOG_FILE = "/home/pi/PnR-Final/log_robot.log"  # don't forget to make this file!
LOG_FORMAT = "%(asctime)s %(levelname)s %(message)s"
logging.basicConfig(filename=LOG_FILE, format=LOG_FORMAT, level=LOG_LEVEL)


class Piggy(pigo.Pigo):
    """Student project, inherits teacher Pigo class which wraps all RPi specific functions"""

    def __init__(self):
        """The robot's constructor: sets variables and runs menu loop"""
        print("I have been instantiated!")
        # Our servo turns the sensor. What angle of the servo( ) method sets it straight?
        self.MIDPOINT = 74
        # YOU DECIDE: How close can an object get (cm) before we have to stop?
        self.SAFE_STOP_DIST = 30
        self.HARD_STOP_DIST = 15
        # YOU DECIDE: What left motor power helps straighten your fwd()?
        self.LEFT_SPEED = 125
        # YOU DECIDE: What left motor power helps straighten your fwd()?
        self.RIGHT_SPEED = 130
        # This one isn't capitalized because it changes during runtime, the others don't
        self.turn_track = 0
        # Our scan list! The index will be the degree and it will store distance
        self.scan = [None] * 180
        self.set_speed(self.LEFT_SPEED, self.RIGHT_SPEED)
        # let's use an event-driven model, make a handler of sorts to listen for "events"
        if __name__ == "__main__":
            while True:
                self.stop()
                self.menu()

    def menu(self):
        """Displays menu dictionary, takes key-input and calls method"""
        ## This is a DICTIONARY, it's a list with custom index values
        # You may change the menu if you'd like to add an experimental method
        menu = {"n": ("Navigate forward", self.nav),
                "d": ("Dance", self.dance),
                "o": ("Obstacle count", self.obstacle_count),
                "c": ("Calibrate", self.calibrate),
                "s": ("Check status", self.status),
                "q": ("Quit", quit_now),
                "f": ("Forward", self.move_straight),
                "r": ("Right", self.move_right),
                "l": ("Left", self.move_left),
                "b": ("Back", self.move_back)
                }
        # loop and print the menu...
        for key in sorted(menu.keys()):
            print(key + ":" + menu[key][0])
        # store the user's answer
        ans = raw_input("Your selection: ")
        # activate the item selected
        menu.get(ans, [None, error])[1]()

    def move_straight(self):
        self.encF(int(input("How far forward?: ")))

    def move_right(self):
        self.encR(int(input("How far right?: ")))

    def move_left(self):
        self.encL(int(input("How far left?: ")))

    def move_back(self):
        self.encB(int(input("How far back?: ")))

    # YOU DECIDE: How does your GoPiggy dance?
    def dance(self):
        """executes a series of methods that add up to a compound dance"""
        if not self.safe_to_dance():
            print("\n---- NOT SAFE TO DANCE ----\n")
        if self.safe_to_dance():
            print("\n---- LET'S DANCE ----\n")
        ##### WRITE YOUR FIRST PROJECT HERE
            self.twist()
            self.shake()
            self.swerve()
            self.forward_and_back()
            self.surprise()
            self.wheelie()
            self.s_curve_dance()
            self.final_move()
            self.x_up()

    def safe_to_dance(self):
        """circles around and checks for any obstacle"""
        # check for problems
        for x in range(4):
            if not self.is_clear():
                return False
            self.encR(7) # is this 90 deg?
        # if we find no problems:
        return True

    def twist(self):
        """the robot goes forward and swivels then moves its head"""
        self.encF(20)
        self.encR(25)
        self.encL(25)
        self.servo(120)
        self.servo(60)

    def shake(self):
        """I want the robot to shake right and left quickly"""
        for x in range(3):
            self.encR(5)
            self.encL(5)

    def swerve(self):
        """The robot will go forward and turn right"""
        self.encF(10)
        self.encR(20)
        self.encF(10)
        self.encL(20)

    def forward_and_back(self):
        """The robot will go back and forth"""
        for x in range(2):
            self.encF(8)
            self.encB(8)

    def surprise(self):
        """the robot will move foward and back up in increments"""
        for x in range(2):
            self.encF(30)
            self.encL(5)
            self.encB(5)
            self.encR(10)
            self.encB(5)
            self.encL(5)
            self.encB(5)
            self.encR(10)
            self.encB(5)
            self.encL(5)
            self.encB(5)
            self.encR(10)
            self.encB(5)
            self.encL(5)
            self.encB(5)
            self.encR(10)
            self.encB(5)

    def x_up(self):
        """supposed to make an X formation"""
        for x in range(4):
            self.encB(9)
            self.encR(2)
            self.encF(9)
            self.encL(2)
            self.encB(9)
            self.encL(2)
            self.encF(9)
            self.encR(2)

    def wheelie(self):
        """the idea was that the robot would make a wheelie quickly while going backwards"""
        self.set_speed(255, 255)
        self.encF(50)
        self.encB(100)
        self.set_speed(self.LEFT_SPEED, self.RIGHT_SPEED)

    def s_curve_dance(self):
        self.fwd()
        self.set_speed(200,200)
        time.sleep(.5)
        self.fwd()
        self.set_speed(175,200)
        time.sleep(.5)
        self.fwd()
        self.set_speed(150,200)
        time.sleep(.5)
        self.fwd()
        self.set_speed(175,200)
        time.sleep(.5)
        self.fwd()
        self.set_speed(200,200)
        time.sleep(.5)
        self.fwd()
        self.set_speed(200,175)
        time.sleep(.5)
        self.fwd()
        self.set_speed(200,150)
        time.sleep(.5)
        self.fwd()
        self.set_speed(200,175)
        time.sleep(.5)
        self.fwd()
        self.set_speed(200,200)
        time.sleep(.5)
        self.fwd()
        self.set_speed(175,200)
        time.sleep(.5)
        self.fwd()
        self.set_speed(150,200)
        time.sleep(.5)
        self.fwd()
        self.set_speed(175,200)
        time.sleep(.5)

    def final_move(self):
        """just a simple swivel of the head"""
        for x in range(110, 30, -5):
            self.servo(x)


    def obstacle_count(self):
        """scans and estimates the number of obstacles within sight"""
        self.wide_scan()
        found_something = False
        counter = 0
        for ang, distance in enumerate(self.scan):
            if distance and distance < 200 and not found_something:
                found_something = True
                counter += 1
                print("Object # %d found, I think" % counter)
            if distance and distance > 200 and found_something:
                found_something = False
        print("\n----I SEE %d OBJECTS----\n" % counter)

    def safety_check(self):
        """subroutine of the dance method"""
        self.servo(self.MIDPOINT)  # look straight ahead
        for loop in range(4):
            if not self.is_clear():
                print("NOT GOING TO DANCE")
                return False
            print("Check #%d" % (loop + 1))
            self.encR(8)  # figure out 90 deg
        print("Safe to dance!")
        return True

    def nav(self):
        """auto pilots and attempts to maintain original heading"""
        logging.debug("Starting the nav method")
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        print("-------- [ Press CTRL + C to stop me ] --------\n")
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        while True:
            if self.is_clear():
                self.cruise()
            else:
                self.encR(10)

    def cruise(self):
        """ drive straight while path is clear """
        self.fwd()
        while self.dist() > self.SAFE_STOP_DIST:
            time.sleep(.5)
        self.stop()
####################################################
############### STATIC FUNCTIONS

def error():
    """records general, less specific error"""
    logging.error("ERROR")
    print('ERROR')


def quit_now():
    """shuts down app"""
    raise SystemExit

##################################################################
######## The app starts right here when we instantiate our GoPiggy


try:
    g = Piggy()
except (KeyboardInterrupt, SystemExit):
    pigo.stop_now()
except Exception as ee:
    logging.error(ee.__str__())
