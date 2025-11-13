import json
import os
import shutil


def update_data() -> object:
    data_file = 'data/resources.json'
    backup_file = 'data/resources_backup.json'

    # Создаем бэкап существующего файла
    if os.path.exists(data_file):
        shutil.copy2(data_file, backup_file)
        print(f"Создан бэкап: {backup_file}")

    # Новые данные со всеми ресурсами
    new_data = {
        "groups": [
            {
                "name": "Справочники",
                "resources": [
                    {
                        "number": 1,
                        "logo": "https://www.rlsnet.ru/favicon.ico",
                        "url": "https://www.rlsnet.ru",
                        "description": "Регистр лекарственных средств России - информация о лекарственных препаратах"
                    },
                    {
                        "number": 2,
                        "logo": "https://www.vidal.ru/favicon.ico",
                        "url": "https://www.vidal.ru",
                        "description": "Справочник лекарственных препаратов Vidal"
                    },
                    {
                        "number": 3,
                        "logo": "http://web.ref003.ru/images/favicon.ico",
                        "url": "http://web.ref003.ru/",
                        "description": "Справочник аптек - ГУП РО Фармацевтический центр"
                    }
                ]
            },
            {
                "name": "Калькуляторы",
                "resources": [
                    {
                        "number": 4,
                        "logo": "https://www.rlsnet.ru/favicon.ico",
                        "url": "https://www.rlsnet.ru/med-calculators",
                        "description": "Медицинские калькуляторы на RLSnet - расчет доз, индексов и других медицинских показателей"
                    }
                ]
            },
            {
                "name": "Другие информационные системы",
                "resources": [
                    {
                        "number": 5,
                        "logo": "https://rostov-tfoms.ru/favicon.ico",
                        "url": "https://rostov-tfoms.ru",
                        "description": "Территориальный фонд обязательного медицинского страхования Ростовской области"
                    },
                    {
                        "number": 6,
                        "logo": "https://edu.rosminzdrav.ru/favicon.ico",
                        "url": "https://edu.rosminzdrav.ru",
                        "description": "Образовательный портал Министерства здравоохранения РФ"
                    },
                    {
                        "number": 7,
                        "logo": "https://tmk.minzdrav.gov.ru/favicon.ico",
                        "url": "https://tmk.minzdrav.gov.ru",
                        "description": "Телемедицинская консультация Министерства здравоохранения РФ"
                    },
                    {
                        "number": 8,
                        "logo": "https://vimis.egisz.rosminzdrav.ru/favicon.ico",
                        "url": "https://vimis.egisz.rosminzdrav.ru",
                        "description": "Ведомственная интегрированная медицинская информационная система ЕГИСЗ"
                    },
                    {
                        "number": 9,
                        "logo": "https://orph.egisz.rosminzdrav.ru/favicon.ico",
                        "url": "https://orph.egisz.rosminzdrav.ru",
                        "description": "Федеральный регистр лиц, страдающих орфанными заболеваниями"
                    },
                    {
                        "number": 10,
                        "logo": "https://cr.minzdrav.gov.ru/favicon.ico",
                        "url": "https://cr.minzdrav.gov.ru",
                        "description": "Рубрикатор Клинических рекомендаций"
                    },
                    {
                        "number": 11,
                        "logo": "https://portalmr.egisz.rosminzdrav.ru/favicon.ico",
                        "url": "https://portalmr.egisz.rosminzdrav.ru",
                        "description": "ФРМР Федеральный регистр медицинских работников"
                    },
                    {
                        "number": 12,
                        "logo": "https://lkmr.egisz.rosminzdrav.ru/favicon.ico",
                        "url": "https://lkmr.egisz.rosminzdrav.ru",
                        "description": "ЛК ФРМР - Личный кабинет медицинского работника"
                    },
                    {
                        "number": 13,
                        "logo": "https://diaregistry.ru/favicon.ico",
                        "url": "https://diaregistry.ru",
                        "description": "Федеральный регистр сахарного диабета"
                    },
                    {
                        "number": 14,
                        "logo": "https://www.gosuslugi.ru/favicon.ico",
                        "url": "https://www.gosuslugi.ru",
                        "description": "Портал государственных услуг Российской Федерации"
                    },
                    {
                        "number": 15,
                        "logo": "https://grls.rosminzdrav.ru/favicon.ico",
                        "url": "https://grls.rosminzdrav.ru",
                        "description": "Государственный реестр лекарственных средств"
                    },
                    {
                        "number": 16,
                        "logo": "https://roszdravnadzor.gov.ru/favicon.ico",
                        "url": "https://roszdravnadzor.gov.ru/",
                        "description": "Федеральная служба по надзору в сфере здравоохранения"
                    }
                ]
            },
            {
                "name": "Честный знак",
                "resources": [
                    {
                        "number": 17,
                        "logo": "https://mdlp.crpt.ru/favicon.ico",
                        "url": "https://mdlp.crpt.ru",
                        "description": "Мониторинг движения лекарственных препаратов"
                    },
                    {
                        "number": 18,
                        "logo": "https://честныйзнак.рф/favicon.ico",
                        "url": "https://честныйзнак.рф",
                        "description": "Официальный портал системы маркировки \"Честный знак\""
                    },
                    {
                        "number": 19,
                        "logo": "https://support.crpt.ru/ws-crpt-login/images/favicon.png",
                        "url": "https://support.crpt.ru",
                        "description": "Техническая поддержка системы \"Честный знак\""
                    },
                    {
                        "number": 20,
                        "logo": "https://markirovka.crpt.ru/favicon.ico",
                        "url": "https://markirovka.crpt.ru",
                        "description": "Личный кабинет системы \"Честный знак\""
                    }
                ]
            },
            {
                "name": "Другие медицинские организации",
                "resources": [
                    {
                        "number": 21,
                        "logo": "https://www.center-zdorovie.ru/sites/all/themes/health/images/2022_head_logo_kdc_1.png",
                        "url": "https://center-zdorovie.ru",
                        "description": "ГБУ РО «КДЦ «Здоровье» в г. Ростове-на-Дону"
                    },
                    {
                        "number": 22,
                        "logo": "https://rokdc.ru/favicon.ico",
                        "url": "https://rokdc.ru",
                        "description": "Областной консультативно-диагностический центр"
                    },
                    {
                        "number": 23,
                        "logo": "https://legeartis-don.ru/favicon.ico",
                        "url": "https://legeartis-don.ru",
                        "description": "Медицинский центр \"Леге Артис\" в Ростове-на-Дону"
                    }
                ]
            }
        ]
    }

    # Создаем директорию если ее нет
    os.makedirs(os.path.dirname(data_file), exist_ok=True)

    # Записываем новые данные
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(new_data, f, ensure_ascii=False, indent=2)

    print("Данные успешно обновлены!")
    print(f"Всего групп: {len(new_data['groups'])}")
    print(f"Всего ресурсов: {sum(len(group['resources']) for group in new_data['groups'])}")

if __name__ == '__main__':
    update_data()