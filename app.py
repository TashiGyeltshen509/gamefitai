from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import base64

from detection.process_frame import gen_frames_from_client
from detection import shaired_socketio

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')
shaired_socketio.socketio = socketio  # Share SocketIO instance


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/demo')
def demo():
    return render_template('demo.html')


@app.route('/games')
def games():
    return render_template('games.html')


@app.route('/teams')
def teams():
    return render_template('teams.html')


@app.route('/playing')
def play():
    return render_template('play.html')


@app.route('/ping')
def ping():
    return "pong", 200


@socketio.on('client_frame')
def handle_frame(data):
    try:
        frame_data = data.get("frame")
        token = data.get("token")

        if not frame_data or not token:
            print("Missing frame or token")
            return

        frame_gen = gen_frames_from_client([frame_data])
        processed_frame_bytes = next(frame_gen)

        if processed_frame_bytes is None:
            raise ValueError("Processed frame is None")

        encoded_frame = base64.b64encode(processed_frame_bytes).decode('utf-8')
        emit(f"processed_frame_{token}", {
            "frame": f"data:image/jpeg;base64,{encoded_frame}"
        })

    except Exception as e:
        print("Error in handle_frame:", e)
        emit(f"processed_frame_{data.get('token', 'unknown')}", {
            "error": "Server error processing frame"
        })


@socketio.on('disconnect')
def on_disconnect():
    try:
        print("Client disconnected cleanly.")
    except Exception as e:
        print(f"Error during disconnect: {e}")


if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
