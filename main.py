import cv2
import mediapipe as mp
import random
import time

# ---------------- MEDIAPIPE SETUP ----------------

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# ---------------- CAMERA ----------------

cap = cv2.VideoCapture(0)

# ---------------- GAME VARIABLES ----------------

choices = ["Rock", "Paper", "Scissors"]

computer_choice = random.choice(choices)

player_score = 0
computer_score = 0
draw_score = 0

result = "Show your hand!"

last_player_choice = "Unknown"
last_round_time = 0

# ---------------- FUNCTIONS ----------------

def get_fingers(hand_landmarks):

    tips = [4, 8, 12, 16, 20]
    pips = [3, 6, 10, 14, 18]

    fingers = 0

    # Thumb
    if hand_landmarks.landmark[tips[0]].x < hand_landmarks.landmark[pips[0]].x:
        fingers += 1

    # Four fingers
    for tip, pip in zip(tips[1:], pips[1:]):
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[pip].y:
            fingers += 1

    return fingers


def get_choice(fingers):

    if fingers == 0:
        return "Rock"

    elif fingers == 2:
        return "Scissors"

    elif fingers == 5:
        return "Paper"

    else:
        return "Unknown"


def get_result(player, computer):

    if player == computer:
        return "Draw"

    if (
        (player == "Rock" and computer == "Scissors")
        or
        (player == "Paper" and computer == "Rock")
        or
        (player == "Scissors" and computer == "Paper")
    ):
        return "You Win!"

    return "Computer Wins!"


# ---------------- MAIN LOOP ----------------

while True:

    success, frame = cap.read()

    if not success:
        break

    frame = cv2.flip(frame, 1)

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb_frame)

    player_choice = "Unknown"

    # ---------------- HAND DETECTION ----------------

    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:

            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            fingers = get_fingers(hand_landmarks)

            player_choice = get_choice(fingers)

    # ---------------- NEW ROUND ----------------

    if player_choice != "Unknown" and player_choice != last_player_choice:

        computer_choice = random.choice(choices)

        result = get_result(player_choice, computer_choice)

        if result == "You Win!":
            player_score += 1

        elif result == "Computer Wins!":
            computer_score += 1

        else:
            draw_score += 1

        last_round_time = time.time()

        last_player_choice = player_choice

    # Reset detection after 2 seconds
    if time.time() - last_round_time > 2:

        last_player_choice = "Unknown"

    # ---------------- DISPLAY ----------------

    cv2.putText(
        frame,
        "You: " + player_choice,
        (30, 55),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.1,
        (0, 255, 0),
        3
    )

    cv2.putText(
        frame,
        "Computer: " + computer_choice,
        (30, 100),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.1,
        (255, 0, 0),
        3
    )

    cv2.putText(
        frame,
        result,
        (30, 155),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.3,
        (0, 255, 255),
        3
    )

    # Score
    cv2.putText(
        frame,
        f"You: {player_score}",
        (30, 220),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        (0, 255, 0),
        2
    )

    cv2.putText(
        frame,
        f"Computer: {computer_score}",
        (30, 260),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        (255, 0, 0),
        2
    )

    cv2.putText(
        frame,
        f"Draw: {draw_score}",
        (30, 300),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        (255, 255, 0),
        2
    )

    # Instructions
    cv2.putText(
        frame,
        "Rock = Fist | Paper = 5 | Scissors = 2",
        (30, 430),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        "Press Q to Quit",
        (30, 470),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )

    cv2.imshow(
        "Rock Paper Scissors Game",
        frame
    )

    # Quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()