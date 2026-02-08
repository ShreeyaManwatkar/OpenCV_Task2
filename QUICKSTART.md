# ⚡ QUICKSTART - Get Running in 2 Minutes!

## 🚀 Fastest Way to Run

### **Option 1: Quick Run (No venv)**

```bash
# 1. Install dependencies
pip install opencv-python numpy

# 2. Go to code folder
cd code

# 3. Run program
python member2_gaze_tracking.py

# 4. Press 'q' to quit
```

**That's it!** ✅

---

### **Option 2: Professional Setup (With venv)**

```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate it
venv\Scripts\activate              # Windows
source venv/bin/activate           # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run program
cd code
python member2_gaze_tracking.py

# 5. Press 'q' to quit
```

---

## 🎮 Controls

| Key | Action |
|-----|--------|
| `q` | Quit program |
| `r` | Reset warnings |

---

## 🎯 What You'll See

1. **Terminal output**: System status and info
2. **Webcam window**: Your face with tracking overlay
3. **Visual info**:
   - Blue box around face
   - Yellow circles on eyes
   - Gaze direction label
   - Head pose angles
   - Warning messages (if any)

---

## ✅ Success Checklist

After running, you should see:
- [ ] Terminal shows "System is now monitoring..."
- [ ] Webcam window opens
- [ ] Blue rectangle around your face
- [ ] Yellow circles on your eyes
- [ ] "Gaze: CENTER" label

---

## 🐛 Quick Fixes

### ❌ "Module not found: cv2"
```bash
pip install opencv-python
```

### ❌ "Cannot open camera"
- Close other apps using webcam (Zoom, Teams, etc.)
- Check camera permissions

### ❌ "python not recognized"
Try:
```bash
python3 member2_gaze_tracking.py
# or
py member2_gaze_tracking.py
```

---

## 📁 Folder Structure

```
Member2_GazeTracking_Package/
├── code/                              ← GO HERE!
│   ├── member2_gaze_tracking.py       ← RUN THIS!
│   └── haarcascade_frontalface_default.xml
├── examples/
├── docs/
└── requirements.txt
```

---

## 🎓 Using in VS Code

### **Method 1: Terminal**
1. Open folder in VS Code
2. Open terminal (`Ctrl + \``)
3. Run commands above

### **Method 2: Run Button**
1. Open `code/member2_gaze_tracking.py`
2. Click ▶️ button (top-right)
3. Program runs!

---

## 📊 What It Tracks

- ✅ Gaze direction (9 directions)
- ✅ Head rotation angles
- ✅ Look-away duration
- ✅ Suspicious behavior
- ✅ Automatic warnings

---

## 🔗 Need More Info?

- **Full guide**: `docs/USAGE_GUIDE.md`
- **Technical docs**: `docs/README_MEMBER2.md`
- **Package overview**: `docs/PACKAGE_OVERVIEW.md`
- **Warning fixes**: `docs/WARNING_FIXES.md`

---

## ⏱️ 30-Second Test

```bash
pip install opencv-python numpy
cd code
python member2_gaze_tracking.py
```

Press **'q'** when done. Done! ✅

---

## 🎉 You're Ready!

The program is working if you see:
1. Webcam window with your face
2. Blue box tracking your face
3. Gaze direction updating as you move

**Happy tracking!** 🚀
