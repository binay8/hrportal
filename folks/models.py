from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Person(models.Model):
    """
    Abstract base class representing a person entity with first name, middle initial, and last name.
    Attributes:
        firstname (CharField): The first name of the person, with a maximum length of 30 characters.
        middle_initial (CharField): The middle initial of the person, with a maximum length of 1 character. This field is optional.
        lastname (CharField): The last name of the person, with a maximum length of 30 characters.
    Meta:
        abstract (bool): Indicates that this is an abstract base class and should not be used to create any database table.
    """

    GENDER_CHOICES = [
        ("Male", "Male"),
        ("Female", "Female"),
    ]
    firstname = models.CharField(max_length=30, blank=False, null=False)
    middle_initial = models.CharField(max_length=3, blank=True, null=True)
    lastname = models.CharField(max_length=30, blank=False, null=False)
    gender = models.CharField(
        max_length=10, choices=GENDER_CHOICES, blank=True, null=True
    )
    ethnicity = models.CharField(max_length=50, blank=True, null=True)
    race = models.CharField(max_length=50, blank=True, null=True)
    nationality = models.CharField(max_length=50, blank=True, null=True)
    preferred_name = models.CharField(max_length=50, blank=True, null=True)
    pronouns = models.CharField(max_length=50, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    street_address = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    province = models.CharField(max_length=50, blank=True, null=True)
    zipcode = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    government_id = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    social_security_number = models.CharField(max_length=20, blank=True, null=True)
    personal_email = models.EmailField(blank=True, null=True)
    emergency_contact_name = models.CharField(max_length=50, blank=True, null=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.fullname

    @property
    def fullname(self):
        """
        Returns the full name of the person by combining first name, middle initial, and last name.
        """
        if self.middle_initial:
            return f"{self.firstname} {self.middle_initial} {self.lastname}"
        return f"{self.firstname} {self.lastname}"

    class Meta:
        """
        Meta class for defining model options.

        Attributes:
            abstract (bool): Indicates that this model is an abstract base class.
        """

        abstract = True


class Employee(Person):
    """
    Represents an employee in the HR portal.
        primary_email (EmailField): The primary email address of the employee.
        alternate_email (EmailField): An alternate email address for the employee, optional.
        alias1 (CharField): An optional alias for the employee.
        alias2 (CharField): A second optional alias for the employee.
        hire_date (DateField): The date the employee was hired.
        employment_end_date (DateField): The date the employee's employment ended, optional.
        employment_status (CharField): The current employment status of the employee.
        last_promotion_date (DateField): The date of the employee's last promotion, optional.
        manager_id (ForeignKey): A reference to the employee's manager, optional.
        work_location_building (CharField): The building where the employee works, optional.
        work_location_office (CharField): The office where the employee works, optional.
        new_hire (BooleanField): Indicates if the employee is a new hire.
        rehire (BooleanField): Indicates if the employee is a rehire.
        previous_employee_id (IntegerField): The ID of the employee's previous employment, optional.
    Properties:
        current_role (str): The current role of the employee from the related RoleDetails table.
        full_address (str): The full address of the employee.
        years_of_service (int): The number of years the employee has been in service based on the hire date.

    """

    user = models.OneToOneField(
        User, null=True, on_delete=models.CASCADE, related_name="employee_user_profile"
    )
    alias1 = models.CharField(max_length=50, blank=True, null=True, unique=True)
    alias2 = models.CharField(max_length=50, blank=True, null=True, unique=True)
    # primary_email = models.EmailField()
    # alternate_email = models.EmailField(blank=True, null=True)
    hire_date = models.DateField()
    employment_end_date = models.DateField(blank=True, null=True)
    EMPLOYMENT_STATUS_CHOICES = [
        ("Active", "Active"),
        ("Inactive", "Inactive"),
        ("Leave of Absence", "Leave of Absence"),
        ("Terminated", "Terminated"),
    ]
    employment_status = models.CharField(
        max_length=50, choices=EMPLOYMENT_STATUS_CHOICES, blank=True, null=True
    )
    EMPLOYEE_TYPE_CHOICES = [
        ("Full-time", "Full-time"),
        ("Part-time", "Part-time"),
        ("Contractor", "Contractor"),
        ("Intern", "Intern"),
        ("Seasonal", "Seasonal"),
        ("Temporary", "Temporary"),  # Fixed typo: was 'Temporaty'
    ]
    employee_type = models.CharField(
        max_length=50, choices=EMPLOYEE_TYPE_CHOICES, blank=True, null=True
    )
    last_promotion_date = models.DateField(blank=True, null=True)
    manager_id = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="direct_reports",
    )
    # manager_id = models.IntegerField(blank=True, null=True)
    work_location_building = models.CharField(max_length=50, blank=True, null=True)
    work_location_office = models.CharField(max_length=50, blank=True, null=True)
    new_hire = models.BooleanField(default=False)
    rehire = models.BooleanField(default=False)
    previous_employee_id = models.IntegerField(blank=True, null=True)

    # This function generates an unique alias for employee based on their first name and last name initials.
    # The convention is to use the first name and the first letter of the last name.
    # If the alias already exists in the database, it appends additional letters from last name until a unique alias is found.
    # If all letters of the last name are used, it appends a number to the alias.
    def auto_generate_alias(self):
        first_name = self.firstname
        last_name = self.lastname
        # Check if the preferred alias already exists in the database
        preferred_alias = f"{first_name}{last_name[0]}"
        # Query only the relevant alias values for efficiency
        existing_aliases = Employee.objects.exclude(pk=self.pk).values_list(
            "alias1", flat=True
        )
        alias = preferred_alias
        increment = 1
        last_name_length = len(last_name)
        while alias in existing_aliases:
            if increment < last_name_length:
                alias = f"{preferred_alias}{last_name[increment]}"
            else:
                alias = f"{preferred_alias}{increment}"
            increment += 1
        return alias

    @property
    def primary_email(self):
        """
        Automatically assigns the primary email based on alias1 value.
        The primary email will be alias1 + '@folks.com'.
        """
        if self.alias1:
            return f"{self.alias1}@folks.com"
        return None

    @property
    def alternate_email(self):
        """
        Automatically assigns the alternate email based on alias2 value.
        The alternate email will be alias2 + '@folks.com'.
        """
        if self.alias2:
            return f"{self.alias2}@folks.com"
        return None

    @property
    def current_role(self):
        """
        Returns the current role of the employee from the related RoleDetails table.
        """
        role = RoleDetail.objects.filter(employee=self).order_by("-start_date").first()
        return role.job_title if role else None

    @property
    def user_roles(self):
        """
        Returns a list of roles assigned to the employee.
        """
        return UserRole.objects.filter(user=self)

    @property
    def full_address(self):
        """
        Returns the full address of the employee by combining street address, city, state, zip code, and country.
        """
        return f"{self.street_address}, {self.city}, {self.state} {self.zipcode}, {self.country}"

    @property
    def years_of_service(self):
        """
        Returns the number of years the employee has been in service based on the hire date.

        """
        from datetime import date

        today = date.today()
        hire_year = self.hire_date.year
        end_year = (
            self.employment_end_date.year if self.employment_end_date else today.year
        )
        return end_year - hire_year

        ### If you get an error "Instance of 'DateField' has no 'year' member", go to File > Preferences > Settings > Extensions > Python and add "python.linting.pylintArgs": ["--generate-members"] to the settings.json file.

    class Meta:
        """
        Meta class for defining model options.

        Attributes:
            db_table (str): The name of the database table to use for this model.
        """

        db_table = "employees"


class RoleDetail(models.Model):
    """
    Represents the employment details of an employee.
    Attributes:
        employee (ForeignKey): A foreign key to the Employee model.
        job_title (CharField): The job title of the employee, with a maximum length of 50 characters.
        hire_date (DateField): The date when the employee was hired.
        end_date (DateField): The date when the employee's employment ended. This field is optional.
        department (CharField): The department where the employee works, with a maximum length of 50 characters.
        pay_type (CharField): The type of pay (e.g., hourly, salary), with a maximum length of 20 characters.
        pay_frequency (CharField): The frequency of pay (e.g., weekly, bi-weekly), with a maximum length of 20 characters.
        hourly_rate (DecimalField): The hourly rate of pay. This field is optional.
        annual_salary (DecimalField): The annual salary. This field is optional.
        reason_for_end (CharField): The reason for the end of employment, with a maximum length of 100 characters. This field is optional.
        overtime_rate (DecimalField): The overtime rate of pay. This field is optional.
        hourly_full_time (BooleanField): Indicates if the employee is a full-time hourly employee.
        hourly_start_day (DateField): The start day for hourly employees. This field is optional.
    """

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    department = models.ForeignKey(
        "Department", on_delete=models.SET_NULL, blank=True, null=True
    )
    job_title = models.CharField(max_length=50)
    job_title_short = models.CharField(max_length=6, blank=True, null=True)
    previous_job_title = models.CharField(max_length=50, blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    # pay_type = models.CharField(max_length=20)
    # reason_for_end = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.employee.fullname

    class Meta:
        """
        Meta class for defining model options.

        Attributes:
            db_table (str): The name of the database table to use for this model.
        """

        db_table = "role_details"


class SalaryDetail(models.Model):
    """Represents the salary details of an employee."""

    PAY_FREQUENCY_CHOICES = [
        ("Weekly", "Weekly"),
        ("Bi-Weekly", "Bi-Weekly"),
        ("Monthly", "Monthly"),
        ("Quarterly", "Quarterly"),
        ("Annually", "Annually"),
    ]
    PAY_TYPE_CHOICES = [
        ("Salaried", "Salaried"),
        ("Hourly", "Hourly"),
        ("Contract", "Contract"),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    pay_type = models.CharField(
        max_length=20, choices=PAY_TYPE_CHOICES, blank=False, null=True
    )
    # is_salaried = models.BooleanField(default=False)
    # is_hourly = models.BooleanField(default=False)
    is_bonus_eligible = models.BooleanField(default=False)
    pay_frequency = models.CharField(
        max_length=20,
        choices=PAY_FREQUENCY_CHOICES,
        blank=False,
        null=False,
        default="Bi-Weekly",
    )
    annual_salary = models.DecimalField(
        max_digits=15, decimal_places=2, blank=True, null=True
    )
    hourly_rate = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    overtime_rate = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    bonus_category = models.CharField(max_length=50, blank=True, null=True)
    bonus_amount = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    effective_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    hourly_full_time = models.BooleanField(default=False)
    hourly_start_day = models.DateField(blank=True, null=True)

    def clean(self):
        super().clean()
        # Validate that either annual_salary or hourly_rate is provided based on pay_type'
        if self.pay_type == "Salaried" and not self.annual_salary:
            raise ValueError("ERROR: Annual salary is required for salaried employees.")
        if self.pay_type == "Hourly" and not self.hourly_rate:
            raise ValueError("ERROR: Hourly rate is required for hourly employees.")

    def __str__(self):
        return self.employee.fullname

    class Meta:
        db_table = "salarydetails"


class Department(models.Model):
    """
    Represents a department within the organization.
    Attributes:
        name (CharField): The name of the department, with a maximum length of 50 characters.
        description (TextField): A brief description of the department. This field is optional.
        manager (ForeignKey): A foreign key to the Employee model representing the manager of the department. This field is optional.
    """

    name = models.CharField(max_length=50)
    short_name = models.CharField(max_length=6, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    head = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="managed_departments",
    )

    def __str__(self):
        return self.name

    @property
    def head_full_name(self):
        """
        Returns the full name of the department head.
        """
        return self.head.fullname if self.head else None

    class Meta:
        """
        Meta class for defining model options.
        Attributes:
            db_table (str): The name of the database table to use for this model.
        """

        db_table = "departments"


class EmployeeHourlyShift(models.Model):
    """
    Represents an hourly shift for an employee.
    Attributes:
        employee (ForeignKey): A foreign key to the Employee model.
        shift_date (DateField): The date of the shift.
        start_time (TimeField): The start time of the shift.
        end_time (TimeField): The end time of the shift.
        hours_worked (DecimalField): The total hours worked during the shift.
    """

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    shift_start_date_time = models.DateTimeField()
    shift_end_date_time = models.DateTimeField()

    @property
    def total_hours(self):
        """
        Returns the total hours worked during the shift.
        """
        return self.shift_end_date_time - self.shift_start_date_time

    def __str__(self):
        return f"{self.employee.fullname} - {self.shift_start_date_time} to {self.shift_end_date_time}"

    class Meta:
        db_table = "employee_hourly_shifts"


class EmployeeHourlyBreak(models.Model):
    """
    Represents a break taken by an employee during an hourly shift.
    Attributes:
        employee (ForeignKey): A foreign key to the Employee model.
        break_start_time (TimeField): The start time of the break.
        break_end_time (TimeField): The end time of the break.
        break_duration (DecimalField): The duration of the break in hours.
    """

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    shift_id = models.ForeignKey(
        EmployeeHourlyShift, on_delete=models.CASCADE, related_name="breaks"
    )
    break_start_date_time = models.DateTimeField()
    break_end_date_time = models.DateTimeField()
    paid_break = models.BooleanField(default=False)

    @property
    def break_duration(self):
        """
        Returns the duration of the break in hours.
        """
        return (
            self.break_end_date_time - self.break_start_date_time
        ).total_seconds() / 3600

    def __str__(self):
        return f"{self.employee.fullname} - Break from {self.break_start_date_time} to {self.break_end_date_time}"

    class Meta:
        db_table = "employee_hourly_breaks"


class EmployeePayCheck(models.Model):
    """
    Represents a paycheck for an employee.
    Attributes:
        employee (ForeignKey): A foreign key to the Employee model.
        pay_period_start (DateField): The start date of the pay period.
        pay_period_end (DateField): The end date of the pay period.
        gross_pay (DecimalField): The total gross pay for the pay period.
        net_pay (DecimalField): The total net pay after deductions for the pay period.
        deductions (DecimalField): The total deductions for the pay period.
    """

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    pay_period_start = models.DateField()
    pay_period_end = models.DateField()
    # gross_pay = models.DecimalField(max_digits=15, decimal_places=2)
    net_pay = models.DecimalField(max_digits=15, decimal_places=2)
    deductions = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return f"{self.employee.fullname} - {self.pay_period_start} to {self.pay_period_end}"

    @property
    def gross_pay_salaried(self):
        """
        Returns the gross pay for the paycheck.
        """
        # calculate gross pay based on salary details
        salary_details = SalaryDetail.objects.filter(employee=self.employee).first()
        if salary_details:
            if (
                salary_details.pay_type == "Salaried"
                and salary_details.pay_frequency == "Bi-Weekly"
            ):
                return round(salary_details.annual_salary / 26, 2)
            elif (
                salary_details.pay_type == "Salaried"
                and salary_details.pay_frequency == "Monthly"
            ):
                return round(salary_details.annual_salary / 12, 2)

    @property
    def gross_pay_hourly(self):
        """
        Returns the gross pay for the paycheck.
        """
        # calculate gross pay based on hourly details
        # Get the salary details for the employee. Need this to get hourly rate.
        salary_details = SalaryDetail.objects.filter(employee=self.employee).first()
        # Calculate the total hours worked in the pay period. Create a query to extract number of hours worked in the pay period from EmployeeHourlyShift
        hourly_shifts = EmployeeHourlyShift.objects.filter(
            employee=self.employee,
            shift_date__range=[self.pay_period_start, self.pay_period_end],
        )
        total_hours = sum(shift.total_hours for shift in hourly_shifts)
        return total_hours * self.hourly_rate

    class Meta:
        db_table = "employee_paychecks"


class UserRole(models.Model):
    """
    Represents the roles assigned to a user.
    Attributes:
        user (ForeignKey): A foreign key to the User model.
        role (CharField): The role assigned to the user, with a maximum length of 50 characters.
    """

    user = models.ForeignKey(Employee, on_delete=models.CASCADE)
    role = models.CharField(max_length=50)

    class Meta:
        """
        Meta class for defining model options.
        Attributes:
            db_table (str): The name of the database table to use for this model.
        """

        db_table = "user_roles"


class LeaveDetail(models.Model):
    """
    Represents the details of a leave request for an employee.
    Attributes:
        employee (ForeignKey): A foreign key to the Employee model.
        leave_type (CharField): The type of leave (e.g., Sick, Vacation).
        start_date (DateField): The start date of the leave.
        end_date (DateField): The end date of the leave.
        status (CharField): The status of the leave request (e.g., Approved, Pending).
    """

    LEAVE_TYPE_CHOICES = [
        ("Sick", "Sick Leave"),
        ("Vacation", "Vacation Leave"),
        ("Personal", "Personal Leave"),
        ("Emergency", "Emergency Leave"),
        ("Unpaid", "Unpaid Leave"),
    ]
    STATUS_CHOICES = [
        ("Submitted", "Submitted"),
        ("Pending Approval", "Pending Approval"),
        ("Approved", "Approved"),
        ("Denied", "Denied"),
    ]

    active = models.BooleanField(default=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=50, choices=LEAVE_TYPE_CHOICES)
    start_date = models.DateField(blank=False, null=False)
    end_date = models.DateField(blank=False, null=False)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    message = models.TextField(blank=True, null=True)

    class Meta:
        """
        Meta class for defining model options.
        Attributes:
            db_table (str): The name of the database table to use for this model.
        """

        db_table = "leave_details"
