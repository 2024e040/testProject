from django.test import TestCase
from .models import WorkoutLog

class WorkoutModelTest(TestCase):
    def test_str_representation(self):
        
        log = WorkoutLog.objects.create(name='ベンチプレス', weight=60, reps=10)

        
        output = str(log)

    
        self.assertEqual(output, 'ベンチプレス: 60kg x 10回')
