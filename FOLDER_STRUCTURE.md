# 📁 Folder Structure Explained

## Overview

```
Member2_GazeTracking_Package/
│
├── 📄 README.md                      ← Start here! Main overview
├── 📄 QUICKSTART.md                  ← 2-minute setup guide
├── 📄 requirements.txt               ← Python dependencies
│
├── 🔧 setup.bat                      ← Windows setup script
├── 🔧 run.bat                        ← Windows run script
├── 🔧 setup.sh                       ← Mac/Linux setup script
├── 🔧 run.sh                         ← Mac/Linux run script
│
├── 📁 code/                          ← YOUR MAIN CODE
│   ├── member2_gaze_tracking.py      ← RUN THIS FILE! Main program
│   └── haarcascade_frontalface_default.xml  ← Face detection model
│
├── 📁 examples/                      ← Integration examples
│   └── integrated_member1_member2.py ← How to use with Member 1
│
└── 📁 docs/                          ← Documentation
    ├── PACKAGE_OVERVIEW.md           ← Complete package info
    ├── README_MEMBER2.md             ← Technical documentation
    ├── USAGE_GUIDE.md                ← Detailed usage instructions
    └── WARNING_FIXES.md              ← Latest warning system fixes
```

---

## 📂 What's in Each Folder?

### 📁 **code/** - Your Main Code
This is where your actual program lives.

**Files:**
- `member2_gaze_tracking.py` - Main program (RUN THIS!)
- `haarcascade_frontalface_default.xml` - Required for face detection

**How to use:**
```bash
cd code
python member2_gaze_tracking.py
```

---

### 📁 **examples/** - Sample Code
Example code showing how to integrate Member 2 with other components.

**Files:**
- `integrated_member1_member2.py` - Complete example with Member 1

**How to use:**
```bash
cd examples
python integrated_member1_member2.py
```

---

### 📁 **docs/** - Documentation
All documentation files explaining how everything works.

**Files:**
- `PACKAGE_OVERVIEW.md` - Complete overview of the package
- `README_MEMBER2.md` - Technical details and API
- `USAGE_GUIDE.md` - Step-by-step usage instructions
- `WARNING_FIXES.md` - Explanation of warning system fixes

**When to read:**
- New to project? → `PACKAGE_OVERVIEW.md`
- Need setup help? → `USAGE_GUIDE.md`
- Want technical details? → `README_MEMBER2.md`
- Warning issues? → `WARNING_FIXES.md`

---

## 🔧 Scripts Explained

### Windows Users:

**setup.bat** - First-time setup
- Creates virtual environment
- Installs dependencies
- Run once when you first download

**run.bat** - Daily use
- Activates venv
- Runs the program
- Double-click to use!

### Mac/Linux Users:

**setup.sh** - First-time setup
```bash
./setup.sh
```

**run.sh** - Daily use
```bash
./run.sh
```

---

## 📄 Root Files

### **README.md**
Main documentation file. Read this first!

### **QUICKSTART.md**
Fastest way to get up and running (2 minutes).

### **requirements.txt**
List of Python packages needed:
```
opencv-python>=4.8.0
numpy>=1.24.0
```

---

## 🎯 Common Tasks

### **First Time Setup:**
```bash
# Windows
setup.bat

# Mac/Linux
./setup.sh
```

### **Run Program:**
```bash
# Windows
run.bat

# Mac/Linux
./run.sh

# OR manually:
cd code
python member2_gaze_tracking.py
```

### **Read Documentation:**
```bash
# Open in your browser or text editor
docs/PACKAGE_OVERVIEW.md
docs/USAGE_GUIDE.md
```

### **See Integration Example:**
```bash
cd examples
python integrated_member1_member2.py
```

---

## 📦 After Setup (venv created)

Your folder will have an additional `venv/` folder:

```
Member2_GazeTracking_Package/
├── venv/                             ← Virtual environment (auto-created)
│   ├── Scripts/  (Windows)
│   ├── bin/      (Mac/Linux)
│   └── Lib/
├── code/
├── examples/
├── docs/
└── ...
```

**Don't delete `venv/`!** This contains your Python packages.

---

## 🎯 Quick Reference

| I want to... | Go to... |
|--------------|----------|
| Run the program | `code/member2_gaze_tracking.py` |
| See example integration | `examples/integrated_member1_member2.py` |
| Learn how it works | `docs/PACKAGE_OVERVIEW.md` |
| Get setup help | `docs/USAGE_GUIDE.md` |
| Understand warnings | `docs/WARNING_FIXES.md` |
| Install packages | `requirements.txt` |
| Quick setup | `setup.bat` or `setup.sh` |
| Quick run | `run.bat` or `run.sh` |

---

## 💡 Tips

1. **Always work in the package folder** - All paths are relative
2. **Use venv** - Keeps your system Python clean
3. **Check docs/** - Most questions answered there
4. **Use scripts** - Easier than typing commands
5. **Keep structure intact** - Don't move files around

---

## ✅ Checklist

After downloading:
- [ ] Read `README.md`
- [ ] Run `setup.bat` or `setup.sh`
- [ ] Try running with `run.bat` or `run.sh`
- [ ] Check `docs/QUICKSTART.md` if issues
- [ ] Read `docs/PACKAGE_OVERVIEW.md` for details

---

Happy coding! 🚀
