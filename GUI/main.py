from tkinter import *
import utils
import quanly_xemay 

class MainApp:
    def __init__(self, root, role, fullname):
        self.root = root
        self.root.title("Phần Mềm Quản Lý Cửa Hàng Xe Máy")
        self.root.state('zoomed') # Full màn hình
        utils.setup_style()

        # --- CHIA LAYOUT (Giống hình bạn gửi) ---
        # 1. MENU TRÁI (Sidebar)
        self.sidebar = Frame(root, bg=utils.COLOR_MENU_BG, width=220)
        self.sidebar.pack(side=LEFT, fill=Y)
        self.sidebar.pack_propagate(False) # Cố định chiều rộng

        # 2. NỘI DUNG PHẢI (Content)
        self.content = Frame(root, bg=utils.COLOR_MAIN_BG)
        self.content.pack(side=RIGHT, fill=BOTH, expand=True)

        # --- NỘI DUNG MENU TRÁI ---
        # Logo/Avatar
        Label(self.sidebar, text="QL XE MÁY", font=("Arial", 18, "bold"), 
              bg=utils.COLOR_MENU_BG, fg="white").pack(pady=30)
        
        Label(self.sidebar, text=f"Hi, {fullname}", font=("Arial", 10, "italic"),
              bg=utils.COLOR_MENU_BG, fg="#f1c40f").pack(pady=(0, 20))

        # Các nút Menu
        self.create_menu_btn("Trang Chủ", self.show_home)
        self.create_menu_btn("Quản Lý Xe Máy", self.show_xe)
        self.create_menu_btn("Quản Lý Nhân Viên", lambda: None) # Chưa làm
        self.create_menu_btn("Hóa Đơn", lambda: None) # Chưa làm
        
        Button(self.sidebar, text="Đăng Xuất", command=root.destroy, bg="red", fg="white").pack(side=BOTTOM, fill=X)

        self.show_home() # Mặc định vào trang chủ

    def create_menu_btn(self, text, command):
        btn = Button(self.sidebar, text=text, command=command,
                     bg=utils.COLOR_MENU_BG, fg=utils.COLOR_MENU_FG,
                     font=("Arial", 11), anchor="w", padx=20, pady=12,
                     relief="flat", activebackground=utils.COLOR_BTN_HOVER)
        btn.pack(fill=X, pady=1)

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def show_home(self):
        self.clear_content()
        Label(self.content, text="TRANG CHỦ", font=("Arial", 30), bg=utils.COLOR_MAIN_BG).pack(pady=100)

    def show_xe(self):
        self.clear_content()
        quanly_xemay.create_ui(self.content)

def main_screen(role, name):
    root = Tk()
    MainApp(root, role, name)
    root.mainloop()