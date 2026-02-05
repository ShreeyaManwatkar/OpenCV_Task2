# Member 2 - Head Movement & Gaze Direction Tracking

## 🎯 Main Job
**Decide where the candidate is looking**

## 📋 Overview
Member 2 is responsible for tracking head movements and gaze direction during exam proctoring. It analyzes where candidates are looking, how long they look away, and detects suspicious patterns like frequent glancing or excessive head rotation.

## 🔧 Core Responsibilities

### 1. **Gaze Direction Detection**
- Tracks eye positions using Haar Cascade eye detection
- Calculates gaze direction: **left**, **right**, **center**, **up**, **down**
- Measures horizontal and vertical deviation from screen center
- Uses eye midpoint for accurate gaze estimation

### 2. **Head Pose Estimation**
- Calculates head rotation angles:
  - **Pitch** (up/down tilt)
  - **Yaw** (left/right turn)
  - **Roll** (head tilt sideways)
- Uses 3D facial landmarks and solvePnP algorithm
- Detects excessive head turns beyond acceptable thresholds

### 3. **Suspicious Behavior Detection**
- **Long look-away duration**: Triggers warning if looking away > 3 seconds
- **Frequent glancing**: Detects patterns of repeated side glances
- **Head rotation**: Alerts when head turns exceed 25 degrees
- **Time-based tracking**: Accumulates total time spent looking away

### 4. **Real-time Monitoring**
- Frame-by-frame processing at webcam speed
- Visual feedback with overlay information
- Live warning display on screen
- Comprehensive tracking data output

## 🛠️ Technical Implementation

### Technologies Used
- **OpenCV**: Face and eye detection, image processing
- **NumPy**: Mathematical calculations, matrix operations
- **Haar Cascades**: 
  - `haarcascade_frontalface_default.xml` - Face detection
  - `haarcascade_eye.xml` - Eye detection
- **solvePnP**: 3D head pose estimation from 2D landmarks

### Key Algorithms

#### 1. Eye Detection & Gaze Calculation
```python
# Detects eyes within face region
# Calculates eye centers (left and right)
# Computes eye midpoint
# Measures deviation from frame center
```

#### 2. Head Pose Estimation
```python
# Uses 6 facial landmarks (nose, chin, eyes, mouth corners)
# Creates 3D model points
# Solves perspective-n-point problem
# Extracts Euler angles (pitch, yaw, roll)
```

#### 3. Behavior Pattern Analysis
```python
# Tracks look-away start time
# Accumulates total look-away duration
# Maintains glance history (last 20 glances)
# Checks for frequent glancing patterns
# Validates against time-based thresholds
```

## 📊 Output Data Structure

### Tracking Data Dictionary
```python
{
    "direction": "center",  # left/right/center/up/down/no_face
    "horizontal_deviation": 15,  # pixels from center
    "vertical_deviation": -8,    # pixels from center
    "head_pose": {
        "pitch": 5.2,   # degrees (up/down)
        "yaw": -12.3,   # degrees (left/right)
        "roll": 2.1     # degrees (tilt)
    },
    "warnings": [
        "Looking right for 3.2s",
        "Head turned left: 28.5°"
    ],
    "total_look_away_time": 12.5  # cumulative seconds
}
```

## 🔍 Detection Thresholds

### Configurable Parameters
```python
HORIZONTAL_THRESHOLD = 80      # pixels for left/right detection
VERTICAL_THRESHOLD = 60        # pixels for up/down detection
MAX_LOOK_AWAY_TIME = 3.0       # seconds before warning
MAX_HEAD_TURN_ANGLE = 25       # degrees before warning
FREQUENT_GLANCE_COUNT = 5      # glances to trigger warning
GLANCE_TIME_WINDOW = 10        # seconds for counting glances
```

## 🚀 Usage

### Standalone Execution
```bash
python member2_gaze_tracking.py
```

**Controls:**
- Press **'q'** to quit
- Press **'r'** to reset warnings

### Integration with Other Members
```python
from member2_gaze_tracking import GazeTracker

# Initialize tracker
tracker = GazeTracker()

# Process video frame
annotated_frame, tracking_data = tracker.process_frame(frame)

# Access tracking information
direction = tracking_data["direction"]
warnings = tracking_data["warnings"]
head_pose = tracking_data["head_pose"]

# Get session summary
summary = tracker.get_summary()
```

## 📈 Visual Feedback

### On-Screen Display
1. **Face bounding box** (blue rectangle)
2. **Eye positions** (yellow circles)
3. **Eye center** (magenta dot)
4. **Center reference lines** (gray crosshair)
5. **Gaze direction label** (green if center, orange if away)
6. **Head pose angles** (pitch, yaw in degrees)
7. **Active warnings** (red text, last 5 warnings)
8. **Session statistics** (total look-away time, warning count)

### Color Coding
- 🟢 **Green**: Looking at center (normal)
- 🟠 **Orange**: Looking away (caution)
- 🔵 **Blue**: Face boundary
- 🟡 **Yellow**: Eye positions
- 🔴 **Red**: Warnings and alerts

## ⚙️ Class Methods

### `GazeTracker` Class

#### Initialization
```python
__init__()
```
Sets up cascades, thresholds, and tracking variables

#### Core Methods
```python
detect_eyes(face_roi, face_gray)
# Returns: left_eye_center, right_eye_center

calculate_gaze_direction(frame_center, eye_midpoint)
# Returns: direction, horizontal_dev, vertical_dev

estimate_head_pose(face_landmarks, frame_width, frame_height)
# Returns: pitch, yaw, roll (in degrees)

process_frame(frame)
# Returns: annotated_frame, tracking_data

update_tracking(current_time)
# Updates warnings and look-away metrics

check_head_rotation(yaw, pitch)
# Validates head angles against thresholds
```

#### Utility Methods
```python
reset_warnings()
# Clear all warnings and metrics

get_summary()
# Return session summary dictionary
```

## 🔄 Integration Points

### Input from Member 1
- Receives video frames from webcam
- Uses face detection results
- Works with grayscale conversion

### Output to Member 4
```python
tracking_data = {
    "direction": str,           # Current gaze direction
    "horizontal_deviation": int,
    "vertical_deviation": int,
    "head_pose": dict,          # Rotation angles
    "warnings": list,           # Active warnings
    "total_look_away_time": float
}
```

Member 4 (Behavior Analysis) uses this data to make final decisions about suspicious behavior.

## 📝 Session Summary

After each session, get comprehensive statistics:

```python
summary = tracker.get_summary()

# Output:
{
    "total_warnings": 7,
    "total_look_away_time": 18.3,
    "warnings_list": [
        "Looking right for 3.2s",
        "Head turned left: 28.5°",
        "Frequent glances: 5 in 10s",
        # ... more warnings
    ]
}
```

## 🎓 Example Scenarios

### Normal Behavior
- Gaze: **center** (looking at screen)
- Head pose: pitch ±10°, yaw ±10°
- No warnings triggered
- Minimal look-away time

### Suspicious Behavior
- Gaze: **left/right** for extended periods
- Head pose: yaw > 25° (turning to side)
- Multiple warnings:
  - "Looking left for 4.5s"
  - "Head turned right: 32.1°"
  - "Frequent glances: 6 in 10s"

## 🐛 Troubleshooting

### No eyes detected
- Falls back to face center for gaze estimation
- Less accurate but still functional
- Improve lighting conditions for better detection

### Inaccurate head pose
- Ensure good lighting
- Position face clearly in frame
- Avoid extreme angles (> 45°)

### False positives
- Adjust thresholds in `__init__()` method
- Increase `MAX_LOOK_AWAY_TIME` for more tolerance
- Increase `MAX_HEAD_TURN_ANGLE` for natural movement

## 📦 Dependencies

```bash
pip install opencv-python numpy
```

## 🎯 Performance Notes

- Processes at webcam framerate (~30 FPS)
- Low latency for real-time monitoring
- Efficient cascade classifiers
- Minimal CPU usage with optimizations

## 🔮 Future Enhancements

1. **Deep learning models**: MediaPipe Face Mesh for better landmarks
2. **Iris tracking**: More precise gaze estimation
3. **Calibration system**: Personalized thresholds per user
4. **Machine learning**: Pattern recognition for cheating behaviors
5. **Multi-face support**: Track multiple candidates simultaneously

## 📞 Support

For questions about Member 2 implementation:
- Review code comments for detailed explanations
- Check integration examples
- Test with provided standalone mode
- Adjust thresholds based on your use case

---

**Member 2 Status**: ✅ Fully Implemented
**Integration Ready**: ✅ Yes
**Testing Status**: ✅ Standalone mode available
