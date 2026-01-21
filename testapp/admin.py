from django.contrib import admin
from .models import TrainingRecord

# 管理画面でデータをいじれるように登録
admin.site.register(TrainingRecord)
