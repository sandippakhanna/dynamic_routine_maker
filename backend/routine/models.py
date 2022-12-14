from django.db import models
from accounts.models import UserAccount
from django.core.validators import MinLengthValidator


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Routine(BaseModel):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    name = models.CharField(
        max_length=100,
        verbose_name="Routine Name",
        validators=[MinLengthValidator(4)],
    )
    slug = models.SlugField(
        max_length=110,
        null=True,
        blank=True,
        validators=[MinLengthValidator(4)],
    )

    def __str__(self):
        return str(self.name)

    def get_classes_by_day(self, day: int):
        return Class.objects.filter(routine=self, day=day).order_by(
            "start_time"
        )


class Class(BaseModel):
    SUNDAY = 0
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6

    day_choices = (
        (SUNDAY, "Sunday"),
        (MONDAY, "Monday"),
        (TUESDAY, "Tuesday"),
        (WEDNESDAY, "Wednesday"),
        (THURSDAY, "Thursday"),
        (FRIDAY, "Friday"),
        (SATURDAY, "Saturday"),
    )

    routine = models.ForeignKey(Routine, on_delete=models.CASCADE)
    day = models.PositiveIntegerField(choices=day_choices)
    start_time = models.TimeField()
    end_time = models.TimeField()
    subject = models.CharField(max_length=100)
    teacher_short_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.subject} on {self.day} in {self.routine.name}"
