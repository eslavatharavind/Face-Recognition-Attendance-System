import os
import sys

def create_required_directories():
    """Create all required directories for the application."""
    directories = [
        'TrainingImage',
        'TrainingImageLabel',
        'StudentDetails',
        'Attendance'
    ]
    
    for directory in directories:
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
                print(f"Created directory: {directory}")
            else:
                print(f"Directory already exists: {directory}")
        except Exception as e:
            print(f"Error creating directory {directory}: {str(e)}")
            return False
    return True

def check_requirements():
    """Check if all required packages are installed."""
    try:
        import cv2
        import numpy
        import PIL
        import pandas
        import geopy
        print("All required packages are installed.")
        return True
    except ImportError as e:
        print(f"Missing required package: {str(e)}")
        print("Please install required packages using: pip install -r requirements.txt")
        return False

def main():
    print("Setting up Face Recognition Attendance System...")
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("Error: Python 3.7 or higher is required")
        return False
    
    # Create directories
    if not create_required_directories():
        print("Error: Failed to create required directories")
        return False
    
    # Check requirements
    if not check_requirements():
        print("Error: Missing required packages")
        return False
    
    print("\nSetup completed successfully!")
    print("\nYou can now run the application using: python AMS_Run.py")
    return True

if __name__ == "__main__":
    main() 