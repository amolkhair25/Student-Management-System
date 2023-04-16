from django.shortcuts import render,redirect # for render, redirect page 
from S_M_S.models import *
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
    
    return render(request,'Students/home.html',context)


def STUDENT_NOTIFICATION(request):
    student=Student.objects.filter(admin= request.user.id)
    for i in student:
        student_id=i.id
    
        notification = Student_Notification.objects.filter(student_id=student_id)

        context={
            'notification':notification,
        }


    return render(request,'Students/notification.html',context)    


def STUDENT_NOTIFICATION_MARK_AS_DONE(request,id):
    notification = Student_Notification.objects.get(id = id)
    notification.status = 1
    notification.save()
    return redirect('student_notification')



def STUDENT_FEEDBACK(request):
    student_id = Student.objects.get(admin=request.user.id)
    feedback_history = Student_Feedback.objects.filter(student_id=student_id)

    context ={
        'feedback_history':feedback_history,
    }
    return render(request,'Students/feedback.html',context)


def STUDENT_FEEDBACK_SAVE(request):
    
    if request.method == 'POST':
        feedback = request.POST.get('feedback')
        student =  Student.objects.get(admin=request.user.id)
        feedbacks = Student_Feedback(
            student_id = student,
            feedback = feedback,
            feedback_reply="",

        )
        feedbacks.save()

        return redirect('student_feedback')



def STUDENT_LEAVE(request):
    student=Student.objects.get(admin=request.user.id)
    student_leave_history = Student_leave.objects.filter(student_id=student)
    context={
        'student_leave_history':student_leave_history,
    }
    return render(request,'Students/apply_leave.html',context)        


def STUDENT_APPLY_LEAVE_SAVE(request):   
    if request.method == 'POST':
        leave_date = request.POST.get('leave_date')
        leave_message = request.POST.get('leave_message') 
        
        student_id =Student.objects.get(admin=request.user.id)
        
        student_leave =Student_leave(
            student_id = student_id,
            date = leave_date,
            message =leave_message,
        )
        student_leave.save()
        request.session['message'] = "Leave Are Successfully Send!"
    return redirect('student_leave')


def STUDENT_VIEW_ATTENDANCE(request):
    student = Student.objects.get(admin = request.user.id)
    course_id = student.course_id
    subject = Subject.objects.filter(course = course_id)
    action =request.GET.get('action')
    get_subject=None
    attendance_report=None


    if action is not None:
        if request.method == "POST":
            subject_id = request.POST.get('subject_id')

            get_subject = Subject.objects.get(id =subject_id)

            
            attendance_report = Attendance_Report.objects.filter(student_id = student,attendance_id__subject_id=subject_id)
    context ={
        'subject':subject,
        'action' : action,
        'get_subject':get_subject,
        'attendance_report':attendance_report,
    }
    return render(request,'Students/view_attendance.html',context)    


def VIEW_RESULT (request):
    mark = None
    student = Student.objects.get(admin=request.user.id)
    
    result = Student_Result.objects.filter(student_id=student)

    for i in result:
        assignment_mark = i.assignment_mark
        exam_mark=i.exam_Mark

        mark =assignment_mark + exam_mark

    context={
        'result':result,
        'mark':mark,
    }

    return render(request,'Students/view_result.html',context)    