from django.db import transaction
from rest_framework.exceptions import ValidationError

from restapi.models import (
    Event,
    EventSchedule,
    EventEquipment,
    EventParameter,
    Department,
    Employee,
    Equipments,
    EquipmentDetails,
    Parameters,
)

# =========================
# SCHEDULE TYPE CONSTANTS
# =========================
ONE_TIME = 1
DAILY = 2
WEEKLY = 3
MONTHLY = 4
SEMIANNUAL = 5
PER_USE = 6


# ---------------- VALIDATION ----------------
def validate_event_create(serializer, attrs):

    # =========================
    # Department
    # =========================
    department = Department.objects.get(id=attrs["department_id"])

    # =========================
    # Assignment
    # =========================
    assignment = (
        Employee.objects.get(id=attrs["assignment_id"])
        if attrs.get("assignment_id")
        else serializer.context["request"].user.employee
    )

    equipment_details_ids = attrs.get("equipment_details_ids", [])
    parameter_ids = attrs.get("parameter_ids", [])

    # =========================
    # VALIDATE EQUIPMENT DETAILS
    # =========================
    equipment_details = EquipmentDetails.objects.filter(
        id__in=equipment_details_ids,
        equipment__dep=department,
        is_active=True
    )

    if equipment_details.count() != len(set(equipment_details_ids)):
        raise ValidationError("Invalid equipment details selection")

    # =========================
    # DERIVE EQUIPMENTS (MASTER)
    # =========================
    equipments = Equipments.objects.filter(
        id__in=equipment_details.values_list("equipment_id", flat=True),
        is_active=True,
        is_deleted=False
    )

    # =========================
    # VALIDATE PARAMETERS
    # =========================
    parameters = Parameters.objects.filter(
        id__in=parameter_ids,
        is_active=True
    )

    invalid = parameters.exclude(equipment__in=equipments)

    if invalid.exists():
        raise ValidationError(
            "Parameters must belong to selected equipments"
        )

    # =========================
    # VALIDATE SCHEDULE
    # =========================
    schedule = attrs.get("schedule", {})
    schedule_type = schedule.get("type")

    if schedule_type not in [1,2,3,4,5,6]:
        raise ValidationError("Invalid schedule type")

    # ONE TIME
    if schedule_type == ONE_TIME:
        if not schedule.get("one_time_date"):
            raise ValidationError("one_time_date required for one-time events")

    # DAILY
    elif schedule_type == DAILY:
        if not schedule.get("start_date"):
            raise ValidationError("start_date required for daily schedule")

    # WEEKLY
    elif schedule_type == WEEKLY:
        if not schedule.get("days"):
            raise ValidationError("days required for weekly schedule")

    # MONTHLY
    elif schedule_type == MONTHLY:
        if not schedule.get("months"):
            raise ValidationError("months required for monthly schedule")

    # SEMIANNUAL
    elif schedule_type == SEMIANNUAL:
        if not schedule.get("months"):
            raise ValidationError("months required for semiannual schedule")

    # PER USE
    elif schedule_type == PER_USE:
        # No schedule validation needed
        pass

    
    
    # Store validated objects
    attrs["department"] = department
    attrs["assignment"] = assignment
    attrs["equipment_details"] = equipment_details
    attrs["parameters"] = parameters

    return attrs


# ---------------- CREATE ----------------
@transaction.atomic
def create_event(validated_data):
    event = Event.objects.create(
        department=validated_data["department"],
        assignment=validated_data["assignment"],
        event_name=validated_data["event_name"],
        description=validated_data["description"]
    )

    # Create schedule
    EventSchedule.objects.create(
        event=event,
        **validated_data["schedule"]
    )

    # Link equipment details
    for ed in validated_data["equipment_details"]:
        EventEquipment.objects.create(
            event=event,
            equipment_details=ed
        )

    # Link parameters
    for p in validated_data["parameters"]:
        EventParameter.objects.create(
            event=event,
            parameter=p
        )

    return event
