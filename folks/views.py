from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.contrib.auth.models import User

from .models import Employee, EmployeePayCheck, LeaveDetail
from .forms import CreateEmployee, CreateEmpFromModel, RequestLeave
import time


@login_required
def home(request):
    # This view should only display the home page for authenticated users

    # First get employee information from Employee using relationship with user.
    try:
        employee = Employee.objects.get(user=request.user)
        print(f"Employee found: {employee}")  # Debug print
    except Employee.DoesNotExist:
        employee = None
        print("No employee found for the user")  # Debug print

    # Get last pay details from EmployeePayCheck using relationship between EmployeePayCheck and employee
    if employee is not None:
        try:
            last_pay = (
                EmployeePayCheck.objects.filter(employee=employee)
                .order_by("-pay_period_end")
                .first()
            )
            print(f"Last pay found: {last_pay} for {employee}")  # Debug print
        except EmployeePayCheck.DoesNotExist:
            last_pay = None
            print("No last pay found for the employee")  # Debug print

    return render(
        request,
        "folks/home.html",
        {"user": request.user, "employee": employee, "last_pay": last_pay},
    )


def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        print(f"Attempting login with username: {username}")  # Debug print

        # Check if user exists
        try:
            user_exists = User.objects.get(username=username)
            print(f"User {username} exists in database")  # Debug print
        except User.DoesNotExist:
            print(f"User {username} does not exist")  # Debug print
            messages.error(request, "User does not exist")
            return render(request, "folks/login.html")

        # Attempt authentication
        user = authenticate(request, username=username, password=password)
        print(f"Authentication result: {user}")  # Debug print

        if user is not None:
            print(f"Login successful for user: {username}")  # Debug print
            auth_login(request, user)
            return redirect("home")  # Redirect to home after successful login
        else:
            print(f"Authentication failed for user: {username}")  # Debug print
            messages.error(request, "Invalid username or password")

    return render(request, "folks/login.html")


@login_required
def create(request):
    if request.method == "POST":
        form = CreateEmpFromModel(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            return redirect("home")  # Redirect after successful creation
    form = CreateEmpFromModel()
    return render(request, "folks/create.html", {"form": form})


# @login_required
# def request_leave_alt(request):
#     # Get the employee object from the logged-in user, same as in home view
#     try:
#         employee = Employee.objects.get(user=request.user)
#         print(f"Employee Found: {employee}")
#     except Employee.DoesNotExist:
#         employee = None

#     # Retrieve leave choices from LeaveDetail model
#     leave_choices = LeaveDetail.LEAVE_TYPE_CHOICES

#     if request.method == "POST":
#         # Process the leave request form submission
#         # For now, just print the submitted data for debugging
#         leave_type = request.POST.get("leave_type")
#         start_date = request.POST.get("start_date")
#         end_date = request.POST.get("end_date")
#         message = request.POST.get("message")
#         print(request.POST)
#         messages.success(request, "Leave request submitted successfully.")
#         return redirect('home')
#     return render(request, "folks/request_leave.html", {
#         "employee": employee,
#         "user": request.user,
#         'leave_choices': leave_choices
#     })


@login_required
def view_leave_requests(request):
    # Get the employee object from the logged-in user, same as in home view
    try:
        employee = Employee.objects.get(user=request.user)
        print(f"Employee Found: {employee}")
    except Employee.DoesNotExist:
        employee = None

    # Retrieve leave requests for the employee
    if employee is not None:
        leave_requests = LeaveDetail.objects.filter(employee=employee).order_by(
            "-start_date"
        )
        print(f"Leave requests found: {leave_requests}")  # Debug print
    else:
        leave_requests = []
        print("No employee found, so no leave requests")  # Debug print

    if request.method == "POST":
        # Process any actions on leave requests if needed (e.g., cancel request)
        pass
    return render(
        request,
        "folks/view_leave.html",
        {"employee": employee, "leave_requests": leave_requests},
    )


@login_required
def request_leave(request):
    # Get the employee object from the logged-in user, same as in home view
    try:
        employee = Employee.objects.get(user=request.user)
        print(f"Employee Found: {employee}")
    except Employee.DoesNotExist:
        employee = None

    # Retrieve leave choices from LeaveDetail model
    leave_choices = LeaveDetail.LEAVE_TYPE_CHOICES

    if request.method == "POST":
        # Process the leave request form submission
        # For now, just print the submitted data for debugging
        leave_form = RequestLeave(request.POST)
        print(request.POST)
        if leave_form.is_valid():
            leave_form.instance.employee = employee
            leave_form.instance.status = "Submitted"
            leave_form.save()
            print("Success!!")
            messages.success(request, "Leave request submitted successfully.")
            return redirect("home")
        else:
            messages.error(request, "Failed to submit leave request.")
            print(leave_form.errors)
    else:
        leave_form = RequestLeave()
    return render(
        request,
        "folks/request_leave.html",
        {"employee": employee, "user": request.user, "leave_form": leave_form},
    )
