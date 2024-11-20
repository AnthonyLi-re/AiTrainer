import cv2
import numpy as np
import time
import PoseModule as pm

# Set up the camera instead of a video file
cap = cv2.VideoCapture(0)  # Use 0 for the default webcam. You can use 1, 2, etc. for additional cameras.

# Initialize the detector
detector = pm.poseDetector()
count = 0
dir = 0
pTime = 0

while True:
    success, img = cap.read()
    
    if not success:
        print("Error: Could not read from camera.")
        break
    
    # Resize the image if desired (optional, but useful for consistent processing)
    img = cv2.resize(img, (1280, 720))

    # Detect pose
    img = detector.findPose(img, False)
    lmList = detector.findPosition(img, False)

    # Proceed if landmarks are found
    if len(lmList) != 0:
        # Right Arm (adjust points based on your requirements)
        angle = detector.findAngle(img, 12, 14, 16)

        # Calculate the percentage of the curl (for visualization)
        per = np.interp(angle, (210, 310), (0, 100))
        bar = np.interp(angle, (220, 310), (650, 100))

        # Check for the dumbbell curls and count
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
        cv2.putText(img, f'{int(per)} %', (1100, 75), cv2.FONT_HERSHEY_PLAIN, 4,
                    color, 4)

        # Draw Curl Count
        cv2.rectangle(img, (0, 450), (250, 720), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(int(count)), (45, 670), cv2.FONT_HERSHEY_PLAIN, 15,
                    (255, 0, 0), 25)

    # Calculate Frames Per Second (FPS)
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    # Display FPS on screen
    cv2.putText(img, str(int(fps)), (50, 100), cv2.FONT_HERSHEY_PLAIN, 5,
                (255, 0, 0), 5)

    # Show the image in a window
    cv2.imshow("Image", img)

    # Exit condition, press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
