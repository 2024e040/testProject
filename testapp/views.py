import requests
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post 
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from rest_framework import generics
from .serializers import PostSerializer
from django.http import JsonResponse
from django.db.models import Prefetch

def timeline(request):
    query = request.GET.get('q')

    # N+1対策（authorとlikesを事前に取得）
    base_qs = Post.objects.select_related('author').prefetch_related('likes').order_by('-created_at')

    if query:
        # 検索時も最適化されたクエリをベースにする
        posts = base_qs.filter(content__icontains=query)
    else:
        posts = base_qs

    context = {
        'posts': posts,
        'query': query, 
    }
    
    return render(request, 'timeline.html', context)

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk) 
    return render(request, 'post_detail.html', {'post': post})


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('timeline') 
    else:
        form = PostForm()
    
    return render(request, 'post_create.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:
        return redirect('post_detail', pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'post_edit.html', {'form': form, 'post': post})
    
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:
        return redirect('post_detail', pk=pk)

    if request.method == 'POST':
        post.delete()
        return redirect('timeline')
    return render(request, 'post_confirm_delete.html', {'post': post}) 

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

class PostListAPIView(generics.ListAPIView):
    # どのデータの一覧を返すか
    queryset = Post.objects.all()
    # どの翻訳者(シリアライザ)を使ってJSONに変換するか
    serializer_class = PostSerializer

@login_required  # ログイン必須 [cite: 77]
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user = request.user

    # トグル処理：既にいいねしていれば解除、していなければ追加 [cite: 84]
    if post.likes.filter(id=user.id).exists():
        post.likes.remove(user)
        liked = False
    else:
        post.likes.add(user)
        liked = True
    context = {
        'liked': liked,
        'count': post.total_likes(),
    }
    
    return JsonResponse(context)


def weather(request):
    
    locations = {
        'Kanazawa': {'lat': 36.59, 'lon': 136.60},
        'Tokyo':    {'lat': 35.68, 'lon': 139.76},
        'Osaka':    {'lat': 34.69, 'lon': 135.50},
        'Sapporo':  {'lat': 43.06, 'lon': 141.35},
        'Naha':     {'lat': 26.21, 'lon': 127.68},
    }

    
    city_name = 'Kanazawa'
    if request.GET.get('city') and request.GET.get('city') in locations:
        city_name = request.GET.get('city')

    
    lat = locations[city_name]['lat']
    lon = locations[city_name]['lon']

    
    api_url = f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true'

    
    response = requests.get(api_url)
    data = response.json()

    
    context = {
        'city': city_name,
        'temperature': data['current_weather']['temperature'],
        'windspeed': data['current_weather']['windspeed'],
        'weathercode': data['current_weather']['weathercode'],
    }

    return render(request, 'weather.html', context)

import requests
from django.shortcuts import render

def pokemon_viewer(request):
    # ユーザーが入力したポケモン名を取得（デフォルトは'pikachu'）
    pokemon_name = request.GET.get('pokemon_name', 'pikachu').lower()

    # APIのエンドポイントURL
    api_url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}'
    
    # データを格納する辞書
    context = {}
    
    try:
        # APIにリクエストを送信
        response = requests.get(api_url)
        
        # ステータスコードが200（成功）以外の場合はエラーとして処理
        if response.status_code != 200:
            context['error_message'] = f'ポケモン "{pokemon_name}" が見つかりませんでした。'
            # テンプレートに渡すために、リクエストした名前は保持しておく
            context['pokemon_name'] = pokemon_name 
            return render(request, 'pokemon.html', context)
        
        # JSONデータをPythonの辞書に変換
        data = response.json()
        
        # 必要な情報を抽出
        context = {
            # 表示用に、名前の最初の文字を大文字にする
            'name': data['name'].capitalize(),
            # ポケモンの図鑑番号（ID）
            'id': data['id'],
            # 画像（フロントスプライト）のURL
            'image_url': data['sprites']['front_default'],
            # ポケモンのタイプをリストで取得（例: ['electric']）
            'types': [t['type']['name'].capitalize() for t in data['types']],
            # ステータス（HP, 攻撃, 防御など）をリストで取得
            'stats': [
                {'name': s['stat']['name'].capitalize(), 'value': s['base_stat']}
                for s in data['stats']
            ],
            'pokemon_name': pokemon_name # フォームの初期値として使用
        }
        
    except requests.exceptions.RequestException:
        # ネットワークエラーなどの例外処理
        context['error_message'] = 'APIへの接続中にエラーが発生しました。'
        context['pokemon_name'] = pokemon_name 

    return render(request, 'pokemon.html', context)

# app/views.py
posts = Post.objects.select_related('author').prefetch_related('likes').order_by('-created_at')