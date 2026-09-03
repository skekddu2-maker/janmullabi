import tkinter as tk
from tkinter import messagebox
import undetected_chromedriver as uc
import urllib.parse
import threading

# 공통 드라이버 생성 함수
def get_uc_driver():
    options = uc.ChromeOptions()
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = uc.Chrome(options=options, use_subprocess=True)
    return driver

def run_browser(url, name):
    status_label.config(text=f"🚀 [{name}] 브라우저 실행 및 접속 중...")
    def task():
        try:
            driver = get_uc_driver()
            driver.get(url)
            status_label.config(text=f"✨ [{name}] 검색 완료!")
        except Exception as e:
            status_label.config(text=f"❌ [{name}] 검색 중 오류 발생")
    threading.Thread(target=task, daemon=True).start()

# 국가별 분류 데이터 구조
country_data = {
    "🇰🇷 한국 (Korea)": {
        "🔍 검색엔진": [
            ("네이버 통합검색", lambda q: f"https://search.naver.com/search.naver?query={urllib.parse.quote(q)}", "#059669"),
            ("다음 통합검색", lambda q: f"https://search.daum.net/search?w=tot&q={urllib.parse.quote(q)}", "#D97706")
        ],
        "🛒 중고 플랫폼": [
            ("번개장터", lambda q: f"https://m.bunjang.co.kr/search/products?q={urllib.parse.quote(q)}", "#DC2626"),
            ("당근마켓", lambda q: f"https://www.daangn.com/search/{urllib.parse.quote(q)}", "#FF6F0F"),
            ("후르츠패밀리", lambda q: f"https://fruitsfamily.com/search/{urllib.parse.quote(q)}?sort=RELEVANCE", "#6366F1")
        ]
    },
    "🇯🇵 일본 (Japan)": {
        "🔍 검색엔진": [
            ("야후 재팬 (Yahoo!)", lambda q: f"https://search.yahoo.co.jp/search?p={urllib.parse.quote(q)}", "#7C3AED")
        ],
        "🛒 중고 플랫폼": [
            ("메루카리 (Mercari)", lambda q: f"https://jp.mercari.com/search?keyword={urllib.parse.quote(q)}", "#E11D48"),
            ("야후 옥션 (Yahoo Auction)", lambda q: f"https://auctions.yahoo.co.jp/search/search?p={q.replace(' ', '+')}&s1=cb0", "#EA580C")
        ]
    },
    "🇺🇸 미국 및 글로벌 (Global)": {
        "🔍 검색엔진": [
            ("구글 (Google)", lambda q: f"https://www.google.com/search?q={urllib.parse.quote(q)}", "#2563EB")
        ],
        "🛒 중고 & 빈티지 플랫폼": [
            ("이베이 (eBay)", lambda q: f"https://www.ebay.com/sch/i.html?_nkw={q.replace(' ', '+')}&_sop=15", "#1D4ED8"),
            ("페이스북 마켓플레이스", lambda q: f"https://www.facebook.com/marketplace/search/?query={urllib.parse.quote(q)}", "#1E40AF"),
            ("빈티드 (Vinted)", lambda q: f"https://www.vinted.fr/catalog?search_text={urllib.parse.quote(q)}", "#0D9488"),
            ("포시마크 (Poshmark)", lambda q: f"https://poshmark.com/search?query={urllib.parse.quote(q)}", "#BE185D"),
            ("그레일드 (Grailed)", lambda q: f"https://www.grailed.com/shop?query={urllib.parse.quote(q)}", "#4B5563"),
            ("디팝 (Depop)", lambda q: f"https://www.depop.com/search/?q={urllib.parse.quote(q)}", "#EF4444"),
            ("베스티에르 콜렉티브", lambda q: f"https://www.vestiairecollective.com/search/?q={urllib.parse.quote(q)}", "#374151")
        ]
    }
}

# 다크 테마 색상 정의
BG_DARK = "#121212"
CARD_BG = "#1e1e1e"
TEXT_MAIN = "#f3f4f6"
TEXT_SUB = "#9ca3af"
PLACEHOLDER_COLOR = "#6b7280"

# UI 구성
root = tk.Tk()
root.title("검색쟁이 (Multi-Platform Searcher)")
root.geometry("480x520")
root.configure(bg=BG_DARK)

# 상단 입력 영역
top_frame = tk.Frame(root, bg=BG_DARK)
top_frame.pack(pady=(15, 5), fill=tk.X, padx=20)

label = tk.Label(top_frame, text="🔍 통합 검색어 입력", font=("맑은 고딕", 10, "bold"), bg=BG_DARK, fg=TEXT_MAIN)
label.pack(anchor="w", pady=(0, 4))

entry = tk.Entry(top_frame, font=("맑은 고딕", 11), bg="#2d2d2d", fg=PLACEHOLDER_COLOR, insertbackground="white", relief="flat", bd=6)
entry.pack(fill=tk.X, pady=2)

PLACEHOLDER_TEXT = "(검색어 입력하셈^^ )"
entry.insert(0, PLACEHOLDER_TEXT)

def on_entry_click(event):
    if entry.get() == PLACEHOLDER_TEXT:
        entry.delete(0, tk.END)
        entry.config(fg=TEXT_MAIN)

def on_focusout(event):
    if not entry.get().strip():
        entry.insert(0, PLACEHOLDER_TEXT)
        entry.config(fg=PLACEHOLDER_COLOR)

entry.bind("<FocusIn>", on_entry_click)
entry.bind("<FocusOut>", on_focusout)

status_label = tk.Label(root, text="💡 국가 버튼을 눌러 해당 국가 플랫폼을 열고 닫으세요.", font=("맑은 고딕", 9), bg=BG_DARK, fg=TEXT_SUB)
status_label.pack(pady=(2, 8))

# 스크롤 가능한 영역 컨테이너
container = tk.Frame(root, bg=BG_DARK)
container.pack(fill=TK_BOTH if 'TK_BOTH' in globals() else tk.BOTH, expand=True, padx=20, pady=(0, 15))

canvas = tk.Canvas(container, bg=BG_DARK, highlightthickness=0)
scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg=BG_DARK)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill=tk.BOTH, expand=True)
scrollbar.pack(side="right", fill=tk.Y)

def _on_mousewheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")
canvas.bind_all("<MouseWheel>", _on_mousewheel)

# 국가별 아코디언 메뉴 생성
for country_name, subcategories in country_data.items():
    sub_frame = tk.Frame(scrollable_frame, bg=CARD_BG, highlightbackground="#333333", highlightthickness=1)
    
    for sub_title, items in subcategories.items():
        sub_lbl = tk.Label(sub_frame, text=sub_title, font=("맑은 고딕", 9, "bold"), fg=TEXT_SUB, bg=CARD_BG)
        sub_lbl.pack(anchor="w", padx=12, pady=(10, 2))
        
        for name, url_func, color in items:
            def make_click(uf=url_func, n=name):
                def click():
                    keyword = entry.get().strip()
                    if not keyword or keyword == PLACEHOLDER_TEXT:
                        messagebox.showwarning("경고", "검색어를 먼저 입력해주세요!")
                        return
                    run_browser(uf(keyword), n)
                return click

            btn = tk.Button(sub_frame, text=name, command=make_click(), bg=color, fg="white", activebackground=color, activeforeground="white", font=("맑은 고딕", 9, "bold"), relief="flat", bd=0, pady=5, cursor="hand2")
            btn.pack(fill=tk.X, padx=12, pady=2)
            
        tk.Label(sub_frame, text="", bg=CARD_BG, height=1).pack()

    def toggle_menu(sf=sub_frame):
        if sf.winfo_ismapped():
            sf.pack_forget()
        else:
            sf.pack(fill=tk.X, padx=2, pady=4)

    country_btn = tk.Button(scrollable_frame, text=country_name, font=("맑은 고딕", 10, "bold"), bg="#262626", fg=TEXT_MAIN, activebackground="#383838", activeforeground=TEXT_MAIN, relief="flat", bd=0, pady=8, cursor="hand2", command=lambda sf=sub_frame: toggle_menu(sf))
    country_btn.pack(fill=tk.X, pady=3)

root.mainloop()