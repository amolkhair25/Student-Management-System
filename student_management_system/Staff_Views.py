from django.shortcuts import render,redirect # for render, redirect page 
from S_M_S.models import Staff,Staff_Notification,Staff_leave,Staff_Feedback,Subject,Session_Year,Course, Student,Attendance,Attendance_Report,Student_Result
from django.contrib.auth.decorators import login_required 

@login_required(login_url='/')
def HOME(request):
    student_count = Student.objects.all().count() # count Students
    staff_count = Staff.objects.all().count()
    course_count = Course.objects.all().count()
    subject_count = Subject.objects.all().count()
    
    # for how many male and female students
    student_gender_male = Student.objects.filter(gender = "Male").count()
    student_gender_female = Student.objects.filter(gender="Female").count()
    
    # send this data to home.html
    context = {
        'student_count':student_count,
        'staff_count':staff_count,
        'course_count':course_count,
        'subject_count':subject_count,
        'student_gender_male':student_gender_male, 
        'student_gender_female':student_gender_female,
    }
    return render(request,'Staff/home.html',context)

@login_required(login_url='/')
def NOTIFICATIONS(request):
    staff =Staff.objects.filter(admin=request.user.id) # (request.user.id )means ata jo user open ahe tyachi info admin shi match karel ani tyacha data staff madhe store karel
    for i in staff: # open user cha sarv data forloop ne i madhe takla (e.g. id,first_name,last_name,username,email etc)
        staff_id = i.id # open user cha id staff_id madhe takla

        notification = Staff_Notification.objects.filter(staff_id=staff_id)#Staff_Notification id(staff_id) match with staff_id

        context = {
            'notification':notification,
        }
        return render (request,'Staff/notification.html',context)  
    return render (request,'Staff/notification.html')         

@login_required(login_url='/')
def STAFF_NOTIFICATION_MARK_AS_DONE(request,id):
    notification = Staff_Notification.objects.get(id = id)
    notification.status = 1
    notification.save()
    return redirect('notifications')


@login_required(login_url='/')
def STAFF_APPLY_LEAVE(request):
    staff = Staff.objects.filter(admin = request.user.id)
    for i in staff:
        staff_id = i.id

        staff_leave_history = Staff_leave.objects.filter(staff_id = staff_id)

        context={
            'staff_leave_history':staff_leave_history,
        }
    return render (request,'Staff/apply_leave.html',context)


@login_required(login_url='/')
def STAFF_APPLY_LEAVE_SAVE(request):
    if request.method == 'POST':
        leave_date = request.POST.get('leave_date')
        leave_message = request.POST.get('leave_message')

        staff=Staff.objects.get(admin = request.user.id)

        leave=Staff_leave(
            staff_id = staff,
            date = leave_date,
            message = leave_message,
        )
        leave.save()
        request.session['message'] = "Leave Successfully Send!" 
        return redirect('staff_apply_leave')

    return render (request,'Staff/apply_leave.html')    

@login_required(login_url='/')
def STAFF_FEEDBACK(request):
    staff_id = Staff.objects.get(admin = request.user.id)
    feedback_history = Staff_Feedback.objects.filter (staff_id=staff_id)
    context = {
        'feedback_history' : feedback_history,
    }
    return render(request,'Staff/feedback.html',context)  


def STAFF_FEEDBACK_SAVE(request):
    if request.method == 'POST':
        feedback = request.POST.get('feedback')
        
        staff=Staff.objects.get(admin = request.user.id)

        feedback = Staff_Feedback(
            staff_id = staff,
            feedback = feedback,
            feedback_reply = "",
        )
        feedback.save()
        return redirect ('staff_feedback')
    return render(request,'Staff/feedback.html')      


def STAFF_TAKE_ATTENDANCE(request):
    staff_id = Staff.objects.get(admin=request.user.id)

    subject= Subject.objects.filter(staff=staff_id)
    session_year = Session_Year.objects.all()
    

    action= request.GET.get('action')
    get_subject = None
    get_session_year = None
    students = None

    if action is not None:
        if request.method == "POST":
            subject_id = request.POST.get('subject_id')
            session_year_id = request.POST.get('session_year_id')

            get_subject=Subject.objects.get(id = subject_id)
            get_session_year = Session_Year.objects.get(id= session_year_id)




            subject = Subject.objects.filter(id=subject_id)
            for i in subject:
                course_id = i.course_id
                students = Student.objects.filter(course_id = course_id)

    context = {
        'subject' : subject,
        'session_year' :session_year,
        'get_subject':get_subject,
        'get_session_year':get_session_year,
        'action':action,
        'students':students,
    }

    return render(request,'Staff/take_attendance.html',context)    


def STAFF_SAVE_ATTENDANCE(request):
    if request.method=='POST':
        subject_id = request.POST.get('subject_id')
        session_year_id = request.POST.get('session_year_id')
        attendance_date = request.POST.get('attendance_date')
        student_id = request.POST.getlist('student_id')
        
        get_subject=Subject.objects.get(id = subject_id)
        get_session_year = Session_Year.objects.get(id= session_year_id)

        attendance = Attendance(
            subject_id = get_subject,
            attendance_date = attendance_date,
            session_year_id = get_session_year,
        )
        attendance.save()

        for i in student_id:
            stud_id = i
            
            p_student = Student.objects.get(id=stud_id)
            attendance_report = Attendance_Report(
                student_id = p_student,
                attendance_id = attendance,
            )
            attendance_report.save()

        return redirect ('staff_take_attendance')


def STAFF_VIEW_ATTENDANCE(request):
    staff_id =Staff.objects.get(admin = request.user.id)
    subject=Subject.objects.filter(staff_id = staff_id)
    session_year=Session_Year.objects.all()
    action= request.GET.get('action')
    get_subject=None
    get_session_year=None
    attendance_date = None
    attendance_report=None


    if action is not None:
        if request.method== "POST":
            
            subject_id = request.POST.get('subject_id')
            session_year_id =  request.POST.get('session_year_id')
            attendance_date = request.POST.get('attendance_date')
            
            get_subject = Subject.objects.get(id=subject_id)
            get_session_year = Session_Year.objects.get(id=session_year_id)
            
            attendance =Attendance.objects.filter(subject_id = get_subject,attendance_date=attendance_date)
            for i in attendance:
                attendance_id = i.id
                attendance_report = Attendance_Report.objects.filter(attendance_id=attendance_id)
            
           
    context = {
        'subject':subject,
        'session_year':session_year,
        'action':action,
        'get_subject':get_subject,
        'get_session_year':get_session_year,
        'attendance_date' :attendance_date,
        'attendance_report':attendance_report,
    }
    return render(request,'Staff/view_attendance.html',context)        


def STAFF_ADD_RESULT(request):
    staff = Staff.objects.get(admin = request.user.id)
    subject =Subject.objects.filter(staff_id=staff)
    session_year = Session_Year.objects.all()
    action= request.GET.get('action')
    get_subject=None
    get_session=None
    student=None

    if action is not None:
        if request.method == "POST":
            subject_id = request.POST.get('subject_id')
            session_year_id = request.POST.get('session_year_id')
            
            get_subject =Subject.objects.get(id = subject_id)
            get_session= Session_Year.objects.get(id = session_year_id )

            subject = Subject.objects.filter(id = subject_id)
            for i in subject:
                student_id = i.course.id
                student=Student.objects.filter(course_id=student_id)

    context={
        'subject':subject,
        'session_year':session_year,
        'action':action,
        'get_subject':get_subject,
        'get_session':get_session,
        'student':student,
    }
    return render(request,'Staff/add_result.html',context)    


def STAFF_SAVE_RESULT(request):
    if request.method == "POST":
        subject_id = request.POST.get('subject_id')
        session_year_id = request.POST.get('session_year_id')
        student_id = request.POST.get('student_id')
        assignment_mark = request.POST.get('assignment_mark')
        Exam_mark = request.POST.get('Exam_mark')

        get_student = Student.objects.get(admin = student_id)
        get_subject = Subject.objects.get(id = subject_id )

        check_exists = Student_Result.objects.filter(subject_id = get_subject,student_id=get_student).exists()
        if check_exists:
            result = Student_Result.objects.get(subject_id=get_student,student_id=get_student)
            result.assignment_mark=assignment_mark
            result.exam_mark=Exam_mark
            result.save()
            request.session['message'] = "Result Are Successfully Updated!"
            return redirect('staff_add_result') 

        else:
            result = Student_Result(
                student_id = get_student,
                subject_id = get_subject,
                exam_Mark = Exam_mark,
                assignment_mark = assignment_mark,
            )
            result.save()
            request.session['message'] = "Result Are Successfully Added!"
            return redirect('staff_add_result') 


   