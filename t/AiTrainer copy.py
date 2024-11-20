import cv2
import numpy as np
import time
import PoseModule as pm
import tkinter as tk
from tkinter import messagebox

def start_detection(exercise_type):
    # This will start the exercise detection based on the exercise type selected
    setup_capture_window(exercise_type)


def main():
    # Set up the main GUI window
    root = tk.Tk()
    root.title("AI Trainer Exercise Detection")
    root.geometry("500x600")

    # Create UI elements
    label = tk.Label(root, text="Select the exercise you want to detect:", font=("Helvetica", 16, "bold"))
    label.pack(pady=20)

    # Create a scrollable frame for multiple buttons (optional if many exercises)
    exercise_frame = tk.Frame(root)
    exercise_frame.pack()

    exercises = [
        ("Dumbbell Curls", "curls"),
        ("Squats", "squats"),
        ("Push-Ups", "pushups"),
        ("Lunges", "lunges"),
        ("Planks", "planks"),
        ("Jumping Jacks", "jumpingjacks"),
        ("Side Plank", "sideplank"),
        ("Mountain Climbers", "mountainclimbers"),
        ("Sit-Ups", "situps"),
        ("Overhead Shoulder Press", "shoulderpress"),
        ("Tricep Dips", "tricepdips"),
        ("Wall Sit", "wallsit"),
        ("Side Lunges", "sidelunges"),
        ("Calf Raises", "calfraises"),
        ("Leg Raises", "legraises"),
        ("Burpees", "burpees")
    ]

    # Generate buttons for each exercise dynamically
    for (exercise_name, exercise_key) in exercises:
        btn = tk.Button(exercise_frame, text=exercise_name, font=("Helvetica", 12), command=lambda key=exercise_key: start_detection(key))
        btn.pack(pady=5)

    # Run the main loop of the GUI
    root.mainloop()



def setup_capture_window(exercise_name):
    cap = cv2.VideoCapture(0)  # Use 0 for default webcam
    detector = pm.poseDetector()
    count = 0
    dir = 0
    pTime = 0

    while True:
        success, img = cap.read()
        if not success:
            print("Error: Could not read from camera.")
            break

        img = cv2.resize(img, (1280, 720))
        img = detector.findPose(img, False)
        lmList = detector.findPosition(img, False)

        # Depending on the exercise, call appropriate functions here to update the count and angles
        if len(lmList) != 0:
            count, img = exercise_specific_detection(img, detector, lmList, exercise_name, count, dir)

        # Calculate Frames Per Second (FPS)
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        # Display FPS
        cv2.putText(img, str(int(fps)), (50, 100), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)

        cv2.imshow(f"{exercise_name} Detection", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def exercise_specific_detection(img, detector, lmList, exercise_name, count, dir):
    # This function should include the logic for each exercise to track repetitions or posture.
    if exercise_name == 'curls':
        # Dumbbell Curls Enhanced Detection Logic
        # Key Landmarks: Shoulder (12), Elbow (14), Wrist (16)

        # Calculate the angle between shoulder, elbow, and wrist
        angle = detector.findAngle(img, 12, 14, 16)

        # Calculate percentage and bar position for visualization
        per = np.interp(angle, (210, 310), (0, 100))
        bar = np.interp(angle, (220, 310), (650, 100))

        # Determine if in the correct position to count a rep
        color = (255, 0, 255)
        
        # Adding Buffer Threshold
        threshold_up = 95  # Threshold for upper bound to detect completed curl
        threshold_down = 5  # Threshold for lower bound to detect completed extension

        # Counting Logic
        if per >= threshold_up:
            color = (0, 255, 0)  # Green when at the top
            if dir == 0:  # Moving upwards
                # Only change direction after completing the full rep
                count += 0.5
                dir = 1

        elif per <= threshold_down:
            color = (0, 255, 0)  # Green when at the bottom
            if dir == 1:  # Moving downwards
                # Only change direction after reaching the bottom
                count += 0.5
                dir = 0

        # Draw Bar to indicate exercise progress
        cv2.rectangle(img, (1100, 100), (1175, 650), color, 3)
        cv2.rectangle(img, (1100, int(bar)), (1175, 650), color, cv2.FILLED)
        cv2.putText(img, f'{int(per)} %', (1100, 75), cv2.FONT_HERSHEY_PLAIN, 4, color, 4)

        # Draw Curl Count
        cv2.rectangle(img, (0, 450), (250, 720), (0, 255, 0), -1)
        cv2.putText(img, f'Reps: {int(count)}', (15, 670), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)


    # Similarly, add the detection logic for all other exercises
    elif exercise_name == 'squats':
        # Hip-Knee-Ankle points for squat detection (using points 24, 26, 28 for the right side)
        angle = detector.findAngle(img, 24, 26, 28)
        per = np.interp(angle, (200, 300), (0, 100))
        bar = np.interp(angle, (200, 300), (650, 100))

        color = (255, 0, 255)
        if per == 100:
            color = (0, 255, 0)
            if dir == 0:
                count += 0.5
                dir = 1
        if per == 0:
            color = (0, 255, 0)
            if dir == 1:
                count += 0.5
                dir = 0

        # Draw Bar to indicate exercise progress
        cv2.rectangle(img, (1100, 100), (1175, 650), color, 3)
        cv2.rectangle(img, (1100, int(bar)), (1175, 650), color, cv2.FILLED)
        cv2.putText(img, f'{int(per)} %', (1100, 75), cv2.FONT_HERSHEY_PLAIN, 4, color, 4)

        # Draw Squat Count
        cv2.rectangle(img, (0, 450), (250, 720), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(int(count)), (45, 670), cv2.FONT_HERSHEY_PLAIN, 15, (255, 0, 0), 25)

    elif exercise_name == 'pushups':
        # Push-Up Detection Logic
        # Shoulder (11, 12), Elbow (13, 14), Wrist (15, 16)
        angle = detector.findAngle(img, 11, 13, 15)  # Right side push-up angle

        # Calculate percentage and bar position for visualization
        per = np.interp(angle, (90, 160), (0, 100))
        bar = np.interp(angle, (90, 160), (650, 100))

        color = (255, 0, 255)
        if per == 100:
            color = (0, 255, 0)
            if dir == 0:
                count += 0.5
                dir = 1
        if per == 0:
            color = (0, 255, 0)
            if dir == 1:
                count += 0.5
                dir = 0

        # Draw Progress Bar
        cv2.rectangle(img, (1100, 100), (1175, 650), color, 3)
        cv2.rectangle(img, (1100, int(bar)), (1175, 650), color, cv2.FILLED)
        cv2.putText(img, f'{int(per)} %', (1100, 75), cv2.FONT_HERSHEY_PLAIN, 4, color, 4)

        # Draw Push-Up Count
        cv2.rectangle(img, (0, 450), (250, 720), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(int(count)), (45, 670), cv2.FONT_HERSHEY_PLAIN, 15, (255, 0, 0), 25)
    elif exercise_name == 'lunges':
        # Lunges Detection Logic
        # Hip (24), Knee (26), Ankle (28) for the right leg
        angle = detector.findAngle(img, 24, 26, 28)

        # Calculate percentage and bar position for visualization
        per = np.interp(angle, (70, 160), (0, 100))  # 70 when knee is bent, 160 when standing
        bar = np.interp(angle, (70, 160), (650, 100))

        color = (255, 0, 255)
        if per == 100:
            color = (0, 255, 0)
            if dir == 0:
                count += 0.5
                dir = 1
        if per == 0:
            color = (0, 255, 0)
            if dir == 1:
                count += 0.5
                dir = 0

        # Draw Progress Bar
        cv2.rectangle(img, (1100, 100), (1175, 650), color, 3)
        cv2.rectangle(img, (1100, int(bar)), (1175, 650), color, cv2.FILLED)
        cv2.putText(img, f'{int(per)} %', (1100, 75), cv2.FONT_HERSHEY_PLAIN, 4, color, 4)

        # Draw Lunge Count
        cv2.rectangle(img, (0, 450), (250, 720), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(int(count)), (45, 670), cv2.FONT_HERSHEY_PLAIN, 15, (255, 0, 0), 25)
    elif exercise_name == 'planks':
        # Plank Detection Logic
        # Ensure straight alignment between Shoulder (11, 12), Hip (23, 24), Ankle (27, 28)
        # We'll focus on hip to detect if the user sags or maintains a good plank form

        # Calculate angle between shoulder, hip, and ankle on the right side
        angle = detector.findAngle(img, 11, 23, 27)

        # Set criteria for proper plank (e.g., angle between 160 and 180 degrees indicates good form)
        if 160 <= angle <= 180:
            color = (0, 255, 0)  # Good form in plank
            count += 0.5  # Increase count as user holds the plank for a duration
        else:
            color = (0, 0, 255)  # Bad form in plank
        
        # Draw Plank Status
        cv2.putText(img, f'Plank Form: {"Good" if color == (0, 255, 0) else "Fix Posture"}',
                    (50, 100), cv2.FONT_HERSHEY_PLAIN, 3, color, 3)

        # Draw Plank Count or Hold Time
        cv2.rectangle(img, (0, 450), (250, 720), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, f'Held: {int(count)}s', (45, 670), cv2.FONT_HERSHEY_PLAIN, 15, (255, 0, 0), 25)
    elif exercise_name == 'jumpingjacks':
        # Jumping Jacks Detection Logic
        # Key Landmarks: Wrist (15, 16), Shoulder (11, 12), Ankle (27, 28)
        
        # Calculate the distance between wrists to detect hands overhead
        left_wrist_y = lmList[15][2]
        right_wrist_y = lmList[16][2]
        left_ankle_y = lmList[27][2]
        right_ankle_y = lmList[28][2]

        # Determine if the user is in an "open" or "closed" position
        open_position = left_wrist_y < left_ankle_y and right_wrist_y < right_ankle_y
        closed_position = left_wrist_y > left_ankle_y and right_wrist_y > right_ankle_y

        color = (255, 0, 255)
        if open_position:
            color = (0, 255, 0)
            if dir == 0:
                count += 0.5
                dir = 1
        elif closed_position:
            color = (0, 255, 0)
            if dir == 1:
                count += 0.5
                dir = 0

        # Draw Jumping Jacks Count
        cv2.rectangle(img, (0, 450), (250, 720), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(int(count)), (45, 670), cv2.FONT_HERSHEY_PLAIN, 15, (255, 0, 0), 25)
    elif exercise_name == 'sideplank':
        # Side Plank Detection Logic
        # Key Landmarks: Elbow (13), Shoulder (11), Hip (23)
        # We want the elbow, shoulder, and hip to be in a straight line for a proper side plank

        # Calculate the angle between the elbow, shoulder, and hip on the right side
        angle = detector.findAngle(img, 13, 11, 23)

        # Set criteria for a proper side plank (e.g., angle between 150 and 180 degrees indicates good form)
        if 150 <= angle <= 180:
            color = (0, 255, 0)  # Good form in side plank
            count += 0.5  # Increase count as user holds the side plank for a duration
        else:
            color = (0, 0, 255)  # Incorrect form

        # Draw Side Plank Status
        cv2.putText(img, f'Side Plank: {"Good" if color == (0, 255, 0) else "Fix Posture"}',
                    (50, 100), cv2.FONT_HERSHEY_PLAIN, 3, color, 3)

        # Draw Hold Time for Side Plank
        cv2.rectangle(img, (0, 450), (250, 720), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, f'Held: {int(count)}s', (45, 670), cv2.FONT_HERSHEY_PLAIN, 15, (255, 0, 0), 25)
    elif exercise_name == 'mountainclimbers':
        # Mountain Climbers Detection Logic
        # Key Landmarks: Knee (25, 26), Wrist (15, 16)
        # Detect alternating knee movement towards the corresponding wrist
        
        # Using the right knee (26) and right wrist (16)
        right_knee_y = lmList[26][2]
        right_wrist_y = lmList[16][2]
        left_knee_y = lmList[25][2]
        left_wrist_y = lmList[15][2]

        # Detect if the right or left knee is near the corresponding wrist (i.e., the climber position)
        right_knee_high = right_knee_y < right_wrist_y + 50
        left_knee_high = left_knee_y < left_wrist_y + 50

        color = (255, 0, 255)
        if right_knee_high or left_knee_high:
            color = (0, 255, 0)
            if dir == 0:
                count += 0.5
                dir = 1
        else:
            if dir == 1:
                count += 0.5
                dir = 0

        # Draw Mountain Climbers Count
        cv2.rectangle(img, (0, 450), (250, 720), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(int(count)), (45, 670), cv2.FONT_HERSHEY_PLAIN, 15, (255, 0, 0), 25)
    elif exercise_name == 'situps':
        # Sit-Ups Detection Logic
        # Key Landmarks: Shoulder (11), Hip (23), Knee (25)
        # The sit-up is detected based on the angle change between the hip and shoulder

        # Calculate the angle between hip (23), shoulder (11), and knee (25) to detect sit-up position
        angle = detector.findAngle(img, 23, 11, 25)

        # Calculate percentage and bar position for visualization
        per = np.interp(angle, (60, 120), (0, 100))  # 60 when curled up, 120 when lying down
        bar = np.interp(angle, (60, 120), (650, 100))

        color = (255, 0, 255)
        if per == 100:
            color = (0, 255, 0)
            if dir == 0:
                count += 0.5
                dir = 1
        if per == 0:
            color = (0, 255, 0)
            if dir == 1:
                count += 0.5
                dir = 0

        # Draw Progress Bar
        cv2.rectangle(img, (1100, 100), (1175, 650), color, 3)
        cv2.rectangle(img, (1100, int(bar)), (1175, 650), color, cv2.FILLED)
        cv2.putText(img, f'{int(per)} %', (1100, 75), cv2.FONT_HERSHEY_PLAIN, 4, color, 4)

        # Draw Sit-Up Count
        cv2.rectangle(img, (0, 450), (250, 720), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(int(count)), (45, 670), cv2.FONT_HERSHEY_PLAIN, 15, (255, 0, 0), 25)
    elif exercise_name == 'shoulderpress':
        # Overhead Shoulder Press Detection Logic
        # Key Landmarks: Shoulder (11, 12), Elbow (13, 14), Wrist (15, 16)

        # Calculate the angle between shoulder, elbow, and wrist to detect if arms are raised
        left_angle = detector.findAngle(img, 11, 13, 15)  # Left side
        right_angle = detector.findAngle(img, 12, 14, 16)  # Right side

        # Consider arms to be raised when the angle is approximately 180 degrees (fully extended upwards)
        per_left = np.interp(left_angle, (60, 180), (0, 100))  # 60 when lowered, 180 when raised
        per_right = np.interp(right_angle, (60, 180), (0, 100))
        
        # Calculate bar position for visualization (showing the average of left and right)
        bar = np.interp((left_angle + right_angle) / 2, (60, 180), (650, 100))

        color = (255, 0, 255)
        if per_left == 100 and per_right == 100:
            color = (0, 255, 0)
            if dir == 0:
                count += 0.5
                dir = 1
        if per_left == 0 and per_right == 0:
            color = (0, 255, 0)
            if dir == 1:
                count += 0.5
                dir = 0

        # Draw Progress Bar
        cv2.rectangle(img, (1100, 100), (1175, 650), color, 3)
        cv2.rectangle(img, (1100, int(bar)), (1175, 650), color, cv2.FILLED)
        cv2.putText(img, f'{int(per_left)} %', (1100, 75), cv2.FONT_HERSHEY_PLAIN, 4, color, 4)

        # Draw Shoulder Press Count
        cv2.rectangle(img, (0, 450), (250, 720), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(int(count)), (45, 670), cv2.FONT_HERSHEY_PLAIN, 15, (255, 0, 0), 25)
    elif exercise_name == 'tricepdips':
        # Tricep Dips Detection Logic
        # Key Landmarks: Shoulder (11, 12), Elbow (13, 14), Wrist (15, 16)

        # Calculate the angle between the shoulder, elbow, and wrist to detect the dip
        left_angle = detector.findAngle(img, 11, 13, 15)  # Left side
        right_angle = detector.findAngle(img, 12, 14, 16)  # Right side

        # Consider arms to be dipped when the angle is less than 90 degrees, and extended above 140 degrees
        per_left = np.interp(left_angle, (60, 140), (0, 100))  # 60 when lowered, 140 when raised
        per_right = np.interp(right_angle, (60, 140), (0, 100))

        # Calculate bar position for visualization (showing the average of left and right)
        bar = np.interp((left_angle + right_angle) / 2, (60, 140), (650, 100))

        color = (255, 0, 255)
        if per_left == 100 and per_right == 100:
            color = (0, 255, 0)
            if dir == 0:
                count += 0.5
                dir = 1
        if per_left == 0 and per_right == 0:
            color = (0, 255, 0)
            if dir == 1:
                count += 0.5
                dir = 0

        # Draw Progress Bar
        cv2.rectangle(img, (1100, 100), (1175, 650), color, 3)
        cv2.rectangle(img, (1100, int(bar)), (1175, 650), color, cv2.FILLED)
        cv2.putText(img, f'{int(per_left)} %', (1100, 75), cv2.FONT_HERSHEY_PLAIN, 4, color, 4)

        # Draw Tricep Dips Count
        cv2.rectangle(img, (0, 450), (250, 720), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(int(count)), (45, 670), cv2.FONT_HERSHEY_PLAIN, 15, (255, 0, 0), 25)
    elif exercise_name == 'wallsit':
        # Wall Sit Detection Logic
        # Key Landmarks: Hip (23, 24), Knee (25, 26), Ankle (27, 28)

        # Calculate the angle between hip, knee, and ankle for the right leg
        right_angle = detector.findAngle(img, 24, 26, 28)  # Right side
        left_angle = detector.findAngle(img, 23, 25, 27)  # Left side

        # Set criteria for proper wall sit (e.g., knee angle between 80 and 100 degrees indicates proper form)
        if 80 <= right_angle <= 100 and 80 <= left_angle <= 100:
            color = (0, 255, 0)  # Proper form in wall sit
            count += 0.5  # Increase count as user holds the wall sit for a duration
        else:
            color = (0, 0, 255)  # Incorrect form
        
        # Draw Wall Sit Status
        cv2.putText(img, f'Wall Sit: {"Good" if color == (0, 255, 0) else "Fix Posture"}',
                    (50, 100), cv2.FONT_HERSHEY_PLAIN, 3, color, 3)

        # Draw Wall Sit Hold Time
        cv2.rectangle(img, (0, 450), (250, 720), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, f'Held: {int(count)}s', (45, 670), cv2.FONT_HERSHEY_PLAIN, 15, (255, 0, 0), 25)
    elif exercise_name == 'sidelunges':
        # Side Lunges Detection Logic
        # Key Landmarks: Hip (23, 24), Knee (25, 26), Ankle (27, 28)

        # Calculate the angle between hip, knee, and ankle for the right leg (24, 26, 28)
        right_angle = detector.findAngle(img, 24, 26, 28)

        # Calculate the angle between hip, knee, and ankle for the left leg (23, 25, 27)
        left_angle = detector.findAngle(img, 23, 25, 27)

        # Calculate the percentage of movement between the bent and extended leg position
        per_right = np.interp(right_angle, (90, 160), (0, 100))  # 90 when bent, 160 when extended
        per_left = np.interp(left_angle, (90, 160), (0, 100))

        bar = np.interp((right_angle + left_angle) / 2, (90, 160), (650, 100))

        color = (255, 0, 255)
        if per_right == 100 or per_left == 100:
            color = (0, 255, 0)
            if dir == 0:
                count += 0.5
                dir = 1
        if per_right == 0 or per_left == 0:
            color = (0, 255, 0)
            if dir == 1:
                count += 0.5
                dir = 0

        # Draw Progress Bar
        cv2.rectangle(img, (1100, 100), (1175, 650), color, 3)
        cv2.rectangle(img, (1100, int(bar)), (1175, 650), color, cv2.FILLED)
        cv2.putText(img, f'{int(per_right)} %', (1100, 75), cv2.FONT_HERSHEY_PLAIN, 4, color, 4)

        # Draw Side Lunges Count
        cv2.rectangle(img, (0, 450), (250, 720), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(int(count)), (45, 670), cv2.FONT_HERSHEY_PLAIN, 15, (255, 0, 0), 25)
    elif exercise_name == 'calfraises':
        # Calf Raises Detection Logic
        # Key Landmarks: Ankle (27, 28), Hip (23, 24)

        # Calculate the y-coordinates for the left and right ankle
        left_ankle_y = lmList[27][2]
        right_ankle_y = lmList[28][2]

        # Also get y-coordinates of the hips to determine relative movement
        left_hip_y = lmList[23][2]
        right_hip_y = lmList[24][2]

        # Consider the relative movement of the ankle to detect a calf raise
        color = (255, 0, 255)
        if left_ankle_y < left_hip_y - 50 and right_ankle_y < right_hip_y - 50:
            color = (0, 255, 0)  # When both heels are lifted, indicating a proper calf raise
            if dir == 0:
                count += 0.5
                dir = 1
        elif left_ankle_y > left_hip_y - 20 and right_ankle_y > right_hip_y - 20:
            color = (0, 255, 0)  # When both heels are back down, completing the calf raise cycle
            if dir == 1:
                count += 0.5
                dir = 0

        # Draw Calf Raises Count
        cv2.rectangle(img, (0, 450), (250, 720), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(int(count)), (45, 670), cv2.FONT_HERSHEY_PLAIN, 15, (255, 0, 0), 25)
    elif exercise_name == 'legraises':
        # Leg Raises Detection Logic
        # Key Landmarks: Hip (23, 24), Knee (25, 26), Ankle (27, 28)

        # Calculate the angle between the hip, knee, and ankle to detect the leg raise
        left_leg_angle = detector.findAngle(img, 23, 25, 27)  # Left side leg raise
        right_leg_angle = detector.findAngle(img, 24, 26, 28)  # Right side leg raise

        # Consider legs to be raised when the angle is close to 90 degrees (straight up)
        per_left = np.interp(left_leg_angle, (90, 180), (0, 100))  # 90 when fully raised, 180 when down
        per_right = np.interp(right_leg_angle, (90, 180), (0, 100))

        # Calculate bar position for visualization
        bar = np.interp((left_leg_angle + right_leg_angle) / 2, (90, 180), (650, 100))

        color = (255, 0, 255)
        if per_left == 100 or per_right == 100:
            color = (0, 255, 0)
            if dir == 0:
                count += 0.5
                dir = 1
        if per_left == 0 or per_right == 0:
            color = (0, 255, 0)
            if dir == 1:
                count += 0.5
                dir = 0

        # Draw Progress Bar
        cv2.rectangle(img, (1100, 100), (1175, 650), color, 3)
        cv2.rectangle(img, (1100, int(bar)), (1175, 650), color, cv2.FILLED)
        cv2.putText(img, f'{int(per_left)} %', (1100, 75), cv2.FONT_HERSHEY_PLAIN, 4, color, 4)

        # Draw Leg Raises Count
        cv2.rectangle(img, (0, 450), (250, 720), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(int(count)), (45, 670), cv2.FONT_HERSHEY_PLAIN, 15, (255, 0, 0), 25)
    elif exercise_name == 'burpees':
        # Burpees Detection Logic
        # Key Landmarks: Wrist (15, 16), Shoulder (11, 12), Hip (23, 24), Ankle (27, 28)

        # Burpees involve multiple movements: jumping, plank, and a push-up-like movement
        # For simplicity, we will check for the "squat down" and "jump up" parts of the exercise

        left_ankle_y = lmList[27][2]
        right_ankle_y = lmList[28][2]
        left_wrist_y = lmList[15][2]
        right_wrist_y = lmList[16][2]
        left_hip_y = lmList[23][2]
        right_hip_y = lmList[24][2]

        # Detecting squat down (wrist close to ankle indicating squat position)
        squat_down = left_wrist_y > left_hip_y and right_wrist_y > right_hip_y

        # Detecting jump up (ankles raised indicating that the user has jumped)
        jump_up = left_ankle_y < left_hip_y - 50 and right_ankle_y < right_hip_y - 50

        color = (255, 0, 255)
        if squat_down:
            color = (0, 255, 0)
            if dir == 0:
                count += 0.5
                dir = 1
        elif jump_up:
            color = (0, 255, 0)
            if dir == 1:
                count += 0.5
                dir = 0

        # Draw Burpees Count
        cv2.rectangle(img, (0, 450), (250, 720), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(int(count)), (45, 670), cv2.FONT_HERSHEY_PLAIN, 15, (255, 0, 0), 25)

    return count, img


if __name__ == "__main__":
    main()
