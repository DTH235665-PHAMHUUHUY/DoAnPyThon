import tkinter as tk
import sys

# Lấy tham số từ login.py truyền sang
try:
    CURRENT_USER = sys.argv[1]
    CURRENT_ROLE = sys.argv[2]
except IndexError:
    CURRENT_USER = "Test"
    CURRENT_ROLE = "NhanVien"

root = tk.Tk()
root.title(f"Trang chủ - Xin chào {CURRENT_USER} ({CURRENT_ROLE})")
root.geometry("600x400")

tk.Label(root, text=f"HỆ THỐNG QUẢN LÝ XE MÁY", font=("Arial", 20, "bold")).pack(pady=50)
tk.Label(root, text=f"Người dùng: {CURRENT_USER}", font=("Arial", 14)).pack()
tk.Label(root, text=f"Vai trò: {CURRENT_ROLE}", font=("Arial", 14, "bold"), fg="red").pack()

# Thử nghiệm phân quyền đơn giản
if CURRENT_ROLE == "Admin":
    tk.Label(root, text="[Admin] Bạn có quyền quản lý toàn bộ hệ thống", fg="blue").pack(pady=10)
elif CURRENT_ROLE == "QuanLy":
    tk.Label(root, text="[Quản lý] Bạn có quyền quản lý kho và nhân viên", fg="green").pack(pady=10)
else:
    tk.Label(root, text="[Nhân viên] Bạn chỉ có quyền bán hàng", fg="gray").pack(pady=10)

root.mainloop()
