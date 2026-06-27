from django.db import models



# Create your models here.

class Judge(models.Model):
    judge_id = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=100)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)  # Store hashed passwords in production
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name
    


class Team(models.Model):
    team_id = models.CharField(max_length=20, unique=True)
    team_name = models.CharField(max_length=150)

    def __str__(self):
        return self.team_id
        
class Evaluation(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    judge = models.ForeignKey(Judge, on_delete=models.CASCADE)

    innovation = models.PositiveSmallIntegerField()
    problem_understanding = models.PositiveSmallIntegerField()
    technical_implementation = models.PositiveSmallIntegerField()
    ui_ux = models.PositiveSmallIntegerField()
    completeness = models.PositiveSmallIntegerField()
    practical_demo = models.PositiveSmallIntegerField()
    presentation = models.PositiveSmallIntegerField()
    impact = models.PositiveSmallIntegerField()

    total = models.PositiveSmallIntegerField(default=0)

    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('team', 'judge')

    def save(self, *args, **kwargs):
        self.total = (
            self.innovation +
            self.problem_understanding +
            self.technical_implementation +
            self.ui_ux +
            self.completeness +
            self.practical_demo +
            self.presentation +
            self.impact
        )
        super().save(*args, **kwargs)



class JudgeAssignment(models.Model):
    judge = models.ForeignKey(Judge, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("judge", "team")
