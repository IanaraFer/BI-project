print("Hello from Python!")
import sys
print(f"Python version: {sys.version}")
print(f"Python path: {sys.executable}")

try:
    import os
    print(f"Current directory: {os.getcwd()}")
    print(f"Files in directory: {os.listdir('.')}")
except Exception as e:
    print(f"Error: {e}")
