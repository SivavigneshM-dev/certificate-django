from django.db import models

class Certificate(models.Model):
    student_name = models.CharField(max_length=255)
    course_title = models.CharField(max_length=255)
    student_image = models.ImageField(upload_to='certificates/images/' , null=True)
    project_link = models.URLField(max_length=200, blank=True, null=True)
    certificate_file = models.FileField(upload_to='certificates/files/' , null=True)
    

    def __str__(self):
        return f"{self.student_name} - {self.course_title}"
