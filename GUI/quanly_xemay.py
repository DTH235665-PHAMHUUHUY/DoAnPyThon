from tkinter import *
from tkinter import ttk, messagebox
import utils

def create_ui(parent):
    # --- BIẾN DỮ LIỆU ---
    var_sokhung = StringVar()
    var_loaixe = StringVar()
    var_tenxe = StringVar()
    var_hang = StringVar()
    var_mau = StringVar()
    var_nam = StringVar()
    var_gia = StringVar()
    var_search = StringVar()
    
    current_mode = "VIEW" # VIEW, ADD, EDIT

    # --- HÀM LOGIC ---
    def load_data(query=None):
        for i in tree.get_children(): tree.delete(i)
        conn = utils.get_connection()
        cursor = conn.cursor()
        sql = "SELECT SoKhung, LoaiXe, TenXe, HangSanXuat, MauSac, NamSanXuat, GiaBan FROM XeMay"
        if query: sql += " WHERE TenXe LIKE ? OR SoKhung LIKE ?"
        params = (f'%{query}%', f'%{query}%') if query else ()
        cursor.execute(sql, params)
        for row in cursor.fetchall():
            gia = "{:,.0f}".format(row[6])
            tree.insert("", END, values=(row[0], row[1], row[2], row[3], row[4], row[5], gia))
        conn.close()

    def set_state(mode):
        nonlocal current_mode
        current_mode = mode
        
        state_input = "normal" if mode != "VIEW" else "readonly"
        
        # Mở/Khóa ô nhập liệu
        entry_sokhung.config(state="normal" if mode == "ADD" else "readonly") # Khóa chính chỉ nhập khi ADD
        cbb_loai.config(state="readonly" if mode != "VIEW" else "disabled")
        entry_ten.config(state=state_input)
        entry_hang.config(state=state_input)
        entry_mau.config(state=state_input)
        entry_nam.config(state=state_input)
        entry_gia.config(state=state_input)
        
        # Ẩn/Hiện nút bấm
        if mode == "VIEW":
            btn_them.config(state="normal")
            btn_sua.config(state="normal")
            btn_xoa.config(state="normal")
            btn_luu.config(state="disabled")
            btn_huy.config(state="disabled")
        else: # ADD hoặc EDIT
            btn_them.config(state="disabled")
            btn_sua.config(state="disabled")
            btn_xoa.config(state="disabled")
            btn_luu.config(state="normal")
            btn_huy.config(state="normal")

    def clear_form():
        var_sokhung.set("")
        var_loaixe.set("")
        var_tenxe.set("")
        var_hang.set("")
        var_mau.set("")
        var_nam.set("")
        var_gia.set("")

    def on_click_tree(event):
        if current_mode != "VIEW": return
        item = tree.focus()
        if item:
            val = tree.item(item, 'values')
            var_sokhung.set(val[0])
            var_loaixe.set(val[1])
            var_tenxe.set(val[2])
            var_hang.set(val[3])
            var_mau.set(val[4])
            var_nam.set(val[5])
            var_gia.set(val[6].replace(",", ""))

    # --- BUTTON ACTIONS ---
    def act_them():
        clear_form()
        set_state("ADD")
        entry_sokhung.focus()

    def act_sua():
        if not var_sokhung.get(): return messagebox.showwarning("","Chọn xe cần sửa")
        set_state("EDIT")

    def act_huy():
        set_state("VIEW")
        clear_form()

    def act_xoa():
        if not var_sokhung.get(): return
        if messagebox.askyesno("Xóa", "Bạn chắc chắn xóa xe này?"):
            conn = utils.get_connection()
            try:
                conn.execute("DELETE FROM XeMay WHERE SoKhung=?", (var_sokhung.get(),))
                conn.commit()
                load_data()
                clear_form()
            except: messagebox.showerror("Lỗi", "Không thể xóa (Đã bán?)")
            finally: conn.close()

    def act_luu():
        conn = utils.get_connection()
        cursor = conn.cursor()
        try:
            val = (var_loaixe.get(), var_tenxe.get(), var_hang.get(), var_mau.get(), var_nam.get(), var_gia.get())
            if current_mode == "ADD":
                cursor.execute("INSERT INTO XeMay VALUES (?,?,?,?,?,?,?)", (var_sokhung.get(),) + val)
            else: # EDIT
                cursor.execute("UPDATE XeMay SET LoaiXe=?, TenXe=?, HangSanXuat=?, MauSac=?, NamSanXuat=?, GiaBan=? WHERE SoKhung=?", val + (var_sokhung.get(),))
            conn.commit()
            messagebox.showinfo("OK", "Lưu thành công!")
            act_huy()
            load_data()
        except Exception as e: messagebox.showerror("Lỗi", str(e))
        finally: conn.close()

    # --- LAYOUT GIAO DIỆN (GIỐNG HÌNH) ---
    
    # 1. Header
    Label(parent, text="QUẢN LÝ THÔNG TIN XE MÁY", font=("Arial", 20, "bold"), fg="#2c3e50", bg=utils.COLOR_MAIN_BG).pack(pady=15)

    # 2. Frame Form (Thông tin chi tiết)
    # Dùng LabelFrame để có cái viền bao quanh giống trong hình
    fr_info = LabelFrame(parent, text="Thông tin chi tiết", font=("Arial", 10, "bold"), bg=utils.COLOR_MAIN_BG, padx=10, pady=10)
    fr_info.pack(fill=X, padx=20)

    # Grid Layout cho Form (3 cột)
    # Cột 1
    Label(fr_info, text="Số Khung:", bg=utils.COLOR_MAIN_BG).grid(row=0, column=0, sticky=W, pady=5)
    entry_sokhung = Entry(fr_info, textvariable=var_sokhung, width=25)
    entry_sokhung.grid(row=0, column=1, padx=5)

    Label(fr_info, text="Loại Xe:", bg=utils.COLOR_MAIN_BG).grid(row=1, column=0, sticky=W, pady=5)
    cbb_loai = ttk.Combobox(fr_info, textvariable=var_loaixe, values=["Xe Tay Ga", "Xe Số", "Xe Côn Tay"], width=22)
    cbb_loai.grid(row=1, column=1, padx=5)

    # Cột 2
    Label(fr_info, text="Tên Xe:", bg=utils.COLOR_MAIN_BG).grid(row=0, column=2, sticky=W, pady=5, padx=(30,0))
    entry_ten = Entry(fr_info, textvariable=var_tenxe, width=25)
    entry_ten.grid(row=0, column=3, padx=5)

    Label(fr_info, text="Hãng SX:", bg=utils.COLOR_MAIN_BG).grid(row=1, column=2, sticky=W, pady=5, padx=(30,0))
    entry_hang = Entry(fr_info, textvariable=var_hang, width=25)
    entry_hang.grid(row=1, column=3, padx=5)

    # Cột 3
    Label(fr_info, text="Màu Sắc:", bg=utils.COLOR_MAIN_BG).grid(row=0, column=4, sticky=W, pady=5, padx=(30,0))
    entry_mau = Entry(fr_info, textvariable=var_mau, width=25)
    entry_mau.grid(row=0, column=5, padx=5)

    Label(fr_info, text="Giá Bán:", bg=utils.COLOR_MAIN_BG).grid(row=1, column=4, sticky=W, pady=5, padx=(30,0))
    entry_gia = Entry(fr_info, textvariable=var_gia, width=25)
    entry_gia.grid(row=1, column=5, padx=5)
    
    # Ẩn/Hiện Năm SX (Có thể thêm vào nếu cần, ở đây tôi demo 6 trường cho đẹp)
    entry_nam = Entry(fr_info, textvariable=var_nam) # Biến ảo để giữ code logic không lỗi

    # 3. Frame Button & Search
    fr_btn = Frame(parent, bg=utils.COLOR_MAIN_BG, pady=10)
    fr_btn.pack(fill=X, padx=20)

    # Nhóm nút CRUD
    btn_them = Button(fr_btn, text="Thêm", command=act_them, width=8, bg="#3498db", fg="white")
    btn_them.pack(side=LEFT, padx=5)
    
    btn_sua = Button(fr_btn, text="Sửa", command=act_sua, width=8, bg="#f39c12", fg="white")
    btn_sua.pack(side=LEFT, padx=5)
    
    btn_xoa = Button(fr_btn, text="Xóa", command=act_xoa, width=8, bg="#e74c3c", fg="white")
    btn_xoa.pack(side=LEFT, padx=5)

    Label(fr_btn, width=2, bg=utils.COLOR_MAIN_BG).pack(side=LEFT) # Khoảng cách

    btn_luu = Button(fr_btn, text="Lưu", command=act_luu, width=8, bg="#2ecc71", fg="white")
    btn_luu.pack(side=LEFT, padx=5)
    
    btn_huy = Button(fr_btn, text="Hủy", command=act_huy, width=8, bg="#95a5a6", fg="white")
    btn_huy.pack(side=LEFT, padx=5)

    # Tìm kiếm (Góc phải)
    Button(fr_btn, text="Tìm", command=lambda: load_data(var_search.get())).pack(side=RIGHT)
    Entry(fr_btn, textvariable=var_search, width=20).pack(side=RIGHT, padx=5)
    Label(fr_btn, text="Tìm kiếm:", bg=utils.COLOR_MAIN_BG).pack(side=RIGHT)

    # 4. Table Treeview
    fr_tree = Frame(parent)
    fr_tree.pack(fill=BOTH, expand=True, padx=20, pady=(0, 20))

    cols = ("SoKhung", "LoaiXe", "TenXe", "Hang", "Mau", "Nam", "Gia")
    tree = ttk.Treeview(fr_tree, columns=cols, show="headings")
    
    headers = ["Số Khung", "Loại Xe", "Tên Xe", "Hãng SX", "Màu", "Năm", "Giá Bán"]
    widths = [100, 100, 150, 100, 80, 60, 120]
    
    for c, h, w in zip(cols, headers, widths):
        tree.heading(c, text=h)
        tree.column(c, width=w)

    sb = Scrollbar(fr_tree, orient=VERTICAL, command=tree.yview)
    tree.configure(yscroll=sb.set)
    sb.pack(side=RIGHT, fill=Y)
    tree.pack(fill=BOTH, expand=True)
    
    tree.bind("<<TreeviewSelect>>", on_click_tree)

    # Init
    set_state("VIEW")
    load_data()