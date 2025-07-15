import tkinter as tk
from tkinter import *
from tkinter import ttk  # Add this import for Combobox
from tkinter import messagebox
import cv2
import csv
import os
import numpy as np
from PIL import Image, ImageTk
import pandas as pd
from datetime import datetime
import time
import subprocess
import requests
import json
import socket
from tkcalendar import Calendar  # Add this import for calendar widget

# Window is our Main frame of system
window = tk.Tk()
window.title("FAMS-Face Recognition Based Attendance Management System")

window.geometry('1280x720')
window.configure(background='grey80')

# For clear textbox
def clear():
    txt.delete(first=0, last=22)

def clear1():
    txt2.delete(first=0, last=22)

def del_sc1():
    sc1.destroy()

def err_screen():
    global sc1
    sc1 = tk.Tk()
    sc1.geometry('300x100')
    sc1.title('Warning!!')
    sc1.configure(background='grey80')
    Label(sc1, text='Enrollment & Name required!!!', fg='black',
          bg='white', font=('times', 16)).pack()
    Button(sc1, text='OK', command=del_sc1, fg="black", bg="lawn green", width=9,
           height=1, activebackground="Red", font=('times', 15, ' bold ')).place(x=90, y=50)

# Error screen2
def del_sc2():
    sc2.destroy()

def err_screen1():
    global sc2
    sc2 = tk.Tk()
    sc2.geometry('300x100')
    sc2.title('Warning!!')
    sc2.configure(background='grey80')
    Label(sc2, text='Please enter your subject name!!!', fg='black',
          bg='white', font=('times', 16)).pack()
    Button(sc2, text='OK', command=del_sc2, fg="black", bg="lawn green", width=9,
           height=1, activebackground="Red", font=('times', 15, ' bold ')).place(x=90, y=50)

# Function to get GPS coordinates using free API
def get_gps_location():
    try:
        # Try to get location from multiple APIs for better accuracy
        location_data = None
        
        # Try ip-api.com first (more accurate)
        try:
            response = requests.get('http://ip-api.com/json/')
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'success':
                    location_data = {
                        'latitude': data.get('lat', 0.0),
                        'longitude': data.get('lon', 0.0),
                        'address': f"{data.get('city', '')}, {data.get('regionName', '')}, {data.get('country', '')}"
                    }
        except:
            pass

        # If first API fails, try ipapi.co
        if not location_data:
            try:
                response = requests.get('https://ipapi.co/json/')
                if response.status_code == 200:
                    data = response.json()
                    location_data = {
                        'latitude': data.get('latitude', 0.0),
                        'longitude': data.get('longitude', 0.0),
                        'address': f"{data.get('city', '')}, {data.get('region', '')}, {data.get('country_name', '')}"
                    }
            except:
                pass

        # If both APIs fail, try ipinfo.io
        if not location_data:
            try:
                response = requests.get('https://ipinfo.io/json')
                if response.status_code == 200:
                    data = response.json()
                    loc = data.get('loc', '0,0').split(',')
                    location_data = {
                        'latitude': float(loc[0]) if len(loc) > 0 else 0.0,
                        'longitude': float(loc[1]) if len(loc) > 1 else 0.0,
                        'address': f"{data.get('city', '')}, {data.get('region', '')}, {data.get('country', '')}"
                    }
            except:
                pass

        # Validate location data
        if location_data:
            # Check if coordinates are valid
            if (location_data['latitude'] == 0.0 and location_data['longitude'] == 0.0) or \
               (abs(location_data['latitude']) > 90) or (abs(location_data['longitude']) > 180):
                raise Exception("Invalid coordinates received")
            
            # Check if address is meaningful
            if not any(part.strip() for part in location_data['address'].split(',')):
                raise Exception("Invalid address received")
            
            return location_data
        else:
            raise Exception("Could not get location from any API")

    except requests.exceptions.RequestException as e:
        print(f"Network error: {str(e)}")
        return {
            'latitude': 0.0,
            'longitude': 0.0,
            'address': 'Network error - Check internet connection'
        }
    except Exception as e:
        print(f"Error getting location: {str(e)}")
        return {
            'latitude': 0.0,
            'longitude': 0.0,
            'address': f'Location error: {str(e)}'
        }

# For take images for datasets
def take_img():
    l1 = txt.get()
    l2 = txt2.get()
    l3 = txt3.get()  # Get password
    if l1 == '':
        err_screen()
    elif l2 == '':
        err_screen()
    elif l3 == '':  # Check if password is empty
        err_screen()
    else:
        try:
            cam = cv2.VideoCapture(0)
            if not cam.isOpened():
                messagebox.showerror("Error", "Could not open camera. Please check if your camera is connected and not in use by another application.")
                return
                
            detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
            Enrollment = txt.get()
            Name = txt2.get()
            Password = txt3.get()  # Store password
            sampleNum = 0
            
            # Create a named window
            cv2.namedWindow('Frame', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('Frame', 640, 480)
            
            while (True):
                ret, img = cam.read()
                if not ret:
                    messagebox.showerror("Error", "Failed to grab frame from camera")
                    break
                    
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = detector.detectMultiScale(gray, 1.3, 5)
                
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    # incrementing sample number
                    sampleNum = sampleNum + 1
                    # saving the captured face in the dataset folder
                    cv2.imwrite("TrainingImage/ " + Name + "." + Enrollment + '.' + str(sampleNum) + ".jpg",
                                gray[y:y+h, x:x+w])  # Save only the face region
                    print("Images Saved for Enrollment :", Enrollment)
                
                # Display the frame
                cv2.imshow('Frame', img)
                
                # wait for 100 miliseconds
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                # break if the sample number is more than 70
                elif sampleNum > 70:
                    break

            cam.release()
            cv2.destroyAllWindows()
            
            ts = time.time()
            Date = datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
            Time = datetime.fromtimestamp(ts).strftime('%H:%M:%S')
            row = [Enrollment, Name, Date, Time, Password]  # Include password in student details
            
            # Create StudentDetails directory if it doesn't exist
            if not os.path.exists('StudentDetails'):
                os.makedirs('StudentDetails')
                
            with open('StudentDetails/StudentDetails.csv', 'a+') as csvFile:
                writer = csv.writer(csvFile, delimiter=',')
                writer.writerow(row)
                csvFile.close()
                
            res = "Images Saved for Enrollment : " + Enrollment + " Name : " + Name
            Notification.configure(
                text=res, bg="SpringGreen3", width=50, font=('times', 18, 'bold'))
            Notification.place(x=250, y=100)
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            if 'cam' in locals():
                cam.release()
            cv2.destroyAllWindows()

# for choose subject and fill attendance
def get_current_subject():
    try:
        # Get current time and day
        current_time = datetime.now().strftime('%H:%M')
        current_day = datetime.now().strftime('%A')
        
        # Read timetable
        timetable_df = pd.read_csv('Attendance/timetable.csv')
        
        # Filter for current day
        day_schedule = timetable_df[timetable_df['Day'] == current_day]
        
        # Find the current time slot
        for _, row in day_schedule.iterrows():
            start_time, end_time = row['Time_Slot'].split('-')
            if start_time <= current_time <= end_time:
                return row['Subject']
        
        return None
    except Exception as e:
        print(f"Error getting current subject: {str(e)}")
        return None

def subjectchoose():
    def Attf():
        try:
            # Create a new window for statistics filtering
            filter_window = tk.Tk()
            filter_window.title("Attendance Statistics Filter")
            filter_window.geometry('800x600')
            filter_window.configure(background='grey80')
            
            # Search type selection - Fix StringVar initialization
            search_type = tk.StringVar(filter_window)
            search_type.set("monthly")  # Default value
            
            # Create radio buttons for search type
            search_label = Label(filter_window, text="Search by:", bg='grey80', font=('times', 12, 'bold'))
            search_label.place(x=50, y=30)
            
            def on_search_type_change(*args):  # Add *args to handle variable trace
                # Clear previous filter options
                for widget in filter_frame.winfo_children():
                    widget.destroy()
                
                # Show relevant filter options based on selection
                if search_type.get() == "monthly":
                    # Month selection
                    month_label = Label(filter_frame, text="Select Month:", bg='grey80', font=('times', 12))
                    month_label.pack(pady=5)
                    month_dropdown = ttk.Combobox(filter_frame, values=[
                        'January', 'February', 'March', 'April', 'May', 'June',
                        'July', 'August', 'September', 'October', 'November', 'December'
                    ], state='readonly', width=20)
                    month_dropdown.pack(pady=5)
                    month_dropdown.current(datetime.now().month - 1)
                    
                    # Year selection for monthly view
                    year_label = Label(filter_frame, text="Select Year:", bg='grey80', font=('times', 12))
                    year_label.pack(pady=5)
                    current_year = datetime.now().year
                    year_dropdown = ttk.Combobox(filter_frame, 
                        values=[str(year) for year in range(current_year-2, current_year+1)],
                        state='readonly', width=20)
                    year_dropdown.pack(pady=5)
                    year_dropdown.set(str(current_year))
                    
                elif search_type.get() == "yearly":
                    # Year selection
                    year_label = Label(filter_frame, text="Select Year:", bg='grey80', font=('times', 12))
                    year_label.pack(pady=5)
                    current_year = datetime.now().year
                    year_dropdown = ttk.Combobox(filter_frame, 
                        values=[str(year) for year in range(current_year-2, current_year+1)],
                        state='readonly', width=20)
                    year_dropdown.pack(pady=5)
                    year_dropdown.set(str(current_year))
                    
                elif search_type.get() == "subject":
                    # Subject selection
                    subject_label = Label(filter_frame, text="Select Subject:", bg='grey80', font=('times', 12))
                    subject_label.pack(pady=5)
                    
                    # Read subjects from attendance records
                    subjects = []
                    try:
                        if os.path.exists('Attendance/Attendance.csv'):
                            attendance_df = pd.read_csv('Attendance/Attendance.csv')
                            subjects = attendance_df['Subject'].str.strip().unique().tolist()
                            subjects = [s for s in subjects if s]  # Remove empty strings
                    except Exception as e:
                        print(f"Error reading attendance subjects: {str(e)}")
                        subjects = ['Mathematics', 'Physics', 'Chemistry']  # Default subjects
                        
                    subject_dropdown = ttk.Combobox(filter_frame, 
                        values=subjects,
                        state='readonly', width=20)
                    subject_dropdown.pack(pady=5)
                    if subjects:
                        subject_dropdown.current(0)
                    
                elif search_type.get() == "student":
                    # Student enrollment input
                    enrollment_label = Label(filter_frame, text="Enter Enrollment ID:", bg='grey80', font=('times', 12))
                    enrollment_label.pack(pady=5)
                    enrollment_entry = Entry(filter_frame, width=20, font=('times', 12))
                    enrollment_entry.pack(pady=5)
            
            # Create radio buttons
            radio_frame = Frame(filter_window, bg='grey80')
            radio_frame.place(x=50, y=60)
            
            # Create radio buttons with the StringVar
            Radiobutton(radio_frame, text="Monthly", variable=search_type, value="monthly",
                       bg='grey80', command=on_search_type_change).pack(anchor=W)
            Radiobutton(radio_frame, text="Yearly", variable=search_type, value="yearly",
                       bg='grey80', command=on_search_type_change).pack(anchor=W)
            Radiobutton(radio_frame, text="By Subject", variable=search_type, value="subject",
                       bg='grey80', command=on_search_type_change).pack(anchor=W)
            Radiobutton(radio_frame, text="By Student", variable=search_type, value="student",
                       bg='grey80', command=on_search_type_change).pack(anchor=W)
            
            # Frame for dynamic filter options
            filter_frame = Frame(filter_window, bg='grey80')
            filter_frame.place(x=50, y=200)
            
            # Common filters
            common_frame = Frame(filter_window, bg='grey80')
            common_frame.place(x=400, y=50)
            
            # Course Dropdown
            course_label = Label(common_frame, text="Course:", bg='grey80', font=('times', 12))
            course_label.pack(pady=5)
            course_dropdown = ttk.Combobox(common_frame, values=['B.Tech', 'M.Tech', 'MBA'], 
                                         state='readonly', width=20)
            course_dropdown.pack(pady=5)
            course_dropdown.current(0)
            
            # Year Dropdown
            year_label = Label(common_frame, text="Year:", bg='grey80', font=('times', 12))
            year_label.pack(pady=5)
            year_dropdown = ttk.Combobox(common_frame, values=['1', '2', '3', '4'], 
                                       state='readonly', width=20)
            year_dropdown.pack(pady=5)
            year_dropdown.current(0)
            
            # Semester Dropdown
            semester_label = Label(common_frame, text="Semester:", bg='grey80', font=('times', 12))
            semester_label.pack(pady=5)
            semester_dropdown = ttk.Combobox(common_frame, 
                                           values=['1', '2', '3', '4', '5', '6', '7', '8'],
                                           state='readonly', width=20)
            semester_dropdown.pack(pady=5)
            semester_dropdown.current(0)
            
            # Branch Dropdown
            branch_label = Label(common_frame, text="Branch:", bg='grey80', font=('times', 12))
            branch_label.pack(pady=5)
            branch_dropdown = ttk.Combobox(common_frame, 
                                         values=['CSE', 'ECE', 'CSM', 'CIVIL', 'MECHANICAL', 'IT'],
                                         state='readonly', width=20)
            branch_dropdown.pack(pady=5)
            branch_dropdown.current(0)
            
            # Section Dropdown
            section_label = Label(common_frame, text="Section:", bg='grey80', font=('times', 12))
            section_label.pack(pady=5)
            section_dropdown = ttk.Combobox(common_frame, values=['A', 'B'], 
                                          state='readonly', width=20)
            section_dropdown.pack(pady=5)
            section_dropdown.current(0)
            
            def show_filtered_statistics():
                try:
                    # Read attendance data
                    if not os.path.exists('Attendance/Attendance.csv'):
                        messagebox.showerror("Error", "No attendance records found")
                        return
                    
                    attendance_df = pd.read_csv('Attendance/Attendance.csv')
                    if attendance_df.empty:
                        messagebox.showerror("Error", "No attendance records found")
                        return
                    
                    # Clean up the data: Convert relevant columns to string and fill potential NaN
                    attendance_df['Subject'] = attendance_df['Subject'].astype(str).fillna('')
                    attendance_df['Date'] = attendance_df['Date'].astype(str).fillna('')
                    attendance_df['Enrollment'] = attendance_df['Enrollment'].astype(str).fillna('')
                    
                    # Get search type and value
                    search_by = search_type.get()
                    
                    # Apply filter based on search type
                    if search_by == "monthly":
                        month = filter_frame.winfo_children()[1].get()  # Get month
                        year = filter_frame.winfo_children()[3].get()   # Get year
                        month_num = datetime.strptime(month, '%B').month
                        date_filter = f"{year}-{month_num:02d}"
                        filtered_df = attendance_df[attendance_df['Date'].str.startswith(date_filter)]
                    elif search_by == "yearly":
                        year = filter_frame.winfo_children()[1].get()  # Get year
                        filtered_df = attendance_df[attendance_df['Date'].str.startswith(year)]
                    elif search_by == "subject":
                        subject = filter_frame.winfo_children()[1].get()  # Get subject
                        filtered_df = attendance_df[attendance_df['Subject'].str.strip() == subject.strip()]
                    elif search_by == "student":
                        enrollment = filter_frame.winfo_children()[1].get().strip()  # Get enrollment
                        filtered_df = attendance_df[attendance_df['Enrollment'].str.strip() == enrollment.strip()]
                    
                    if filtered_df.empty:
                        messagebox.showinfo("Info", "No records found for the selected filters")
                        return
                    
                    # Calculate statistics
                    stats = []
                    for _, student in filtered_df.groupby('Enrollment'):
                        for subject in student['Subject'].unique():
                            subject_attendance = student[student['Subject'] == subject]
                            total_classes = len(filtered_df[filtered_df['Subject'] == subject])
                            if total_classes > 0:  # Avoid division by zero
                                stats.append({
                                    'Name': student['Name'].iloc[0],
                                    'Enrollment': student['Enrollment'].iloc[0],
                                    'Subject': subject,
                                    'Classes_Attended': len(subject_attendance),
                                    'Total_Classes': total_classes,
                                    'Attendance_Percentage': f"{(len(subject_attendance) / total_classes * 100):.2f}%"
                                })
                    
                    if not stats:
                        messagebox.showinfo("Info", "No attendance records found for the selected filters")
                        return
                    
                    # Create and show statistics window
                    stats_window = tk.Tk()
                    stats_window.title("Attendance Statistics")
                    stats_window.configure(background='grey80')
                    
                    # Create headers
                    headers = ['Name', 'Enrollment', 'Subject', 'Classes Attended', 'Total Classes', 'Attendance %']
                    for c, header in enumerate(headers):
                        label = tk.Label(stats_window, text=header, width=15, height=2, fg="black", bg="grey",
                                font=('times', 12, 'bold'))
                        label.grid(row=0, column=c, padx=5, pady=5)
                    
                    # Display data
                    for r, stat in enumerate(stats, 1):
                        for c, (key, value) in enumerate(stat.items(), 0):
                            label = tk.Label(stats_window, text=str(value), width=15, height=1, fg="black",
                                    bg="white", font=('times', 10))
                            label.grid(row=r, column=c, padx=5, pady=2)
                    
                    # Add export button
                    def export_to_csv():
                        stats_df = pd.DataFrame(stats)
                        export_path = os.path.join("Attendance", "Filtered_Statistics.csv")
                        stats_df.to_csv(export_path, index=False)
                        messagebox.showinfo("Success", f"Statistics exported to {export_path}")
                    
                    export_btn = tk.Button(stats_window, text="Export to CSV", command=export_to_csv,
                                         fg="black", bg="SkyBlue1", width=20, height=2,
                                         activebackground="white", font=('times', 12, 'bold'))
                    export_btn.grid(row=len(stats) + 1, column=0, columnspan=6, pady=10)
                    
                    stats_window.mainloop()
                    
                except Exception as e:
                    print(f"Error in show_filtered_statistics: {str(e)}")
                    messagebox.showerror("Error", f"An error occurred: {str(e)}")
            
            # Show Statistics Button
            show_stats_btn = Button(filter_window, text="Show Statistics", command=show_filtered_statistics,
                                  fg="black", bg="lawn green", width=20, height=2,
                                  activebackground="Red", font=('times', 15, ' bold '))
            show_stats_btn.place(x=400, y=400)
            
            # Initialize with monthly view
            on_search_type_change()
            
            filter_window.mainloop()
        except Exception as e:
            print(f"Error in Attf: {str(e)}")  # Add print for debugging
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def submit_details():
        try:
            # Get all the selected values
            selected_date = cal.get_date()
            # Convert the date to YYYY-MM-DD format
            formatted_date = datetime.strptime(selected_date, '%m/%d/%y').strftime('%Y-%m-%d')
            selected_course = course_dropdown.get()
            selected_year = year_dropdown.get()
            selected_semester = semester_dropdown.get()
            selected_branch = branch_dropdown.get()
            selected_section = section_dropdown.get()
            
            # Get the current subject based on time
            sub = get_current_subject()
            if sub is None:
                messagebox.showerror("Error", "No class scheduled at this time!")
                return
                
            # Save the details to a CSV file
            details_file = os.path.join("Attendance", "Attendance_Details.csv")
            if not os.path.exists(details_file):
                with open(details_file, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(['Date', 'Course', 'Year', 'Semester', 'Branch', 'Section', 'Subject'])
            
            with open(details_file, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    formatted_date,
                    selected_course,
                    selected_year,
                    selected_semester,
                    selected_branch,
                    selected_section,
                    sub
                ])
            
            # Close the details window
            details_window.destroy()
            
            # Start the attendance process
            Fill_Attendance(sub)
            
        except Exception as e:
            print(f"Error in submit_details: {str(e)}")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    # Create a new window for details input
    details_window = tk.Tk()
    details_window.title("Attendance Details")
    details_window.geometry('800x600')
    details_window.configure(background='grey80')
    
    # Calendar
    cal_label = Label(details_window, text="Select Date:", bg='grey80', font=('times', 12, 'bold'))
    cal_label.place(x=50, y=20)
    cal = Calendar(details_window, selectmode='day', year=datetime.now().year, 
                  month=datetime.now().month, day=datetime.now().day)
    cal.place(x=50, y=50)
    
    # Course Dropdown
    course_label = Label(details_window, text="Select Course:", bg='grey80', font=('times', 12, 'bold'))
    course_label.place(x=400, y=50)
    course_dropdown = ttk.Combobox(details_window, values=['B.Tech', 'M.Tech', 'MBA'], state='readonly', width=20)
    course_dropdown.place(x=400, y=80)
    course_dropdown.current(0)  # Set first item as default
    
    # Year Dropdown
    year_label = Label(details_window, text="Select Year:", bg='grey80', font=('times', 12, 'bold'))
    year_label.place(x=400, y=120)
    year_dropdown = ttk.Combobox(details_window, values=['1', '2', '3', '4'], state='readonly', width=20)
    year_dropdown.place(x=400, y=150)
    year_dropdown.current(0)  # Set first item as default
    
    # Semester Dropdown
    semester_label = Label(details_window, text="Select Semester:", bg='grey80', font=('times', 12, 'bold'))
    semester_label.place(x=400, y=190)
    semester_dropdown = ttk.Combobox(details_window, values=['1', '2', '3', '4', '5', '6', '7', '8'], state='readonly', width=20)
    semester_dropdown.place(x=400, y=220)
    semester_dropdown.current(0)  # Set first item as default
    
    # Branch Dropdown
    branch_label = Label(details_window, text="Select Branch:", bg='grey80', font=('times', 12, 'bold'))
    branch_label.place(x=400, y=260)
    branch_dropdown = ttk.Combobox(details_window, values=['CSE', 'ECE', 'CSM', 'CIVIL', 'MECHANICAL', 'IT'], state='readonly', width=20)
    branch_dropdown.place(x=400, y=290)
    branch_dropdown.current(0)  # Set first item as default
    
    # Section Dropdown
    section_label = Label(details_window, text="Select Section:", bg='grey80', font=('times', 12, 'bold'))
    section_label.place(x=400, y=330)
    section_dropdown = ttk.Combobox(details_window, values=['A', 'B'], state='readonly', width=20)
    section_dropdown.place(x=400, y=360)
    section_dropdown.current(0)  # Set first item as default
    
    # Submit Button
    submit_btn = Button(details_window, text="Submit", command=submit_details,
                       fg="black", bg="lawn green", width=20, height=2,
                       activebackground="Red", font=('times', 15, ' bold '))
    submit_btn.place(x=400, y=420)
    
    # View Statistics Button
    view_stats_btn = Button(details_window, text="View Statistics", command=Attf,
                           fg="black", bg="lawn green", width=20, height=2,
                           activebackground="Red", font=('times', 15, ' bold '))
    view_stats_btn.place(x=400, y=500)
    
    details_window.mainloop()

def admin_panel():
    win = tk.Tk()
    win.title("LogIn")
    win.geometry('880x420')
    win.configure(background='grey80')

    def log_in():
        username = un_entr.get()
        password = pw_entr.get()

        if username == 'admin':
            if password == 'admin123':
                win.destroy()
                show_admin_options()
            else:
                valid = 'Incorrect ID or Password'
                Nt.configure(text=valid, bg="red", fg="white",
                             width=38, font=('times', 19, 'bold'))
                Nt.place(x=120, y=350)
        else:
            valid = 'Incorrect ID or Password'
            Nt.configure(text=valid, bg="red", fg="white",
                         width=38, font=('times', 19, 'bold'))
            Nt.place(x=120, y=350)

    def show_admin_options():
        admin_win = tk.Tk()
        admin_win.title("Admin Panel")
        admin_win.geometry('880x420')
        admin_win.configure(background='grey80')

        def view_student_details():
            try:
                if not os.path.exists('StudentDetails/StudentDetails.csv'):
                    messagebox.showerror("Error", "No student details found")
                    return

                # Read the CSV file
                student_df = pd.read_csv('StudentDetails/StudentDetails.csv', on_bad_lines='skip')
                if student_df.empty:
                    messagebox.showerror("Error", "No student records found")
                    return

                # Create a new window for student details
                details_win = tk.Tk()
                details_win.title("Student Details")
                details_win.configure(background='grey80')

                # Create a main frame
                main_frame = Frame(details_win, bg='grey80')
                main_frame.pack(fill=BOTH, expand=1)

                # Create a Canvas
                my_canvas = Canvas(main_frame, bg='grey80')
                my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

                # Add a Scrollbar to the Canvas
                my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
                my_scrollbar.pack(side=RIGHT, fill=Y)

                # Configure the Canvas
                my_canvas.configure(yscrollcommand=my_scrollbar.set)
                my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion = my_canvas.bbox("all")))

                # Create another frame inside the canvas to hold the content
                second_frame = Frame(my_canvas, bg='grey80')

                # Add that new frame to a window in the canvas
                my_canvas.create_window((0,0), window=second_frame, anchor="nw")

                # Create headers
                headers = ['Enrollment', 'Name', 'Registration Date', 'Registration Time', 'Action']
                for col, header in enumerate(headers):
                    label = tk.Label(second_frame, text=header, width=20, height=2,
                                   fg="black", bg="grey", font=('times', 12, 'bold'))
                    label.grid(row=0, column=col, padx=5, pady=5)

                # Function to delete a student
                def delete_student(enrollment):
                    try:
                        # Confirm deletion
                        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete student with enrollment {enrollment}?"):
                            # Remove from DataFrame
                            student_df.drop(student_df[student_df['Enrollment'] == enrollment].index, inplace=True)
                            # Save updated DataFrame
                            student_df.to_csv('StudentDetails/StudentDetails.csv', index=False)
                            # Refresh the window
                            details_win.destroy()
                            view_student_details()
                    except Exception as e:
                        messagebox.showerror("Error", f"Failed to delete student: {str(e)}")

                # Display student data
                for row_idx, row in student_df.iterrows():
                    # Enrollment
                    tk.Label(second_frame, text=str(row['Enrollment']), width=20, height=2,
                           fg="black", bg="white", font=('times', 11)).grid(row=row_idx+1, column=0, padx=5, pady=2)
                    # Name
                    tk.Label(second_frame, text=str(row['Name']), width=20, height=2,
                           fg="black", bg="white", font=('times', 11)).grid(row=row_idx+1, column=1, padx=5, pady=2)
                    # Date
                    tk.Label(second_frame, text=str(row['Date']), width=20, height=2,
                           fg="black", bg="white", font=('times', 11)).grid(row=row_idx+1, column=2, padx=5, pady=2)
                    # Time
                    tk.Label(second_frame, text=str(row['Time']), width=20, height=2,
                           fg="black", bg="white", font=('times', 11)).grid(row=row_idx+1, column=3, padx=5, pady=2)
                    # Delete Button
                    delete_btn = tk.Button(second_frame, text="Delete", 
                                         command=lambda e=row['Enrollment']: delete_student(e),
                                         fg="white", bg="red", width=10, height=1,
                                         activebackground="white", font=('times', 10, 'bold'))
                    delete_btn.grid(row=row_idx+1, column=4, padx=5, pady=2)

                # Add export button
                def export_to_csv():
                    try:
                        export_path = os.path.join("StudentDetails", "Exported_StudentDetails.csv")
                        student_df.to_csv(export_path, index=False)
                        messagebox.showinfo("Success", f"Student details exported to {export_path}")
                    except Exception as e:
                        messagebox.showerror("Error", f"Failed to export: {str(e)}")

                # Place the export button within the second_frame
                export_btn = tk.Button(second_frame, text="Export to CSV", command=export_to_csv,
                                     fg="black", bg="SkyBlue1", width=20, height=2,
                                     activebackground="white", font=('times', 12, 'bold'))
                export_btn.grid(row=len(student_df)+1, column=0, columnspan=5, pady=10)

                details_win.mainloop()

            except Exception as e:
                print(f"Error in view_student_details: {str(e)}")
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

        def view_attendance_stats():
            try:
                # Create a new window for statistics filtering
                filter_window = tk.Tk()
                filter_window.title("Attendance Statistics Filter")
                filter_window.geometry('800x600')
                filter_window.configure(background='grey80')
                
                # Search type selection
                search_type = tk.StringVar(filter_window)
                search_type.set("monthly")  # Default value
                
                # Create radio buttons for search type
                search_label = Label(filter_window, text="Search by:", bg='grey80', font=('times', 12, 'bold'))
                search_label.place(x=50, y=30)
                
                def on_search_type_change():
                    # Clear previous filter options
                    for widget in filter_frame.winfo_children():
                        widget.destroy()
                    
                    # Show relevant filter options based on selection
                    if search_type.get() == "monthly":
                        # Month selection
                        month_label = Label(filter_frame, text="Select Month:", bg='grey80', font=('times', 12))
                        month_label.pack(pady=5)
                        month_dropdown = ttk.Combobox(filter_frame, values=[
                            'January', 'February', 'March', 'April', 'May', 'June',
                            'July', 'August', 'September', 'October', 'November', 'December'
                        ], state='readonly', width=20)
                        month_dropdown.pack(pady=5)
                        month_dropdown.current(datetime.now().month - 1)
                        
                        # Year selection for monthly view
                        year_label = Label(filter_frame, text="Select Year:", bg='grey80', font=('times', 12))
                        year_label.pack(pady=5)
                        current_year = datetime.now().year
                        year_dropdown = ttk.Combobox(filter_frame, 
                            values=[str(year) for year in range(current_year-2, current_year+1)],
                            state='readonly', width=20)
                        year_dropdown.pack(pady=5)
                        year_dropdown.set(str(current_year))
                        
                    elif search_type.get() == "yearly":
                        # Year selection
                        year_label = Label(filter_frame, text="Select Year:", bg='grey80', font=('times', 12))
                        year_label.pack(pady=5)
                        current_year = datetime.now().year
                        year_dropdown = ttk.Combobox(filter_frame, 
                            values=[str(year) for year in range(current_year-2, current_year+1)],
                            state='readonly', width=20)
                        year_dropdown.pack(pady=5)
                        year_dropdown.set(str(current_year))
                        
                    elif search_type.get() == "subject":
                        # Subject selection
                        subject_label = Label(filter_frame, text="Select Subject:", bg='grey80', font=('times', 12))
                        subject_label.pack(pady=5)
                        
                        # Read subjects from attendance records
                        subjects = []
                        try:
                            if os.path.exists('Attendance/Attendance.csv'):
                                attendance_df = pd.read_csv('Attendance/Attendance.csv')
                                subjects = attendance_df['Subject'].str.strip().unique().tolist()
                                subjects = [s for s in subjects if s]  # Remove empty strings
                        except Exception as e:
                            print(f"Error reading attendance subjects: {str(e)}")
                            subjects = ['Mathematics', 'Physics', 'Chemistry']  # Default subjects
                            
                        subject_dropdown = ttk.Combobox(filter_frame, 
                            values=subjects,
                            state='readonly', width=20)
                        subject_dropdown.pack(pady=5)
                        if subjects:
                            subject_dropdown.current(0)
                        
                    elif search_type.get() == "student":
                        # Student enrollment input
                        enrollment_label = Label(filter_frame, text="Enter Enrollment ID:", bg='grey80', font=('times', 12))
                        enrollment_label.pack(pady=5)
                        enrollment_entry = Entry(filter_frame, width=20, font=('times', 12))
                        enrollment_entry.pack(pady=5)
                
                # Create radio buttons
                radio_frame = Frame(filter_window, bg='grey80')
                radio_frame.place(x=50, y=60)
                
                Radiobutton(radio_frame, text="Monthly", variable=search_type, value="monthly",
                           bg='grey80', command=on_search_type_change).pack(anchor=W)
                Radiobutton(radio_frame, text="Yearly", variable=search_type, value="yearly",
                           bg='grey80', command=on_search_type_change).pack(anchor=W)
                Radiobutton(radio_frame, text="By Subject", variable=search_type, value="subject",
                           bg='grey80', command=on_search_type_change).pack(anchor=W)
                Radiobutton(radio_frame, text="By Student", variable=search_type, value="student",
                           bg='grey80', command=on_search_type_change).pack(anchor=W)
                
                # Frame for dynamic filter options
                filter_frame = Frame(filter_window, bg='grey80')
                filter_frame.place(x=50, y=200)
                
                def show_filtered_statistics():
                    try:
                        # Read attendance data
                        if not os.path.exists('Attendance/Attendance.csv'):
                            messagebox.showerror("Error", "No attendance records found")
                            return
                        
                        attendance_df = pd.read_csv('Attendance/Attendance.csv')
                        if attendance_df.empty:
                            messagebox.showerror("Error", "No attendance records found")
                            return
                        
                        # Clean up the data: Convert relevant columns to string and fill potential NaN
                        attendance_df['Subject'] = attendance_df['Subject'].astype(str).fillna('')
                        attendance_df['Date'] = attendance_df['Date'].astype(str).fillna('')
                        attendance_df['Enrollment'] = attendance_df['Enrollment'].astype(str).fillna('')
                        
                        # Get search type and value
                        search_by = search_type.get()
                        
                        # Apply filter based on search type
                        if search_by == "monthly":
                            month = filter_frame.winfo_children()[1].get()  # Get month
                            year = filter_frame.winfo_children()[3].get()   # Get year
                            month_num = datetime.strptime(month, '%B').month
                            date_filter = f"{year}-{month_num:02d}"
                            filtered_df = attendance_df[attendance_df['Date'].str.startswith(date_filter)]
                        elif search_by == "yearly":
                            year = filter_frame.winfo_children()[1].get()  # Get year
                            filtered_df = attendance_df[attendance_df['Date'].str.startswith(year)]
                        elif search_by == "subject":
                            subject = filter_frame.winfo_children()[1].get()  # Get subject
                            filtered_df = attendance_df[attendance_df['Subject'].str.strip() == subject.strip()]
                        elif search_by == "student":
                            enrollment = filter_frame.winfo_children()[1].get().strip()  # Get enrollment
                            filtered_df = attendance_df[attendance_df['Enrollment'].str.strip() == enrollment.strip()]
                        
                        if filtered_df.empty:
                            messagebox.showinfo("Info", "No records found for the selected filters")
                            return
                        
                        # Calculate statistics
                        stats = []
                        for _, student in filtered_df.groupby('Enrollment'):
                            for subject in student['Subject'].unique():
                                subject_attendance = student[student['Subject'] == subject]
                                total_classes = len(filtered_df[filtered_df['Subject'] == subject])
                                if total_classes > 0:  # Avoid division by zero
                                    stats.append({
                                        'Name': student['Name'].iloc[0],
                                        'Enrollment': student['Enrollment'].iloc[0],
                                        'Subject': subject,
                                        'Classes_Attended': len(subject_attendance),
                                        'Total_Classes': total_classes,
                                        'Attendance_Percentage': f"{(len(subject_attendance) / total_classes * 100):.2f}%"
                                    })
                        
                        if not stats:
                            messagebox.showinfo("Info", "No attendance records found for the selected filters")
                            return
                        
                        # Create and show statistics window
                        stats_window = tk.Tk()
                        stats_window.title("Attendance Statistics")
                        stats_window.configure(background='grey80')
                        
                        # Create headers
                        headers = ['Name', 'Enrollment', 'Subject', 'Classes Attended', 'Total Classes', 'Attendance %']
                        for c, header in enumerate(headers):
                            label = tk.Label(stats_window, text=header, width=15, height=2, fg="black", bg="grey",
                                    font=('times', 12, 'bold'))
                            label.grid(row=0, column=c, padx=5, pady=5)
                        
                        # Display data
                        for r, stat in enumerate(stats, 1):
                            for c, (key, value) in enumerate(stat.items(), 0):
                                label = tk.Label(stats_window, text=str(value), width=15, height=1, fg="black",
                                        bg="white", font=('times', 10))
                                label.grid(row=r, column=c, padx=5, pady=2)
                        
                        # Add export button
                        def export_to_csv():
                            stats_df = pd.DataFrame(stats)
                            export_path = os.path.join("Attendance", "Filtered_Statistics.csv")
                            stats_df.to_csv(export_path, index=False)
                            messagebox.showinfo("Success", f"Statistics exported to {export_path}")
                        
                        export_btn = tk.Button(stats_window, text="Export to CSV", command=export_to_csv,
                                             fg="black", bg="SkyBlue1", width=20, height=2,
                                             activebackground="white", font=('times', 12, 'bold'))
                        export_btn.grid(row=len(stats) + 1, column=0, columnspan=6, pady=10)
                        
                        stats_window.mainloop()
                        
                    except Exception as e:
                        print(f"Error in show_filtered_statistics: {str(e)}")
                        messagebox.showerror("Error", f"An error occurred: {str(e)}")
                
                # Show Statistics Button
                show_stats_btn = Button(filter_window, text="Show Statistics", command=show_filtered_statistics,
                                      fg="black", bg="lawn green", width=20, height=2,
                                      activebackground="Red", font=('times', 15, ' bold '))
                show_stats_btn.place(x=400, y=400)
                
                # Initialize with monthly view
                on_search_type_change()
                
                filter_window.mainloop()
            
            except Exception as e:
                print(f"Error in view_attendance_stats: {str(e)}")
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

        # Create buttons for admin options
        view_students_btn = tk.Button(admin_win, text="View Student Details", command=view_student_details,
                                     fg="black", bg="SkyBlue1", width=20, height=2,
                                     activebackground="white", font=('times', 15, 'bold'))
        view_students_btn.place(x=100, y=100)

        view_stats_btn = tk.Button(admin_win, text="View Attendance Statistics", command=view_attendance_stats,
                                  fg="black", bg="SkyBlue1", width=20, height=2,
                                  activebackground="white", font=('times', 15, 'bold'))
        view_stats_btn.place(x=400, y=100)

        admin_win.mainloop()

    Nt = tk.Label(win, text="Attendance filled Successfully", bg="Green", fg="white", width=40,
                  height=2, font=('times', 19, 'bold'))

    un = tk.Label(win, text="Enter username : ", width=15, height=2, fg="black", bg="grey",
                  font=('times', 15, ' bold '))
    un.place(x=30, y=50)

    pw = tk.Label(win, text="Enter password : ", width=15, height=2, fg="black", bg="grey",
                  font=('times', 15, ' bold '))
    pw.place(x=30, y=150)

    def c00():
        un_entr.delete(first=0, last=22)

    un_entr = tk.Entry(win, width=20, bg="white", fg="black",
                       font=('times', 23))
    un_entr.place(x=290, y=55)

    def c11():
        pw_entr.delete(first=0, last=22)

    pw_entr = tk.Entry(win, width=20, show="*", bg="white",
                       fg="black", font=('times', 23))
    pw_entr.place(x=290, y=155)

    c0 = tk.Button(win, text="Clear", command=c00, fg="white", bg="black", width=10, height=1,
                   activebackground="white", font=('times', 15, ' bold '))
    c0.place(x=690, y=55)

    c1 = tk.Button(win, text="Clear", command=c11, fg="white", bg="black", width=10, height=1,
                   activebackground="white", font=('times', 15, ' bold '))
    c1.place(x=690, y=155)

    Login = tk.Button(win, text="LogIn", fg="black", bg="SkyBlue1", width=20,
                      height=2,
                      activebackground="Red", command=log_in, font=('times', 15, ' bold '))
    Login.place(x=290, y=250)
    win.mainloop()

def student_login():
    win = tk.Tk()
    win.title("Student Login")
    win.geometry('880x420')
    win.configure(background='grey80')

    def log_in():
        enrollment = un_entr.get()
        password = pw_entr.get()

        if enrollment == "" or password == "":
            messagebox.showerror("Error", "Please enter both enrollment number and password")
            return

        try:
            # Read student details with proper error handling
            if not os.path.exists('StudentDetails/StudentDetails.csv'):
                messagebox.showerror("Error", "Student details file not found")
                return

            # Read CSV with error handling for malformed lines
            student_df = pd.read_csv('StudentDetails/StudentDetails.csv', on_bad_lines='skip')
            
            # Ensure the DataFrame has the required columns
            required_columns = ['Enrollment', 'Name', 'Password']
            if not all(col in student_df.columns for col in required_columns):
                messagebox.showerror("Error", "Student details file is not properly formatted")
                return

            # Check if enrollment exists
            entered_enrollment = enrollment.lstrip('0').strip()
            student_df['Enrollment_stripped'] = student_df['Enrollment'].astype(str).str.lstrip('0').str.strip()
            entered_password = password.strip()
            if entered_enrollment in student_df['Enrollment_stripped'].values:
                idx = student_df[student_df['Enrollment_stripped'] == entered_enrollment].index[0]
                stored_password = str(student_df.loc[idx, 'Password']).strip()
                if entered_password == stored_password:
                    win.destroy()
                    show_student_attendance(student_df.loc[idx, 'Enrollment'])
                else:
                    messagebox.showerror("Error", "Incorrect Password")
            else:
                messagebox.showerror("Error", "Enrollment not found")
        except Exception as e:
            messagebox.showerror("Error", f"Error during login: {str(e)}")

    def show_student_attendance(enrollment):
        try:
            # Read attendance data
            attendance_df = pd.read_csv('Attendance/Attendance.csv')
            student_df = pd.read_csv('StudentDetails/StudentDetails.csv')
            # Get student details
            student = student_df[student_df['Enrollment'].astype(str).str.lstrip('0').str.strip() == str(enrollment).lstrip('0').strip()].iloc[0]
            # Calculate total classes per subject
            total_classes = attendance_df.groupby('Subject').size()
            # Calculate attendance for this student
            student_attendance = attendance_df[attendance_df['Enrollment'].astype(str).str.lstrip('0').str.strip() == str(enrollment).lstrip('0').strip()]
            attendance_stats = []
            for subject in total_classes.index:
                classes_attended = len(student_attendance[student_attendance['Subject'] == subject])
                total = total_classes[subject]
                percentage = (classes_attended / total * 100) if total > 0 else 0
                attendance_stats.append({
                    'Subject': subject,
                    'Classes_Attended': classes_attended,
                    'Total_Classes': total,
                    'Attendance_Percentage': f"{percentage:.2f}%"
                })
            # Display the statistics
            root = tk.Tk()
            root.title(f"Attendance Statistics - {student['Name']}")
            root.configure(background='grey80')
            # Display student info using grid
            tk.Label(root, text=f"Name: {student['Name']}", font=('times', 14, 'bold'), bg='grey80').grid(row=0, column=0, columnspan=2, pady=(10,0))
            tk.Label(root, text=f"Enrollment: {enrollment}", font=('times', 14, 'bold'), bg='grey80').grid(row=1, column=0, columnspan=2, pady=(0,10))
            row_offset = 2
            # Create headers
            headers = ['Subject', 'Classes Attended', 'Total Classes', 'Attendance %']
            for c, header in enumerate(headers):
                label = tk.Label(root, text=header, width=15, height=2, fg="black", bg="grey",
                                font=('times', 12, 'bold'))
                label.grid(row=row_offset, column=c, padx=5, pady=5)
            # Display data
            for r, stat in enumerate(attendance_stats, 1):
                for c, (key, value) in enumerate(stat.items(), 0):
                    label = tk.Label(root, text=str(value), width=15, height=1, fg="black",
                                    bg="white", font=('times', 10))
                    label.grid(row=row_offset + r, column=c, padx=5, pady=2)
            root.mainloop()
        except Exception as e:
            error_win = tk.Tk()
            error_win.title("Error")
            error_win.geometry('300x100')
            error_win.configure(background='grey80')
            Label(error_win, text=f'Error: {str(e)}', fg='red',
                  bg='white', font=('times', 12)).pack()
            Button(error_win, text='OK', command=error_win.destroy, fg="black", bg="lawn green",
                   width=9, height=1, activebackground="Red",
                   font=('times', 12, 'bold')).place(x=90, y=50)
            error_win.mainloop()

    Nt = tk.Label(win, text="", bg="Green", fg="white", width=40,
                  height=2, font=('times', 19, 'bold'))

    un = tk.Label(win, text="Enter Enrollment : ", width=15, height=2, fg="black", bg="grey",
                  font=('times', 15, ' bold '))
    un.place(x=30, y=50)

    pw = tk.Label(win, text="Enter Password : ", width=15, height=2, fg="black", bg="grey",
                  font=('times', 15, ' bold '))
    pw.place(x=30, y=150)

    def c00():
        un_entr.delete(first=0, last=22)

    un_entr = tk.Entry(win, width=20, bg="white", fg="black",
                       font=('times', 23))
    un_entr.place(x=290, y=55)

    def c11():
        pw_entr.delete(first=0, last=22)

    pw_entr = tk.Entry(win, width=20, show="*", bg="white",
                       fg="black", font=('times', 23))
    pw_entr.place(x=290, y=155)

    c0 = tk.Button(win, text="Clear", command=c00, fg="white", bg="black", width=10, height=1,
                   activebackground="white", font=('times', 15, ' bold '))
    c0.place(x=690, y=55)

    c1 = tk.Button(win, text="Clear", command=c11, fg="white", bg="black", width=10, height=1,
                   activebackground="white", font=('times', 15, ' bold '))
    c1.place(x=690, y=155)

    Login = tk.Button(win, text="LogIn", fg="black", bg="SkyBlue1", width=20,
                      height=2,
                      activebackground="Red", command=log_in, font=('times', 15, ' bold '))
    Login.place(x=290, y=250)
    win.mainloop()

# For train the model
def trainimg():
    try:
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        global detector
        detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        
        # Check if cascade file exists
        if not os.path.exists("haarcascade_frontalface_default.xml"):
            Notification.configure(text="Error: haarcascade_frontalface_default.xml not found", 
                                bg="red", width=50, font=('times', 18, 'bold'))
            Notification.place(x=250, y=100)
            return

        try:
            print("Starting training process...")
            print("Getting images and labels...")
            global faces, Id
            faces, Id = getImagesAndLabels("TrainingImage")
            print(f"Found {len(faces)} faces and {len(Id)} labels")
            
            if len(faces) == 0:
                Notification.configure(text="No faces found in training images!", 
                                    bg="red", width=50, font=('times', 18, 'bold'))
                Notification.place(x=250, y=100)
                return
                
            print("Training model...")
            recognizer.train(faces, np.array(Id))
            print("Model training completed")
            
            # Ensure directory exists
            if not os.path.exists("TrainingImageLabel"):
                os.makedirs("TrainingImageLabel")
                
            print("Saving model...")
            recognizer.save("TrainingImageLabel/Trainner.yml")
            print("Model saved successfully")
            
            res = "Model Trained Successfully!"
            Notification.configure(text=res, bg="SpringGreen3",
                                width=50, font=('times', 18, 'bold'))
            Notification.place(x=250, y=100)
            
        except Exception as e:
            print(f"Error during training: {str(e)}")
            Notification.configure(text=f"Training Error: {str(e)}", 
                                bg="red", width=50, font=('times', 18, 'bold'))
            Notification.place(x=250, y=100)
            
    except Exception as e:
        print(f"Error initializing training: {str(e)}")
        Notification.configure(text=f"Initialization Error: {str(e)}", 
                            bg="red", width=50, font=('times', 18, 'bold'))
        Notification.place(x=250, y=100)

def getImagesAndLabels(path):
    try:
        # Get all file paths
        imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
        faceSamples = []
        Ids = []
        
        print(f"Found {len(imagePaths)} images in {path}")
        
        for imagePath in imagePaths:
            try:
                # Load and convert image
                print(f"Processing image: {imagePath}")
                pilImage = Image.open(imagePath).convert('L')
                imageNp = np.array(pilImage, 'uint8')
                
                # Get ID from filename
                Id = int(os.path.split(imagePath)[-1].split(".")[1])
                
                # Detect faces
                faces = detector.detectMultiScale(
                    imageNp,
                    scaleFactor=1.1,
                    minNeighbors=4,
                    minSize=(30, 30)
                )
                
                print(f"Found {len(faces)} faces in image {imagePath}")
                
                # Store face samples and IDs
                for (x, y, w, h) in faces:
                    faceSamples.append(imageNp[y:y + h, x:x + w])
                    Ids.append(Id)
                    
            except Exception as e:
                print(f"Error processing image {imagePath}: {str(e)}")
                continue
                
        print(f"Total faces collected: {len(faceSamples)}")
        print(f"Total IDs collected: {len(Ids)}")
        return faceSamples, Ids
        
    except Exception as e:
        print(f"Error in getImagesAndLabels: {str(e)}")
        return [], []

def Fill_Attendance(subject):
    # Create Attendance directory if it doesn't exist
    if not os.path.exists("Attendance"):
        os.makedirs("Attendance")
    
    # Create Images directory if it doesn't exist
    if not os.path.exists("Attendance/Images"):
        os.makedirs("Attendance/Images")

    # Initialize camera
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        messagebox.showerror("Error", "Could not open camera")
        return
        
    # Create or load attendance file
    attendance_file = os.path.join("Attendance", "Attendance.csv")
    if not os.path.exists(attendance_file):
        with open(attendance_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Enrollment', 'Name', 'Date', 'Time', 'Subject', 'Latitude', 'Longitude', 'Location'])

    # Load existing attendance data
    attendance_data = []
    if os.path.exists(attendance_file):
        with open(attendance_file, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            attendance_data = list(reader)

    # Load face recognition model
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    try:
        recognizer.read("TrainingImageLabel/Trainner.yml")
    except:
        messagebox.showerror("Error", "Model not found, Please train model")
        cam.release()
        cv2.destroyAllWindows()
        return

    hcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(hcascadePath)
    
    # Load student details with error handling
    try:
        student_df = pd.read_csv("StudentDetails/StudentDetails.csv", on_bad_lines='skip')
        if student_df.empty:
            messagebox.showerror("Error", "No student details found")
            cam.release()
            cv2.destroyAllWindows()
            return
    except Exception as e:
        messagebox.showerror("Error", f"Error reading student details: {str(e)}")
        cam.release()
        cv2.destroyAllWindows()
        return

    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names = ['Enrollment', 'Name', 'Date', 'Time', 'Subject', 'Latitude', 'Longitude', 'Location']
    attendance = pd.DataFrame(columns=col_names)

    # Get current date and time
    now = datetime.now()
    date = now.strftime('%Y-%m-%d')
    time = now.strftime('%H:%M:%S')

    # Get GPS location once at the start
    gps_data = get_gps_location()
    if gps_data['latitude'] == 0.0 and gps_data['longitude'] == 0.0:
        retry = messagebox.askretrycancel("Warning", 
            "Could not get GPS location. Would you like to retry?\n\n" +
            "Make sure you have a stable internet connection.")
        if retry:
            gps_data = get_gps_location()
            if gps_data['latitude'] == 0.0 and gps_data['longitude'] == 0.0:
                messagebox.showwarning("Warning", 
                    "Still could not get GPS location. Attendance will be marked without location data.")
    else:
        # Show location confirmation
        messagebox.showinfo("Location Detected", 
            f"Location detected:\n{gps_data['address']}\n\n" +
            f"Latitude: {gps_data['latitude']}\n" +
            f"Longitude: {gps_data['longitude']}")

    # Keep track of students who have already been marked present today
    marked_students = set()

    # Process video frames
    while True:
        ret, im = cam.read()
        if not ret:
            messagebox.showerror("Error", "Failed to capture image from camera")
            break

        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        # Adjust parameters for better face detection
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,  # Reduced from 1.2 for better detection
            minNeighbors=3,   # Reduced from 5 for more sensitive detection
            minSize=(30, 30)  # Add minimum size for detected faces
        )

        # Add debug information
        cv2.putText(im, f"Detected faces: {len(faces)}", (10, 30), font, 1, (255, 255, 255), 2)
        
        for (x, y, w, h) in faces:
            enrollment, conf = recognizer.predict(gray[y:y + h, x:x + w])
            enrollment_str = str(enrollment).lstrip('0').strip()
            student_df['Enrollment_stripped'] = student_df['Enrollment'].astype(str).str.lstrip('0').str.strip()
            match = student_df[student_df['Enrollment_stripped'] == enrollment_str]
            
            if conf < 50 and not match.empty:
                name = match['Name'].values[0]
                color = (0, 255, 0)
                
                # Check if already present in today's attendance for this subject
                student_key = f"{enrollment_str}_{subject}_{date}"
                if student_key not in marked_students:
                    # Save the image with location details
                    try:
                        # Get absolute path for the Images directory
                        current_dir = os.path.dirname(os.path.abspath(__file__))
                        images_dir = os.path.join(current_dir, "Attendance", "Images")
                        
                        # Create directory if it doesn't exist
                        if not os.path.exists(images_dir):
                            os.makedirs(images_dir)
                            print(f"Created directory: {images_dir}")
                        
                        # Create filename with timestamp to ensure uniqueness
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        image_filename = os.path.join(images_dir, f"{name}_{enrollment}_{timestamp}.jpg")
                        
                        # Add location details to the image
                        location_text = f"📍 Lat: {gps_data['latitude']:.4f}, Lon: {gps_data['longitude']:.4f}"
                        address_text = f"Location: {gps_data['address']}"
                        
                        # Create a copy of the image to add text
                        img_with_text = im.copy()
                        
                        # Add text to image
                        cv2.putText(img_with_text, location_text, (10, img_with_text.shape[0] - 60), font, 0.7, (255, 255, 255), 2)
                        cv2.putText(img_with_text, address_text, (10, img_with_text.shape[0] - 30), font, 0.7, (255, 255, 255), 2)
                        
                        # Save the image
                        print(f"Attempting to save image to: {image_filename}")
                        success = cv2.imwrite(image_filename, img_with_text)
                        
                        if success:
                            print(f"Image saved successfully: {image_filename}")
                            # Verify the file exists
                            if os.path.exists(image_filename):
                                print(f"Verified file exists: {image_filename}")
                                print(f"File size: {os.path.getsize(image_filename)} bytes")
                            else:
                                print(f"Warning: File not found after saving: {image_filename}")
                        else:
                            print(f"Failed to save image: {image_filename}")
                        
                    except Exception as e:
                        print(f"Error saving image: {str(e)}")
                        import traceback
                        traceback.print_exc()
                    
                    # Mark attendance
                    with open(attendance_file, 'a', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow([
                            enrollment, 
                            name, 
                            date, 
                            time, 
                            subject,  # Subject
                            gps_data['latitude'],
                            gps_data['longitude'],
                            gps_data['address']
                        ])
                    
                    marked_students.add(student_key)
                    print(f"Attendance marked for {enrollment} {name}")
                
                label = str(enrollment) + " " + str(name)
            else:
                name = "Unknown"
                color = (225, 0, 0)
                label = str(enrollment) + " " + str(name)
            
            cv2.rectangle(im, (x, y), (x + w, y + h), color, 2)
            cv2.putText(im, label, (x, y + h), font, 1, (255, 255, 255), 2)

        cv2.imshow('Attendance', im)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == 27:  # 27 is ESC
            break
        if cv2.getWindowProperty('Attendance', cv2.WND_PROP_VISIBLE) < 1:
            break

    # Save attendance
    if not attendance.empty:
        attendance.to_csv(attendance_file, mode='a', header=False, index=False)
        messagebox.showinfo("Success", "Attendance marked successfully!")

    # Clean up
    cam.release()
    cv2.destroyAllWindows()

    # After marking attendance, update the statistics
    update_attendance_statistics()
    
    # Show attendance sheet
    root = tk.Tk()
    root.title("Attendance of " + subject)
    root.configure(background='grey80')
    
    # Create headers
    headers = ['Enrollment', 'Name', 'Date', 'Time', 'Subject', 'Latitude', 'Longitude', 'Location']
    for c, header in enumerate(headers):
        label = tk.Label(root, text=header, width=15, height=2, fg="black", bg="grey",
                        font=('times', 12, 'bold'))
        label.grid(row=0, column=c, padx=5, pady=5)
    
    # Read and display attendance for this subject and date
    row_num = 1
    with open(attendance_file, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        for row in reader:
            if len(row) >= 5 and row[2] == date and row[4] == subject:
                for c, value in enumerate(row):
                    label = tk.Label(root, text=str(value), width=15, height=1, fg="black",
                                    bg="white", font=('times', 10))
                    label.grid(row=row_num, column=c, padx=5, pady=2)
                row_num += 1
    root.mainloop()

def update_attendance_statistics():
    try:
        # Read attendance data
        if not os.path.exists('Attendance/Attendance.csv'):
            return
            
        attendance_df = pd.read_csv('Attendance/Attendance.csv')
        if attendance_df.empty:
            return
            
        # Read student details
        if not os.path.exists('StudentDetails/StudentDetails.csv'):
            return
            
        student_df = pd.read_csv('StudentDetails/StudentDetails.csv')
        if student_df.empty:
            return
            
        # Clean up the data
        attendance_df = attendance_df[attendance_df['Subject'].notna()]
        student_df = student_df.drop_duplicates(subset=['Enrollment'], keep='first')
        
        # Calculate total classes per subject
        total_classes = attendance_df.groupby('Subject').size()
        
        # Calculate attendance per student per subject
        attendance_stats = []
        for _, student in student_df.iterrows():
            student_attendance = attendance_df[attendance_df['Enrollment'].astype(str).str.lstrip('0').str.strip() == 
                                            str(student['Enrollment']).lstrip('0').strip()]
            for subject in total_classes.index:
                classes_attended = len(student_attendance[student_attendance['Subject'] == subject])
                total = total_classes[subject]
                percentage = (classes_attended / total * 100) if total > 0 else 0
                attendance_stats.append({
                    'Name': student['Name'],
                    'Enrollment': student['Enrollment'],
                    'Subject': subject,
                    'Classes_Attended': classes_attended,
                    'Total_Classes': total,
                    'Attendance_Percentage': f"{percentage:.2f}%"
                })
        
        # Create DataFrame and save to CSV
        stats_df = pd.DataFrame(attendance_stats)
        stats_df = stats_df.sort_values(['Name', 'Subject'])
        stats_df.to_csv('Attendance/Attendance_Statistics.csv', index=False)
        
    except Exception as e:
        print(f"Error updating attendance statistics: {str(e)}")

window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        window.destroy()

window.protocol("WM_DELETE_WINDOW", on_closing)

message = tk.Label(window, text="Face-Recognition-Based-Attendance-Management-System", bg="black", fg="white", width=50,
                   height=3, font=('times', 30, ' bold '))

message.place(x=80, y=20)

Notification = tk.Label(window, text="All things good", bg="Green", fg="white", width=15,
                        height=3, font=('times', 17))

lbl = tk.Label(window, text="Enter Enrollment : ", width=20, height=2,
               fg="black", bg="grey", font=('times', 15, 'bold'))
lbl.place(x=200, y=200)

def testVal(inStr, acttyp):
    if acttyp == '1':  # insert
        if not inStr.isdigit():
            return False
    return True

txt = tk.Entry(window, validate="key", width=20, bg="white",
               fg="black", font=('times', 25))
txt['validatecommand'] = (txt.register(testVal), '%P', '%d')
txt.place(x=550, y=210)

lbl2 = tk.Label(window, text="Enter Name : ", width=20, fg="black",
                bg="grey", height=2, font=('times', 15, ' bold '))
lbl2.place(x=200, y=300)

txt2 = tk.Entry(window, width=20, bg="white",
                fg="black", font=('times', 25))
txt2.place(x=550, y=310)

lbl3 = tk.Label(window, text="Enter Password : ", width=20, fg="black",
                bg="grey", height=2, font=('times', 15, ' bold '))
lbl3.place(x=200, y=400)

txt3 = tk.Entry(window, width=20, show="*", bg="white",
                fg="black", font=('times', 25))
txt3.place(x=550, y=410)

def clear2():
    txt3.delete(first=0, last=22)

clearButton2 = tk.Button(window, text="Clear", command=clear2, fg="white", bg="black",
                         width=10, height=1, activebackground="white", font=('times', 15, ' bold '))
clearButton2.place(x=950, y=410)

AP = tk.Button(window, text="Check Registered students", command=admin_panel, fg="black",
               bg="SkyBlue1", width=19, height=1, activebackground="white", font=('times', 15, ' bold '))
AP.place(x=990, y=410)

takeImg = tk.Button(window, text="Take Images", command=take_img, fg="black", bg="SkyBlue1",
                    width=20, height=3, activebackground="white", font=('times', 15, ' bold '))
takeImg.place(x=90, y=500)

trainImg = tk.Button(window, text="Train Images", fg="black", command=trainimg, bg="SkyBlue1",
                     width=20, height=3, activebackground="white", font=('times', 15, ' bold '))
trainImg.place(x=390, y=500)

FA = tk.Button(window, text="Automatic Attendance", fg="black", command=subjectchoose,
               bg="SkyBlue1", width=20, height=3, activebackground="white", font=('times', 15, ' bold '))
FA.place(x=690, y=500)

# Add Student Login button to main window
student_login_btn = tk.Button(window, text="Student Login", command=student_login, fg="black",
                             bg="SkyBlue1", width=20, height=3, activebackground="white", font=('times', 15, ' bold '))
student_login_btn.place(x=990, y=500)

window.mainloop()
