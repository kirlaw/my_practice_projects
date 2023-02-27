import cv2
import mediapipe as mp
import numpy as np
import pygame
import random

# Initialize MediaPipe drawing tools
mp_drawing = mp.solutions.drawing_utils

# Define the maximum number of hands to be detected
max_hands = 1

# Start the camera
cap = cv2.VideoCapture(0)

# Initialize the Mediapipe hand detection module
mp_hands = mp.solutions.hands.Hands(max_num_hands=max_hands, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# set up Pygame window
pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Eat Game")

game_over = False


def game_start():
    # set up game variables
    player = pygame.Rect(300, 400, 40, 40)
    # background_image = pygame.image.load('background.png')
    # player_image = pygame.image.load('player.png')
    foods = [pygame.Rect(random.randint(0, 600), random.randint(0, 400), 20, 20) for i in range(10)]
    score = 0
    font = pygame.font.SysFont('Arial', 25)

    global game_over
    while not game_over:
        # Read the camera image
        success, image = cap.read()
        if not success:
            break

        image = cv2.flip(image, 1)

        # Convert the image to RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Process the image with Mediapipe
        results = mp_hands.process(image)
        landmarks = []
        thumb_x, thumb_y, index_x, index_y = 0, 0, 0, 0
        # Extract the hand landmarks if available
        if results.multi_hand_landmarks:
            landmarks = results.multi_hand_landmarks[0]

            # Get the coordinates of the thumb and index finger
            thumb_x, thumb_y = int(
                landmarks.landmark[mp.solutions.hands.HandLandmark.THUMB_TIP].x * image.shape[1]), int(
                landmarks.landmark[mp.solutions.hands.HandLandmark.THUMB_TIP].y * image.shape[0])
            index_x, index_y = int(
                landmarks.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP].x * image.shape[1]), int(
                landmarks.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP].y * image.shape[0])

        # Display the image with the hand landmarks
        mp_drawing.draw_landmarks(image, landmarks, mp.solutions.hands.HAND_CONNECTIONS)
        cv2.imshow("Camera", image)

        # detect hand gesture
        x, y, x1, y1 = thumb_x, thumb_y, index_x, index_y

        # draw hand bounding box on frame
        cv2.rectangle(image, (x, y), (x1, y1), (0, 255, 0), 2)

        # update player position based on hand position
        player.x = x
        player.y = y

        # draw player and food on Pygame window
        screen.fill((255, 255, 255))
        pygame.draw.rect(screen, (255, 0, 0), player)
        for food in foods:
            pygame.draw.rect(screen, (0, 255, 0), food)

        if not foods:
            game_over = True
            text_end = font.render(f"Game Over", True, (0, 0, 0))
            screen.blit(text_end, (200, 200))

        # check for collision between player and food
        for food in foods:
            if player.colliderect(food):
                foods.remove(food)
                score += 1

        # draw score on Pygame window
        text = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(text, (10, 10))

        # update Pygame window
        pygame.display.update()

    # quit game if user presses 'q' key or 'Esc'
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                pygame.quit()
                cap.release()
                cv2.destroyAllWindows()
                quit()
            if event.key == pygame.K_r:
                game_over = False
        elif event.type == pygame.QUIT:
            pygame.quit()
            cap.release()
            cv2.destroyAllWindows()
            quit()


if __name__ == "__main__":
    # press 'r' to restart game
    while True:
        game_start()
