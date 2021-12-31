"""This module creates a pygame app that shows the hand points tracked
by opencv, by doing this it creates an animated hand real life tracked
in python."""

import cv2
import mediapipe as mp
import pygame

# Initialize pygame and opencv state variables
cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
clock = pygame.time.Clock()
pygame.init()
screen = pygame.display.set_mode((900, 600))
pygame.display.set_caption("Juego")
run = True
# Create both app loops
while run:
    # Capture data and pygame events
    succes, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # To close the program exit the pygame app
            run = False
    # Show hand tracking results if any
    if results.multi_hand_landmarks:
        # Fill the pygame background before displaying points
        screen.fill((255,255,255))
        # display the point tracked on the pygame window
        for handLms in results.multi_hand_landmarks:
            for ids, lm in enumerate(handLms.landmark):
                # Get the size of the screen
                h, w, c = img.shape
                # Mirror and show the points
                cx, cy = 600-int(lm.x*w), int(lm.y*h)
                # Draw them as circles
                pygame.draw.circle(screen,(0,255,255),(cx,cy),10)
            # Flip the screen and show the tracking on the webcam video
            pygame.display.flip()
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
    # Show the webcam frame
    cv2.imshow("image", img)
    cv2.waitKey(1)
