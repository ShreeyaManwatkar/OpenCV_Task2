# 🎓 Member 2 - Gaze Tracking & Head Movement Detection

**Exam Proctoring System - Task 2**

---

## 📦 Package Contents

This package contains everything you need for Member 2 - Gaze Tracking system.

```
Member2_GazeTracking_Package/
├── 📁 code/                          ← Your main code files
│   ├── member2_gaze_tracking.py      ← MAIN FILE (run this!)
│   └── haarcascade_frontalface_default.xml
│
├── 📁 examples/                      ← Integration examples
│   └── integrated_member1_member2.py
│
├── 📁 docs/                          ← Documentation
│   ├── PACKAGE_OVERVIEW.md           ← Start here!
│   ├── README_MEMBER2.md             ← Technical docs
│   ├── USAGE_GUIDE.md                ← How to use
│   └── WARNING_FIXES.md              ← Latest fixes
│
├── requirements.txt                  ← Install dependencies
├── README.md                         ← This file
└── QUICKSTART.md                     ← Fast setup guide
```

---

## 🚀 Quick Start (3 Steps)

### **Step 1: Install Dependencies**
```bash
pip install -r requirements.txt
```

### **Step 2: Navigate to Code Folder**
```bash
cd code
```

### **Step 3: Run the Program**
```bash
python member2_gaze_tracking.py
```

**Controls:**
- Press **'q'** to quit
- Press **'r'** to reset warnings

---

## 🎯 What This Does

Member 2 tracks:
- ✅ **Gaze direction** (left/right/center/up/down)
- ✅ **Head movements** (pitch, yaw, roll angles)
- ✅ **Look-away time** (how long they look away)
- ✅ **Suspicious patterns** (frequent glancing)
- ✅ **Automatic warnings** (when thresholds exceeded)

---

## 🛠️ Using Virtual Environment (Recommended)

### **Setup (First Time):**
```bash
# Create venv
python -m venv venv

# Activate venv
venv\Scripts\activate              # Windows
source venv/bin/activate           # Mac/Linux

# Install packages
pip install -r requirements.txt

# Run program
cd code
python member2_gaze_tracking.py
```

### **Daily Use:**
```bash
# Activate venv
venv\Scripts\activate              # Windows
source venv/bin/activate           # Mac/Linux

# Run program
cd code
python member2_gaze_tracking.py
```

---

## 📚 Documentation

### **New to this project?**
👉 Read: `docs/PACKAGE_OVERVIEW.md`

### **Need setup help?**
👉 Read: `docs/USAGE_GUIDE.md`

### **Want technical details?**
👉 Read: `docs/README_MEMBER2.md`

### **Warning system issues?**
👉 Read: `docs/WARNING_FIXES.md`

---

## 🔗 Integration

### **Use as a Module:**
```python
import sys
sys.path.append('./code')  # Add code folder to path

from member2_gaze_tracking import GazeTracker
import cv2

# Initialize
tracker = GazeTracker()

# Process frame
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
annotated_frame, tracking_data = tracker.process_frame(frame)

# Use data
print(tracking_data['direction'])
print(tracking_data['warnings'])
```

### **See Integration Example:**
```bash
cd examples
python integrated_member1_member2.py
```

---

## 🎮 Features

### ✨ **Gaze Tracking**
- 9 direction detection (center, left, right, up, down, diagonals)
- Eye center tracking
- Pixel-level deviation measurement

### ✨ **Head Pose Estimation**
- Pitch (up/down): ±30°
- Yaw (left/right): ±45°
- Roll (tilt): ±15°
- Real-time angle display

### ✨ **Smart Warnings**
- One warning per incident (not per frame!)
- Auto-clear when behavior improves
- Clean display (max 3 unique warnings)
- Accurate warning count

### ✨ **Visual Feedback**
- Face bounding box
- Eye position markers
- Gaze direction label
- Head pose angles
- Warning messages
- Session statistics

---

## ⚙️ System Requirements

- **Python**: 3.7 or higher
- **Webcam**: Required
- **OS**: Windows, Mac, or Linux
- **RAM**: 100MB minimum
- **CPU**: Any modern processor

---

## 📦 Dependencies

```
opencv-python >= 4.8.0
numpy >= 1.24.0
```

Install with:
```bash
pip install -r requirements.txt
```

---

## 🐛 Troubleshooting

### **Camera won't open?**
- Close other apps using webcam
- Check camera permissions
- Try different camera index: `cap = cv2.VideoCapture(1)`

### **Module not found?**
```bash
pip install opencv-python numpy
```

### **Too many warnings?**
- The latest version fixes this!
- Read: `docs/WARNING_FIXES.md`

### **Need more help?**
- Check: `docs/USAGE_GUIDE.md`
- See troubleshooting section

---

## 🎓 Project Context

### **Team Members:**
1. **Member 1**: Face Detection & Camera Handling ✅
2. **Member 2**: Gaze Tracking & Head Movement ⭐ (This package!)
3. **Member 3**: Body Posture Detection
4. **Member 4**: Behavior Analysis & Decision Making

### **Your Role (Member 2):**
Track where candidates are looking and detect suspicious head movements during exams.

---

## ✅ Testing Checklist

Before using in production:

- [ ] Dependencies installed
- [ ] Webcam working
- [ ] Program runs without errors
- [ ] Face detected (blue box appears)
- [ ] Eyes detected (yellow circles)
- [ ] Gaze direction updates
- [ ] Warnings trigger correctly
- [ ] Can quit with 'q'

---

## 📞 Support

### **Quick Help:**
1. Read `QUICKSTART.md`
2. Check `docs/USAGE_GUIDE.md`
3. Review `docs/WARNING_FIXES.md`

### **Common Questions:**
- How to run? → See `QUICKSTART.md`
- Using venv? → See this README above
- Integration? → See `examples/` folder
- Warnings spam? → Fixed! See `docs/WARNING_FIXES.md`

---

## 🎯 Next Steps

1. ✅ Install dependencies
2. ✅ Test standalone mode
3. ✅ Adjust thresholds if needed
4. ✅ Integrate with Member 1
5. ✅ Prepare for Member 3 & 4 integration

---

## 📄 License

Educational project for exam proctoring system.

---

## 🎉 Ready to Start?

```bash
# Install
pip install -r requirements.txt

# Run
cd code
python member2_gaze_tracking.py
```

**Enjoy!** 🚀

---

**Version**: 2.0 (Warning System Fixed)  
**Last Updated**: 2026  
**Status**: ✅ Production Ready
