from django.db import models


class TimeSlot(models.Model):
    id = models.AutoField(primary_key=True)
    year = models.IntegerField(db_index=True)
    week = models.IntegerField(db_index=True)
    day = models.IntegerField(db_index=True)
    booked_slot = models.BooleanField(default=False)
    user_id = models.CharField(max_length=255, null=True, default=None)

    def __str__(self):
        return f"{self.year, self.week, self.day, self.booked_slot, self.user_id}"

    class Meta:
        db_table = 'time_slots'
        indexes = [
            models.Index(fields=['user_id'], name='user_id_idx'),
        ]


class User(models.Model):
    id = models.CharField(max_length=255, primary_key=True, unique=True, db_index=True)
    email = models.CharField(max_length=255, unique=True, db_index=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.email, self.name}"

    class Meta:
        db_table = "users"
