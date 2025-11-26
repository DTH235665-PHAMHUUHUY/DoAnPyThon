from tkinter import *
from tkinter import messagebox
import hashlib
import utils
import main 

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Đăng Nhập Hệ Thống")
        self.root.geometry("450x350")
        self.root.configure(bg="white")

        # Tiêu đề
        Label(root, text="QUẢN LÝ XE MÁY", font=("Arial", 20, "bold"), fg="#2980b9", bg="white").pack(pady=30)

        # Form
        frame = Frame(root, bg="white")
        frame.pack()

        Label(frame, text="Tên đăng nhập:", font=("Arial", 10), bg="white").grid(row=0, column=0, sticky=W, pady=10)
        self.entry_user = Entry(frame, width=30, font=("Arial", 11), relief="solid")
        self.entry_user.grid(row=0, column=1, pady=10)

        Label(frame, text="Mật khẩu:", font=("Arial", 10), bg="white").grid(row=1, column=0, sticky=W, pady=10)
        self.entry_pass = Entry(frame, width=30, font=("Arial", 11), show="*", relief="solid")
        self.entry_pass.grid(row=1, column=1, pady=10)

        # Nút đăng nhập
        Button(root, text="ĐĂNG NHẬP", command=self.login, 
               font=("Arial", 11, "bold"), bg="#2980b9", fg="white", 
               width=20, height=2, relief="flat").pack(pady=30)

    def login(self):
        user = self.entry_user.get()
        pwd = self.entry_pass.get()
        
        # Hash pass
        hashed = hashlib.sha256(pwd.encode()).hexdigest()

        conn = utils.get_connection()
        if conn:
            cursor = conn.cursor()
            sql = """SELECT TK.VaiTro, NV.HoVaTen 
                     FROM TaiKhoan TK JOIN NhanVien NV ON TK.MaNhanVien=NV.MaNhanVien 
                     WHERE TK.TenDangNhap=? AND TK.MatKhau=?"""
            cursor.execute(sql, (user, hashed))
            row = cursor.fetchone()
            conn.close()

            if row:
                self.root.destroy()
                # Mở màn hình chính
                main.main_screen(row[0], row[1]) 
            else:
                messagebox.showerror("Lỗi", "Sai thông tin đăng nhập!")

if __name__ == "__main__":
    tk = Tk()
    app = LoginApp(tk)
    tk.mainloop()