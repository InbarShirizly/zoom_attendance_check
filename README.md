![GitHub](https://img.shields.io/github/license/InbarShirizly/zoom_attendance_check?style=plastic)
![GitHub language count](https://img.shields.io/github/languages/count/InbarShirizly/zoom_attendance_check)
![GitHub top language](https://img.shields.io/github/languages/top/InbarShirizly/zoom_attendance_check)

# Zoom Attendance check

#### check participants attendance in your zoom session


### What is this platform?

- Check your participants attendance in few clicks
- Check actively which zoom users where present in class - integrate to your student list of the class
- Multiple checks in one zoom talk
- English and Hebrew support



### Usage workflow

- **Register** register to the service
- **Create new classroom** - upload excel/csv file of the student list of your class
- **Save zoom chat** - save file locally. 
    - explanation of the content needed in the chat can be found **here**
    - explanation of how to download zoom chat file via the zoom up can be found **here**
- **Upload report** - upload zoom chat file (.txt file) to the platform under the relevant classroom
    - when uploading the file, a configuration page will open. the user will chose specific
     configuration for his own class. explanation can be found **here**
 - **Manage report** - after the uplaod, a managing pop-up will appear with the program automatic attendance check.
 The window will contain a table of the students names and status color.
    - For each student the program will assign a status color:
        - **red - student missing**: means that the student **didn't wrote** under his name in **all** the teacher's sessions
        - **yellow - student partially missing**: means that the student **wrote only in part** of the sessions of the teacher
        - **green - student attendant**: means that the student **wrote in all** the teacher's sessions
    - Teacher **must** decide manually over all the *yellow students*. Furthermore, the teacher can change other student status according to his choice
    - When report is done, the teacher will submit the report, it will be stored in the service (up to 10 reports)
- **Classroom reports** - The teacher can check at any time the his last 10 reports. The page will contain a table with student names and
there reports, when each column will be assigned to different report with the specific start time and the session date.
    - teacher can change statuses of his report in any time
    
### Zoom chat file

![Alt Text](https://github.com/InbarShirizly/zoom_attendance_check/blob/master/docs/Images%20for%20README/create%20and%20save%20chat%20file%20from%20zoom%20app.gif)


#### content in the chat file

- Teacher (or the zoom session "manager") needs to write a "start sentence". 
This sentence is will be configured to each report or remain in a default value according to the user preference.
- The students need to write one of their referring information (name/ ID/ phone)
 that is part of the information on the student that exists in the teacher classroom file upload (so in the platform database as well)
- The student have limited time to write a valuable data - this time period is confabulated by the user.
- The teacher can start new "session" whenever he wants during the zoom meeting, and the students will have to
 respond similar to the first time.

#### Save chat file - via zoom app

- When zoom meeting is about to end (or when the teacher decides that he finished his "report" for this meeting),
the teacher needs to save the chat file via the zoom file, with the bottom from the image below (and described in the giff).
- The chat file will be saved in a folder that the zoom app picked, and now the teacher needs to upload the chat file from there
(or to copy to his preference folder and then..)

![image](https://github.com/InbarShirizly/zoom_attendance_check/blob/master/docs/Images%20for%20README/Save%20chat%20file.jpg)


### upload report configuration

### Database  - ERD

The database keeps track as following:

- `teacher` - Each user has his own account
- `classroom` - Each user has many classes
- `student` - Each classroom has many students with their personal info loaded from the excel/csv file
- `report` - Each classroom has many reports over the class, containing time of class and short description 
- `session` - Each report has many session (depend on teacher decision), session has start time - first message
- `zoom_names` + `chat`
    - **These tables are currently not supported in the platform** - should be expressed when it will part of the project
 - `student_status` - For each report, each student has status of participating in class. 
    - this value can be updated by the teacher when managing the report - without effecting the rest of the tables
 
![image](https://github.com/InbarShirizly/zoom_attendance_check/blob/master/docs/Images%20for%20README/ERD%20zoom%20attendnace%20check.JPG)

### code 

            
   