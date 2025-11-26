import tkinter as tk
from tkinter import messagebox
import hashlib
import sys
import os
import subprocess
import utils  # Import file utils vừa tạo

def hash_password(password):
    """Mã hóa mật khẩu sang SHA-256 để so sánh với CSDL."""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def check_login(event=None):
    username = entry_username.get()
    password = entry_password.get()

    if not username or not password:
        messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập Tên đăng nhập và Mật khẩu.")
        return

    conn = utils.connect_db()
    if conn is None: return

    try:
        cur = conn.cursor()
        # Lấy Mật khẩu, Vai trò và Mã NV dựa trên tên đăng nhập
        sql = "SELECT MatKhau, VaiTro, MaNhanVien FROM TaiKhoan WHERE TenDangNhap = ?"
        cur.execute(sql, (username,))
        record = cur.fetchone()

        if record:
            db_pass = record[0]
            db_role = record[1]
            # db_manv = record[2] # Có thể dùng sau này nếu cần
            
            input_hash = hash_password(password)
            
            # So sánh mật khẩu đã mã hóa
            if input_hash == db_pass:
                messagebox.showinfo("Thành công", f"Đăng nhập thành công!\nVai trò: {db_role}")
                login_window.destroy()
                open_main_menu(username, db_role)
            else:
                messagebox.showerror("Lỗi", "Sai mật khẩu.")
        else:
            messagebox.showerror("Lỗi", "Tên đăng nhập không tồn tại.")
            
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi hệ thống: {e}")
    finally:
        if conn: conn.close()

def open_main_menu(username, role):
    """Mở file main.py và truyền tham số."""
    python_exec = sys.executable
    script_path = os.path.join(os.path.dirname(_file_), "main.py")
    
    if not os.path.exists(script_path):
        messagebox.showerror("Lỗi", "Không tìm thấy file main.py")
        return

    # Truyền username và role sang main.py
    subprocess.Popen([python_exec, script_path, username, role])

# --- GIAO DIỆN LOGIN ---
login_window = tk.Tk()
login_window.title("Đăng nhập - Quản lý Cửa hàng Xe máy")
login_window.geometry("400x300")
login_window.resizable(False, False)

# Căn giữa màn hình
screen_width = login_window.winfo_screenwidth()
screen_height = login_window.winfo_screenheight()
x = (screen_width/2) - (400/2)
y = (screen_height/2) - (300/2)
login_window.geometry('%dx%d+%d+%d' % (400, 300, x, y))

# Widget
tk.Label(login_window, text="ĐĂNG NHẬP HỆ THỐNG", font=("Arial", 16, "bold"), fg="#0078D7").pack(pady=30)

frame_form = tk.Frame(login_window)
frame_form.pack()

tk.Label(frame_form, text="Tài khoản:").grid(row=0, column=0, padx=5, pady=10, sticky="e")
entry_username = tk.Entry(frame_form, font=("Arial", 12))
entry_username.grid(row=0, column=1, padx=5, pady=10)

tk.Label(frame_form, text="Mật khẩu:").grid(row=1, column=0, padx=5, pady=10, sticky="e")
entry_password = tk.Entry(frame_form, font=("Arial", 12), show="*")
entry_password.grid(row=1, column=1, padx=5, pady=10)

btn_login = tk.Button(login_window, text="Đăng nhập", font=("Arial", 12, "bold"), 
                      bg="#0078D7", fg="white", width=20, command=check_login)
btn_login.pack(pady=30)

login_window.bind('<Return>', check_login)
login_window.mainloop()


