import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import pandas as pd

# Step 1: 데이터 로드 및 전처리
def load_and_preprocess_data(file_path):
    try:
        data = pd.read_csv(file_path)
    except FileNotFoundError:
        print("데이터 파일 없습니다")
        return None

    # 알코올 강도 분류 함수
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

    # 알코올 강도 열 생성
    data['Alcohol_level'] = data['Alc_type'].apply(classify_alcohol)

    # 칵테일 이름과 재료를 기준으로 중복 제거
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
        return "조건에 맞는 칵테일이 없습니다. 조건을 변경해주세요!"
    
    result = ""
    for _, row in filtered_cocktails.iterrows():
        result += f"- {row['strDrink']}: {row['strIngredients']} ({row['strGlass']})\n"
        result += f"  만드는 방법: {row['strInstructions']}\n\n"
    return result


# UI 구성
class CocktailRecommendationApp:
    def __init__(self, root, data_file_path):
        self.root = root
        self.root.title("칵테일 추천 프로그램")
        self.root.geometry("1280x720")

        # 배경 이미지 추가
        bg_image = Image.open(r"C:\Users\kimmingu\Desktop\칵테일\스크린샷 2024-12-13 143255.png")
        bg_image = bg_image.resize((1280, 720), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(bg_image)

        bg_label = tk.Label(root, image=self.bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # 헤더
        header_label = tk.Label(root, text="🍸 칵테일 추천 프로그램 🍸", font=("Arial", 24, 'bold'), bg="#ffffff", fg="#4CAF50")
        header_label.pack(pady=30)

        # 프레임
        main_frame = tk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # 왼쪽 프레임 (추천 기능)
        left_frame = tk.Frame(main_frame, width=400, height=720, bg="#ffffff", padx=20, pady=20)
        left_frame.pack(side=tk.LEFT, fill=tk.Y)

        # 알코올 강도, 분위기, 맛 선택
        selection_frame = tk.Frame(left_frame, bg="#ffffff")
        selection_frame.pack(pady=10, fill=tk.X)

        self.alcohol_var = tk.StringVar(value="잘모르겠음")
        alcohol_label = tk.Label(selection_frame, text="알코올 강도:", bg="#ffffff", font=("Arial", 12))
        alcohol_label.grid(row=0, column=0, padx=10)
        alcohol_options = ["약한", "중간", "강한", "잘모르겠음"]
        self.alcohol_menu = ttk.Combobox(selection_frame, textvariable=self.alcohol_var, values=alcohol_options, state="readonly", width=10)
        self.alcohol_menu.grid(row=0, column=1, padx=10)

        self.mood_var = tk.StringVar(value="잘모르겠음")
        mood_label = tk.Label(selection_frame, text="분위기:", bg="#ffffff", font=("Arial", 12))
        mood_label.grid(row=0, column=2, padx=10)
        mood_options = ["여유로운", "파티", "고급스러운", "잘모르겠음"]
        self.mood_menu = ttk.Combobox(selection_frame, textvariable=self.mood_var, values=mood_options, state="readonly", width=10)
        self.mood_menu.grid(row=0, column=3, padx=10)

        taste_label = tk.Label(left_frame, text="맛 (콤마로 구분):", bg="#ffffff", font=("Arial", 12))
        taste_label.pack(pady=10)
        self.taste_entry = tk.Entry(left_frame, width=30, font=("Arial", 12))
        self.taste_entry.pack(pady=10)

        # 추천 버튼
        recommend_button = tk.Button(left_frame, text="추천 받기", bg="#4CAF50", fg="white", font=("Arial", 14, 'bold'), relief="flat", command=self.recommend_cocktails)
        recommend_button.pack(pady=10)

        # 오른쪽 프레임 (추천 결과)
        right_frame = tk.Frame(main_frame, width=880, height=720, bg="#f5f5f5", padx=20, pady=20)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y)

        # 결과 출력
        self.result_text = tk.Text(right_frame, width=80, height=30, bg="#f5f5f5", font=("Arial", 12), wrap="word", bd=2, relief="solid")
        self.result_text.pack(pady=15, fill=tk.Y)

        self.cocktail_data = load_and_preprocess_data(data_file_path)
        if self.cocktail_data is None:
            self.root.quit()

    def recommend_cocktails(self):
        # 알코올 강도 필터링
        alcohol_preference = self.alcohol_var.get().strip()
        filtered_cocktails = filter_by_alcohol(self.cocktail_data, alcohol_preference)

        # 맛 필터링
        taste_preferences_input = self.taste_entry.get().strip()
        taste_preferences = [taste_translation_dict[taste] for taste in taste_preferences_input.split(",") if taste in taste_translation_dict]
        filtered_cocktails = filter_by_taste(filtered_cocktails, taste_preferences)

        # 분위기 필터링
        mood_preference = self.mood_var.get().strip()
        filtered_cocktails = filter_by_mood(filtered_cocktails, mood_preference)

        # 결과 출력
        result = recommend_cocktails(filtered_cocktails)
        self.result_text.delete(1.0, tk.END)  # 기존 텍스트 지우기
        self.result_text.insert(tk.END, result)


# 실행
if __name__ == "__main__":
    root = tk.Tk()
    app = CocktailRecommendationApp(root, r"C:\Users\kimmingu\Desktop\칵테일\data_cocktails.csv")
    root.mainloop()
