import pyodbc
from tkinter import ttk, messagebox

# --- CẤU HÌNH MÀU SẮC ---
NAV_BG = "#2c3e50"
NAV_FG = "white"
NAV_HOVER = "#34495e"
MAIN_BG = "#ecf0f1"
BTN_PRIMARY = "#2980b9"
BTN_DANGER = "#c0392b"

# --- QUAN TRỌNG: BIẾN LƯU NGƯỜI ĐĂNG NHẬP ---
# (Nếu thiếu dòng này, trang Thông tin tài khoản sẽ bị lỗi trắng màn hình)
current_user = {} 

def get_connection():
    # Thay tên Server của bạn vào đây
    server = 'DESKTOP-BL8B9B2\\SQLEXPRESS01' 
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
    style = ttk.Style()
    style.theme_use('clam')
    style.configure("Treeview", background="white", foreground="black", rowheight=25, fieldbackground="white")
    style.map('Treeview', background=[('selected', '#3498db')])
    style.configure("Treeview.Heading", font=('Arial', 10, 'bold'))
    style.configure("Title.TLabel", font=("Arial", 18, "bold"), foreground="#2c3e50")
    style.configure("TFrame", background=MAIN_BG)
    return style