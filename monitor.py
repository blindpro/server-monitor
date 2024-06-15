import subprocess
import sys
import os
import time
import psutil
import datetime

# List of required packages
required_packages = ['psutil', 'accessible-output2']

def install_packages():
    """Install required packages if they are not already installed."""
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

# Install required packages
install_packages()

# Import packages after installation
import psutil
from accessible_output2.outputs import auto

# Initialize Accessible Output 2
speaker = auto.Auto()

def log_message(message):
    """Log the message with a timestamp and provide audio output."""
    try:
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"{timestamp} - {message}"
        print(log_entry)
        speaker.speak(log_entry)
        with open('server_monitor.log', 'a') as log_file:
            log_file.write(log_entry + '\n')
    except Exception as e:
        error_message = f"Failed to log message: {e}"
        print(error_message)
        speaker.speak(error_message)

def is_server_running():
    """Check if server.exe is currently running."""
    try:
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == 'server.exe':
                return True
    except Exception as e:
        log_message(f"Error checking server.exe: {e}")
    return False

def start_server():
    """Start the server.exe process."""
    log_message("Attempting to start server.exe...")
    try:
        server_path = os.path.join(os.getcwd(), 'server.exe')
        subprocess.Popen([server_path])
        log_message("server.exe started successfully.")
    except Exception as e:
        log_message(f"Failed to start server.exe: {e}")

def monitor_server():
    """Monitor server.exe and restart it if it stops."""
    while True:
        try:
            if not is_server_running():
                crash_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                log_message(f"server.exe crashed at {crash_time}. Restarting...")
                start_server()
        except Exception as e:
            log_message(f"Error in monitoring loop: {e}")
        time.sleep(5)  # Check every 5 seconds

if __name__ == "__main__":
    log_message("Starting server monitor script.")
    try:
        monitor_server()
    except Exception as e:
        log_message(f"Script crashed: {e}")
