# import cv2
# import mediapipe as mp
# import time
# import pygame
# from pygame import display
# import random
# from ctypes import POINTER, cast
# import math
# from comtypes import CLSCTX_ALL
# from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# class Text:
#     def __init__(self, screen, color, x, y):
#         self.screen = screen
#         self.color = color
#         self.x = x
#         self.y = y
#     def display(self, font, message):
#         img = font.render(message,True, self.color)
#         self.screen.blit(img, (self.x, self.y))

# class hand:
#     def __init__(self) -> None:
#         self.thx = None
#         self.thy = None
#         self.ix = None
#         self.iy = None
#         self.ifx = None
#         self.ify = None
#     def distance(self):
#         self.separation = math.sqrt(((self.thx-self.ix)**2)+((self.thy-self.iy)**2))
#         return int(self.separation)
#     def separacion(self):
#         self.separ = math.hypot(self.ix-self.ifx,self.iy-self.ify)
#         return int(self.separ)



# cap = cv2.VideoCapture(0)
# mpHands = mp.solutions.hands
# hands = mpHands.Hands()
# mpDraw = mp.solutions.drawing_utils
# clock = pygame.time.Clock()
# pygame.init()
# screen = pygame.display.set_mode((900, 600))
# pygame.display.set_caption("Juego")
# devices = AudioUtilities.GetSpeakers()
# interface = devices.Activate(
# IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
# volume = cast(interface, POINTER(IAudioEndpointVolume))
# # volume.SetMasterVolumeLevel(-74, None)
# font = pygame.font.SysFont("C:\Windows\Fonts\Arial", 24)
# timeLabel = Text(screen,(0,0,255),20,20)
# Label = Text(screen,(0,0,255),40,40)

# fingertips_id = {4,7,8}
# max_separation = 0
# distance = []
# y=0
# mano = hand()
# puntas = {12,16,20}


# while True:
#     succes, img = cap.read()
#     imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     results = hands.process(img)
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             run = False
#     if results.multi_hand_landmarks:
#         screen.fill((255,255,255))
#         for handLms in results.multi_hand_landmarks:
#             for ids, lm in enumerate(handLms.landmark):
#                 h, w, c = img.shape
#                 cx, cy = 600-int(lm.x*w), int(lm.y*h)
#                 if ids in fingertips_id:
#                     match ids:
#                         case 4:
#                             mano.thx = cx
#                             mano.thy = cy
#                             color = (255,0,0)
#                         case 7:
#                             mano.ifx = cx
#                             mano.ify = cy
#                             color = (0,255,0)
#                         case 8:
#                             color = (255,0,0)
#                             mano.ix = cx
#                             mano.iy = cy
#                 elif ids in puntas:
#                     color = (255,0,0)
#                 else:
#                     color = (0,255,255)
#                 pygame.draw.circle(screen,color,(cx,cy),10)
#             # volume.SetMasterVolumeLevel(80, None)
#             dist = round(int(80*(((mano.distance()/180)/(mano.separacion()/100))/4)),0)
#             if dist >= 80:
#                 volume.SetMasterVolumeLevel(6, None)
#             elif dist <= 10:
#                 volume.SetMasterVolumeLevel(-74, None)
#             else:
#                 volume.SetMasterVolumeLevel((-74+dist), None)
#             acercamiento = math.hypot((mano.ix-mano.ifx),(mano.iy-mano.ify))
#             timeLabel.display(font, f" separación: {mano.ix}")
#             Label.display(font, f" acercamiento: {mano.iy}")
#             pygame.display.flip()
#             mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
#             # print(volume.GetVolumeRange())
#     cv2.imshow("image", img)
#     cv2.waitKey(1)
# pygame.quit()

import cv2
import mediapipe as mp
import time
import pygame
from pygame import display
import random
from ctypes import POINTER, cast
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import pyautogui

class Text:
    def __init__(self, screen, color, x, y):
        self.screen = screen
        self.color = color
        self.x = x
        self.y = y
    def display(self, font, message):
        img = font.render(message,True, self.color)
        self.screen.blit(img, (self.x, self.y))

class hand:
    def __init__(self) -> None:
        self.thx = None
        self.thy = None
        self.ix = None
        self.iy = None
        self.ifx = None
        self.ify = None
        self.my = None
        self.mx = None
    def distance(self):
        self.separation = math.sqrt(((self.thx-self.ix)**2)+((self.thy-self.iy)**2))
        return int(self.separation)
    def separacion(self):
        self.separ = math.hypot(self.ix-self.ifx,self.iy-self.ify)
        return int(self.separ)



cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
clock = pygame.time.Clock()
pygame.init()
screen = pygame.display.set_mode((900, 600))
pygame.display.set_caption("Juego")
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.SetMasterVolumeLevel(-74, None)
font = pygame.font.SysFont("C:\Windows\Fonts\Arial", 24)
timeLabel = Text(screen,(0,0,255),20,20)
Label = Text(screen,(0,0,255),40,40)

fingertips_id = {4,7,8,12}
max_separation = 0
distance = []
y=0
mano = hand()
puntas = {12,16,20}


while True:
    succes, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    if results.multi_hand_landmarks:
        screen.fill((255,255,255))
        for handLms in results.multi_hand_landmarks:
            for ids, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = 600-int(lm.x*w), int(lm.y*h)
                if ids in fingertips_id:
                    match ids:
                        case 4:
                            mano.thx = cx
                            mano.thy = cy
                            color = (255,0,0)
                        case 7:
                            mano.ifx = cx
                            mano.ify = cy
                            color = (0,255,0)
                        case 8:
                            color = (255,0,0)
                            mano.ix = cx
                            mano.iy = cy
                        case 12:
                            mano.mx = cx
                            mano.my = cy
                            color = (255,0,255)

                elif ids in puntas:
                    color = (255,0,0)
                else:
                    color = (0,255,255)
                pygame.draw.circle(screen,color,(cx,cy),10)
            x = mano.ifx/300
            y = mano.ify/300
            pyautogui.moveTo(x*1920, y*1080)
            click = math.hypot(mano.mx-mano.thx,mano.my-mano.thy)
            if click < 50:
                pyautogui.press('space')
            pygame.display.flip()
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
            # print(volume.GetVolumeRange())
    cv2.imshow("image", img)
    cv2.waitKey(1)
pygame.quit()

