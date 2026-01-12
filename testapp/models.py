from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    # --- 1. 投稿データ (既存機能) ---
    # 投稿者: Userモデルと紐付け
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # 投稿内容
    content = models.TextField()
    # 投稿日時: 自動記録
    created_at = models.DateTimeField(auto_now_add=True)
    
    # --- 2. 講義資料での追加部分 (いいね機能など) ---
    # タイトル (講義資料に記載があるため追加、エラー回避用にデフォルト値を設定)
    title = models.CharField(max_length=200, default='No Title')
    
    # [cite_start]★重要: いいね機能用の多対多フィールド [cite: 58, 59]
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    # --- メソッド定義 ---
    def __str__(self):
        # 管理画面での表示用
        return f'{self.author.username}: {self.content[:20]}'

    # [cite_start]いいね総数を返すメソッド [cite: 60, 61]
    def total_likes(self):
        return self.likes.count()
    
from django.db import models

class WorkoutLog(models.Model):
    name = models.CharField(max_length=100)  # 種目名（例：ベンチプレス）
    weight = models.IntegerField()           # 重量（kg）
    reps = models.IntegerField()             # 回数

    def __str__(self):
        # 画面に表示される時の形式を定義
        return f"{self.name}: {self.weight}kg x {self.reps}回"