# OpenSketch_AR_Painter
# Hand Gesture Drawing with OpenCV & MediaPipe

### Description
This project enables real-time hand gesture recognition using **OpenCV** and **MediaPipe** to draw on the screen. Users can select colors, adjust line thickness, and erase drawings by interacting with on-screen options using their index finger.

### Features
- ✋ **Hand Tracking** using MediaPipe's Hand module.
- 🎨 **Color Selection** based on fingertip proximity to on-screen labels.
- ➕ **Increase Line Thickness** when the fingertip is near `"+"`.
- ➖ **Decrease Line Thickness** when the fingertip is near `"-"`.
- 🖌️ **Draw Using Gestures**, using the index finger to create lines.
- 🗑️ **Erase Drawings** when all fingers are closed.
- 📷 **Live Webcam Feed** for real-time drawing.

### Requirements
Ensure the following dependencies are installed:
```bash
pip install opencv-python mediapipe numpy

python hand_draw.py

```

#How It Works

The webcam captures frames.

MediaPipe Hands detects hand landmarks.

Index fingertip position is tracked to:

Change colors (Red, Blue, Green).

Adjust line thickness (+ or -).

Drawing happens when the index finger is extended.

When all fingers are closed, the screen is cleared.

#Customization

redpos = (int(w/6), 50)   # Adjusting text positions dynamically
bluepos = (int(2*(w/6)), 50)
greenpos = (int(3*(w/6)), 50)
pluspos = (int(4*(w/6)), 50)
minuspos = (int(5*(w/6)), 50)

#License
This project is open-source and available under the MIT License



