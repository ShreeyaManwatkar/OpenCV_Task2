"""
Integration Example: Member 1 + Member 2
==========================================

This file demonstrates how Member 1 (Face Detection) and Member 2 (Gaze Tracking)
work together in the exam proctoring system.

Member 1: Provides base face detection and camera handling
Member 2: Adds gaze direction and head pose analysis

This combined system provides:
- Face detection and tracking
- Eye position tracking
- Gaze direction analysis
- Head pose estimation
- Real-time warnings and alerts
"""

import cv2
from member2_gaze_tracking import GazeTracker


def main():
    print("="*70)
    print("INTEGRATED PROCTORING SYSTEM: MEMBER 1 + MEMBER 2")
    print("="*70)
    print("\n🎥 Member 1: Face Detection & Camera Handling")
    print("👁️  Member 2: Gaze Tracking & Head Movement Analysis")
    print("\n" + "="*70)
    print("\nInitializing system...")
    
    # Member 1 Component: Face detection setup
    face_cascade = cv2.CascadeClassifier(
        "haarcascade_frontalface_default.xml"
    )
    
    # Member 2 Component: Gaze tracker
    gaze_tracker = GazeTracker()
    
    # Member 1: Start webcam
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ ERROR: Could not open webcam!")
        return
    
    print("✅ System initialized successfully!")
    print("\n" + "="*70)
    print("CONTROLS:")
    print("  'q' - Quit system")
    print("  'r' - Reset warnings")
    print("  's' - Show session summary")
    print("\nMONITORING:")
    print("  ✓ Face presence")
    print("  ✓ Gaze direction")
    print("  ✓ Head pose angles")
    print("  ✓ Look-away duration")
    print("  ✓ Suspicious behavior patterns")
    print("="*70)
    print("\n🟢 System is now active...\n")
    
    frame_count = 0
    
    while True:
        # Member 1: Capture frame
        ret, frame = cap.read()
        if not ret:
            print("❌ ERROR: Failed to read frame!")
            break
        
        # Member 1: Preprocess frame
        frame = cv2.resize(frame, (640, 480))
        frame = cv2.flip(frame, 1)
        
        # Member 2: Process frame with gaze tracking
        annotated_frame, tracking_data = gaze_tracker.process_frame(frame)
        
        # Display additional info from both members
        frame_count += 1
        
        # Add frame counter
        cv2.putText(
            annotated_frame,
            f"Frame: {frame_count}",
            (annotated_frame.shape[1] - 150, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),
            1
        )
        
        # Add system status
        status_color = (0, 255, 0) if tracking_data["direction"] == "center" else (0, 165, 255)
        if tracking_data["direction"] == "no_face":
            status_color = (0, 0, 255)
        
        cv2.putText(
            annotated_frame,
            "STATUS: " + ("NORMAL" if len(tracking_data["warnings"]) == 0 else "ALERT"),
            (annotated_frame.shape[1] - 200, annotated_frame.shape[0] - 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            status_color,
            2
        )
        
        # Display integrated view
        cv2.imshow("Exam Proctoring System - Member 1 + 2", annotated_frame)
        
        # Print real-time tracking info to console (every 30 frames)
        if frame_count % 30 == 0:
            print(f"[Frame {frame_count}] Direction: {tracking_data['direction']:>10} | "
                  f"Warnings: {len(tracking_data['warnings']):>2} | "
                  f"Look-away: {tracking_data['total_look_away_time']:>5.1f}s")
        
        # Handle keyboard input
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q'):
            print("\n🛑 Shutting down system...")
            break
        elif key == ord('r'):
            gaze_tracker.reset_warnings()
            print("\n🔄 Warnings reset!")
        elif key == ord('s'):
            summary = gaze_tracker.get_summary()
            print("\n" + "="*70)
            print("📊 SESSION SUMMARY")
            print("="*70)
            print(f"Total Frames Processed: {frame_count}")
            print(f"Total Warnings: {summary['total_warnings']}")
            print(f"Total Look-Away Time: {summary['total_look_away_time']:.1f} seconds")
            print("\nRecent Warnings:")
            for i, warning in enumerate(summary['warnings_list'][-10:], 1):
                print(f"  {i}. {warning}")
            print("="*70 + "\n")
    
    # Cleanup - Member 1 responsibility
    cap.release()
    cv2.destroyAllWindows()
    
    # Final summary
    final_summary = gaze_tracker.get_summary()
    print("\n" + "="*70)
    print("📋 FINAL SESSION REPORT")
    print("="*70)
    print(f"Total Frames Processed: {frame_count}")
    print(f"Total Warnings Generated: {final_summary['total_warnings']}")
    print(f"Total Look-Away Time: {final_summary['total_look_away_time']:.1f} seconds")
    print(f"Average Look-Away per Warning: {final_summary['total_look_away_time'] / max(1, final_summary['total_warnings']):.1f}s")
    print("\nAll Warnings:")
    if final_summary['warnings_list']:
        for i, warning in enumerate(final_summary['warnings_list'], 1):
            print(f"  {i}. {warning}")
    else:
        print("  ✅ No warnings - Clean session!")
    print("="*70)
    print("\n✅ System shutdown complete.")


if __name__ == "__main__":
    main()
