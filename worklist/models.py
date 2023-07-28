from django.db import models


class Worklist(models.Model):
    MAX_USERS = 10  # maximum users to display