from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin # UserAdmin built-in process used for user creation whose backend working is hidden
                                   # ready process for admin creation in UserAdmin
# Register your models here.
# class UserModel(UserAdmin): # use for costom admin class to display only necesaary data ('username','user_type') on admin page
    # list_Display = ['username','user_type',]  # user choices (HOD,Staff,Student)


admin.site.register (CustomUser,UserAdmin) # ready process for admin creation in UserAdmin + add customuser datatype user_type, profile_pic
admin.site.register(Course)
admin.site.register(Session_Year)
admin.site.register(Student)
admin.site.register(Staff)
admin.site.register(Subject)
admin.site.register(Staff_Notification)
admin.site.register(Staff_leave)
admin.site.register(Staff_Feedback)
admin.site.register(Student_Notification)
admin.site.register(Student_Feedback)
admin.site.register(Student_leave)
admin.site.register(Attendance)
admin.site.register(Attendance_Report)
admin.site.register(Student_Result)