# 🎓 Member 2 - Complete Usage Guide

## 📚 Table of Contents
1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [Running Standalone](#running-standalone)
4. [Integration with Member 1](#integration-with-member-1)
5. [Configuration](#configuration)
6. [Understanding Outputs](#understanding-outputs)
7. [Troubleshooting](#troubleshooting)

---

## 📦 Installation

### Step 1: Install Python Dependencies
```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install opencv-python numpy
```

### Step 2: Verify Installation
```bash
python -c "import cv2; import numpy; print('✅ All dependencies installed!')"
```

### Step 3: Check Cascade Files
The system uses two Haar Cascade XML files:
- `haarcascade_frontalface_default.xml` (for face detection)
- Built-in eye cascade from OpenCV

If you need the face cascade file separately:
```bash
# It's included in the uploads, or download from OpenCV
wget https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml
```

---

## 🚀 Quick Start

### Option 1: Run Member 2 Standalone
```bash
python member2_gaze_tracking.py
```

### Option 2: Run Integrated System (Member 1 + 2)
```bash
python integrated_member1_member2.py
```

**Controls:**
- Press **'q'** to quit
- Press **'r'** to reset warnings
- Press **'s'** to show summary (integrated mode only)

---

## 🎯 Running Standalone

Member 2 can run independently for testing and development:

```bash
python member2_gaze_tracking.py
```

### What You'll See:
1. **Face detection** - Blue rectangle around your face
2. **Eye tracking** - Yellow circles on your eyes
3. **Eye center** - Magenta dot between eyes
4. **Gaze direction** - Label showing where you're looking
5. **Head pose angles** - Pitch and yaw in degrees
6. **Warnings** - Red text when suspicious behavior detected
7. **Statistics** - Look-away time and warning count

### Example Output:
```
============================================================
MEMBER 2 - HEAD MOVEMENT & GAZE DIRECTION TRACKING
============================================================

Initializing gaze tracking system...

Controls:
  'q' - Quit
  'r' - Reset warnings

Monitoring:
  - Gaze direction (left/right/center/up/down)
  - Head pose angles (pitch, yaw, roll)
  - Look-away duration
  - Frequent glancing patterns
============================================================

Webcam started successfully!
System is now monitoring gaze direction...
```

---

## 🔗 Integration with Member 1

### Using as a Module

```python
from member2_gaze_tracking import GazeTracker
import cv2

# Initialize components
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
gaze_tracker = GazeTracker()

# Start webcam (Member 1)
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Preprocess (Member 1)
    frame = cv2.resize(frame, (640, 480))
    frame = cv2.flip(frame, 1)
    
    # Analyze (Member 2)
    annotated_frame, tracking_data = gaze_tracker.process_frame(frame)
    
    # Use the data
    print(f"Direction: {tracking_data['direction']}")
    print(f"Warnings: {len(tracking_data['warnings'])}")
    
    # Display
    cv2.imshow("Proctoring", annotated_frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

### Accessing Tracking Data

```python
tracking_data = {
    "direction": "center",           # Current gaze direction
    "horizontal_deviation": 15,      # Pixels from center (positive = right)
    "vertical_deviation": -8,        # Pixels from center (positive = down)
    "head_pose": {
        "pitch": 5.2,                # Up/down angle (degrees)
        "yaw": -12.3,                # Left/right angle (degrees)
        "roll": 2.1                  # Tilt angle (degrees)
    },
    "warnings": [                    # List of active warnings
        "Looking right for 3.2s",
        "Head turned left: 28.5°"
    ],
    "total_look_away_time": 12.5    # Cumulative seconds
}
```

---

## ⚙️ Configuration

### Adjusting Thresholds

Edit the `__init__()` method in `GazeTracker` class:

```python
class GazeTracker:
    def __init__(self):
        # Gaze direction thresholds (in pixels)
        self.HORIZONTAL_THRESHOLD = 80   # ← Adjust for left/right sensitivity
        self.VERTICAL_THRESHOLD = 60     # ← Adjust for up/down sensitivity
        
        # Warning thresholds
        self.MAX_LOOK_AWAY_TIME = 3.0    # ← Seconds before warning
        self.MAX_HEAD_TURN_ANGLE = 25    # ← Degrees before warning
        self.FREQUENT_GLANCE_COUNT = 5   # ← Number of glances
        self.GLANCE_TIME_WINDOW = 10     # ← Time window for counting
```

### Recommended Settings

#### Strict Exam Mode
```python
self.HORIZONTAL_THRESHOLD = 60
self.VERTICAL_THRESHOLD = 40
self.MAX_LOOK_AWAY_TIME = 2.0
self.MAX_HEAD_TURN_ANGLE = 20
self.FREQUENT_GLANCE_COUNT = 4
```

#### Lenient Practice Mode
```python
self.HORIZONTAL_THRESHOLD = 100
self.VERTICAL_THRESHOLD = 80
self.MAX_LOOK_AWAY_TIME = 5.0
self.MAX_HEAD_TURN_ANGLE = 30
self.FREQUENT_GLANCE_COUNT = 8
```

---

## 📊 Understanding Outputs

### Gaze Directions

| Direction | Meaning |
|-----------|---------|
| `center` | Looking at screen (normal) ✅ |
| `left` | Looking to the left side |
| `right` | Looking to the right side |
| `up` | Looking upward |
| `down` | Looking downward |
| `up-left` | Looking diagonally up-left |
| `up-right` | Looking diagonally up-right |
| `down-left` | Looking diagonally down-left |
| `down-right` | Looking diagonally down-right |
| `no_face` | No face detected ⚠️ |

### Head Pose Angles

#### Pitch (Up/Down)
- **Negative**: Looking up
- **Zero**: Looking straight
- **Positive**: Looking down
- **Range**: Typically -30° to +30°

#### Yaw (Left/Right)
- **Negative**: Head turned left
- **Zero**: Facing forward
- **Positive**: Head turned right
- **Range**: Typically -45° to +45°

#### Roll (Tilt)
- **Negative**: Head tilted left
- **Zero**: Head upright
- **Positive**: Head tilted right
- **Range**: Typically -15° to +15°

### Warning Messages

| Warning | Trigger Condition |
|---------|------------------|
| "Looking [direction] for X.Xs" | Looking away > 3 seconds |
| "Head turned [direction]: X.X°" | Head rotation > 25° |
| "Frequent glances: X in 10s" | 5+ glances in 10-second window |

---

## 🐛 Troubleshooting

### Issue: Eyes Not Detected
**Symptoms:** No yellow circles on eyes, using face center instead

**Solutions:**
1. Improve lighting - face should be well-lit
2. Remove glasses if possible
3. Position face clearly in frame
4. Adjust eye cascade parameters:
```python
eyes = self.eye_cascade.detectMultiScale(
    face_gray,
    scaleFactor=1.05,  # Try lower value (was 1.1)
    minNeighbors=3,    # Try lower value (was 5)
    minSize=(15, 15)   # Try smaller size (was 20, 20)
)
```

### Issue: Too Many False Warnings
**Symptoms:** Warnings trigger on normal movements

**Solutions:**
1. Increase thresholds:
```python
self.MAX_LOOK_AWAY_TIME = 5.0      # More tolerance
self.MAX_HEAD_TURN_ANGLE = 35      # Allow more rotation
```

2. Reduce sensitivity:
```python
self.HORIZONTAL_THRESHOLD = 100    # Larger dead zone
self.VERTICAL_THRESHOLD = 80
```

### Issue: Head Pose Inaccurate
**Symptoms:** Wrong pitch/yaw/roll angles

**Solutions:**
1. Ensure face is clearly visible
2. Avoid extreme angles (> 45°)
3. Check camera position - should be eye-level
4. Improve lighting conditions

### Issue: "NO FACE DETECTED" Message
**Symptoms:** Red text, no face tracking

**Solutions:**
1. Position yourself in frame center
2. Ensure adequate lighting
3. Check if webcam is working:
```bash
python -c "import cv2; cap = cv2.VideoCapture(0); print('Camera OK' if cap.isOpened() else 'Camera Error')"
```
4. Try different camera index:
```python
cap = cv2.VideoCapture(1)  # Try 1 instead of 0
```

### Issue: Webcam Won't Open
**Symptoms:** "ERROR: Could not open webcam!"

**Solutions:**
1. Check camera permissions
2. Close other applications using webcam
3. Try different camera:
```python
# Test multiple cameras
for i in range(5):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        print(f"Camera found at index {i}")
        cap.release()
```

### Issue: Low Frame Rate / Laggy
**Symptoms:** Choppy video, slow processing

**Solutions:**
1. Reduce frame size:
```python
frame = cv2.resize(frame, (480, 360))  # Smaller resolution
```

2. Skip frames:
```python
frame_count += 1
if frame_count % 2 == 0:  # Process every other frame
    annotated_frame, data = gaze_tracker.process_frame(frame)
```

3. Disable head pose estimation temporarily:
```python
# Comment out in process_frame():
# pitch, yaw, roll = self.estimate_head_pose(...)
```

---

## 📝 Session Summary

### Getting Summary Data
```python
# During session
summary = gaze_tracker.get_summary()

# Print summary
print(f"Total Warnings: {summary['total_warnings']}")
print(f"Total Look-Away Time: {summary['total_look_away_time']:.1f}s")
print("Warnings:", summary['warnings_list'])
```

### Resetting Warnings
```python
# Clear all warnings and metrics
gaze_tracker.reset_warnings()
```

### Exporting Data (Custom)
```python
import json

# Get summary
summary = gaze_tracker.get_summary()

# Save to file
with open('session_report.json', 'w') as f:
    json.dump(summary, f, indent=2)
```

---

## 🎯 Best Practices

### For Testing
1. Start with standalone mode
2. Test in good lighting
3. Position face clearly in center
4. Try different head positions
5. Verify warnings trigger correctly

### For Integration
1. Import `GazeTracker` class
2. Initialize once at startup
3. Process each frame
4. Check `tracking_data` for decisions
5. Reset warnings between sessions

### For Production
1. Log all warnings to database
2. Adjust thresholds based on environment
3. Implement fallback for eye detection failures
4. Add calibration phase for each user
5. Monitor false positive/negative rates

---

## 📞 Support & Next Steps

### Testing Checklist
- [ ] Dependencies installed
- [ ] Cascade files available
- [ ] Webcam accessible
- [ ] Standalone mode works
- [ ] Eye detection functional
- [ ] Gaze tracking accurate
- [ ] Warnings triggering correctly
- [ ] Integration tested

### Integration with Member 3 & 4
Member 2 outputs are designed to feed into:
- **Member 3**: Body posture analysis
- **Member 4**: Final behavior decision

Data flows: **Member 1 → Member 2 → Member 3 → Member 4**

---

**Ready to test?** Run:
```bash
python member2_gaze_tracking.py
```

**Need integration?** Check:
```bash
python integrated_member1_member2.py
```

Good luck with your exam proctoring system! 🎓
