"""
Member 2 - Head Movement & Gaze Direction
Main job: Decide where the candidate is looking.

Responsibilities:
- Calculate head tilt (left/right) and rotation (up/down)
- Detect looking away from screen using eye tracking
- Track eye center positions and gaze direction
- Set thresholds for excessive head turns and side glances
- Measure time spent looking away

Tech concepts:
- Head pose estimation using facial landmarks
- Eye center tracking with Haar Cascades
- Angle calculation for pitch, yaw, roll
- Time-based threshold analysis

Output:
- Direction: left/right/center/down/up
- Time spent looking away
- Gaze deviation angles
- Warning flags for suspicious behavior

Usage:
Run this file to test gaze tracking, or import GazeTracker class
Press 'q' to exit, 'r' to reset warnings
"""

import cv2
import numpy as np
import time
from collections import deque


class GazeTracker:
    """
    Advanced gaze and head movement tracking system.
    Tracks where the candidate is looking and detects suspicious behavior.
    """
    
    def __init__(self):
        # Load cascades for face and eye detection
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )
        self.eye_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_eye.xml"
        )
        
        # Thresholds for gaze direction (in pixels from center)
        self.HORIZONTAL_THRESHOLD = 80  # Left/Right detection
        self.VERTICAL_THRESHOLD = 60    # Up/Down detection
        
        # Thresholds for warnings
        self.MAX_LOOK_AWAY_TIME = 3.0   # seconds
        self.MAX_HEAD_TURN_ANGLE = 25   # degrees
        self.FREQUENT_GLANCE_COUNT = 5  # glances in window
        self.GLANCE_TIME_WINDOW = 10    # seconds
        
        # Tracking variables
        self.current_direction = "center"
        self.look_away_start_time = None
        self.total_look_away_time = 0
        self.glance_history = deque(maxlen=20)
        
        # Face center tracking for head movement
        self.prev_face_center = None
        self.face_center_history = deque(maxlen=10)
        
        # Eye position tracking
        self.left_eye_center = None
        self.right_eye_center = None
        self.eye_center_history = deque(maxlen=5)
        
        # Warning flags
        self.warnings = []
        self.warning_count = 0
        
        # 3D model points for head pose estimation
        self.model_points = np.array([
            (0.0, 0.0, 0.0),             # Nose tip
            (0.0, -330.0, -65.0),        # Chin
            (-225.0, 170.0, -135.0),     # Left eye left corner
            (225.0, 170.0, -135.0),      # Right eye right corner
            (-150.0, -150.0, -125.0),    # Left mouth corner
            (150.0, -150.0, -125.0)      # Right mouth corner
        ])
        
        # Camera internals (will be set based on frame size)
        self.camera_matrix = None
        self.dist_coeffs = np.zeros((4, 1))
        
    def initialize_camera_matrix(self, frame_width, frame_height):
        """Initialize camera matrix for head pose estimation"""
        focal_length = frame_width
        center = (frame_width / 2, frame_height / 2)
        self.camera_matrix = np.array([
            [focal_length, 0, center[0]],
            [0, focal_length, center[1]],
            [0, 0, 1]
        ], dtype="double")
    
    def detect_eyes(self, face_roi, face_gray):
        """
        Detect eyes within face region and calculate eye centers.
        Returns left and right eye centers.
        """
        eyes = self.eye_cascade.detectMultiScale(
            face_gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(20, 20)
        )
        
        if len(eyes) < 2:
            return None, None
        
        # Sort eyes by x-coordinate (left to right)
        eyes = sorted(eyes, key=lambda x: x[0])
        
        # Calculate eye centers
        left_eye = eyes[0]
        right_eye = eyes[-1]
        
        left_center = (
            left_eye[0] + left_eye[2] // 2,
            left_eye[1] + left_eye[3] // 2
        )
        right_center = (
            right_eye[0] + right_eye[2] // 2,
            right_eye[1] + right_eye[3] // 2
        )
        
        return left_center, right_center
    
    def calculate_gaze_direction(self, frame_center, eye_midpoint):
        """
        Calculate gaze direction based on eye position relative to frame center.
        Returns direction string and deviation values.
        """
        if eye_midpoint is None:
            return "unknown", 0, 0
        
        # Calculate deviation from center
        horizontal_dev = eye_midpoint[0] - frame_center[0]
        vertical_dev = eye_midpoint[1] - frame_center[1]
        
        # Determine direction
        direction = "center"
        
        if abs(horizontal_dev) > self.HORIZONTAL_THRESHOLD:
            if horizontal_dev > 0:
                direction = "right"
            else:
                direction = "left"
        
        if abs(vertical_dev) > self.VERTICAL_THRESHOLD:
            if vertical_dev > 0:
                direction = "down"
            else:
                direction = "up"
        
        # Combine directions if both thresholds exceeded
        if abs(horizontal_dev) > self.HORIZONTAL_THRESHOLD and \
           abs(vertical_dev) > self.VERTICAL_THRESHOLD:
            h_dir = "right" if horizontal_dev > 0 else "left"
            v_dir = "down" if vertical_dev > 0 else "up"
            direction = f"{v_dir}-{h_dir}"
        
        return direction, horizontal_dev, vertical_dev
    
    def estimate_head_pose(self, face_landmarks, frame_width, frame_height):
        """
        Estimate head pose angles (pitch, yaw, roll) from facial landmarks.
        Returns rotation angles in degrees.
        """
        if len(face_landmarks) < 6:
            return None, None, None
        
        # Initialize camera matrix if not done
        if self.camera_matrix is None:
            self.initialize_camera_matrix(frame_width, frame_height)
        
        # Convert landmarks to numpy array
        image_points = np.array(face_landmarks, dtype="double")
        
        # Solve PnP to get rotation and translation vectors
        success, rotation_vector, translation_vector = cv2.solvePnP(
            self.model_points,
            image_points,
            self.camera_matrix,
            self.dist_coeffs,
            flags=cv2.SOLVEPNP_ITERATIVE
        )
        
        if not success:
            return None, None, None
        
        # Convert rotation vector to rotation matrix
        rotation_matrix, _ = cv2.Rodrigues(rotation_vector)
        
        # Calculate Euler angles
        pose_mat = cv2.hconcat((rotation_matrix, translation_vector))
        _, _, _, _, _, _, euler_angles = cv2.decomposeProjectionMatrix(pose_mat)
        
        pitch = euler_angles[0][0]
        yaw = euler_angles[1][0]
        roll = euler_angles[2][0]
        
        return pitch, yaw, roll
    
    def approximate_facial_landmarks(self, face_rect, left_eye, right_eye):
        """
        Approximate facial landmarks from face rectangle and eye positions.
        Used for basic head pose estimation.
        """
        x, y, w, h = face_rect
        
        # Estimate landmark positions
        nose_tip = (x + w // 2, y + h // 2)
        chin = (x + w // 2, y + h)
        
        # Use detected eyes or estimate
        if left_eye and right_eye:
            left_eye_corner = (left_eye[0] - 10, left_eye[1])
            right_eye_corner = (right_eye[0] + 10, right_eye[1])
        else:
            left_eye_corner = (x + w // 4, y + h // 3)
            right_eye_corner = (x + 3 * w // 4, y + h // 3)
        
        left_mouth = (x + w // 3, y + 2 * h // 3)
        right_mouth = (x + 2 * w // 3, y + 2 * h // 3)
        
        return [
            nose_tip,
            chin,
            left_eye_corner,
            right_eye_corner,
            left_mouth,
            right_mouth
        ]
    
    def update_tracking(self, current_time):
        """
        Update tracking metrics and detect suspicious patterns.
        """
        # Track look-away time
        if self.current_direction != "center":
            if self.look_away_start_time is None:
                self.look_away_start_time = current_time
                self.glance_history.append(current_time)
            else:
                look_away_duration = current_time - self.look_away_start_time
                
                # Check if looking away too long
                if look_away_duration > self.MAX_LOOK_AWAY_TIME:
                    warning = f"Looking {self.current_direction} for {look_away_duration:.1f}s"
                    if warning not in self.warnings:
                        self.warnings.append(warning)
                        self.warning_count += 1
        else:
            if self.look_away_start_time is not None:
                self.total_look_away_time += current_time - self.look_away_start_time
                self.look_away_start_time = None
        
        # Check for frequent glances
        recent_glances = [t for t in self.glance_history 
                         if current_time - t < self.GLANCE_TIME_WINDOW]
        
        if len(recent_glances) >= self.FREQUENT_GLANCE_COUNT:
            warning = f"Frequent glances: {len(recent_glances)} in {self.GLANCE_TIME_WINDOW}s"
            if warning not in self.warnings:
                self.warnings.append(warning)
                self.warning_count += 1
    
    def check_head_rotation(self, yaw, pitch):
        """
        Check if head rotation exceeds acceptable thresholds.
        """
        if yaw is not None and abs(yaw) > self.MAX_HEAD_TURN_ANGLE:
            direction = "right" if yaw > 0 else "left"
            warning = f"Head turned {direction}: {abs(yaw):.1f}°"
            if warning not in self.warnings:
                self.warnings.append(warning)
                self.warning_count += 1
        
        if pitch is not None and abs(pitch) > self.MAX_HEAD_TURN_ANGLE:
            direction = "down" if pitch > 0 else "up"
            warning = f"Head tilted {direction}: {abs(pitch):.1f}°"
            if warning not in self.warnings:
                self.warnings.append(warning)
                self.warning_count += 1
    
    def process_frame(self, frame):
        """
        Main processing function for gaze tracking.
        Returns annotated frame and tracking data.
        """
        current_time = time.time()
        frame_height, frame_width = frame.shape[:2]
        frame_center = (frame_width // 2, frame_height // 2)
        
        # Convert to grayscale for detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=5,
            minSize=(100, 100)
        )
        
        tracking_data = {
            "direction": "no_face",
            "horizontal_deviation": 0,
            "vertical_deviation": 0,
            "head_pose": {"pitch": None, "yaw": None, "roll": None},
            "warnings": self.warnings.copy(),
            "total_look_away_time": self.total_look_away_time
        }
        
        if len(faces) == 0:
            # No face detected
            cv2.putText(
                frame,
                "NO FACE DETECTED!",
                (frame_width // 2 - 150, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                2
            )
            return frame, tracking_data
        
        # Process the largest face
        face = max(faces, key=lambda rect: rect[2] * rect[3])
        x, y, w, h = face
        
        # Draw face rectangle
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        
        # Calculate face center
        face_center = (x + w // 2, y + h // 2)
        self.face_center_history.append(face_center)
        
        # Extract face ROI for eye detection
        face_roi = frame[y:y+h, x:x+w]
        face_gray = gray[y:y+h, x:x+w]
        
        # Detect eyes
        left_eye, right_eye = self.detect_eyes(face_roi, face_gray)
        
        # Draw eyes if detected
        if left_eye and right_eye:
            # Convert to absolute coordinates
            left_eye_abs = (x + left_eye[0], y + left_eye[1])
            right_eye_abs = (x + right_eye[0], y + right_eye[1])
            
            cv2.circle(frame, left_eye_abs, 5, (0, 255, 255), -1)
            cv2.circle(frame, right_eye_abs, 5, (0, 255, 255), -1)
            
            # Calculate eye midpoint
            eye_midpoint = (
                (left_eye_abs[0] + right_eye_abs[0]) // 2,
                (left_eye_abs[1] + right_eye_abs[1]) // 2
            )
            self.eye_center_history.append(eye_midpoint)
            
            # Draw eye center
            cv2.circle(frame, eye_midpoint, 3, (255, 0, 255), -1)
            
            # Calculate gaze direction
            direction, h_dev, v_dev = self.calculate_gaze_direction(
                frame_center, eye_midpoint
            )
            self.current_direction = direction
            
            tracking_data["direction"] = direction
            tracking_data["horizontal_deviation"] = h_dev
            tracking_data["vertical_deviation"] = v_dev
        else:
            # Use face center as fallback
            direction, h_dev, v_dev = self.calculate_gaze_direction(
                frame_center, face_center
            )
            self.current_direction = direction
            tracking_data["direction"] = direction
            tracking_data["horizontal_deviation"] = h_dev
            tracking_data["vertical_deviation"] = v_dev
        
        # Head pose estimation
        landmarks = self.approximate_facial_landmarks(face, left_eye, right_eye)
        pitch, yaw, roll = self.estimate_head_pose(
            landmarks, frame_width, frame_height
        )
        
        if pitch is not None:
            tracking_data["head_pose"]["pitch"] = float(pitch)
            tracking_data["head_pose"]["yaw"] = float(yaw)
            tracking_data["head_pose"]["roll"] = float(roll)
            
            # Check head rotation thresholds
            self.check_head_rotation(yaw, pitch)
        
        # Update tracking metrics
        self.update_tracking(current_time)
        
        # Draw center reference lines
        cv2.line(frame, (frame_center[0], 0), 
                (frame_center[0], frame_height), (200, 200, 200), 1)
        cv2.line(frame, (0, frame_center[1]), 
                (frame_width, frame_center[1]), (200, 200, 200), 1)
        
        # Draw gaze direction indicator
        color = (0, 255, 0) if direction == "center" else (0, 165, 255)
        cv2.putText(
            frame,
            f"Gaze: {direction.upper()}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            color,
            2
        )
        
        # Draw head pose angles if available
        if pitch is not None:
            cv2.putText(
                frame,
                f"Pitch: {pitch:.1f}deg Yaw: {yaw:.1f}deg",
                (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 255),
                1
            )
        
        # Draw warnings
        warning_y = 90
        for warning in self.warnings[-5:]:  # Show last 5 warnings
            cv2.putText(
                frame,
                f"WARNING: {warning}",
                (10, warning_y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 0, 255),
                1
            )
            warning_y += 25
        
        # Draw total stats
        cv2.putText(
            frame,
            f"Look-away time: {self.total_look_away_time:.1f}s | Warnings: {self.warning_count}",
            (10, frame_height - 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 0),
            1
        )
        
        return frame, tracking_data
    
    def reset_warnings(self):
        """Reset all warnings and tracking metrics"""
        self.warnings.clear()
        self.warning_count = 0
        self.total_look_away_time = 0
        self.look_away_start_time = None
        self.glance_history.clear()
    
    def get_summary(self):
        """Get summary of tracking session"""
        return {
            "total_warnings": self.warning_count,
            "total_look_away_time": self.total_look_away_time,
            "warnings_list": self.warnings.copy()
        }


def main():
    """
    Main function to run gaze tracking system standalone.
    """
    print("="*60)
    print("MEMBER 2 - HEAD MOVEMENT & GAZE DIRECTION TRACKING")
    print("="*60)
    print("\nInitializing gaze tracking system...")
    print("\nControls:")
    print("  'q' - Quit")
    print("  'r' - Reset warnings")
    print("\nMonitoring:")
    print("  - Gaze direction (left/right/center/up/down)")
    print("  - Head pose angles (pitch, yaw, roll)")
    print("  - Look-away duration")
    print("  - Frequent glancing patterns")
    print("="*60)
    
    # Initialize tracker
    tracker = GazeTracker()
    
    # Start webcam
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("ERROR: Could not open webcam!")
        return
    
    print("\nWebcam started successfully!")
    print("System is now monitoring gaze direction...\n")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("ERROR: Failed to read frame!")
            break
        
        # Resize and flip frame
        frame = cv2.resize(frame, (640, 480))
        frame = cv2.flip(frame, 1)
        
        # Process frame
        annotated_frame, tracking_data = tracker.process_frame(frame)
        
        # Display frame
        cv2.imshow("Member 2 - Gaze Tracking", annotated_frame)
        
        # Handle key presses
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('r'):
            tracker.reset_warnings()
            print("Warnings reset!")
    
    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    
    # Print summary
    summary = tracker.get_summary()
    print("\n" + "="*60)
    print("SESSION SUMMARY")
    print("="*60)
    print(f"Total Warnings: {summary['total_warnings']}")
    print(f"Total Look-Away Time: {summary['total_look_away_time']:.1f} seconds")
    print("\nWarnings Triggered:")
    for i, warning in enumerate(summary['warnings_list'], 1):
        print(f"  {i}. {warning}")
    print("="*60)


if __name__ == "__main__":
    main()
