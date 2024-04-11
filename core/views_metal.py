import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods,require_POST

from .forms import MetalForm
from .models import Jobs, Metalextractiondata, Metal, Metalleachresult, Totalbalanceresult

from . import compmodule2 as comp

import random
from datetime import datetime

def metals(request):
    if request.method == 'POST':
        form = MetalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('materials_crud')  # Adjust the redirect to your named URL for this view
    else:
        form = MetalForm()
    metals = Metalextractiondata.objects.all()
    return render(request, 'metals_crud.html', {'metals': metals, 'form': form})

@csrf_exempt
def metal_calculations(request):
    if request.method == 'POST':
        # Инициализация класса MetalLeaching с последним объектом из Metal
        last_metal = Metal.objects.last()
        metal_leaching = comp.MetalLeaching(ore_mass=last_metal.ore_mass, metal_content=last_metal.metal_content)
        
        # Получение всех данных из Metalextractiondata и конвертация в нужный формат
        extraction_data = Metalextractiondata.objects.all().values()
        daily_data = list(extraction_data)
        # Вычисление результатов
        results = metal_leaching.calculate(daily_data)
        totals = metal_leaching.calculate_total_balance()
        # Здесь должен быть ваш код для сохранения результатов в MetalLeachResult
        # Пример сохранения одного из результатов
        # Это условный пример, вам нужно адаптировать его под вашу логику

        random_job_name = "Job_" + str(random.randint(1000, 9999))
        job = Jobs(name=random_job_name)
        job.save()
        
        job_instance = Jobs.objects.get(id=job.id)
        
        for i in range(len(results['extraction'])):
            Metalleachresult.objects.create(
                day=i+1,
                extraction_efficiency=results['extraction'][i],
                c_cu_organic_depleted=results['depleted'][i],
                c_cu_organic_rich=results['rich'][i],
                re_extraction_efficiency_organic=results['re_extracton_organic'][i],
                re_extraction_efficiency_electrolyte=results['re_extraction_electrolyte'][i],
                cu_gain=results['gain'][i],
                total_accumulated_cu=results['total_accumulated_cu_mass'][i],
                total_cu_recovery=results['total_cu_recovery_percent'][i],
                overall_extraction_efficiency=results['overall_extraction_efficiency'][i],
                job = job_instance
            )
        
        Totalbalanceresult.objects.create(in_raf_percent = totals['in_raf_percent'], in_electrolyte_percent = totals['in_electrolyte_percent'], 
                                          in_katods_percent = totals['in_katods_percent'], in_organics_percent = totals['in_organics_percent'], 
                                          ore_remain_percent = totals['ore_remain_percent'], job=job_instance)
        # Перенаправление на страницу результатов или обновление страницы
        return redirect('metal_results')  # Используйте имя URL для перенаправления

    # Для GET запроса просто отображаем данные
    extraction_data = Metalextractiondata.objects.all()
    return render(request, 'metal_calculations.html', {'extraction_data': extraction_data})


def metal_results(request):
    return render(request, 'metal_results.html', {'results': Metalleachresult.objects.all(), 'totals': Totalbalanceresult.objects.all()})