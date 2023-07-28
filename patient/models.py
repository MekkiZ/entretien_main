import uuid
from datetime import date
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

LEG_FRACTURE = "F"
HEMATOMA = "H"
SORE = "S"
ANKLE_SPRAIN = "A"
KNEE_SPRAIN = "K"


class Patient(models.Model):
    """Patient model."""
    WOUND_CHOICES = (
        (LEG_FRACTURE, 'Leg Fracture'),
        (HEMATOMA, 'Hematoma'),
        (KNEE_SPRAIN, 'Knee Sprain'),
        (SORE, 'Sore'),
        (ANKLE_SPRAIN, 'Ankle Sprain'),
    )
    secret_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(_("First name"), max_length=50)
    last_name = models.CharField(_("Last name"), max_length=50)
    birthdate = models.DateField(_("Birth date"), auto_now=False, auto_now_add=False, null=True, blank=True)
    wound = models.CharField(max_length=1, choices=WOUND_CHOICES, null=True, blank=True)
    emergency = models.BooleanField(_("emergency"), default=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        today = date.today()
        self.today = today

    @property
    def fullname(self):
        """Return fullname."""
        r = ' '.join([i.capitalize() for i in self.first_name.split()])
        return f"{r} {self.last_name.upper()}"

    @property
    def birthdate_formatted(self):
        """Return formatted date."""
        return f"{self.birthdate.day}/{self.birthdate.month} {self.birthdate.year}"

    @property
    def age(self):
        """Get the patient's age."""

        if self.today.day >= self.birthdate.day and self.today.month >= self.birthdate.month:
            return self.today.year - self.birthdate.year

        return (self.today.year - self.birthdate.year) - 1

    def age_at_date(self, date_client_at_date):
        """
        Check age with date.
        param: Check age for date given.
        return: age type int or unborn if not
        """

        if (self.birthdate.year <= date_client_at_date.year and
                self.birthdate.month >= date_client_at_date.month and
                self.birthdate.day >= date_client_at_date.day):
            return (self.today.year - self.birthdate.year) + (date_client_at_date.year - self.today.year) - 1
        else:
            return 'unborn'

    @property
    def has_majority(self):
        """Patient is major."""
        if (self.today.year - self.birthdate.year) >= 18:
            return True
        else:
            return False

    def is_wounded(self):
        """Is the patient is wounded."""
        return [choice[1] for choice in self.WOUND_CHOICES] # on choici l'index [1] pour la valeur

    def break_his_leg(self):
        """Call this function to break patient leg."""

    def can_walk(self):
        pass

