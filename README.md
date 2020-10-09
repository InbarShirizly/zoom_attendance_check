# Zoom Attendance Check

![GitHub](https://img.shields.io/github/license/InbarShirizly/zoom_attendance_check?style=plastic)
![GitHub language count](https://img.shields.io/github/languages/count/InbarShirizly/zoom_attendance_check)
![GitHub top language](https://img.shields.io/github/languages/top/InbarShirizly/zoom_attendance_check)


### What is this platform?

- A platform that automatically detects missing students in [zoom](https://zoom.us/) meetings - using the zoom chat file.
- **Check actively** which zoom users where present in class - integrate to your student list of the class.
- **Multiple checks** in one zoom meeting - 
zoom meeting is divided to session according to the chat. In each session the program checks attendance separately.
- **English** and **Hebrew** support.
- Display the current and previous reports for the specific classroom.
- Allow teacher to **edit and manage the report**.


### Table of contents
- [Usage workflow <a name="usage workflow"></a>](#usage-workflow--a-name--usage-workflow----a-)
- [Zoom chat file <a name="Zoom chat file"></a>](#zoom-chat-file--a-name--zoom-chat-file----a-)
  * [Content in the chat file](#content-in-the-chat-file)
  * [Save chat file - via zoom app](#save-chat-file---via-zoom-app)
- [Database  - ERD](#database----erd)

#### Additional info
- [server README](./server/README.md) 
- [client README](./client/README.md)
- [API doc](https://documenter.getpostman.com/view/4335694/TVRg694k)

### Usage workflow <a name="usage workflow"></a>

- **Register and Login**
- **Create new classroom** - upload `excel`/`csv` file of your student list class. `examples` can be found [here](./server/tests/files_to_test/students_list_excel).
- **Upload chat file** - upload `.txt` to the platform under the relevant classroom.
- **Manage report** - managing pop-up will appear with the already filled automatic attendance check for the teacher final decision.
    - For each student the program will assign a status color:
        - **red - student missing**: the student **didn't attend to any** of the teacher's sessions.
        - **yellow - student partially missing**: the student **attend only to part** of the teacher's sessions.
        - **green - student attendant**: means that the student **wrote in all** the teacher's sessions.
    - Teacher can change student's statuses according to his choice.
    - When report is done, the teacher will submit the report, and it will be stored in the service.
- **Classroom reports** - The teacher can view and edit reports at any time.
    
### Zoom chat file <a name="Zoom chat file"></a>

![Alt Text](./docs/Images%20for%20README/create%20and%20save%20chat%20file%20from%20zoom%20app.gif)


#### Content in the chat file

- Attendance check starts with a sentence, for example: "Attendance Check"
- Each student will have limited time to write some credentials (`ID`/`Phone Number`/`Name`)
- There can be as many attendance checks in one session as the teacher desires.
- `start sentence`, the `accepted credentials` and the `time period` can defined by the teacher


#### Save chat file - via zoom app

**`Remember`** to save chat file from the zoom meeting when the meeting is about to end

![image](./docs/Images%20for%20README/Save%20chat%20file.jpg)


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
 
![image](./docs/Images%20for%20README/ERD%20zoom%20attendnace%20check.JPG)


            
   