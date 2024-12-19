import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import csv

# CSV 파일 경로
file_path = r'C:\Users\kimmingu\Desktop\\칵테일\data_cocktails.csv'

# 검색 함수
def search_cocktail(field_choice, search_term):
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

    # 검색 결과 저장
    deduplicated_results = {}
    for record in b:
        if field_choice == "strDrink":
            field_value = record[0]
        elif field_choice == "strIngredients":
            field_value = record[1]
        elif field_choice == "strCategory":
            field_value = record[6]
        elif field_choice == "Basic_taste":
            field_value = record[4]  # Basic_taste로 검색

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

    return deduplicated_results

# UI 설정
def create_ui():
    def on_search_click():
        field_choice = field_var.get()
        search_term = search_entry.get().strip().lower()

        if not search_term:
            messagebox.showwarning("입력 오류", "검색어를 입력해주세요.")
            return

        results = search_cocktail(field_choice, search_term)

        if not results:
            messagebox.showinfo("검색 결과", f"'{search_term}'에 대한 결과가 없습니다.")
            return

        # 결과 출력
        result_window = tk.Toplevel(root)
        result_window.title(f"검색 결과: {search_term}")

        results_listbox = tk.Listbox(result_window, width=60, height=15)
        results_listbox.pack(pady=20)

        for i, drink_name in enumerate(results.keys(), 1):
            results_listbox.insert(tk.END, f"{i}. {drink_name}")

        def on_select_drink(event):
            selected_idx = results_listbox.curselection()
            if selected_idx:
                selected_drink = list(results.keys())[selected_idx[0]]
                fields = results[selected_drink]

                info_window = tk.Toplevel(result_window)
                info_window.title(f"{selected_drink} - 상세 정보")

                text = f"음료 이름: {selected_drink}\n"
                text += f"카테고리: {fields['strCategory']}\n"
                text += f"기본 맛: {fields['Basic_taste']}\n"
                text += f"레시피: {fields['strInstructions']}\n"
                text += f"알콜 타입: {fields['Alc_type']}\n"
                text += "재료 및 추가 정보:\n"

                for ingredient, measure, value_ml, garnish_type, alc_type in fields['Ingredients']:
                    text += f"  - {ingredient}: {measure} (Value_ml: {value_ml}, Alc_type: {alc_type})"
                    if garnish_type != "N/A":
                        text += f", Garnish_type: {garnish_type}"
                    text += "\n"

                label = tk.Label(info_window, text=text, justify=tk.LEFT)
                label.pack(padx=10, pady=10)

        results_listbox.bind("<<ListboxSelect>>", on_select_drink)

    # 중앙 프레임
    center_frame = tk.Frame(root, width=400, height=720, bg="#ffffff", padx=20, pady=20)
    center_frame.pack(side=tk.TOP, fill=tk.Y)

    field_var = tk.StringVar(value="strDrink")  # 기본적으로 strDrink 필드 선택
    search_label = tk.Label(center_frame, text="검색 필드 선택:", font=("Arial", 12))
    search_label.pack(pady=10)

    field_menu = tk.OptionMenu(center_frame, field_var, "strDrink", "strIngredients", "strCategory", "Basic_taste")
    field_menu.pack(pady=10)

    search_label = tk.Label(center_frame, text="검색어 입력:", font=("Arial", 12))
    search_label.pack(pady=10)

    search_entry = tk.Entry(center_frame, width=40)
    search_entry.pack(pady=10)

    search_button = tk.Button(center_frame, text="검색", command=on_search_click)
    search_button.pack(pady=20)

# 메인 UI 실행
root = tk.Tk()
root.title("칵테일 추천 프로그램")
root.geometry("1280x720")

# 배경 이미지 추가
bg_image = Image.open(r"C:\Users\kimmingu\Desktop\칵테일\스크린샷 2024-12-13 143255.png")  # 배경 이미지 경로 설정
bg_image = bg_image.resize((1280, 720), Image.Resampling.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # 배경을 전체 창에 맞게 설정

# 헤더 영역
header_label = tk.Label(root, text="🍸 칵테일 추천 프로그램 🍸", font=("Arial", 24, 'bold'), bg="#ffffff", fg="#4CAF50")
header_label.pack(pady=30)

# UI 실행
create_ui()

root.mainloop()
