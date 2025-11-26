import pyodbc
from tkinter import ttk, messagebox

# --- CẤU HÌNH MÀU SẮC (Theo phong cách file Word) ---
NAV_BG = "#2c3e50"       # Màu nền menu trái (Xanh đậm)
NAV_FG = "#ecf0f1"       # Màu chữ menu
NAV_HOVER = "#34495e"    # Màu khi di chuột menu
MAIN_BG = "#ffffff"      # Màu nền chính
BTN_PRIMARY = "#2980b9"  # Màu nút chính (Xanh dương)
BTN_DANGER = "#c0392b"   # Màu nút xóa (Đỏ)

def get_connection():
    # THAY TÊN SERVER CỦA BẠN VÀO ĐÂY
    server = 'DESKTOP-BL8B9B2\SQLEXPRESS01' 
    database = 'QLCHXM'
    try:
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            f'SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        )
        return conn
    except Exception as e:
        messagebox.showerror("Lỗi DB", str(e))
        return None

def setup_theme(root):
    """Thiết lập Style cho toàn bộ ứng dụng"""
    style = ttk.Style()
    style.theme_use('clam') # Dùng theme clam để dễ tùy biến màu

    # 1. Style cho Treeview (Bảng)
    style.configure("Treeview", 
                    background="white", 
                    foreground="black", 
                    rowheight=25, 
                    fieldbackground="white")
    style.map('Treeview', background=[('selected', '#3498db')])
    
    # Header của bảng
    style.configure("Treeview.Heading", font=('Arial', 10, 'bold'))

    # 2. Style cho Label tiêu đề
    style.configure("Title.TLabel", font=("Arial", 18, "bold"), foreground="#2c3e50")
    
    # 3. Style cho Frame
    style.configure("TFrame", background=MAIN_BG)

    return style