import cv2
import mediapipe as mp
import math
import numpy
from ctypes import POINTER, cast
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


class hand:
    """This class holds the data of the index, thumb and the point generated below 
    the index, it also has two methods two help calculate the distance between
    the tip of the index and thumb, and the index and it's closest point, both
    values help to control volume no matter the separation from the camera"""

    def __init__(self) -> None:
        # Initialize the points for the thumb, index, and the point below it
        self.thumb_x = self.thumb_y = None
        self.index_x = self.index_y = None
        self.index_below_x = self.index_below_y = None
    def pinch_separation(self):
        # Calculate the distance between the tip of the thumb and index
        thumb_index_separation = math.hypot(self.index_x-self.thumb_x,
        self.index_y-self.thumb_y)
        return thumb_index_separation
    def screen_separation(self):
        # Calculate the separation from the screen by calculating the distance
        # Between the index and the point below it
        closest_distance = math.hypot(self.index_below_x-self.index_x,
        self.index_below_y-self.index_y)
        return closest_distance
# Initialize opencv and pycaw state variables
cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_SIMPLEX
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# Create a hand object
mano = hand()
# Create cv app loop
while True:
    # Capture data and pygame
    succes, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img)
    # Show hand tracking results if any
    if results.multi_hand_landmarks:
        # Fill the pygame background before displaying points
        for handLms in results.multi_hand_landmarks:
            for ids, lm in enumerate(handLms.landmark):
                # Get the size of the screen
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                # match the ids to identify the crucial points
                match ids:
                    # The points for the thumb tip
                    case 4:
                        mano.thumb_x, mano.thumb_y = cx,cy
                        color = (255,0,0)
                    # The points for the index tip
                    case 7:
                        mano.index_below_x, mano.index_below_y = cx, cy
                        color = (0,0,255)
                    # The point below the tip of the index
                    case 8:
                        mano.index_x, mano.index_y = cx,cy
                        color = (255,0,0)
                    case default:
                        color = (0,255,0)
                # Display the points and a line conecting the thumb and index
                cv2.line(img,(mano.index_x,mano.index_y),(mano.thumb_x,mano.thumb_y),(255,0,0),5)
                cv2.circle(img,(cx,cy), 10, color, -1)
            # Draw the hand with it's connections
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
        # Calculate the volume change based in the relation bewteen the pinch
        # and the screen separation
        volume_change = int(mano.pinch_separation()/mano.screen_separation())
        decibels = numpy.interp(volume_change, (0,8),(-74, 6))
        # Set the volume accordingly
        volume.SetMasterVolumeLevel(decibels, None)
        # Calculate the volume percentage and display it
        volume_percentage = numpy.interp(decibels, (-74, 6), (0,100))
        cv2.putText(img,f"{volume_percentage}%",(0,200), font, 1,(255,255,255),2)
    cv2.imshow("image", img)
    cv2.waitKey(1)
