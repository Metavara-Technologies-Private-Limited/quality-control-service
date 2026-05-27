from django.db import models
from .department import Department
from .employee import Employee
from .parameter import Parameters
from .equipment import EquipmentDetails

# =========================
# Event
# =========================
class Event(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    assignment = models.ForeignKey(  # assignment_id
        Employee,
        on_delete=models.CASCADE
    )
    event_name = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


# =========================
# Event ↔ Equipment
# =========================
class EventEquipment(models.Model):
    event = models.ForeignKey("Event", on_delete=models.CASCADE)
    equipment_details = models.ForeignKey(
        "EquipmentDetails",
        on_delete=models.CASCADE,
        related_name="event_equipments",
        null=True  # keep for now (safe for existing rows)
    )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("event", "equipment_details")


# =========================
# Event Schedule
# =========================
class EventSchedule(models.Model):

    ONE_TIME = 1
    DAILY = 2
    WEEKLY = 3
    MONTHLY = 4
    SEMIANNUAL = 5
    PER_USE = 6

    TYPE_CHOICES = (
        (ONE_TIME, "One Time Event"),
        (DAILY, "Daily Event"),
        (WEEKLY, "Weekly Event"),
        (MONTHLY, "Monthly Event"),
        (SEMIANNUAL, "Semiannual Event"),
        (PER_USE, "Per Use Event"),
    )

    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    type = models.IntegerField(
        choices=TYPE_CHOICES
    )

    from_time = models.DateTimeField(null=True, blank=True)
    to_time = models.DateTimeField(null=True, blank=True)

    one_time_date = models.DateTimeField(null=True, blank=True)

    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)

    months = models.JSONField(null=True, blank=True)
    days = models.JSONField(null=True, blank=True)

    recurring_duration = models.IntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


# =========================
# Assignee ↔ Event
# =========================
class AssigneeEvent(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    assignment = models.ForeignKey(  # assignment_id
        Employee,
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("event", "assignment")


# =========================
# Event ↔ Parameter
# =========================
class EventParameter(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    parameter = models.ForeignKey(Parameters, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("event", "parameter")

