import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# UI 구성
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

# 프레임 나누기: 왼쪽은 검색 기능, 오른쪽은 결과 창
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

# 왼쪽 프레임 (추천 기능 및 검색)
left_frame = tk.Frame(main_frame, width=400, height=720, bg="#ffffff", padx=20, pady=20)
left_frame.pack(side=tk.LEFT, fill=tk.Y)

# 알코올 강도, 분위기, 맛 선택 (가로로 나열)
selection_frame = tk.Frame(left_frame, bg="#ffffff")
selection_frame.pack(pady=10, fill=tk.X)

# 알코올 강도 선택
alcohol_var = tk.StringVar(value="잘모르겠음")
alcohol_label = tk.Label(selection_frame, text="알코올 강도:", bg="#ffffff", font=("Arial", 12))
alcohol_label.grid(row=0, column=0, padx=10)
alcohol_options = ["약한", "중간", "강한", "잘모르겠음"]
alcohol_menu = ttk.Combobox(selection_frame, textvariable=alcohol_var, values=alcohol_options, state="readonly", width=10)
alcohol_menu.grid(row=0, column=1, padx=10)

# 분위기 선택
mood_var = tk.StringVar(value="잘모르겠음")
mood_label = tk.Label(selection_frame, text="분위기:", bg="#ffffff", font=("Arial", 12))
mood_label.grid(row=0, column=2, padx=10)
mood_options = ["여유로운", "파티", "고급스러운", "잘모르겠음"]
mood_menu = ttk.Combobox(selection_frame, textvariable=mood_var, values=mood_options, state="readonly", width=10)
mood_menu.grid(row=0, column=3, padx=10)

# 맛 선택
taste_label = tk.Label(left_frame, text="맛 (콤마로 구분):", bg="#ffffff", font=("Arial", 12))
taste_label.pack(pady=10)
taste_entry = tk.Entry(left_frame, width=30, font=("Arial", 12))
taste_entry.pack(pady=10)

# 추천 버튼
recommend_button = tk.Button(left_frame, text="추천 받기", bg="#4CAF50", fg="white", font=("Arial", 14, 'bold'), relief="flat")
recommend_button.pack(pady=10)

# 검색 영역 (칵테일 이름으로 검색)
cocktail_name_label = tk.Label(left_frame, text="칵테일 이름으로 검색:", bg="#ffffff", font=("Arial", 12))
cocktail_name_label.pack(pady=5)
cocktail_name_entry = tk.Entry(left_frame, width=30, font=("Arial", 12))
cocktail_name_entry.pack(pady=5)

# 검색 버튼
search_button = tk.Button(left_frame, text="검색", bg="#2196F3", fg="white", font=("Arial", 14, 'bold'), relief="flat")
search_button.pack(pady=10)

# 오른쪽 프레임 (추천 결과)
right_frame = tk.Frame(main_frame, width=880, height=720, bg="#f5f5f5", padx=20, pady=20)
right_frame.pack(side=tk.RIGHT, fill=tk.Y)

# 추천 결과 출력 영역
result_text = tk.Text(right_frame, width=80, height=30, bg="#f5f5f5", font=("Arial", 12), wrap="word", bd=2, relief="solid")
result_text.pack(pady=15, fill=tk.Y)

# 실행
root.mainloop()
