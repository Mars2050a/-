"""
项目名称：图书馆信息管理系统
功能：
    学生登陆，教职工登录，管理员登陆(√)
    依照不同属性（书籍名称，书籍作者，ISBN，书籍编号）检索书籍信息（书籍名称，书籍作者，出版社，ISBN，书籍编号，存放地址，借阅状态）(√)
    全部书籍信息(√)
    借阅书籍，并添加借阅记录(√)
    删除或修改书籍信息(√)
    添加书籍信息(√)
    显示图书借阅记录，并还书(√)
    退出图书馆信息管理系统(√)
作者：Chiang Jiach'i
项目创建时间：西元2024年11月22日
"""

import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk
from tkinter import messagebox, scrolledtext
from tkinter.ttk import *
import pymysql.cursors
from datetime import datetime as dt

"""窗口位置大小"""
def location(window, w, h):
    screenwidth = window.winfo_screenwidth()
    screenheight = window.winfo_screenheight()
    x = (screenwidth - w) / 2
    y = (screenheight - h) / 2
    window.geometry("%dx%d+%d+%d" % (w, h, x, y))

""" 右页：首页 """
def begin(window, notbook):
    begin_frame = tk.Frame(window, bg='white')
    content = tk.Label(begin_frame,
                      text="\n\n>>>欢迎登录哈尔滨师范大学图书馆信息管理系统<<<\n\nEdition: V1.0.0\n\n@Author: Chiang Jiach'i\n\nCreated Time: 2024年11月22日",
                      font=font.Font(size=25), bg='white')
    content.pack(pady=100)
    notbook.add(begin_frame, text='首页')

""" 右页：全部书籍 """
def all_books(window, notbook):
    all_books_frame = tk.Frame(window, bg='white')
    books_text_box = scrolledtext.ScrolledText(all_books_frame, width=200, height=100)
    books_text_box.pack(padx=10, pady=10)
    books_db = pymysql.connect(host='127.0.0.1', user='root', password='1205', database='library', port=3306)
    cur = books_db.cursor()
    try:
        cur.execute('select * from books')
        books = cur.fetchall()
        s = ('\n' + '\t' + '书名' + '\t' + '\t' + '\t' + '\t' +
             '作者' + '\t' + '\t' +
             '出版社' + '\t' + '\t' +
             'ISBN码' + '\t' + '\t' +
             '存放地址' + '\t' + '\t' +
             '图书编号' + '\t' + '\t' +
             '借阅状态' + '\t' + '\t' + '\n' + '\n' + '\n')
        books_text_box.insert(tk.END, s)
        for row in books:
            book_data = '\t'
            for i in range(len(row)):
                if i == 0:
                    book_data += (str(row[i]) + '\t' + '\t' + '\t' + '\t')
                else:
                    book_data += (str(row[i]) + '\t' + '\t')

            books_text_box.insert(tk.END, book_data + '\n' + '\n' + '\n')
    except Exception as e:
        print("图书信息异常")
    finally:
        books_db.close()
        cur.close()
    notbook.add(all_books_frame, text='全部书籍')

"""修改借阅状态并添加借阅记录"""
def add_borrow_record(window, num, select_text):
    window.destroy()
    messagebox.showinfo('借阅成功', '请在规定日期内归还书籍！')

    # 修改MySQL数据库借阅状态
    books_db = pymysql.connect(host='127.0.0.1', user='root', password='1205', database='library', port=3306)
    cur1 = books_db.cursor()
    select_text_list = list(select_text.split('    '))
    sql1 = f"UPDATE books SET 借阅状态 = '在借' WHERE 图书编号 = '{select_text_list[5]}'"
    cur1.execute(sql1)
    books_db.commit()
    cur1.close()
    books_db.close()

    # 添加借阅记录
    borrow_record = []
    # 这里需要确保uusername和uuserno是已经定义并且有值的变量
    borrow_record.append(uusername)  # 确保这些变量已经被定义
    borrow_record.append(uuserno)    # 确保这些变量已经被定义
    borrow_record.append(select_text_list[0])
    borrow_record.append(select_text_list[5])

    current_time = dt.now().strftime('%Y-%m-%d %H:%M:%S')  # 格式化当前时间为字符串
    borrow_record.append(current_time)

    if num == 1:
        period = '30天'
        borrow_record.append(period)
    else:
        period = '60天'
        borrow_record.append(period)

    borrow_record.append('未还')

    borrow_record_db = pymysql.connect(host='127.0.0.1', user='root', password='1205', database='library', port=3306)
    cur2 = borrow_record_db.cursor()
    # 使用参数化查询来避免SQL注入和格式错误
    sql2 = '''
        INSERT INTO borrow_record(sname, sno, bookname, booknumber, borrowtime, borrowperiod, returnstatus)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    '''
    cur2.execute(sql2, tuple(borrow_record))
    cur2.close()
    borrow_record_db.commit()  # 提交事务
    borrow_record_db.close()

"""确认借阅"""
def Borrow_Book_Yes(borrow_book_frame, selected_text):
    borrow_book_frame.destroy()
    if selected_text[-6:-4] != '在架':
        messagebox.showerror('借阅失败', '本书在借中，请重新选择书籍！')
    else:
        borrow_period_frame = tk.Toplevel()  # 创建一个新的Toplevel窗口
        borrow_period_frame.title("借阅时长")
        borrow_period_frame.iconbitmap("output_icon.ico")

        location(borrow_period_frame, 250, 300)  # 假设这是设置位置的函数

        var = tk.IntVar()
        var.set(1)

        large_font = font.Font(size=15)

        label = tk.Label(borrow_period_frame, text='请选择借阅时长', font=large_font)
        label.pack(pady=30)

        period1 = tk.Radiobutton(borrow_period_frame, text='30天', font=large_font, variable=var, value=1)
        period1.pack(pady=0)

        period2 = tk.Radiobutton(borrow_period_frame, text='60天', font=large_font, variable=var, value=2)
        period2.pack(pady=30)

        # 直接在按钮的命令中获取 Radiobutton 的值
        button = tk.Button(borrow_period_frame, text='确定', bg='silver', font=large_font, width=10,
                           command=lambda: add_borrow_record(borrow_period_frame, var.get(), selected_text))
        button.pack()

        borrow_period_frame.mainloop()

"""借阅书籍 """
def borrow_book():
    selection = books_text_box.curselection()
    if selection:
        # 获取选中项的文本
        selected_text = books_text_box.get(selection)
        if selected_text[-6:-4] == '在架' or selected_text[-6:-4] == '在借':

            borrow_book_frame = tk.Toplevel()  # 创建一个新的Toplevel窗口
            borrow_book_frame.title("书籍借阅")
            borrow_book_frame.iconbitmap("output_icon.ico")

            location(borrow_book_frame, 300, 150)  # 假设这是设置位置的函数

            frame1=tk.Frame(borrow_book_frame)
            frame1.pack(pady=20)
            frame2=tk.Frame(borrow_book_frame)
            frame2.pack(pady=10)

            large_font = font.Font(size=15)
            lite_font = font.Font(size=10)

            label = tk.Label(frame1,text='确定借阅此书？',font=large_font)
            label.pack()

            borrow_yes = tk.Button(frame2,text='确定',bg='silver',font=lite_font, command = lambda : Borrow_Book_Yes(borrow_book_frame,selected_text))
            borrow_yes.pack(side='left',padx=20)
            borrow_no = tk.Button(frame2,text='取消',bg='silver',font=lite_font, command = lambda : borrow_book_frame.destroy())
            borrow_no.pack(side='left',padx=20)

            borrow_book_frame.mainloop()

# 销毁页面上的所有组件
def clear_page(page):
    for widget in page.winfo_children():
        widget.destroy()

"""检索书籍"""
def book_search_button(page, book_name, book_author, book_publisher, book_ISBN, book_number):
    clear_page(page)
    global books_text_box  # 使用全局变量books_text_box
    books_text_box = tk.Listbox(page, width=200, height=100)
    books_text_box.pack(padx=10, pady=10)
    books_db = pymysql.connect(host='127.0.0.1', user='root', password='1205', database='library', port=3306)
    cur = books_db.cursor()
    try:
        if book_name != '' or book_author != '' or book_publisher != '' or book_ISBN != '' or book_number != '':
            sql = 'select * from books where'
            book_entry = [book_name, book_author, book_publisher, book_ISBN, book_number]
            book_attribute = ['书名', '作者', '出版社', 'ISBN', '图书编号']
            space_count = 1
            for i in range(len(book_entry)):
                if book_entry[i] != '':
                    if space_count == 1:
                        sql += f" {book_attribute[i]} = '{book_entry[i]}'"
                        space_count += 1
                    else:
                        sql += f" and {book_attribute[i]} = '{book_entry[i]}'"
        else:
            sql = 'select * from books'

        cur.execute(sql)
        books = cur.fetchall()
        top = '书名     作者     出版社     ISBN码     存放地址     图书编号     借阅状态 '
        books_text_box.insert(tk.END, top)
        for row in books:
            book_data = ''
            for i in range(len(row)):
                book_data += (row[i] + '    ')
            books_text_box.insert(tk.END, book_data)

        if page == search_books_frame:
            books_text_box.bind('<<ListboxSelect>>', lambda event: borrow_book())  # 绑定选择事件
        else:
            books_text_box.bind('<<ListboxSelect>>', lambda event: choose_delete_modify())  # 绑定选择事件

    except Exception as e:
        print("图书信息异常", e)
    finally:
        books_db.close()
        cur.close()

""" 右页：根据不同属性检索书籍信息 """
search_books_frame = None
def search_books(window, notbook):
    large_font = font.Font(size=30)
    global search_books_frame
    search_books_frame = tk.Frame(window)

    tips_frame = tk.Frame(search_books_frame)
    tips_frame.pack(pady=50)
    tips_label = tk.Label(tips_frame, text='>>>请输入检索字段（可不全填），输入书名时请加上书名号<<<', font=font.Font(size=17))
    tips_label.pack(side='left')

    book_name_frame = tk.Frame(search_books_frame)
    book_name_frame.pack(pady=0)
    book_name_label = tk.Label(book_name_frame, text='书  名：', font=large_font)
    book_name_label.pack(side='left')
    global book_name_entry
    book_name_entry = tk.Entry(book_name_frame, font=large_font)
    book_name_entry.pack()

    book_author_frame = tk.Frame(search_books_frame)
    book_author_frame.pack(pady=50)
    book_author_label = tk.Label(book_author_frame, text='作  者：', font=large_font)
    book_author_label.pack(side='left')
    global book_author_entry
    book_author_entry = tk.Entry(book_author_frame, font=large_font)
    book_author_entry.pack()

    book_publisher_frame = tk.Frame(search_books_frame)
    book_publisher_frame.pack(pady=0)
    book_publisher_label = tk.Label(book_publisher_frame, text='出版社：', font=large_font)
    book_publisher_label.pack(side='left')
    global book_publisher_entry
    book_publisher_entry = tk.Entry(book_publisher_frame, font=large_font)
    book_publisher_entry.pack()

    book_ISBN_frame = tk.Frame(search_books_frame)
    book_ISBN_frame.pack(pady=50)
    book_ISBN_label = tk.Label(book_ISBN_frame, text='ISBN码：', font=large_font)
    book_ISBN_label.pack(side='left')
    global book_ISBN_entry
    book_ISBN_entry = tk.Entry(book_ISBN_frame, font=large_font)
    book_ISBN_entry.pack()

    book_number_frame = tk.Frame(search_books_frame)
    book_number_frame.pack(pady=0)
    book_number_label = tk.Label(book_number_frame, text='编  号：', font=large_font)
    book_number_label.pack(side='left')
    global book_number_entry
    book_number_entry = tk.Entry(book_number_frame, font=large_font)
    book_number_entry.pack()

    # 确认查询按钮的回调函数
    def on_search():
        book_search_button(search_books_frame, book_name_entry.get(), book_author_entry.get(), book_publisher_entry.get(), book_ISBN_entry.get(), book_number_entry.get())

    book_search = tk.Button(search_books_frame, text='确认查询', font=font.Font(size=20), padx=50, bg='silver',
                            command=on_search)
    book_search.pack(pady=50)

    notbook.add(search_books_frame, text='馆藏查询 / 书籍借阅')

"""删除书籍信息"""
def Delete(frame, selected_text):
    frame.destroy()

    # 修改MySQL数据库书籍信息
    books_db = pymysql.connect(host='127.0.0.1', user='root', password='1205', database='library', port=3306)
    cur = books_db.cursor()
    select_text_list = list(selected_text.split('    '))
    sql = f"DELETE from books WHERE 图书编号 = '{select_text_list[5]}'"
    try:
        # SQL执行代码
        cur.execute(sql)
        books_db.commit()
        messagebox.showinfo('删除成功', '退出并重新进入系统后将更新书籍信息!')

    except pymysql.Error as e:
        print(f"Error: {e}")
        messagebox.showerror('删除失败', '无法删除书籍信息，请检查错误信息!')
    finally:
        cur.close()
        books_db.close()

"""确定删除书籍信息？"""
def delete_book(frame):
    frame.destroy()
    selection = books_text_box.curselection()
    if selection:
        # 获取选中项的文本
        selected_text = books_text_box.get(selection)

        delete_book_frame = tk.Toplevel()  # 创建一个新的Toplevel窗口
        delete_book_frame.title("删除修改书籍信息")
        delete_book_frame.iconbitmap("output_icon.ico")

        location(delete_book_frame, 300, 150)  # 假设这是设置位置的函数

        frame1 = tk.Frame(delete_book_frame)
        frame1.pack(pady=20)
        frame2 = tk.Frame(delete_book_frame)
        frame2.pack(pady=10)

        large_font = font.Font(size=15)
        lite_font = font.Font(size=10)

        label = tk.Label(frame1, text='确定要删除该条书籍信息吗？', font=large_font)
        label.pack()

        delete_yes = tk.Button(frame2, text='确定', bg='silver', font=lite_font,
                               command=lambda: Delete(delete_book_frame, selected_text))
        delete_yes.pack(side='left', padx=20)
        delete_no = tk.Button(frame2, text='取消', bg='silver', font=lite_font,
                              command=lambda: delete_book_frame.destroy())
        delete_no.pack(side='left', padx=20)

        delete_book_frame.mainloop()

"""修改书籍信息"""
def modify(frame, book_name, book_author, book_publisher,book_ISBN_, book_address, book_status):
    frame.destroy()
    selection = books_text_box.curselection()
    if selection:
        # 获取选中项的文本
        selected_text = books_text_box.get(selection)
        lst = list(selected_text.split('    '))
        book_number = lst[5]
        # book_number = selected_text[-16:-10]
        # print(book_number)

        book_entry = [book_name,book_author,book_publisher,book_ISBN_,book_address,book_status]
        book_attribute = ['书名','作者','出版社','ISBN','存放地址','借阅状态']
        books_db = pymysql.connect(host='127.0.0.1', user='root', password='1205', database='library', port=3306)
        cur = books_db.cursor()
        try:
            if lst[6] == '在架':
                for i in range(len(book_entry)):
                    if book_entry[i] != '':
                        sql = f"update books set {book_attribute[i]} = '{book_entry[i]}' where 图书编号 = '{book_number}'"
                        cur.execute(sql)
                        books_db.commit()
                messagebox.showinfo('修改成功','退出并重新进入系统后将更新书籍信息！')
            else:
                messagebox.showerror('修改失败','在借状态禁止修改书籍信息！')
        except pymysql.Error as e:
            print(f"Error: {e}")
            messagebox.showerror('修改失败', '无法修改书籍信息，请检查错误信息!')
        finally:
            cur.close()
            books_db.close()

"""修改书籍信息界面"""
def modify_book(frame):
    frame.destroy()

    large_font = font.Font(size=17)

    modify_frame = tk.Toplevel()  # 创建一个新的Toplevel窗口
    modify_frame.title("修改书籍信息")
    modify_frame.iconbitmap("output_icon.ico")

    location(modify_frame, 500, 650)

    tips_frame = tk.Frame(modify_frame)
    tips_frame.pack(pady=40)
    tips_label = tk.Label(tips_frame, text='>>>请依照字段提示输入修改后的内容<<<', font=font.Font(size=15))
    tips_label.pack(side='left')

    book_name_frame1 = tk.Frame(modify_frame)
    book_name_frame1.pack(pady=0)
    book_name_label1 = tk.Label(book_name_frame1, text='书  名：', font=large_font)
    book_name_label1.pack(side='left')
    book_name_entry1 = tk.Entry(book_name_frame1, font=large_font)
    book_name_entry1.pack()

    book_author_frame1 = tk.Frame(modify_frame)
    book_author_frame1.pack(pady=40)
    book_author_label1 = tk.Label(book_author_frame1, text='作  者：', font=large_font)
    book_author_label1.pack(side='left')
    book_author_entry1 = tk.Entry(book_author_frame1, font=large_font)
    book_author_entry1.pack()

    book_publisher_frame1 = tk.Frame(modify_frame)
    book_publisher_frame1.pack(pady=0)
    book_publisher_label1 = tk.Label(book_publisher_frame1, text='出版社：', font=large_font)
    book_publisher_label1.pack(side='left')
    book_publisher_entry1 = tk.Entry(book_publisher_frame1, font=large_font)
    book_publisher_entry1.pack()

    book_ISBN_frame1 = tk.Frame(modify_frame)
    book_ISBN_frame1.pack(pady=40)
    book_ISBN_label1 = tk.Label(book_ISBN_frame1, text='ISBN号：', font=large_font)
    book_ISBN_label1.pack(side='left')
    book_ISBN_entry1 = tk.Entry(book_ISBN_frame1, font=large_font)
    book_ISBN_entry1.pack()

    book_address_frame1 = tk.Frame(modify_frame)
    book_address_frame1.pack(pady=0)
    book_address_label1 = tk.Label(book_address_frame1, text='地  址：', font=large_font)
    book_address_label1.pack(side='left')
    book_address_entry1 = tk.Entry(book_address_frame1, font=large_font)
    book_address_entry1.pack()

    # book_number_frame1 = tk.Frame(modify_frame)
    # book_number_frame1.pack(pady=40)
    # book_number_label1 = tk.Label(book_number_frame1, text='编  号：', font=large_font)
    # book_number_label1.pack(side='left')
    # book_number_entry1 = tk.Entry(book_number_frame1, font=large_font)
    # book_number_entry1.pack()

    book_status_frame1 = tk.Frame(modify_frame)
    book_status_frame1.pack(pady=40)
    book_status_label1 = tk.Label(book_status_frame1, text='状  态：', font=large_font)
    book_status_label1.pack(side='left')
    book_status_entry1 = tk.Entry(book_status_frame1, font=large_font)
    book_status_entry1.pack()

    def on_modify():
        modify(modify_frame,book_name_entry1.get(),book_author_entry1.get(),book_publisher_entry1.get(),book_ISBN_entry1.get(),book_address_entry1.get(),book_status_entry1.get())


    button_frame = tk.Frame(modify_frame)
    button_frame.pack(pady=0)
    modify_YES = tk.Button(button_frame, text='确认修改', font = font.Font(size = 15), padx = 10, bg='silver',width = 6,
                            command = on_modify)
    modify_YES.pack(side='left', padx=30)
    modify_NO = tk.Button(button_frame, text='取消修改', font = font.Font(size = 15), padx = 10, bg='silver',width = 6,
                           command = lambda : modify_frame.destroy())
    modify_NO.pack(side='left', padx=30)


    modify_frame.mainloop()

"""删除修改书籍信息选择界面"""
def choose_delete_modify():
    selection = books_text_box.curselection()
    if selection:
        # 获取选中项的文本
        selected_text = books_text_box.get(selection)
        if selected_text[-6:-4] == '在架' or selected_text[-6:-4] == '在借':

            choose_delete_modify_frame = tk.Toplevel()  # 创建一个新的Toplevel窗口
            choose_delete_modify_frame.title("删除修改书籍信息")
            choose_delete_modify_frame.iconbitmap("output_icon.ico")

            location(choose_delete_modify_frame, 300, 150)  # 假设这是设置位置的函数

            frame1 = tk.Frame(choose_delete_modify_frame)
            frame1.pack(pady=20)
            frame2 = tk.Frame(choose_delete_modify_frame)
            frame2.pack(pady=10)

            large_font = font.Font(size=15)
            lite_font = font.Font(size=10)

            label = tk.Label(frame1, text='请选择你要执行的操作项目', font=large_font)
            label.pack()

            delete_button = tk.Button(frame2, text='删除书籍信息', bg='silver', font=lite_font,
                                   command=lambda: delete_book(choose_delete_modify_frame))
            delete_button.pack(side='left', padx=20)
            modify_button = tk.Button(frame2, text='修改书籍信息', bg='silver', font=lite_font,
                                  command=lambda: modify_book(choose_delete_modify_frame))
            modify_button.pack(side='left', padx=20)

            choose_delete_modify_frame.mainloop()

""" 右页：根据不同属性检索书籍信息（管理员版） """
def search_books_admin(window, notbook):
    large_font = font.Font(size=30)
    search_books_frame_admin = tk.Frame(window)

    tips_frame = tk.Frame(search_books_frame_admin)
    tips_frame.pack(pady=50)
    tips_label = tk.Label(tips_frame, text='>>>请输入检索字段（可不全填），输入书名时请加上书名号<<<', font=font.Font(size=17))
    tips_label.pack(side='left')

    book_name_frame = tk.Frame(search_books_frame_admin)
    book_name_frame.pack(pady=0)
    book_name_label = tk.Label(book_name_frame, text='书  名：', font=large_font)
    book_name_label.pack(side='left')
    global book_name_entry
    book_name_entry = tk.Entry(book_name_frame, font=large_font)
    book_name_entry.pack()

    book_author_frame = tk.Frame(search_books_frame_admin)
    book_author_frame.pack(pady=50)
    book_author_label = tk.Label(book_author_frame, text='作  者：', font=large_font)
    book_author_label.pack(side='left')
    global book_author_entry
    book_author_entry = tk.Entry(book_author_frame, font=large_font)
    book_author_entry.pack()

    book_publisher_frame = tk.Frame(search_books_frame_admin)
    book_publisher_frame.pack(pady=0)
    book_publisher_label = tk.Label(book_publisher_frame, text='出版社：', font=large_font)
    book_publisher_label.pack(side='left')
    global book_publisher_entry
    book_publisher_entry = tk.Entry(book_publisher_frame, font=large_font)
    book_publisher_entry.pack()

    book_ISBN_frame = tk.Frame(search_books_frame_admin)
    book_ISBN_frame.pack(pady=50)
    book_ISBN_label = tk.Label(book_ISBN_frame, text='ISBN码：', font=large_font)
    book_ISBN_label.pack(side='left')
    global book_ISBN_entry
    book_ISBN_entry = tk.Entry(book_ISBN_frame, font=large_font)
    book_ISBN_entry.pack()

    book_number_frame = tk.Frame(search_books_frame_admin)
    book_number_frame.pack(pady=0)
    book_number_label = tk.Label(book_number_frame, text='编  号：', font=large_font)
    book_number_label.pack(side='left')
    global book_number_entry
    book_number_entry = tk.Entry(book_number_frame, font=large_font)
    book_number_entry.pack()

    # 确认查询按钮的回调函数
    def on_search():
        book_search_button(search_books_frame_admin, book_name_entry.get(), book_author_entry.get(), book_publisher_entry.get(), book_ISBN_entry.get(), book_number_entry.get())

    book_search = tk.Button(search_books_frame_admin, text='确认查询', font=font.Font(size=20), padx=50, bg='silver',
                            command=on_search)
    book_search.pack(pady=50)

    notbook.add(search_books_frame_admin, text='馆藏查询 / 删除书籍信息 / 修改书籍信息')

"""确定还书？"""
def Return_Book_Yes(return_book_frame, selected_text):
    return_book_frame.destroy()
    messagebox.showinfo('书籍归还成功','退出并重新进入系统后将更新书籍信息！')

    # 修改MySQL数据库借阅状态
    books_db = pymysql.connect(host='127.0.0.1', user='root', password='1205', database='library', port=3306)
    cur1 = books_db.cursor()
    select_text_list = list(selected_text.split('   '))
    sql1 = f"UPDATE books SET 借阅状态 = '在架' WHERE 图书编号 = '{select_text_list[3]}'"
    cur1.execute(sql1)
    books_db.commit()
    cur1.close()
    books_db.close()

    # 修改书籍归还状态
    records_db = pymysql.connect(host='127.0.0.1', user='root', password='1205', database='library', port=3306)
    cur2 = records_db.cursor()
    sql2 = f"UPDATE borrow_record SET returnstatus = '已还' WHERE booknumber = '{select_text_list[3]}' and borrowtime = '{select_text_list[4]}' "
    cur2.execute(sql2)
    records_db.commit()
    cur2.close()
    records_db.close()

"""还书"""
def return_book():
    selection = records_text_box.curselection()
    if selection:
        # 获取选中项的文本
        selected_text = records_text_box.get(selection)
        if selected_text[-5:-3] == '未还':

            return_book_frame = tk.Toplevel()  # 创建一个新的Toplevel窗口
            return_book_frame.title("书籍归还")
            return_book_frame.iconbitmap("output_icon.ico")

            location(return_book_frame, 300, 150)  # 假设这是设置位置的函数

            frame1=tk.Frame(return_book_frame)
            frame1.pack(pady=20)
            frame2=tk.Frame(return_book_frame)
            frame2.pack(pady=10)

            large_font = font.Font(size=15)
            lite_font = font.Font(size=10)

            label = tk.Label(frame1,text='确定归还此书？',font=large_font)
            label.pack()

            return_yes = tk.Button(frame2,text='确定',bg='silver',font=lite_font, command = lambda : Return_Book_Yes(return_book_frame,selected_text))
            return_yes.pack(side='left',padx=20)
            return_no = tk.Button(frame2,text='取消',bg='silver',font=lite_font, command = lambda : return_book_frame.destroy())
            return_no.pack(side='left',padx=20)
    
            return_book_frame.mainloop()

"""右页：借阅记录界面"""
def borrow_records(window,notbook,basedwindow):

    borrow_records_frame = tk.Frame(window)

    global records_text_box
    records_text_box = tk.Listbox(borrow_records_frame, width=200, height=100)
    records_text_box.pack(padx=10, pady=10)

    top = '姓名     学号/工号     书籍名称     图书编号     借阅时间     借阅时长     归还状态'
    records_text_box.insert(tk.END,top)

    records_db = pymysql.connect(host='127.0.0.1', user='root', password='1205', database='library', port=3306)
    cur = records_db.cursor()
    if basedwindow == student_teacher:
        sql = f'select * from borrow_record where sno = {uuserno}'
    else:
        sql = 'select * from borrow_record'
    cur.execute(sql)
    records = cur.fetchall()
    for record in records:
        format_record = ''
        for data in record:
            format_record += (data+'   ')
        records_text_box.insert(tk.END,format_record)

    records_text_box.bind('<<ListboxSelect>>', lambda event: return_book())  # 绑定选择事件

    notbook.add(borrow_records_frame,text='借阅记录 / 归还书籍')

    records_db.close()
    cur.close()

"""使用说明界面"""
def instruction(window, notbook):
    instructions_frame = tk.Frame(window, bg='white')
    text_box = tk.Listbox(instructions_frame, width=200, height=100)
    text_box.pack(padx=10, pady=10)

    try:
        with open(r'using_instruction.txt', 'r', encoding='utf-8') as file:
            lines = file.readlines()
        for line in lines:
            text_box.insert(tk.END, line.strip())
    except FileNotFoundError:
        print("文件未找到，请检查文件路径。")
    except Exception as e:
        print(f"读取文件时发生错误：{e}")

    notbook.add(instructions_frame, text='使用说明')

"""右页"""
def right_frame(window):
    rightframe_notbook = Notebook(window)
    begin(window,rightframe_notbook)
    all_books(window,rightframe_notbook)
    search_books(window,rightframe_notbook)
    borrow_records(window, rightframe_notbook,student_teacher)
    instruction(window,rightframe_notbook)

    # 配置Notebook的样式
    style = Style()
    style.configure("TNotebook.Tab", font=('Arial', 12), padding=(10, 5))  # 设置字体大小和选项卡内边距

    rightframe_notbook.pack(fill='both', expand=True)

"""
请不要问我,
为什么全文有这么多相似重复的部分？
还而不用面向对象，
问就是不会！
也不要问我，
为什么不用分支语句？
我只能说敲尼玛， 
本来我只需要复制粘贴修修改改，
就可以实现功能并有非常好的可读性，
结果用个分支语句直接让程序宕机了！
为了除掉一个小小的bug，
直接让整个程序跑不起来！
人善被人欺，
人贱学计算机！cnm!
"""

"""添加书籍信息"""
def add(book_name, book_author, book_publisher, book_ISBN, book_address, book_number, book_status):

    books_db = pymysql.connect(host='127.0.0.1', user='root', password='1205', database='library', port=3306)
    cur1 = books_db.cursor()
    sql1 = 'select 图书编号 from books'
    cur1.execute(sql1)
    book_numbers = cur1.fetchall()
    book_numberss = []
    for number in book_numbers:
        book_numberss.append(number)
    cur1.close()
    books_db.close()

    books_db = pymysql.connect(host='127.0.0.1', user='root', password='1205', database='library', port=3306)
    cur2 = books_db.cursor()
    sql2 = f"insert into books(书名,作者,出版社,ISBN,存放地址,图书编号,借阅状态)values('{book_name}','{book_author}','{book_publisher}','{book_ISBN}','{book_address}','{book_number}','{book_status}')"
    try:
        if book_number not in book_numberss:
            cur2.execute(sql2)
            books_db.commit()
            messagebox.showinfo('添加成功','退出并重新进入系统后将更新书籍信息！')
        else:
            messagebox.showerror('添加失败','图书编号已存在！')
    except pymysql.Error as e:
        print(f"Error: {e}")
        messagebox.showerror('添加失败', '无法修改书籍信息，请检查错误信息!')
    finally:
        cur2.close()
        books_db.close()

"""右页：管理员添加书籍界面"""
def add_book(window, notbook):
    add_book_frame = tk.Frame(window)
    large_font = font.Font(size=25)

    tips_frame = tk.Frame(add_book_frame)
    tips_frame.pack(pady=30)
    tips_label = tk.Label(tips_frame, text='>>>请依照字段提示输入待添加的书籍信息<<<', font=font.Font(size=15))
    tips_label.pack(side='left')

    book_name_frame1 = tk.Frame(add_book_frame)
    book_name_frame1.pack(pady=0)
    book_name_label1 = tk.Label(book_name_frame1, text='书  名：', font=large_font)
    book_name_label1.pack(side='left')
    book_name_entry1 = tk.Entry(book_name_frame1, font=large_font)
    book_name_entry1.pack()

    book_author_frame1 = tk.Frame(add_book_frame)
    book_author_frame1.pack(pady=30)
    book_author_label1 = tk.Label(book_author_frame1, text='作  者：', font=large_font)
    book_author_label1.pack(side='left')
    book_author_entry1 = tk.Entry(book_author_frame1, font=large_font)
    book_author_entry1.pack()

    book_publisher_frame1 = tk.Frame(add_book_frame)
    book_publisher_frame1.pack(pady=0)
    book_publisher_label1 = tk.Label(book_publisher_frame1, text='出版社：', font=large_font)
    book_publisher_label1.pack(side='left')
    book_publisher_entry1 = tk.Entry(book_publisher_frame1, font=large_font)
    book_publisher_entry1.pack()

    book_ISBN_frame1 = tk.Frame(add_book_frame)
    book_ISBN_frame1.pack(pady=30)
    book_ISBN_label1 = tk.Label(book_ISBN_frame1, text='ISBN号：', font=large_font)
    book_ISBN_label1.pack(side='left')
    book_ISBN_entry1 = tk.Entry(book_ISBN_frame1, font=large_font)
    book_ISBN_entry1.pack()

    book_address_frame1 = tk.Frame(add_book_frame)
    book_address_frame1.pack(pady=0)
    book_address_label1 = tk.Label(book_address_frame1, text='地  址：', font=large_font)
    book_address_label1.pack(side='left')
    book_address_entry1 = tk.Entry(book_address_frame1, font=large_font)
    book_address_entry1.pack()

    book_number_frame1 = tk.Frame(add_book_frame)
    book_number_frame1.pack(pady=30)
    book_number_label1 = tk.Label(book_number_frame1, text='编  号：', font=large_font)
    book_number_label1.pack(side='left')
    book_number_entry1 = tk.Entry(book_number_frame1, font=large_font)
    book_number_entry1.pack()

    book_status_frame1 = tk.Frame(add_book_frame)
    book_status_frame1.pack(pady=0)
    book_status_label1 = tk.Label(book_status_frame1, text='状  态：', font=large_font)
    book_status_label1.pack(side='left')
    book_status_entry1 = tk.Entry(book_status_frame1, font=large_font)
    book_status_entry1.pack()

    def on_add():
        add(book_name_entry1.get(), book_author_entry1.get(), book_publisher_entry1.get(), book_ISBN_entry1.get(), book_address_entry1.get(), book_number_entry1.get(), book_status_entry1.get())

    add_YES = tk.Button(add_book_frame, text='确认添加书籍信息', font=font.Font(size=20), padx=20, bg='silver', command=on_add)
    add_YES.pack(pady=30)

    notbook.add(add_book_frame, text='添加书籍信息')


"""右页（管理员版）"""
def right_frame_admin(window):
    rightframe_notbook = Notebook(window)
    begin(window,rightframe_notbook)
    all_books(window,rightframe_notbook)
    search_books_admin(window,rightframe_notbook)
    borrow_records(window, rightframe_notbook,admin)
    add_book(window,rightframe_notbook)
    instruction(window,rightframe_notbook)

    # 配置Notebook的样式
    style = Style()
    style.configure("TNotebook.Tab", font=('Arial', 12), padding=(10, 5))  # 设置字体大小和选项卡内边距

    rightframe_notbook.pack(fill='both', expand=True)

"""左页"""
def left_frame(login_window, username, window):
    large_font = font.Font(size=16)
    if login_window == login_student_window:
        top = tk.Label(window, text=f"hello,{username}同学！", font=large_font)
        top.pack(pady=50)
    if login_window == login_teacher_window:
        top = tk.Label(window, text=f"hello,{username}老师！", font=large_font)
        top.pack(pady=50)
    if login_window == login_admin_window:
        top = tk.Label(window, text=f"  hello,管理员！  ", font=large_font)
        top.pack(pady=50)

    current_time = dt.now()
    formatted_time = current_time.strftime("%Y年%m月%d日\n\n%H时%M分%S秒")
    time_label = tk.Label(window, text=f'本次登陆时间：\n\n{formatted_time}', font=large_font)
    time_label.pack(pady=180)

    # 检查 student_teacher 是否为 None
    if login_window == login_student_window and student_teacher is not None:
        exit_button = tk.Button(window, text='退出系统', padx=20, pady=12, font=large_font, bg='silver',
                                command=lambda: student_teacher.destroy())
        exit_button.pack(pady=50)
    # 检查 admin 是否为 None
    elif login_window == login_admin_window and admin is not None:
        exit_button = tk.Button(window, text='退出系统', padx=20, pady=12, font=large_font, bg='silver',
                                command=lambda: admin.destroy())
        exit_button.pack(pady=50)
    else:
        # 如果 student_teacher 或 admin 为 None，不创建退出按钮或提供其他处理方式
        pass


"""学生教师界面"""
student_teacher = None
def studentteacher(username,userno,login_window):
    global uusername
    uusername = username
    global uuserno
    uuserno = userno

    global student_teacher
    student_teacher = tk.Tk()
    student_teacher.title("哈尔滨师范大学图书馆信息管理系统")
    student_teacher.iconbitmap("output_icon.ico")

    location(student_teacher,1400,820)

    # 设置左右栏
    pw = tk.PanedWindow()
    leftframe = tk.LabelFrame(pw,width=400,height=1175)
    pw.add(leftframe)
    rightframe = tk.LabelFrame(pw,width=400,height=1175)
    pw.add(rightframe)
    pw.pack(fill='both',expand=True,padx=10,pady=10)

    left_frame(login_window,username,leftframe)
    right_frame(rightframe)

    student_teacher.mainloop()

"""管理员界面"""
admin = None
def adminn(username,login_window):
    global admin
    admin = tk.Tk()
    admin.title("哈尔滨师范大学图书馆信息管理系统(管理员)")
    admin.iconbitmap("output_icon.ico")

    location(admin,1400,820)

    # 设置左右栏
    pw = tk.PanedWindow()
    leftframe = tk.LabelFrame(pw,width=400,height=1175)
    pw.add(leftframe)
    rightframe = tk.LabelFrame(pw,width=400,height=1175)
    pw.add(rightframe)
    pw.pack(fill='both',expand=True,padx=10,pady=10)

    left_frame(login_window, username, leftframe)
    right_frame_admin(rightframe)

    admin.mainloop()


"""登录成功"""
def success_tip(username,userno,login_window):
    login_global_window.destroy()
    login_window.destroy()
    if login_window == login_student_window or login_window == login_teacher_window:
        studentteacher(username,userno,login_window)
    else:
        adminn(username,login_window)

"""登陆失败"""
def fail_tip(login_window):
    if login_window == login_student_window:
        messagebox.showerror("登陆失败！","姓名或学号错误！")
    elif login_window == login_teacher_window:
        messagebox.showerror("登陆失败！","姓名或工号错误！")
    else:
        messagebox.showerror("登陆失败！","管理员账号或密码错误！")

"""登录按钮逻辑"""
# 全局变量声明
login_student_window = None
login_teacher_window = None
login_admin_window = None
def auto_login(window):
    # 连接数据库
    db = pymysql.connect(host='127.0.0.1', user='root', password='1205', db='school', port=3306)
    # 获取操作游标
    cur = db.cursor()
    # 分类查询数据库
    if window == login_student_window:
        sql = 'select * from student'
    elif window == login_teacher_window:
        sql = 'select * from teacher'
    else:
        sql = 'select * from admin'

    entry1 = name.get()
    entry2 = no.get()
    flag = False
    try:
        cur.execute(sql)  # 执行查询
        results = cur.fetchall()  # 获取所有查询数据
        for row in results:
            uid = row[0]  # 姓名或账号
            pwd = row[1]  # 学号或工号或密码
            # 判断输入的账号和密码是否正确
            if entry1 == uid and entry2 == pwd:
                username = row[0]
                userno = row[1]
                success_tip(username,userno, window)
                flag = True
                break
        if not flag:
            fail_tip(window)
    except Exception as e:
        fail_tip(window)
    finally:
        cur.close()
        db.close()

"""学生登录"""
def login_student():
    global login_student_window
    login_student_window=tk.Tk()
    login_student_window.title("学生登录")
    login_student_window.iconbitmap("output_icon.ico")

    location(login_student_window,300,150)

    fsname=tk.Frame(login_student_window)
    fsname.pack(pady=10)
    fsno = tk.Frame(login_student_window)
    fsno.pack(pady=10)
    fslog = tk.Frame(login_student_window)
    fslog.pack(pady=10)

    lsname = tk.Label(fsname, text="姓名：")
    lsname.pack(side="left")
    global name
    name = tk.Entry(fsname)
    name.pack()

    lsno = tk.Label(fsno, text="学号：")
    lsno.pack(side="left")
    global no
    no = tk.Entry(fsno)
    no.pack()

    login_student = tk.Button(fslog, text="登录",command= lambda : auto_login(login_student_window))
    login_student.pack(side='left',padx=20)
    login_student_no = tk.Button(fslog, text="取消", command=lambda: login_student_window.destroy())
    login_student_no.pack(side='left',padx=20)

    login_student_window.mainloop()

"""教师登录"""
def login_teacher():
    global login_teacher_window
    login_teacher_window=tk.Tk()
    login_teacher_window.title("教师登录")
    login_teacher_window.iconbitmap("output_icon.ico")

    location(login_teacher_window,300,150)

    ftname=tk.Frame(login_teacher_window)
    ftname.pack(pady=10)
    ftno = tk.Frame(login_teacher_window)
    ftno.pack(pady=10)
    ftlog = tk.Frame(login_teacher_window)
    ftlog.pack(pady=10)

    ltname = tk.Label(ftname, text="姓名：")
    ltname.pack(side="left")
    global name
    name = tk.Entry(ftname)
    name.pack()

    ltno = tk.Label(ftno, text="工号：")
    ltno.pack(side="left")
    global no
    no = tk.Entry(ftno)
    no.pack()

    login_teacher = tk.Button(ftlog, text="登录",command=lambda : auto_login(login_teacher_window))
    login_teacher.pack(side='left',padx=20)
    login_teacher_no = tk.Button(ftlog, text="取消", command=lambda: login_teacher_window.destroy())
    login_teacher_no.pack(side='left',padx=20)

    login_teacher_window.mainloop()

"""管理员登陆"""
def login_admin():
    global login_admin_window
    login_admin_window=tk.Tk()
    login_admin_window.title("管理员登录")
    login_admin_window.iconbitmap("output_icon.ico")

    location(login_admin_window,300,150)

    faccount=tk.Frame(login_admin_window)
    faccount.pack(pady=10)
    fpassword = tk.Frame(login_admin_window)
    fpassword.pack(pady=10)
    falog = tk.Frame(login_admin_window)
    falog.pack(pady=10)

    laccount = tk.Label(faccount, text="账号：")
    laccount.pack(side="left")
    global name
    name = tk.Entry(faccount)
    name.pack()

    lpassword = tk.Label(fpassword, text="密码：")
    lpassword.pack(side="left")
    global no
    no = tk.Entry(fpassword)
    no.pack()

    login_admin = tk.Button(falog, text="登录",command=lambda : auto_login(login_admin_window))
    login_admin.pack(side='left',padx=20)
    login_admin_no = tk.Button(falog, text="取消", command=lambda: login_admin_window.destroy())
    login_admin_no.pack(side='left',padx=20)

    login_admin_window.mainloop()


"""创建登录窗口"""
def login_global():
    global login_global_window
    login_global_window = tk.Tk()
    login_global_window.title("登陆页面")
    login_global_window.iconbitmap("output_icon.ico")

    location(login_global_window,1200,800)

    image = Image.open("微信图片_20241124172307.jpg")
    library_photo = ImageTk.PhotoImage(image)
    canvas = tk.Canvas(login_global_window, width=library_photo.width(), height=library_photo.height())
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=library_photo, anchor="nw")

    login_student_button = tk.Frame(canvas)
    frame_window1 = canvas.create_window(100,50,window=login_student_button)
    login_student_button.pack(side='left',padx=100)
    large_font = font.Font(size=18)
    button_student = tk.Button(login_student_button, text=" 学生登录 ", font = large_font, padx=30, pady=10,bg='white',
                               command=login_student)
    button_student.pack()

    login_teacher_button = tk.Frame(canvas)
    frame_window2 = canvas.create_window(100, 50, window=login_teacher_button)
    login_teacher_button.pack(side='left',padx=100)
    large_font = font.Font(size=18)
    button_teacher = tk.Button(login_teacher_button, text=" 教师登录 ", font=large_font, padx=30, pady=10,bg='white',
                               command=login_teacher)
    button_teacher.pack()

    login_admin_button = tk.Frame(canvas)
    frame_window3 = canvas.create_window(100, 50, window=login_admin_button)
    login_admin_button.pack(side='left',padx=100)
    large_font = font.Font(size=18)
    button_admin = tk.Button(login_admin_button, text="管理员登录", font=large_font, padx=30,pady=10,bg='white',
                             command=login_admin)
    button_admin.pack()

    login_global_window.mainloop()

if __name__ == '__main__':
    login_global()