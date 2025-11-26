import pyodbc
from tkinter import messagebox, ttk

# --- CẤU HÌNH KẾT NỐI ---
# Hãy thay 'YOUR_SERVER_NAME' bằng tên máy chủ của bạn
DB_CONFIG = {
    'driver': '{SQL Server}',
    'server': 'YOUR_SERVER_NAME',  
    'database': 'QL_CuaHangXeMay',
    'trusted_conn': 'yes'
}

def connect_db():
    """Hàm kết nối đến CSDL SQL Server."""
    try:
        conn_string = (
            f"DRIVER={DB_CONFIG['driver']};"
            f"SERVER={DB_CONFIG['server']};"
            f"DATABASE={DB_CONFIG['database']};"
            f"Trusted_Connection={DB_CONFIG['trusted_conn']};"
        )
        conn = pyodbc.connect(conn_string)
        return conn
    except pyodbc.Error as e:
        messagebox.showerror("Lỗi kết nối CSDL", f"Không thể kết nối đến SQL Server:\n{e}")
        return None
    except Exception as e:
        messagebox.showerror("Lỗi không xác định", f"Lỗi: {str(e)}")
        return None

def setup_theme(root):
    """Cài đặt giao diện chung cho các widget."""
    style = ttk.Style(root)
    style.theme_use('clam')  # Sử dụng theme 'clam' cho hiện đại hơn default
    
    # Màu sắc chủ đạo (Xanh dương như mẫu)
    PRIMARY_COLOR = "#0078D7"
    TEXT_COLOR = "#000000"
    
    style.configure("TLabel", font=("Arial", 11))
    style.configure("Title.TLabel", font=("Arial", 18, "bold"), foreground=PRIMARY_COLOR)
    style.configure("Header.TLabel", font=("Arial", 12, "bold"), foreground="#333")
    
    style.configure("TButton", font=("Arial", 10, "bold"), background="#f0f0f0")
    style.map("TButton", background=[('active', '#e0e0e0')])
    
    style.configure("Accent.TButton", background=PRIMARY_COLOR, foreground="white")
    style.map("Accent.TButton", background=[('active', '#005a9e')])
    
    style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
    style.configure("Treeview", rowheight=25)

