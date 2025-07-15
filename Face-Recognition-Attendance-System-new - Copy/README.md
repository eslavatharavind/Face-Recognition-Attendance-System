# Face Recognition Based Attendance Management System

A Python-based attendance management system that uses face recognition to automatically mark attendance. The system now includes GPS location tracking for attendance records.

## Features

- Face recognition-based attendance marking
- Real-time face detection
- Student registration with photos
- Admin panel for managing students
- Student login to view attendance
- GPS location tracking for attendance records
- Automatic attendance marking with location data
- Export attendance records to CSV
- View attendance statistics

## Requirements

- Python 3.7 or higher
- Webcam
- Internet connection (for GPS functionality)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Face-Recognition-Attendance-System.git
cd Face-Recognition-Attendance-System
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## Directory Structure

- `TrainingImage/` - Stores student face images
- `TrainingImageLabel/` - Stores trained model
- `StudentDetails/` - Stores student information
- `Attendance/` - Stores attendance records with GPS data

## Usage

1. Run the main application:
```bash
python AMS_Run.py
```

2. Register new students:
   - Click "Take Images"
   - Enter enrollment number, name, and password
   - Position face in front of camera
   - System will capture multiple images

3. Train the model:
   - Click "Train Images"
   - Wait for training to complete

4. Mark attendance:
   - Click "Automatic Attendance"
   - Enter subject name
   - System will detect faces and mark attendance with GPS location

5. View attendance:
   - Admin can view all attendance records
   - Students can login to view their attendance
   - GPS location data is included in attendance records

## GPS Functionality

The system now includes GPS location tracking:
- Automatically captures location when marking attendance
- Stores latitude, longitude, and address
- Requires internet connection
- Uses IP-based geolocation (approximate location)

## Admin Access

- Username: admin
- Password: admin123

## Student Access

- Use enrollment number and password set during registration

## Notes

- Ensure good lighting for face recognition
- Keep face clearly visible to camera
- Internet connection required for GPS functionality
- GPS location is approximate based on IP address

## Troubleshooting

1. Camera not working:
   - Check if webcam is properly connected
   - Ensure no other application is using the camera

2. Face recognition issues:
   - Ensure good lighting
   - Keep face clearly visible
   - Retrain model if needed

3. GPS not working:
   - Check internet connection
   - Ensure geopy package is installed
   - Check if location services are enabled

## License

This project is licensed under the MIT License - see the LICENSE file for details.

### Sourcerer
<img src="https://avatars.githubusercontent.com/u/84435079?v=4" height="50px" width="50px" alt=""/>

### Code Requirements
- Opencv(`pip install opencv-python`)
- Tkinter(Available in python)
- PIL (`pip install Pillow`)
- Pandas(`pip install pandas`)

### What steps you have to follow??
- Download my Repository 
- Create a `TrainingImage` folder in a project.
- Open a `AMS_Run.py` and change the all paths with your system path
- Run `AMS_Run.py`.

### Project Structure

- After run you need to give your face data to system so enter your ID and name in box than click on `Take Images` button.
- It will collect 200 images of your faces, it save a images in `TrainingImage` folder
- After that we need to train a model(for train a model click on `Train Image` button.
- It will take 5-10 minutes for training(for 10 person data).
- After training click on `Automatic Attendance` ,it can fill attendance by your face using our trained model (model will save in `TrainingImageLabel` )
- it will create `.csv` file of attendance according to time & subject.
- You can store data in database (install wampserver),change the DB name according to your in `AMS_Run.py`.
- `Manually Fill Attendance` Button in UI is for fill a manually attendance (without facce recognition),it's also create a `.csv` and store in a database.

### Screenshots

### Basic UI
<img src="https://github.com/Pragya9ps/Face-Recognition-Attendance-System/blob/main/Screenshot%20(31).png">

### When it Recognises me
<img src="https://github.com/Pragya9ps/Face-Recognition-Attendance-System/blob/main/Screenshot%20(33).png">

### While filling automatic attendance
<img src="https://github.com/Pragya9ps/Face-Recognition-Attendance-System/blob/main/Screenshot%20(38).png">

### Manually attendance filling UI
<img src="https://github.com/Pragya9ps/Face-Recognition-Attendance-System/blob/main/Screenshot%20(35).png">


### Video demo

[Youtube](https://youtu.be/onms2KDOTtY)


### Notes
- It will require high processing power(I have 8 GB RAM)
- Noisy image can reduce the accuracy, so quality of images should be good.


