from tkinter import *
from tkinter import ttk, messagebox
import hashlib
import utils

def create_ui(parent_frame):
    # --- 1. BIẾN DỮ LIỆU ---
    parent_frame.vars = {}
    
    # Biến hiển thị (Chỉ giữ Username và Role)
    var_vaitro = StringVar()
    var_username = StringVar()
    
    # Biến đổi mật khẩu
    var_pass_old = StringVar()
    var_pass_new = StringVar()
    var_pass_confirm = StringVar()

    BG_COLOR = getattr(utils, 'MAIN_BG', 'white')
    
    # Lấy thông tin từ phiên đăng nhập
    current_id = utils.current_user.get('id', '')     
    current_role = utils.current_user.get('role', '') 

    # --- 2. HÀM XỬ LÝ ---
    def load_info():
        """Tải thông tin tài khoản"""
        var_vaitro.set(current_role if current_role else "---")

        # Truy vấn lấy Tên đăng nhập từ DB
        if current_id:
            try:
                conn = utils.get_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT TenDangNhap FROM TaiKhoan WHERE MaNhanVien=?", (current_id,))
                row = cursor.fetchone()
                if row:
                    var_username.set(row[0])
                else:
                    var_username.set("(Chưa có tài khoản)")
                conn.close()
            except:
                var_username.set("Error")

    def act_doi_mat_khau():
        old = var_pass_old.get()
        new = var_pass_new.get()
        confirm = var_pass_confirm.get()
        user = var_username.get()

        # Validate
        if not old or not new or not confirm:
            return messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ các trường mật khẩu!")
        
        if new != confirm:
            return messagebox.showerror("Lỗi", "Mật khẩu mới và Xác nhận không khớp!")
        
        if len(new) < 3:
            return messagebox.showwarning("Yếu", "Mật khẩu mới quá ngắn (tối thiểu 3 ký tự)!")

        try:
            conn = utils.get_connection()
            cursor = conn.cursor()
            
            # 1. Kiểm tra pass cũ
            hashed_old = hashlib.sha256(old.encode()).hexdigest()
            cursor.execute("SELECT MatKhau FROM TaiKhoan WHERE TenDangNhap=?", (user,))
            row = cursor.fetchone()
            
            if not row or row[0] != hashed_old:
                return messagebox.showerror("Sai mật khẩu", "Mật khẩu cũ không đúng!")

            # 2. Cập nhật pass mới
            hashed_new = hashlib.sha256(new.encode()).hexdigest()
            cursor.execute("UPDATE TaiKhoan SET MatKhau=? WHERE TenDangNhap=?", (hashed_new, user))
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Thành công", "Đổi mật khẩu thành công!")
            
            # Xóa trắng ô nhập
            var_pass_old.set("")
            var_pass_new.set("")
            var_pass_confirm.set("")
            
        except Exception as e:
            messagebox.showerror("Lỗi SQL", str(e))

    # --- 3. GIAO DIỆN ---
    
    # Tiêu đề
    Label(parent_frame, text="THÔNG TIN TÀI KHOẢN", 
          font=("Arial", 20, "bold"), fg="#2c3e50", bg=BG_COLOR).pack(pady=20)

    # === KHUNG 1: THÔNG TIN CƠ BẢN ===
    fr_info = LabelFrame(parent_frame, text="Thông tin tài khoản", 
                         font=("Arial", 11, "bold"), bg=BG_COLOR, padx=20, pady=15)
    fr_info.pack(fill=X, padx=50, pady=10)

    # Dòng 1: Tên đăng nhập (Màu Xanh)
    Label(fr_info, text="Tên đăng nhập:", font=("Arial", 11), bg=BG_COLOR).grid(row=0, column=0, sticky=W, pady=8)
    Label(fr_info, textvariable=var_username, font=("Arial", 11, "bold"), fg="blue", bg=BG_COLOR).grid(row=0, column=1, sticky=W, padx=20)

    # Dòng 2: Chức vụ (Màu Đỏ)
    Label(fr_info, text="Chức vụ:", font=("Arial", 11), bg=BG_COLOR).grid(row=1, column=0, sticky=W, pady=8)
    Label(fr_info, textvariable=var_vaitro, font=("Arial", 11, "bold"), fg="red", bg=BG_COLOR).grid(row=1, column=1, sticky=W, padx=20)


    # === KHUNG 2: ĐỔI MẬT KHẨU ===
    fr_pass = LabelFrame(parent_frame, text="Đổi Mật Khẩu", 
                         font=("Arial", 11, "bold"), bg=BG_COLOR, padx=20, pady=15)
    fr_pass.pack(fill=X, padx=50, pady=10)

    # Hàm tạo ô nhập
    def make_entry(label_text, text_var, row_idx):
        Label(fr_pass, text=label_text, font=("Arial", 11), bg=BG_COLOR).grid(row=row_idx, column=0, sticky=W, pady=8)
        Entry(fr_pass, textvariable=text_var, show="*", width=35, font=("Arial", 10)).grid(row=row_idx, column=1, sticky=W, padx=20)

    make_entry("Mật khẩu cũ:", var_pass_old, 0)
    make_entry("Mật khẩu mới:", var_pass_new, 1)
    make_entry("Nhập lại mật khẩu mới:", var_pass_confirm, 2)

    # Nút Xác nhận
    Button(fr_pass, text="LƯU MẬT KHẨU MỚI", command=act_doi_mat_khau,
           bg="#27ae60", fg="white", font=("Arial", 10, "bold"), 
           width=22, height=2, cursor="hand2").grid(row=3, column=1, pady=20, sticky=W, padx=20)

    # Khởi chạy
    load_info()