from django.db import models

class TrainingRecord(models.Model):
    PART_CHOICES = [
        ('chest', '胸'), ('back', '背中'), ('legs', '脚'),
        ('shoulders', '肩'), ('arms', '腕'), ('abs', '腹筋'),
    ]
    date = models.DateField(verbose_name='日付')
    part = models.CharField(max_length=20, choices=PART_CHOICES, verbose_name='部位')
    name = models.CharField(max_length=100, verbose_name='種目名')
    weight = models.FloatField(verbose_name='重量(kg)')
    reps = models.IntegerField(verbose_name='回数')
    one_rm = models.FloatField(verbose_name='推定1RM', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.weight and self.reps:
            self.one_rm = round(self.weight * (1 + self.reps / 30), 1)
        super().save(*args, **kwargs)