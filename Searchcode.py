import csv

# CSV 파일 경로
file_path = r'C:\Users\khskh\OneDrive\바탕 화면\대학\대학 관련프로그램 및 파일\파이썬파일\data_cocktails.csv'

def Search():
    # 검색 함수
    def search():
        print("검색할 필드를 선택하세요:")
        print("1. strDrink (음료 이름)")
        print("2. strIngredients (재료)")
        print("3. strCategory (음료 카테고리)")

        field_choice = input("검색할 필드를 입력하세요 (1/2/3): ")

        if field_choice == "1":
            return "strDrink"
        elif field_choice == "2":
            return "strIngredients"
        elif field_choice == "3":
            return "strCategory"
        else:
            print("잘못된 입력입니다. 기본값인 strDrink로 검색을 진행합니다.")
            return "strDrink"

    # 데이터 딕셔너리 초기화
    data_dict = {
        'strDrink': [],
        'strCategory': [],
        'strIngredients': [],
        'Alc_type': [],
        'Basic_taste': [],
        'strInstructions': [],
        'strMeasures': [],
        'Value_ml': [],
        'Garnish_type': []
    }

    b = []  # 결과를 저장할 리스트

    # CSV 파일 읽기
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data_dict['strDrink'].append(row['strDrink'])
            data_dict['strCategory'].append(row['strCategory'])
            data_dict['strIngredients'].append(row['strIngredients'])
            data_dict['Alc_type'].append(row['Alc_type'])
            data_dict['Basic_taste'].append(row['Basic_taste'])
            data_dict['strInstructions'].append(row['strInstructions'])
            data_dict['strMeasures'].append(row['strMeasures'])
            data_dict['Value_ml'].append(row.get('Value_ml', 'N/A'))  # Value_ml 기본값
            data_dict['Garnish_type'].append(row.get('Garnish_type', 'N/A'))  # Garnish_type 기본값

            record = (
                row['strDrink'],                            # 1번 (strDrink)
                row['strIngredients'],                      # 2번 (strIngredients)
                row['strMeasures'],                         # 3번 (strMeasures)
                row['Alc_type'],                            # 4번 (Alc_type)
                row['Basic_taste'],                         # 5번 (Basic_taste)
                row['strInstructions'],                     # 6번 (strInstructions)
                row['strCategory'],                         # 7번 (strCategory)
                row.get('Value_ml', 'N/A'),                 # 8번 (Value_ml)
                row.get('Garnish_type', 'N/A')              # 9번 (Garnish_type)
            )
            b.append(record)

    # 검색 필드 선택
    field_to_search = search()

    # 사용자에게 검색어 입력 받기
    search_term = input(f"{field_to_search}에 대해 검색할 내용을 입력하세요: ")

    # 공백을 제거한 후 소문자로 변환하여 검색어 처리
    search_term = search_term.replace(" ", "").lower()

    # 검색 결과 저장
    deduplicated_results = {}
    for record in b:
        if field_to_search == "strDrink":
            field_value = record[0]
        elif field_to_search == "strIngredients":
            field_value = record[1]
        else:
            field_value = record[6]  # "strCategory"가 선택된 경우

        # 공백을 제거하고 소문자로 변환하여 비교
        field_value = field_value.replace(" ", "").lower()

        if search_term in field_value:
            drink_name = record[0]  # 중복 제거 기준: strDrink
            if drink_name not in deduplicated_results:
                deduplicated_results[drink_name] = {
                    'strCategory': record[6],
                    'Ingredients': [],  # 재료와 추가 정보를 묶어서 저장
                    'Basic_taste': record[4] if record[4].strip() else "술맛",
                    'strInstructions': record[5],
                    'Alc_type': record[3]  # 음료의 Alc_type을 저장
                }
            ingredients = record[1].split(', ')
            measures = record[2].split(', ')
            value_ml = record[7].split(', ') if record[7] != 'N/A' else ["N/A"] * len(ingredients)
            garnish_type = record[8].split(', ') if record[8] != 'N/A' else ["N/A"] * len(ingredients)
            alc_types = record[3].split(', ') if record[3] != 'N/A' else ["N/A"] * len(ingredients)  # Alc_type 추가

            combined = list(zip(ingredients, measures, value_ml, garnish_type, alc_types))  # 재료와 추가 정보를 매칭
            deduplicated_results[drink_name]['Ingredients'].extend(combined)

    # 검색된 칵테일 목록 출력
    print(f"\n검색된 '{field_to_search}'이(가) 포함된 칵테일 목록:")
    print("=" * 40)
    drink_names = list(deduplicated_results.keys())
    for i, drink_name in enumerate(drink_names, 1):
        print(f"{i}. {drink_name}")
    print("=" * 40)

    # 사용자에게 음료 선택 받기
    choice = int(input("자세한 정보를 보고 싶은 음료 번호를 선택하세요: "))
    if 1 <= choice <= len(drink_names):
        selected_drink = drink_names[choice - 1]
        fields = deduplicated_results[selected_drink]

        # 선택된 음료의 상세 정보 출력
        print(f"\n음료 이름: {selected_drink}")
        print(f"카테고리: {fields['strCategory']}")
        print(f"기본 맛: {fields['Basic_taste']}")
        print(f"레시피: {fields['strInstructions']}")
        print(f"알콜 타입: {fields['Alc_type']}")
        print("재료 및 추가 정보:")
        for ingredient, measure, value_ml, garnish_type, alc_type in fields['Ingredients']:
            print(f"  - {ingredient}: {measure} (Value_ml: {value_ml}", end="")
            if garnish_type != "N/A":
                print(f", Garnish_type: {garnish_type}", end="")
            print(f", Alc_type: {alc_type})")  # 각 재료에 해당하는 Alc_type을 출력
        print("=" * 40)
    else:
        print("잘못된 번호입니다. 다시 시도해 주세요.")
