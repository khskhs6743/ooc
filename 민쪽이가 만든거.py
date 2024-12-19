import pandas as pd
import tkinter as tk
from tkinter import messagebox, simpledialog, Scrollbar, Text

# Step 1: 데이터 로드 및 전처리
def load_and_preprocess_data(file_path):
    try:
        data = pd.read_csv(file_path)
    except FileNotFoundError:
        print("데이터 파일 없습니다")
        return None

    def classify_alcohol(alc_type):
        weak = ['Beer', 'Cider', 'Wine', 'Champagne', 'Prosecco']
        medium = ['Sweet Liqueur', 'Creamy Liqueur', 'Triple Sec', 'Vermouth', 'Schnapps', 'Port']
        strong = ['Vodka', 'Rum', 'Gin', 'Whisky', 'Tequila', 'Absinthe', 'Brandy', 'Sambuca', 'Cachaca', 'Pisco', 'Ouzo']
        
        if alc_type in weak:
            return '약한'
        elif alc_type in medium:
            return '중간'
        elif alc_type in strong:
            return '강한'
        return None

    data['Alcohol_level'] = data['Alc_type'].apply(classify_alcohol)

    data = data.groupby('strDrink').agg({
        'strCategory': 'first',
        'strGlass': 'first',
        'strIngredients': lambda x: ', '.join(x.dropna().astype(str)),
        'Alc_type': 'first',
        'Basic_taste': lambda x: ', '.join(x.dropna().astype(str)),
        'strInstructions': 'first',
        'Alcohol_level': 'first'
    }).reset_index()
    return data

# Step 2: 알코올 강도 필터링
def filter_by_alcohol(cocktail_data, alcohol_preference):
    if alcohol_preference != '잘모르겠음':
        cocktail_data = cocktail_data[cocktail_data['Alcohol_level'] == alcohol_preference]
    return cocktail_data

# 맛 변환 사전
taste_translation_dict = {
    '신맛': 'sour',
    '단맛': 'sweet',
    '크리미한 맛': 'cream',
    '쓴맛': 'bitter',
    '맑고 담백한 맛': 'clean',
    '민트맛': 'mint',
    '계란맛': 'egg',
    '짠맛': 'salty',
    '매운맛': 'spicy'
}

# Step 3: 맛 필터링
def filter_by_taste(cocktail_data, taste_preferences):
    for taste in taste_preferences:
        cocktail_data = cocktail_data[cocktail_data['Basic_taste'].str.contains(taste, na=False)]
    return cocktail_data

# Step 4: 분위기 필터링
def filter_by_mood(cocktail_data, mood_preference='잘모르겠음'):
    if mood_preference == '잘모르겠음':
        return cocktail_data
    mood_categories = {
        '여유로운': ['Milk / Float / Shake', 'Ordinary Drink', 'Coffee / Tea', 'Soft Drink / Soda'],
        '파티': ['Shot', 'Punch / Party Drink'],
        '고급스러운': ['Cocktail', 'Other/Unknown']
    }
    categories = mood_categories.get(mood_preference, [])
    filtered_cocktails = cocktail_data[cocktail_data['strCategory'].isin(categories)]
    return filtered_cocktails

# Step 5: 추천 출력 함수
def recommend_cocktails(filtered_cocktails):
    if filtered_cocktails.empty:
        print("조건에 맞는 칵테일이 없습니다. 조건을 변경해주세요!")
        return

    print("\n추천 칵테일 리스트:")
    for _, row in filtered_cocktails.iterrows():
        print(f"- {row['strDrink']}: {row['strIngredients']} ({row['strGlass']})")
        print(f"  만드는 방법: {row['strInstructions']}\n")

# UI 생성
class CocktailRecommendationApp:
    def __init__(self, root, data_file_path):
        self.root = root
        self.root.title("칵테일 추천 프로그램")
        self.root.geometry("800x600")
        self.data_file_path = data_file_path
        self.cocktail_data = load_and_preprocess_data(self.data_file_path)
        self.filtered_cocktails = self.cocktail_data

        if self.cocktail_data is None:
            self.root.quit()

        self.setup_ui()

    def setup_ui(self):
        # 레이블 및 UI 요소 스타일
        label_font = ('Helvetica', 12)
        entry_font = ('Helvetica', 10)

        # 알코올 강도 선택
        self.alcohol_label = tk.Label(self.root, text="알코올 강도를 선택하세요:", font=label_font)
        self.alcohol_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.alcohol_options = ['약한', '중간', '강한', '잘모르겠음']
        self.alcohol_var = tk.StringVar(self.root)
        self.alcohol_var.set(self.alcohol_options[0])
        self.alcohol_menu = tk.OptionMenu(self.root, self.alcohol_var, *self.alcohol_options)
        self.alcohol_menu.grid(row=0, column=1, padx=10, pady=5)

        # 맛 선택
        self.taste_label = tk.Label(self.root, text="맛을 순서대로 입력하세요 (예: 신맛, 단맛)", font=label_font)
        self.taste_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.taste_entry = tk.Entry(self.root, font=entry_font)
        self.taste_entry.grid(row=1, column=1, padx=10, pady=5)

        # 분위기 선택
        self.mood_label = tk.Label(self.root, text="분위기를 선택하세요:", font=label_font)
        self.mood_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.mood_options = ['여유로운', '파티', '고급스러운', '잘모르겠음']
        self.mood_var = tk.StringVar(self.root)
        self.mood_var.set(self.mood_options[0])
        self.mood_menu = tk.OptionMenu(self.root, self.mood_var, *self.mood_options)
        self.mood_menu.grid(row=2, column=1, padx=10, pady=5)

        # 추천 버튼
        self.recommend_button = tk.Button(self.root, text="추천 받기", command=self.recommend_cocktails, width=20, height=2, bg="#4CAF50", fg="white", font=('Helvetica', 12, 'bold'))
        self.recommend_button.grid(row=3, columnspan=2, pady=20)

        # 결과 출력
        self.result_label = tk.Label(self.root, text="추천된 칵테일: ", font=label_font)
        self.result_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")

        self.result_text = Text(self.root, height=10, width=70, font=entry_font)
        self.result_text.grid(row=5, columnspan=2, padx=10, pady=5)
        self.result_text.config(state=tk.DISABLED)  # 텍스트 박스 수정 불가로 설정

    def recommend_cocktails(self):
        # 알코올 강도 필터링
        alcohol_preference = self.alcohol_var.get().strip()
        self.filtered_cocktails = filter_by_alcohol(self.cocktail_data, alcohol_preference)

        # 맛 필터링
        taste_preferences_input = self.taste_entry.get().strip()
        taste_preferences = [taste_translation_dict[taste] for taste in taste_preferences_input.split(",")]
        self.filtered_cocktails = filter_by_taste(self.filtered_cocktails, taste_preferences)

        # 분위기 필터링
        mood_preference = self.mood_var.get().strip()
        self.filtered_cocktails = filter_by_mood(self.filtered_cocktails, mood_preference)

        # 결과 출력
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        if not self.filtered_cocktails.empty:
            cocktails_list = "\n".join(self.filtered_cocktails['strDrink'])
            self.result_text.insert(tk.END, f"추천된 칵테일:\n{cocktails_list}")
        else:
            self.result_text.insert(tk.END, "조건에 맞는 칵테일이 없습니다.")
        self.result_text.config(state=tk.DISABLED)

# 실행
if __name__ == "__main__":
    root = tk.Tk()
    app = CocktailRecommendationApp(root, r"C:\Users\kimmingu\Desktop\칵테일\data_cocktails.csv")
    root.mainloop()
