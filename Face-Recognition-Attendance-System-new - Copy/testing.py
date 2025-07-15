import cv2
import numpy as np
import os

def test_face_recognition():
    try:
        # Check if model exists
        if not os.path.exists('TrainingImageLabel/trainner.yml'):
            print("Error: Model file not found. Please train the model first.")
            return

        # Initialize recognizer
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read('TrainingImageLabel/trainner.yml')
        
        # Initialize face detector
        cascadePath = "haarcascade_frontalface_default.xml"
        if not os.path.exists(cascadePath):
            print("Error: Face cascade file not found.")
            return
            
        faceCascade = cv2.CascadeClassifier(cascadePath)
        font = cv2.FONT_HERSHEY_SIMPLEX

        # Initialize camera
        cam = cv2.VideoCapture(0)
        if not cam.isOpened():
            print("Error: Could not open camera.")
            return

        print("Press 'q' to quit")
        while True:
            ret, im = cam.read()
            if not ret:
                print("Error: Failed to capture image")
                break

            gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(gray, 1.2, 5)
            
            for(x, y, w, h) in faces:
                try:
                    Id, conf = recognizer.predict(gray[y:y+h, x:x+w])
                    if conf < 50:  # Lower confidence means better match
                        cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        cv2.putText(im, f"ID: {Id}", (x, y-10), font, 0.75, (0, 255, 0), 2)
                    else:
                        cv2.rectangle(im, (x, y), (x + w, y + h), (0, 0, 255), 2)
                        cv2.putText(im, "Unknown", (x, y-10), font, 0.75, (0, 0, 255), 2)
                except Exception as e:
                    print(f"Error processing face: {str(e)}")
                    continue

            cv2.imshow('Face Recognition Test', im)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        if 'cam' in locals():
            cam.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    test_face_recognition()
