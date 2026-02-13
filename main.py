"""
Face Tracker - Fixed Version
Perfect mouth detection + Full eye tracking (including DOWN)
"""

import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh

# Landmark indices
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]
LEFT_IRIS = [468, 469, 470, 471, 472]
RIGHT_IRIS = [473, 474, 475, 476, 477]
NOSE_TIP = 1
NOSE_BRIDGE = [6, 168, 197, 195]
MOUTH_OUTER = [61, 146, 91, 181, 84, 17, 314, 405, 321, 375, 291, 409]
MOUTH_INNER = [78, 191, 80, 81, 82, 13, 312, 311, 310, 415, 308, 324]

# Better mouth landmarks for accurate detection
UPPER_LIP = [61, 185, 40, 39, 37, 0, 267, 269, 270, 409, 291]
LOWER_LIP = [146, 91, 181, 84, 17, 314, 405, 321, 375, 291]
LIP_TOP = 13  # Top of upper lip
LIP_BOTTOM = 14  # Bottom of lower lip


def get_head_direction(face_landmarks, frame_shape):
    """Determine head/face direction"""
    h, w = frame_shape[:2]
    
    # Get key points
    nose_tip = face_landmarks.landmark[NOSE_TIP]
    left_face = face_landmarks.landmark[234]
    right_face = face_landmarks.landmark[454]
    
    # Convert to pixel coordinates
    nose_x = nose_tip.x * w
    left_x = left_face.x * w
    right_x = right_face.x * w
    
    # Calculate face center
    face_center_x = (left_x + right_x) / 2
    
    # Determine direction
    offset = nose_x - face_center_x
    threshold = w * 0.03
    
    if offset > threshold:
        return "Face: RIGHT"
    elif offset < -threshold:
        return "Face: LEFT"
    else:
        # Check vertical
        nose_y = nose_tip.y * h
        chin = face_landmarks.landmark[152]
        forehead = face_landmarks.landmark[10]
        chin_y = chin.y * h
        forehead_y = forehead.y * h
        
        face_center_y = (chin_y + forehead_y) / 2
        v_offset = nose_y - face_center_y
        v_threshold = h * 0.02
        
        if v_offset > v_threshold:
            return "Face: DOWN"
        elif v_offset < -v_threshold:
            return "Face: UP"
    
    return "Face: CENTER"


def get_eye_direction(iris_center, eye_corners):
    """Eye direction with PROPER down detection"""
    eye_center = np.mean(eye_corners, axis=0)
    direction = iris_center - eye_center
    
    # Normalize
    norm = np.linalg.norm(direction)
    if norm > 0:
        direction = direction / norm
    
    # Adjusted thresholds for better detection
    h_threshold = 0.05  # Horizontal (left/right)
    v_threshold = 0.04  # Vertical (up/down) - more sensitive
    
    # Check both directions
    horizontal_movement = abs(direction[0])
    vertical_movement = abs(direction[1])
    
    # Prioritize the stronger movement
    if horizontal_movement > h_threshold or vertical_movement > v_threshold:
        if horizontal_movement > vertical_movement:
            # Horizontal movement is dominant
            if direction[0] > h_threshold:
                return "Eyes: RIGHT"
            elif direction[0] < -h_threshold:
                return "Eyes: LEFT"
        else:
            # Vertical movement is dominant
            if direction[1] > v_threshold:
                return "Eyes: DOWN"
            elif direction[1] < -v_threshold:
                return "Eyes: UP"
    
    return "Eyes: CENTER"


def get_mouth_state(face_landmarks, frame_shape):
    """FIXED: Accurate mouth detection"""
    h, w = frame_shape[:2]
    
    # Get upper and lower lip center points
    upper_lip = face_landmarks.landmark[13]  # Upper lip top
    lower_lip = face_landmarks.landmark[14]  # Lower lip bottom
    
    # Also get left and right corners for width
    left_corner = face_landmarks.landmark[61]
    right_corner = face_landmarks.landmark[291]
    
    # Convert to pixel coordinates
    upper_y = upper_lip.y * h
    lower_y = lower_lip.y * h
    left_x = left_corner.x * w
    right_x = right_corner.x * w
    
    # Calculate distances
    lip_distance = abs(lower_y - upper_y)
    mouth_width = abs(right_x - left_x)
    
    # Calculate ratio (vertical distance / width)
    if mouth_width > 0:
        ratio = lip_distance / mouth_width
    else:
        ratio = 0
    
    # Better thresholds based on actual mouth measurements
    # These values are calibrated for accurate detection
    if ratio > 0.25:  # Clearly open
        return "Mouth: OPEN"
    elif ratio > 0.15:  # Slightly open
        return "Mouth: SLIGHTLY OPEN"
    else:  # Closed
        return "Mouth: CLOSED"


def extract_landmarks(face_landmarks, frame_shape):
    """Extract landmark coordinates"""
    h, w = frame_shape[:2]
    landmarks = {}
    
    # Left eye
    left_eye_points = []
    for idx in LEFT_EYE:
        landmark = face_landmarks.landmark[idx]
        left_eye_points.append([int(landmark.x * w), int(landmark.y * h)])
    landmarks['left_eye'] = np.array(left_eye_points)
    
    # Right eye
    right_eye_points = []
    for idx in RIGHT_EYE:
        landmark = face_landmarks.landmark[idx]
        right_eye_points.append([int(landmark.x * w), int(landmark.y * h)])
    landmarks['right_eye'] = np.array(right_eye_points)
    
    # Left iris
    left_iris_points = []
    for idx in LEFT_IRIS:
        landmark = face_landmarks.landmark[idx]
        left_iris_points.append([int(landmark.x * w), int(landmark.y * h)])
    landmarks['left_iris'] = np.array(left_iris_points)
    
    # Right iris
    right_iris_points = []
    for idx in RIGHT_IRIS:
        landmark = face_landmarks.landmark[idx]
        right_iris_points.append([int(landmark.x * w), int(landmark.y * h)])
    landmarks['right_iris'] = np.array(right_iris_points)
    
    # Nose
    nose_points = []
    for idx in NOSE_BRIDGE:
        landmark = face_landmarks.landmark[idx]
        nose_points.append([int(landmark.x * w), int(landmark.y * h)])
    nose_tip = face_landmarks.landmark[NOSE_TIP]
    nose_points.append([int(nose_tip.x * w), int(nose_tip.y * h)])
    landmarks['nose'] = np.array(nose_points)
    
    # Mouth
    mouth_outer_points = []
    for idx in MOUTH_OUTER:
        landmark = face_landmarks.landmark[idx]
        mouth_outer_points.append([int(landmark.x * w), int(landmark.y * h)])
    landmarks['mouth_outer'] = np.array(mouth_outer_points)
    
    mouth_inner_points = []
    for idx in MOUTH_INNER:
        landmark = face_landmarks.landmark[idx]
        mouth_inner_points.append([int(landmark.x * w), int(landmark.y * h)])
    landmarks['mouth_inner'] = np.array(mouth_inner_points)
    
    return landmarks


def draw_landmarks(frame, landmarks, face_dir, eye_dir, mouth_state):
    """Draw landmarks and status"""
    
    # Draw left eye
    for point in landmarks['left_eye']:
        cv2.circle(frame, tuple(point), 2, (0, 255, 0), -1)
    
    # Draw right eye
    for point in landmarks['right_eye']:
        cv2.circle(frame, tuple(point), 2, (0, 255, 0), -1)
    
    # Draw left iris - larger for visibility
    left_iris_center = np.mean(landmarks['left_iris'], axis=0).astype(int)
    cv2.circle(frame, tuple(left_iris_center), 5, (255, 0, 0), -1)
    cv2.circle(frame, tuple(left_iris_center), 8, (255, 0, 0), 2)
    
    # Draw right iris - larger for visibility
    right_iris_center = np.mean(landmarks['right_iris'], axis=0).astype(int)
    cv2.circle(frame, tuple(right_iris_center), 5, (255, 0, 0), -1)
    cv2.circle(frame, tuple(right_iris_center), 8, (255, 0, 0), 2)
    
    # Draw nose
    for point in landmarks['nose']:
        cv2.circle(frame, tuple(point), 3, (0, 255, 255), -1)
    
    # Draw mouth
    for i in range(len(landmarks['mouth_outer'])):
        pt1 = tuple(landmarks['mouth_outer'][i])
        pt2 = tuple(landmarks['mouth_outer'][(i + 1) % len(landmarks['mouth_outer'])])
        cv2.line(frame, pt1, pt2, (255, 0, 255), 2)
    
    for i in range(len(landmarks['mouth_inner'])):
        pt1 = tuple(landmarks['mouth_inner'][i])
        pt2 = tuple(landmarks['mouth_inner'][(i + 1) % len(landmarks['mouth_inner'])])
        cv2.line(frame, pt1, pt2, (200, 0, 200), 1)
    
    # Status panel
    overlay = frame.copy()
    cv2.rectangle(overlay, (5, 5), (300, 140), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
    
    # Display tracking info
    y_pos = 35
    cv2.putText(frame, face_dir, (15, y_pos), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
    
    y_pos += 35
    cv2.putText(frame, eye_dir, (15, y_pos), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    
    y_pos += 35
    cv2.putText(frame, mouth_state, (15, y_pos), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 255), 2)
    
    # Instruction
    cv2.putText(frame, "Press 'q' to quit", (10, 460), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    return frame


def main():
    """Main tracking function"""
    print("=" * 50)
    print("FACE TRACKER - Fixed Version")
    print("=" * 50)
    print("Starting camera...")
    
    # Initialize webcam
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("ERROR: Cannot access camera!")
        return
    
    print("Camera ready!")
    print("\nTracking:")
    print("  - Face: LEFT/RIGHT/UP/DOWN/CENTER")
    print("  - Eyes: LEFT/RIGHT/UP/DOWN/CENTER")
    print("  - Mouth: OPEN/CLOSED/SLIGHTLY OPEN")
    print("\nPress 'q' to quit")
    print("=" * 50)
    
    # Initialize Face Mesh
    with mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ) as face_mesh:
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            # Resize and flip
            frame = cv2.resize(frame, (640, 480))
            frame = cv2.flip(frame, 1)
            
            # Convert to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Process frame
            results = face_mesh.process(rgb_frame)
            
            if results.multi_face_landmarks:
                face_landmarks = results.multi_face_landmarks[0]
                
                # Extract landmarks
                landmarks = extract_landmarks(face_landmarks, frame.shape)
                
                # Get face direction
                face_dir = get_head_direction(face_landmarks, frame.shape)
                
                # Get eye direction (average both eyes)
                left_iris_center = np.mean(landmarks['left_iris'], axis=0)
                right_iris_center = np.mean(landmarks['right_iris'], axis=0)
                avg_iris = (left_iris_center + right_iris_center) / 2
                avg_eye = (np.mean(landmarks['left_eye'], axis=0) + 
                          np.mean(landmarks['right_eye'], axis=0)) / 2
                eye_dir = get_eye_direction(avg_iris, np.array([avg_eye]))
                
                # Get mouth state - FIXED
                mouth_state = get_mouth_state(face_landmarks, frame.shape)
                
                # Draw everything
                frame = draw_landmarks(frame, landmarks, face_dir, eye_dir, mouth_state)
            
            else:
                # No face detected
                cv2.putText(frame, "No face detected", (50, 240), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)
            
            # Display
            cv2.imshow("Face Tracker - Fixed", frame)
            
            # Quit on 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    print("\nTracking ended. Goodbye!")


if __name__ == "__main__":
    main()
