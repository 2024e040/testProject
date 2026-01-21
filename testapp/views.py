from django.shortcuts import render, redirect
from .models import TrainingRecord
from .forms import RecordForm
import json

def dashboard(request):
    if request.method == 'POST':
        form = RecordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = RecordForm()

    records = TrainingRecord.objects.all().order_by('-date')
    
    # グラフ用データ（ベンチプレスを含む種目を抽出）
    bench_data = TrainingRecord.objects.filter(name__contains='ベンチ').order_by('date')
    dates_list = [record.date.strftime('%Y-%m-%d') for record in bench_data]
    weights_list = [record.one_rm for record in bench_data]

    context = {
        'form': form,
        'records': records,
        'graph_dates': json.dumps(dates_list),
        'graph_weights': json.dumps(weights_list),
    }
    return render(request, 'testapp/dashboard.html', context)