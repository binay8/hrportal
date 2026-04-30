from django.contrib import admin
from .models import *

# Register your models here.


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ["id", "firstname", "lastname", "fullname"]


class RoleDetailAdmin(admin.ModelAdmin):
    list_display = ["id", "job_title", "start_date"]


class SalaryDetailAdmin(admin.ModelAdmin):
    list_display = ["id", "employee", "pay_type"]


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "short_name", "head_full_name"]


class EmployeeHourlyShiftAdmin(admin.ModelAdmin):
    list_display = ["id", "shift_start_date_time", "shift_end_date_time", "total_hours"]


class EmployeeHourlyBreakAdmin(admin.ModelAdmin):
    list_display = ["id", "break_start_date_time", "break_end_date_time"]


class EmployeePayCheckAdmin(admin.ModelAdmin):
    list_display = ["id", "employee", "pay_period_start", "pay_period_end"]


class LeaveDetailAdmin(admin.ModelAdmin):
    list_display = ["id", "employee", "leave_type", "start_date", "end_date", "status"]


admin.site.register(Employee, EmployeeAdmin)
admin.site.register(RoleDetail, RoleDetailAdmin)
admin.site.register(SalaryDetail, SalaryDetailAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(EmployeeHourlyShift, EmployeeHourlyShiftAdmin)
admin.site.register(EmployeeHourlyBreak, EmployeeHourlyBreakAdmin)
admin.site.register(EmployeePayCheck, EmployeePayCheckAdmin)
admin.site.register(LeaveDetail, LeaveDetailAdmin)
