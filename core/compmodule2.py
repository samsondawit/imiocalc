class MetalLeaching:
    def __init__(self, ore_mass, metal_content):
        """
        Инициализация класса для расчёта извлечения металла из руды.
        :param ore_mass: масса исходной руды (в граммах)
        :param metal_content: содержание металла в руде (%)
        """
        self.ore_mass = ore_mass
        self.metal_content = metal_content
        #init_metal_mass: количество металла в руде (в граммах)
        self.init_metal_mass = round(self.ore_mass * self.metal_content / 100, 2)
    
    def calculate_metal_extraction(self, daily_data):
        """
        Расчет процентов извлечения металла из руды для каждого дня.
        :param daily_data: двумерный список, где каждый внутренний список содержит 
                           [концентрация металла в продуктивном растворе (г/л), объем продуктивного раствора (л)]
        :return: Список процентов извлечения металла за каждый день.
        """
        extraction_percentages = []
        for day_data in daily_data:
            metal_concentration, solution_volume = day_data
            extracted_metal_mass = metal_concentration * solution_volume
            extraction_percentage = (extracted_metal_mass / self.init_metal_mass) * 100
            extraction_percentages.append(round(extraction_percentage, 2))
        return extraction_percentages

    def calculate_metal_extraction_with_addons(self, daily_data, initial_cumulative_extraction=0):
        """
        Расчет процентов извлечения металла из руды для каждого дня, учитывая накопленное извлечение.
        :param daily_data: двумерный список, где каждый внутренний список содержит 
                        [концентрация металла в продуктивном растворе (г/л), объем продуктивного раствора (л)]
        :param cumulative_extraction: Накопленный процент извлечения до начала этой серии измерений.
        :return: Список процентов извлечения металла за каждый день.
        """
        extraction_percentages = []
        for day_data in daily_data:
            cumulative_extraction = initial_cumulative_extraction
            metal_concentration, solution_volume = day_data
            extracted_metal_mass = metal_concentration * solution_volume
            daily_extraction_percentage = (extracted_metal_mass / self.init_metal_mass) * 100
            cumulative_extraction += daily_extraction_percentage
            extraction_percentages.append(round(cumulative_extraction, 2))
        return extraction_percentages
    

    def calculate(self, daily_data):
        """
        Делает ВСЕ!

        :param daily_data: Список словарей, каждый из которых содержит данные для одного дня.
                           Ключи в словаре: 'c_cu_prod', 'v_prod', 'c_cu_raf', 'c_cu_electrolyte_rich',
                           'v_electrolyte_rich', 'v_organic'.
        :return: Словарь с двумя ключами 'depleted' и 'rich', которые содержат списки концентраций для каждого дня.
        """
        
        self.daily_data = daily_data

        results = {
            'extraction': [], 'depleted': [], 'rich': [], 're_extracton_organic': [], 're_extraction_electrolyte': [],
            'gain': [], 'total_accumulated_cu_mass': [], 'total_cu_recovery_percent': [], 'overall_extraction_efficiency': [], 
            }
        
        c_cu_electrolyte_rich_prev = v_electrolyte_rich_prev = c_cu_organic_depleted_prev = c_cu_raf_prev = v_prod_prev = 0
        gain_prev = total_accumulated_cu_mass_prev = re_extraction_eff_el_prev = re_extraction_eff_org_prev = 0

        total_accumulated_cu_mass = 0
        
        for day in daily_data:
            #Распаковка переменных для дня
            c_cu_prod = day['c_cu_prod']
            c_cu_raf = day['c_cu_raf']
            v_prod = day['v_prod']
            c_cu_electrolyte_rich = day['c_cu_electrolyte_rich']
            v_electrolyte_rich = day['v_electrolyte_rich']
            v_organic = day['v_organic']
            c_cu_electrolyte_depleted = day['c_cu_electrolyte_depleted']
            v_electrolyte_depleted = day['v_electrolyte_depleted']
            

            #Вычисляем эффективность экстракции
            extraction_eff = (c_cu_prod - c_cu_raf) / c_cu_prod * 100
            results['extraction'].append(round(extraction_eff, 2))

            # Вычисляем концентрацию в обедненной органической фазе
            metal_transferred = (
                c_cu_prod * v_prod - c_cu_raf * v_prod
            ) - (
                c_cu_electrolyte_rich * v_electrolyte_rich - c_cu_electrolyte_rich_prev * v_electrolyte_rich_prev
            ) - gain_prev
            c_cu_organic_depleted = (metal_transferred / v_organic) + c_cu_organic_depleted_prev
            results['depleted'].append(round(c_cu_organic_depleted, 2))
            
            # Вычисляем концентрацию в богатой органической фазе
            metal_balance = (c_cu_prod * v_prod - c_cu_raf * v_prod)
            c_cu_organic_rich = (metal_balance / v_organic) + c_cu_organic_depleted_prev
            results['rich'].append(round(c_cu_organic_rich, 2))
            
            #Вычисляем эффективность pe-экстракции в органике
            try:
                re_extraction_eff_org = (c_cu_electrolyte_rich * v_electrolyte_rich - c_cu_electrolyte_rich_prev * v_electrolyte_rich_prev + gain_prev) / (c_cu_organic_rich * v_organic) * 100
            except ZeroDivisionError:
                re_extraction_eff_org = 0
            finally:
                results['re_extracton_organic'].append(round(re_extraction_eff_org, 2))

            #Вычисляем эффективность pe-экстракции в электролите   
            # re_extraction_eff_el = (c_cu_electrolyte_rich * v_electrolyte_rich - c_cu_electrolyte_rich_prev * v_electrolyte_rich_prev - c_cu_raf_prev * v_prod_prev) / (c_cu_prod * v_prod) * 100
            re_extraction_eff_el = (c_cu_electrolyte_rich * v_electrolyte_rich - c_cu_electrolyte_rich_prev * v_electrolyte_rich_prev + gain_prev) / (c_cu_prod * v_prod) * 100
            results['re_extraction_electrolyte'].append(round(re_extraction_eff_el, 2))
            
            #Прирост m+Cu-катод, г
            if c_cu_electrolyte_depleted == 0 and v_electrolyte_depleted == 0:
                gain = 0
            else:
                gain = c_cu_electrolyte_rich * v_electrolyte_rich - c_cu_electrolyte_depleted * v_electrolyte_depleted
            results['gain'].append(round(gain, 2))

            #Общая масса накопленной Cu, г
            # total_accumulated_cu_mass = gain+gain_prev
            total_accumulated_cu_mass += gain
            results['total_accumulated_cu_mass'].append(round(total_accumulated_cu_mass, 2))

            #Сквозное извлечение меди из руды до металла, %
            total_cu_recovery_percent = total_accumulated_cu_mass / self.init_metal_mass * 100
            results['total_cu_recovery_percent'].append(round(total_cu_recovery_percent, 2))

            #Общее итоговое извлечение, ЕИ, %
            if re_extraction_eff_el_prev == 0 and re_extraction_eff_org_prev == 0:
                overall_extraction_efficiency = (c_cu_prod * v_prod) / self.init_metal_mass * 100
            else:
                overall_extraction_efficiency = (c_cu_prod * v_prod - c_cu_raf_prev * v_prod_prev + c_cu_electrolyte_rich_prev * v_electrolyte_rich_prev + total_accumulated_cu_mass_prev) / self.init_metal_mass * 100
            results['overall_extraction_efficiency'].append(round(overall_extraction_efficiency, 2))

            # Обновляем значения для следующего дня
            c_cu_electrolyte_rich_prev = c_cu_electrolyte_rich
            v_electrolyte_rich_prev = v_electrolyte_rich
            c_cu_organic_depleted_prev = c_cu_organic_depleted
            c_cu_raf_prev = c_cu_raf
            v_prod_prev = v_prod
            gain_prev = gain
            total_accumulated_cu_mass_prev = total_accumulated_cu_mass
            re_extraction_eff_org_prev = re_extraction_eff_org
            re_extraction_eff_el_prev = re_extraction_eff_el

        self.results = results

        return results
    
    def calculate_total_balance(self):
        c_cu_raf_last = self.daily_data[-1]['c_cu_raf']
        v_prod_last = self.daily_data[-1]['v_prod']
        c_cu_electrolyte_depleted_last = self.daily_data[-1]['c_cu_electrolyte_depleted']
        v_electrolyte_depleted_last = self.daily_data[-1]['v_electrolyte_depleted']
        depleted_last = self.results['depleted'][-1]
        v_organic_last = self.daily_data[-1]['v_organic']
        total_accumulated_cu_mass_last = results['total_accumulated_cu_mass'][-1]

        in_raf_percent = c_cu_raf_last * v_prod_last / self.init_metal_mass * 100
        in_electrolyte_percent = c_cu_electrolyte_depleted_last * v_electrolyte_depleted_last / self.init_metal_mass * 100
        in_organics_percent = depleted_last * v_organic_last / self.init_metal_mass * 100
        in_katods_percent = total_accumulated_cu_mass_last / self.init_metal_mass * 100
        ore_remain_percent = 100 - in_electrolyte_percent - in_katods_percent - in_organics_percent - in_raf_percent
        totals = {
            'in_raf_percent': round(in_raf_percent, 2), 'in_electrolyte_percent': round(in_electrolyte_percent, 2), 'in_katods_percent': round(in_katods_percent, 2),
            'in_organics_percent': round(in_organics_percent, 2), 'ore_remain_percent': round(ore_remain_percent, 2)}
        return totals

    

# Пример использования:
# Создание объекта для меди
leaching = MetalLeaching(ore_mass=250000, metal_content=0.24)
daily_data = [[0.2, 5], [0.45, 4.85], [0.64, 4.9]]  # Примерные данные: [концентрация металла в г/л, объем в л] за каждый день

# extraction_percentages = leaching.calculate_metal_extraction(daily_data=daily_data)
# res = leaching.calculate_metal_extraction_with_addons(daily_data=[[0.2, 4.95], [0.35, 4.85]], initial_cumulative_extraction=23.09)
# print(extraction_percentages)
# print(res)




# Подготовка списка словарей с данными для каждого дня
# daily_data = [
#     {'c_cu_prod': 1.4, 'v_prod': 5, 'c_cu_raf': 0.2, 'c_cu_electrolyte_rich': 5.5, 'v_electrolyte_rich': 1, 'v_organic': 2.5},
#     {'c_cu_prod': 1.2, 'v_prod': 5, 'c_cu_raf': 0.15, 'c_cu_electrolyte_rich': 10.8, 'v_electrolyte_rich': 1, 'v_organic': 2.5},
#     {'c_cu_prod': 1.25, 'v_prod': 4.95, 'c_cu_raf': 0.14, 'c_cu_electrolyte_rich': 16.4, 'v_electrolyte_rich': 1, 'v_organic': 2.5},
# ]


final_data = [
    {'c_cu_prod': 0.5, 'v_prod': 40.0, 'c_cu_raf': 0.5, 'c_cu_electrolyte_rich': 0.0, 'v_electrolyte_rich': 5.0, 'v_organic': 5.0, 'c_cu_electrolyte_depleted': 0.0, 'v_electrolyte_depleted': 0.0},
    {'c_cu_prod': 0.65, 'v_prod': 40.0, 'c_cu_raf': 0.65, 'c_cu_electrolyte_rich': 0.0, 'v_electrolyte_rich': 5.0, 'v_organic': 5.0, 'c_cu_electrolyte_depleted': 0.0, 'v_electrolyte_depleted': 0.0},
    {'c_cu_prod': 0.8, 'v_prod': 39.5, 'c_cu_raf': 0.8, 'c_cu_electrolyte_rich': 0.0, 'v_electrolyte_rich': 5.0, 'v_organic': 5.0, 'c_cu_electrolyte_depleted': 0.0, 'v_electrolyte_depleted': 0.0},
    {'c_cu_prod': 0.9, 'v_prod': 39.0, 'c_cu_raf': 0.9, 'c_cu_electrolyte_rich': 0.0, 'v_electrolyte_rich': 5.0, 'v_organic': 5.0, 'c_cu_electrolyte_depleted': 0.0, 'v_electrolyte_depleted': 0.0},
    {'c_cu_prod': 1.05, 'v_prod': 38.5, 'c_cu_raf': 1.05, 'c_cu_electrolyte_rich': 0.0, 'v_electrolyte_rich': 5.0, 'v_organic': 5.0, 'c_cu_electrolyte_depleted': 0.0, 'v_electrolyte_depleted': 0.0},
    {'c_cu_prod': 1.1, 'v_prod': 40.0, 'c_cu_raf': 1.1, 'c_cu_electrolyte_rich': 0.0, 'v_electrolyte_rich': 5.0, 'v_organic': 5.0, 'c_cu_electrolyte_depleted': 0.0, 'v_electrolyte_depleted': 0.0},
    {'c_cu_prod': 1.15, 'v_prod': 40.0, 'c_cu_raf': 1.15, 'c_cu_electrolyte_rich': 0.0, 'v_electrolyte_rich': 5.0, 'v_organic': 5.0, 'c_cu_electrolyte_depleted': 0.0, 'v_electrolyte_depleted': 0.0},
    {'c_cu_prod': 1.2, 'v_prod': 39.5, 'c_cu_raf': 1.2, 'c_cu_electrolyte_rich': 0.0, 'v_electrolyte_rich': 5.0, 'v_organic': 5.0, 'c_cu_electrolyte_depleted': 0.0, 'v_electrolyte_depleted': 0.0},
    {'c_cu_prod': 1.3, 'v_prod': 40.0, 'c_cu_raf': 1.3, 'c_cu_electrolyte_rich': 0.0, 'v_electrolyte_rich': 5.0, 'v_organic': 5.0, 'c_cu_electrolyte_depleted': 0.0, 'v_electrolyte_depleted': 0.0},
    {'c_cu_prod': 1.4, 'v_prod': 40.0, 'c_cu_raf': 1.4, 'c_cu_electrolyte_rich': 0.0, 'v_electrolyte_rich': 5.0, 'v_organic': 5.0, 'c_cu_electrolyte_depleted': 0.0, 'v_electrolyte_depleted': 0.0},
    {'c_cu_prod': 1.5, 'v_prod': 40.0, 'c_cu_raf': 0.3, 'c_cu_electrolyte_rich': 9.0, 'v_electrolyte_rich': 5.0, 'v_organic': 5.0, 'c_cu_electrolyte_depleted': 0.0, 'v_electrolyte_depleted': 0.0},
    {'c_cu_prod': 0.8, 'v_prod': 39.5, 'c_cu_raf': 0.15, 'c_cu_electrolyte_rich': 14.5, 'v_electrolyte_rich': 5.0, 'v_organic': 5.0, 'c_cu_electrolyte_depleted': 0.0, 'v_electrolyte_depleted': 0.0},
    {'c_cu_prod': 0.9, 'v_prod': 39.0, 'c_cu_raf': 0.18, 'c_cu_electrolyte_rich': 20.1, 'v_electrolyte_rich': 5.0, 'v_organic': 5.0, 'c_cu_electrolyte_depleted': 0.0, 'v_electrolyte_depleted': 0.0},
    {'c_cu_prod': 1.05, 'v_prod': 39.5, 'c_cu_raf': 0.17, 'c_cu_electrolyte_rich': 27.1, 'v_electrolyte_rich': 5.0, 'v_organic': 5.0, 'c_cu_electrolyte_depleted': 0.0, 'v_electrolyte_depleted': 0.0},
    {'c_cu_prod': 0.95, 'v_prod': 40.0, 'c_cu_raf': 0.15, 'c_cu_electrolyte_rich': 33.5, 'v_electrolyte_rich': 5.0, 'v_organic': 5.0, 'c_cu_electrolyte_depleted': 0.0, 'v_electrolyte_depleted': 0.0},
    {'c_cu_prod': 0.91, 'v_prod': 39.5, 'c_cu_raf': 0.16, 'c_cu_electrolyte_rich': 39.5, 'v_electrolyte_rich': 5.0, 'v_organic': 5.0, 'c_cu_electrolyte_depleted': 0.0, 'v_electrolyte_depleted': 0.0},
    {'c_cu_prod': 1.0, 'v_prod': 39.5, 'c_cu_raf': 0.2, 'c_cu_electrolyte_rich': 45.7, 'v_electrolyte_rich': 5.0, 'v_organic': 5.0, 'c_cu_electrolyte_depleted': 0.0, 'v_electrolyte_depleted': 0.0},
    {'c_cu_prod': 0.85, 'v_prod': 40.0, 'c_cu_raf': 0.12, 'c_cu_electrolyte_rich': 51.5, 'v_electrolyte_rich': 5.0, 'v_organic': 5.0, 'c_cu_electrolyte_depleted': 0.0, 'v_electrolyte_depleted': 0.0},
    {'c_cu_prod': 0.87, 'v_prod': 39.5, 'c_cu_raf': 0.14, 'c_cu_electrolyte_rich': 57.3, 'v_electrolyte_rich': 5.0, 'v_organic': 5.0, 'c_cu_electrolyte_depleted': 52.5, 'v_electrolyte_depleted': 5.0},
    {'c_cu_prod': 0.9, 'v_prod': 39.0, 'c_cu_raf': 0.12, 'c_cu_electrolyte_rich': 58.6, 'v_electrolyte_rich': 5.0, 'v_organic': 5.0, 'c_cu_electrolyte_depleted': 45.9, 'v_electrolyte_depleted': 5.0},
    {'c_cu_prod': 0.95, 'v_prod': 39.5, 'c_cu_raf': 0.14, 'c_cu_electrolyte_rich': 52.4, 'v_electrolyte_rich': 5.0, 'v_organic': 5.0, 'c_cu_electrolyte_depleted': 42.2, 'v_electrolyte_depleted': 5.0},
    {'c_cu_prod': 0.85, 'v_prod': 39.5, 'c_cu_raf': 0.12, 'c_cu_electrolyte_rich': 47.9, 'v_electrolyte_rich': 5.0, 'v_organic': 5.0, 'c_cu_electrolyte_depleted': 40.0, 'v_electrolyte_depleted': 5.0},
    {'c_cu_prod': 0.85, 'v_prod': 39.0, 'c_cu_raf': 0.12, 'c_cu_electrolyte_rich': 45.7, 'v_electrolyte_rich': 5.0, 'v_organic': 5.0, 'c_cu_electrolyte_depleted': 39.0, 'v_electrolyte_depleted': 5.0},
    {'c_cu_prod': 0.8, 'v_prod': 39.5, 'c_cu_raf': 0.11, 'c_cu_electrolyte_rich': 44.5, 'v_electrolyte_rich': 5.0, 'v_organic': 5.0, 'c_cu_electrolyte_depleted': 36.9, 'v_electrolyte_depleted': 5.0},
    {'c_cu_prod': 0.75, 'v_prod': 39.5, 'c_cu_raf': 0.11, 'c_cu_electrolyte_rich': 42.0, 'v_electrolyte_rich': 5.0, 'v_organic': 5.0, 'c_cu_electrolyte_depleted': 33.2, 'v_electrolyte_depleted': 5.0},
    {'c_cu_prod': 0.75, 'v_prod': 39.0, 'c_cu_raf': 0.12, 'c_cu_electrolyte_rich': 38.1, 'v_electrolyte_rich': 5.0, 'v_organic': 5.0, 'c_cu_electrolyte_depleted': 30.5, 'v_electrolyte_depleted': 5.0},
    {'c_cu_prod': 0.7, 'v_prod': 39.0, 'c_cu_raf': 0.12, 'c_cu_electrolyte_rich': 35.0, 'v_electrolyte_rich': 5.0, 'v_organic': 5.0, 'c_cu_electrolyte_depleted': 30.5, 'v_electrolyte_depleted': 5.0},
    {'c_cu_prod': 0.55, 'v_prod': 40.0, 'c_cu_raf': 0.1, 'c_cu_electrolyte_rich': 34.1, 'v_electrolyte_rich': 5.0, 'v_organic': 5.0, 'c_cu_electrolyte_depleted': 30.1, 'v_electrolyte_depleted': 5.0},
    {'c_cu_prod': 0.4, 'v_prod': 39.5, 'c_cu_raf': 0.05, 'c_cu_electrolyte_rich': 32.8, 'v_electrolyte_rich': 5.0, 'v_organic': 5.0, 'c_cu_electrolyte_depleted': 30.0, 'v_electrolyte_depleted': 5.0},
    {'c_cu_prod': 0.3, 'v_prod': 39.5, 'c_cu_raf': 0.05, 'c_cu_electrolyte_rich': 32.0, 'v_electrolyte_rich': 5.0, 'v_organic': 5.0, 'c_cu_electrolyte_depleted': 29.9, 'v_electrolyte_depleted': 5.0}
]


results = leaching.calculate(daily_data=final_data)

# Выводим результаты
# for day in range(1, len(final_data) + 1):
#     print(f"День {day}:")
#     print(f"Эффективность экстракции {results['extraction'][day-1]}%")
#     print(f"Концентрация меди в обедненной органической фазе = {results['depleted'][day - 1]} г/л")
#     print(f"Концентрация меди в богатой органической фазе = {results['rich'][day - 1]} г/л")
#     print(f"Эффективность ре-экстракции органики {results['re_extracton_organic'][day-1]}%")
#     print(f"Эффективность ре-экстракции электролита {results['re_extraction_electrolyte'][day-1]}%")
#     print(f"Прирост m+Cu-като {results['gain'][day-1]} грамм")
#     print(f"Общая масса накопленной Cu {results['total_accumulated_cu_mass'][day-1]} грамм")
#     print(f"Сквозное извлечение меди из руды до металла {results['total_cu_recovery_percent'][day-1]}%")
#     print(f"Общее итоговое извлечение {results['overall_extraction_efficiency'][day-1]}%")
    

total_balance = leaching.calculate_total_balance()
# print(total_balance)