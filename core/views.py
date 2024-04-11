import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods,require_POST

from .forms import MaterialsForm
from .models import Materials, Jobs, Materialsjobs, Stein, Slag

from . import pvbalch_computing_module as pvcm

import random
from datetime import datetime

def index(request):
    steins = Materials.objects.all()
    context = {
        'steins': steins,
    }
    return render(request, 'index.html', context)


@csrf_exempt
@require_POST
def update_material(request):
    try:
        data = json.loads(request.body)
        material = Materials.objects.get(id=data['id'])
        field_name = data['field']
        value = data['value']
        value = value.replace(',', '.')
        print(field_name, value, type(value))

        if field_name == 'name0':
            setattr(material, field_name, value)
        else:
            try:
                # Attempt to convert to float for numerical fields
                converted_value = float(value)
                setattr(material, field_name, converted_value)
            except ValueError:
                # Specific field name included in the error message
                return JsonResponse({'status': 'error', 'message': f'Invalid input for numerical field: {field_name}'})

        material.save()
        return JsonResponse({'status': 'success'})
    except Materials.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Material not found'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


def materials_create_and_list(request):
    if request.method == 'POST':
        form = MaterialsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('materials_crud')  # Adjust the redirect to your named URL for this view
    else:
        form = MaterialsForm()
    materials = Materials.objects.all()
    return render(request, 'materials_crud.html', {'materials': materials, 'form': form})


def calculate_with_materials(request):
    if request.method == 'POST':
        selected_material_ids = request.POST.getlist('selected_materials')
        materials_data = list(Materials.objects.filter(id__in=selected_material_ids).values(
            'name0', 'Weight', 'Au', 'Ag', 'SiO2', 'CaO', 'S', 'Fe', 'Cu', 'Al2O3', 'As0'
        ))
        print(materials_data)
        
        random_job_name = "Job_" + str(random.randint(1000, 9999))
        job = Jobs(name=random_job_name)
        job.save()

        for m_id in selected_material_ids:
            job_instance = Jobs.objects.get(id=job.id)
            material_instance = Materials.objects.get(id=m_id)  # Retrieve the material instance by its ID
            # Create a MaterialsJobs instance properly
            mj = Materialsjobs(job=job_instance, material=material_instance)
            mj.save()

        
        compounds = [pvcm.Compound(**comp_data) for comp_data in materials_data]

        #Суммарный полный вес всех компонентов
        total_weight = sum(compound.Weight for compound in compounds)

        #Словарь, содержащий общий вес каждого элемента, собранный из всех компонентов
        #В формате элемент:вес, типа {'Au':40.22, 'Cu':288.11}
        total_elements = pvcm.calculate_total_elements(compounds)

        #Процентное соотношение каждого элемента в отношении к total_weight
        element_percentages = pvcm.calculate_element_percentages(total_elements, total_weight)

        #Вычисления параметров штейна и шлака
        stein_results = pvcm.calculate_materials_in_stein(total_elements, total_weight, element_percentages)
        slug_results = pvcm.calculate_materials_in_slug(total_elements, stein_results)

        print(stein_results, slug_results)
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        stein = Stein(Gold=slug_results['gold_concentration_stein'], Silver=slug_results['silver_concentration_stein'], Weight=stein_results['stein_weight'],
                        Copper=stein_results['Cu_in_stein_percentage'], Iron=stein_results['Fe_in_stein_percentage'], Sulfur=stein_results['S_in_stein_percentage'], 
                        job=job_instance, created_at=now)
        stein.save()

        slag = Slag(SiO2=slug_results['SiO2_in_slag_percentage'], CaO=slug_results['CaO_in_slag_percentage'], Al2O3=slug_results['Al2O3_in_slag_percentage'], 
                        FeO=slug_results['FeO_in_slag_percentage'], Weight=slug_results['slag_weight'], job=job_instance, created_at=now)
        slag.save()
        return render(request, 'calculation_results.html', {'stein_results':job.stein_set.values(), 'slag_results':job.slag_set.values()})

    else:
        materials = Materials.objects.all()
        return render(request, 'materials_selection.html', {'materials': materials})



def show_all_results(request):
    # Fetch all records from Stein and Slag models
    stein_results = Stein.objects.all()
    slag_results = Slag.objects.all()
    
    # Pass them to the template context
    return render(request, 'calculation_results.html', {
        'stein_results': stein_results,
        'slag_results': slag_results
    })

@csrf_exempt
@require_http_methods(["DELETE"])
def delete_material(request, material_id):
    try:
        material = Materials.objects.get(id=material_id)
        material.delete()
        return JsonResponse({'status': 'success'})
    except Materials.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Material not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)