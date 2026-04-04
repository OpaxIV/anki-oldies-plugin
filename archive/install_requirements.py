import subprocess
import sys

# Upgrade pip using the Python interpreter's module system
subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])

# Install mypy and aqt with Qt6 support
subprocess.check_call([sys.executable, "-m", "pip", "install", "mypy", "aqt[qt6]"])   
