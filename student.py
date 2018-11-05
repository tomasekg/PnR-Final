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
        self.SAFE_STOP_DIST = 35
        # I changed the safe stop distance to a little higher just to test out
        # tried changing again
        # lowered it back to what i had
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
                "t": ("Test", self.skill_test),
                "s": ("Check status", self.status),
                "h": ("Open House", self.open_house),
                "q": ("Quit", quit_now),
                "f": ("Forward", self.move_straight),
                "r": ("Right", self.move_right),
                "l": ("Left", self.move_left),
                "b": ("Back", self.move_back),
                "L": ("Left",  self.move_left)
                }
        # loop and print the menu...
        for key in sorted(menu.keys()):
            print(key + ":" + menu[key][0])
        # store the user's answer
        ans = raw_input("Your selection: ")
        # activate the item selected
        menu.get(ans, [None, error])[1]()

    def skill_test(self):
        """allows the robot to navigate itself"""
        choice = raw_input("Left/Right or Turn Until Clear?")

        if "l" in choice:
            self.wide_scan() #scan the area
            # picks left or right

            # create two variables, left_total and right_total
            left_total = 0
            right_total = 0
            # loop from self.MIDPOINT - 60 to self.MIDPOINT
            for angle in range(self.MIDPOINT - 60, self.MIDPOINT):
                if self.scan[angle]:
                    # add up the numbers to right_total
                    right_total += self.scan[angle]
            # loop from self.MIDPOINT to self.MIDPOINT + 60
            for angle in range(self.MIDPOINT, self.MIDPOINT + 60):
                if self.scan[angle]:
                # add up the numbers to left_total
                    left_total += self.scan[angle]
            # if right is bigger:
            if right_total > left_total:
                # turn right
                self.encR(6)
            # if left is bigger:
            else:
                # turn left
                self.encL(6)
        else:
            print("\n\nI'll keep turning util it's clear, buddy\n\n")
            for x in range(4):
                if not self.is_clear():
                   self.encR(7)
                else:
                    self.encF(10)
                    break


    def open_house(self):
        """reacts to distant measurement in front of it"""
        while True:
            if self.dist() < 20:
                self.encB(10)
                self.encR(5)
                self.encL(5)
                self.encR(5)
                self.encF(10)
                self.encR(18)
                for x in range(5):
                    self.servo(120)
                    self.servo(40)
                self.servo(self.MIDPOINT)
                self.encF(5)
                self.encR(5)
                self.encL(5)
            time.sleep(.1)

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
# FROM RICKY ROBERTO
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
# FROM COLE
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
        for x in range(4):
             for ang, distance in enumerate(self.scan):
                if distance and distance < 175 and not found_something:
                    found_something = True
                    counter += 1
                    print("Object # %d found, I think" % counter)
                if distance and distance > 175 and found_something:
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
                self.choose_direction()

    def open_house(self):
        """Cute demo used for open house"""
        choice = raw_input("1) Shy;  2) Spin.. ")
        if choice == "1":
            while True:
                if not self.is_clear():
                    self.beShy()
        else:
            while True:
                if not self.is_clear():
                    for x in range(5):
                        self.encR(2)
                        self.encL(2)
                    self.encR(15)

    def cruise(self):
        """ drive straight while path is clear """
        self.fwd()
        while self.dist() > self.SAFE_STOP_DIST:
            # .5 seconds seems to short of a stopping distance....had to change it...realized I made it more time between
            time.sleep(.2)

        self.stop()

    def is_clear(self):
        """does a 3-point scan around the midpoint, returns false if a test fails"""
        # added this into my student.py to enlarge the view range
        print("Running the is_clear method.")
        for x in range((self.MIDPOINT - 30), (self.MIDPOINT + 30), 8):
            self.servo(x)
            scan1 = self.dist()
            # double check the distance
            scan2 = self.dist()
            # if I found a different distance the second time....
            if abs(scan1 - scan2) > 2:
                scan3 = self.dist()
                # take another scan and average the three together
                scan1 = (scan1 + scan2 + scan3) / 3
            self.scan[x] = scan1
            print("Degree: " + str(x) + ", distance: " + str(scan1))
            if scan1 < self.SAFE_STOP_DIST:
                print("Doesn't look clear to me")
                return False
        self.servo(self.MIDPOINT)
        return True

    def choose_direction(self):
        """ makes a smarter decision after stopping and scanning """

        self.wide_scan(count=5) #scan the area
        # picks left or right

        # create two variables, left_total and right_total
        left_total = 0
        right_total = 0
        # loop from self.MIDPOINT - 60 to self.MIDPOINT
        for angle in range(self.MIDPOINT - 60, self.MIDPOINT):
            if self.scan[angle]:
                # add up the numbers to right_total
                right_total += self.scan[angle]
        # loop from self.MIDPOINT to self.MIDPOINT + 60
        for angle in range(self.MIDPOINT, self.MIDPOINT + 60):
            if self.scan[angle]:
            # add up the numbers to left_total
                left_total += self.scan[angle]
        # if right is bigger:
        if right_total > left_total:
            # turn right
            self.encR(6)
        # if left is bigger:
        if left_total > right_total:
            # turn left
            self.encL(6)
        return True

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