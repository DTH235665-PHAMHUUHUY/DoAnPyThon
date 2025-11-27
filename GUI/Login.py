from tkinter import *
from tkinter import messagebox
import hashlib
import utils
import main 

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Đăng Nhập")
        self.root.geometry("400x300")
        
        Label(root, text="HỆ THỐNG QUẢN LÝ XE MÁY", font=("Arial", 14, "bold"), fg="#2c3e50").pack(pady=20)
        
        frame = Frame(root)
        frame.pack(pady=10)
        
        Label(frame, text="Tài khoản:").grid(row=0, column=0, pady=10)
        self.txt_user = Entry(frame, width=25)
        self.txt_user.grid(row=0, column=1)
        
        Label(frame, text="Mật khẩu:").grid(row=1, column=0, pady=10)
        self.txt_pass = Entry(frame, width=25, show="*")
        self.txt_pass.grid(row=1, column=1)
        
        Button(root, text="Đăng Nhập", command=self.login, bg="#2ecc71", fg="white", width=15).pack(pady=20)

    def login(self):
        user = self.txt_user.get()
        pwd = hashlib.sha256(self.txt_pass.get().encode()).hexdigest()
        
        conn = utils.get_connection()
        if conn:
            cursor = conn.cursor()
            # Lấy thông tin VaiTro, HoTen, MaNhanVien
            sql = "SELECT TK.VaiTro, NV.HoVaTen, NV.MaNhanVien FROM TaiKhoan TK JOIN NhanVien NV ON TK.MaNhanVien=NV.MaNhanVien WHERE TK.TenDangNhap=? AND TK.MatKhau=?"
            cursor.execute(sql, (user, pwd))
            row = cursor.fetchone()
            conn.close()
            
            if row:
                # --- LƯU VÀO BIẾN TOÀN CỤC (QUAN TRỌNG) ---
                utils.current_user['role'] = row[0]  # Vai trò
                utils.current_user['name'] = row[1]  # Họ tên
                utils.current_user['id'] = row[2]    # Mã nhân viên
                
                self.root.destroy()
                main.main_screen(row[0], row[1])
            else:
                messagebox.showerror("Lỗi", "Sai tài khoản hoặc mật khẩu!")

if __name__ == "__main__":
    tk = Tk()
    LoginApp(tk)
    tk.mainloop()