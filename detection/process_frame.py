import cv2
import mediapipe as mp
import time
import pickle
import math
import numpy as np
import detection.shaired_socketio as shared
import base64
import re

# Load models once
with open('./data/XG_model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('./data/label_encoder.pkl', 'rb') as f:
    label_encoder = pickle.load(f)

# Initialize MediaPipe once
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, model_complexity=1)
mp_drawing = mp.solutions.drawing_utils


def euclidean_distance(p1, p2):
    return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)


def press_key(key):
    print(f"[ACTION] Pressing key: {key}")
    if shared.socketio is not None:
        shared.socketio.emit('keypress', {'key': key})
    else:
        print("Socket error: shared.socketio is None")


model_active = False


def gen_frames_from_client(base64_stream):
    global model_active
    previous_label = ""
    last_action_time = 0
    cooldown = 1.5
    last_toggle_time = 0
    toggle_cooldown = 2
    last_triggered_label = None

    for frame_b64 in base64_stream:
        start_time = time.time()  # Start time for FPS calculation

        # Decode base64 image
        if frame_b64.startswith("data:image"):
            frame_b64 = re.sub('^data:image/.+;base64,', '', frame_b64)

        image_data = base64.b64decode(frame_b64)
        np_arr = np.frombuffer(image_data, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        if frame is None:
            print("Failed to decode image")
            continue

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = pose.process(rgb)

        height, width, _ = frame.shape
        predicted_label = ""

        if result.pose_landmarks:
            landmarks = result.pose_landmarks.landmark
            left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]
            right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]
            hands_distance = euclidean_distance(left_wrist, right_wrist)
            current_time = time.time()

            # Toggle activation gesture
            if hands_distance < 0.1 and not model_active and (current_time - last_toggle_time) > toggle_cooldown:
                model_active = True
                last_toggle_time = current_time
                print("[TOGGLE] Model is now: ACTIVE (locked on until disconnect)")

            mp_drawing.draw_landmarks(
                frame, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            if model_active:
                data = np.array([[lm.x, lm.y, lm.z]
                                for lm in landmarks]).flatten()
                prediction = model.predict([data])[0]
                predicted_label = label_encoder[prediction]

                if predicted_label != last_triggered_label or predicted_label == 'standing':
                    action_triggered = False

                    # Gesture logic
                    if previous_label == 'standing' and predicted_label == 'left':
                        press_key('left')
                        action_triggered = True
                    elif previous_label == 'standing' and predicted_label == 'right':
                        press_key('right')
                        action_triggered = True
                    elif previous_label == 'standing' and 'jump' in predicted_label:
                        press_key('up')
                        action_triggered = True
                    elif previous_label == 'right' and predicted_label == 'standing':
                        press_key('left')
                        action_triggered = True
                    elif previous_label == 'left' and predicted_label == 'standing':
                        press_key('right')
                        action_triggered = True
                    elif previous_label == 'right' and predicted_label == 'left':
                        press_key('left')
                        press_key('left')
                        action_triggered = True
                    elif previous_label == 'left' and predicted_label == 'left_squat':
                        press_key('down')
                        action_triggered = True
                    elif previous_label == 'right' and predicted_label == 'right_squat':
                        press_key('down')
                        action_triggered = True
                    elif previous_label == 'left_squat' and predicted_label == 'left':
                        press_key('up')
                        action_triggered = True
                    elif previous_label == 'right_squat' and predicted_label == 'right':
                        press_key('up')
                        action_triggered = True
                    elif previous_label == 'left' and predicted_label == 'right':
                        press_key('right')
                        press_key('right')
                        action_triggered = True
                    elif previous_label == 'left_squat' and predicted_label == 'standing':
                        press_key('up')
                        action_triggered = True
                    elif previous_label == 'right_squat' and predicted_label == 'standing':
                        press_key('up')
                        action_triggered = True
                    elif 'jump' in predicted_label:
                        press_key('up')
                        action_triggered = True
                    elif 'squat' in predicted_label:
                        press_key('down')
                        action_triggered = True
                    elif 'left' in predicted_label:
                        press_key('left')
                        action_triggered = True
                    elif 'right' in predicted_label:
                        press_key('right')
                        action_triggered = True

                    if action_triggered:
                        last_action_time = current_time
                        last_triggered_label = predicted_label

                previous_label = predicted_label

        # Draw reference lines
        MID_X = width // 2
        MID_Y = height // 2
        cv2.line(frame, (0, MID_Y), (width, MID_Y), (0, 255, 0), 2)
        cv2.line(frame, (MID_X, 0), (MID_X, height), (0, 0, 255), 2)

        # FPS calculation
        end_time = time.time()
        fps = 1 / (end_time - start_time)

        # FPS display
        cv2.putText(frame, f'FPS: {int(fps)}', (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

        # Mode and gesture label
        status = "ACTIVE" if model_active else "PAUSED"
        cv2.putText(frame, f'MODE: {status}', (10, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 200, 255), 2)
        if predicted_label and model_active:
            cv2.putText(frame, f'Location: {predicted_label}', (10, 110),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)

        # Encode and yield frame
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield frame
