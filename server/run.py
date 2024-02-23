import cv2
import mediapipe as mp
from flask import Flask, Response, send_from_directory
from draw_vid import mediapipe_results
import tensorflow as tf
import subprocess, os
from flask_cors import CORS
import multiprocessing
from flask import request
from draw_vid import clear_alert_cache


speech_to_text_process = None
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_holistic = mp.solutions.holistic

def set_gpu_memory_growth():
    physical_devices = tf.config.experimental.list_physical_devices('GPU')
    if physical_devices:
        try:
            print("---------------------GPU available")
            for dev in physical_devices:
                tf.config.experimental.set_memory_growth(dev, True)
        except RuntimeError as e:
            print(e)
    else:
        print("--------------Using CPU device")

# set cpu or gpu
set_gpu_memory_growth()

app = Flask(__name__, static_folder='build')
CORS(app)


circles = []  # Declare circles as a global variable


@app.route('/clear_circles', methods=['POST'])
def clear_circles():
    global circles  # Refer to the global variable within the function
    circles.clear()  # Clear the global circles list
    # print("Circles cleared")
    return 'Circles cleared', 200

def gen_frames():
    cap = cv2.VideoCapture(0)
    
    # Initialize MediaPipe Holistic and Hands once, outside the loop
    mp_holistic = mp.solutions.holistic
    mpHands = mp.solutions.hands
    mp_draw = mp.solutions.drawing_utils

    hands = mpHands.Hands(
        static_image_mode=False,
        max_num_hands=2,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )

    alert_cache = clear_alert_cache()  # Setup the alert cache outside the loop
    pen_color = 0

    while True:
        success, frame = cap.read()
        if not success:
            break

        frame = mediapipe_results(frame, pen_color, mpHands, hands,mp_draw)

        # The commented-out circle drawing code and color changing logic are assumed
        # to be handled within mediapipe_results efficiently

        # Determine if an alert should be shown and update the cache accordingly
        single_frame_alert = False  # Determine this based on your application logic
        multi_frame_alert = alert_cache.update_cache(single_frame_alert)

        if multi_frame_alert:
            clear_circles()
            single_frame_alert = False
            multi_frame_alert = []

        # Encode and yield the frame
        ret, buffer = cv2.imencode('.jpg', frame)
        if ret:
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')
    
    # Release resources outside the loop
    cap.release()
    hands.close()

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed', defaults={'path': ''})
def serve(path):
    if path and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
