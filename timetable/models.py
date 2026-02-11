# timetable/models.py
from django.db import models
from django.core.exceptions import ValidationError

class Department(models.Model):
    name = models.CharField(max_length=100)
    # New Field: Track which semester is currently active for this department
    active_semester = models.CharField(max_length=20, default='Semester 1')
    
    def __str__(self):
        return self.name

class Faculty(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.name

class TimetableEntry(models.Model):
    DAY_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
    ]
    
    SEMESTER_CHOICES = [
        ('Semester 1', 'Semester 1'),
        ('Semester 2', 'Semester 2'),
        ('Semester 3', 'Semester 3'),
        ('Semester 4', 'Semester 4'),
        ('Semester 5', 'Semester 5'),
        ('Semester 6', 'Semester 6'),
    ]
    
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, blank=True)
    subject = models.CharField(max_length=100)
    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    semester = models.CharField(max_length=20, choices=SEMESTER_CHOICES, default='Semester 1')
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    class Meta:
        verbose_name_plural = "Timetable Entries"
    
    # timetable/models.py

def clean(self):
    if self.start_time and self.end_time and self.start_time >= self.end_time:
        raise ValidationError("End time must be after start time.")
    
    if self.faculty:
        # Check against the active semester of the target department
        conflicts = TimetableEntry.objects.filter(
            faculty=self.faculty,
            day=self.day,
            # This ensures Sem 1 doesn't block Sem 2 if Sem 2 is active
            semester=self.department.active_semester, 
            start_time__lt=self.end_time,
            end_time__gt=self.start_time
        ).exclude(id=self.id)
        
        if conflicts.exists():
            conflict = conflicts.first()
            raise ValidationError(
                f"CONFLICT: {self.faculty.name} is already teaching "
                f"in {conflict.department.name} ({conflict.semester})."
            )
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.department.name} - {self.semester} - {self.subject}"

class TimetableHistory(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    semester = models.CharField(max_length=50)
    year = models.IntegerField()
    data_snapshot = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Timetable Histories"
        ordering = ['-year', '-created_at']
    
    def __str__(self):
        return f"{self.department.name} - {self.semester} ({self.year})"