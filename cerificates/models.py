import uuid
from django.db import models
from django.contrib.auth.models import User


class Certificate(models.Model):
    STATUS_CHOICES = [
        ('valid', 'Valid'),
        ('revoked', 'Revoked'),
    ]

    certificate_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        null=True,
        blank=True
    )
    student_name     = models.CharField(max_length=200)
    course_title     = models.CharField(max_length=300)
    issue_date      = models.DateField()
    status           = models.CharField(max_length=10, choices=STATUS_CHOICES, default='valid')
    student_image    = models.ImageField(upload_to='certificates/images/', blank=True, null=True)
    certificate_file = models.FileField(upload_to='certificates/files/', blank=True, null=True)
    project_link     = models.URLField(blank=True, null=True)
    created_at       = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student_name} — {self.course_title}"

    class Meta:
        ordering = ['-created_at']