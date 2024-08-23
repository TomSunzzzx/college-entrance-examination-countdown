import datetime, time  # 时间相关库
import random  # 随机数库，用于随机产生标语
import tkinter as tk  # GUI的相关库
from tkinter import simpledialog, messagebox, font  # 对话窗口的相关库
import base64  # 简单保护一下密码，对称性加密（够用了）


# 程序变量


# 写给未来接手程序的人！！！
# 由于时间紧张，还没来得及编写设置功能调整时间表。
# 所以将时间表放在程序内部，本人高考结束以后会更新程序为从外部文件读取！！！
# 如有需要更新的版本，请联系我 Q：2979987115
# 如果你有能力修改代码、编译的话，可以按照下面方式更改时间表
# 若要更改时间段，请在datetime.time的括号内输入正确的时间，例如：上午8点40：
# 的格式是datetime.time(8, 40)
# 24小时计时法
# 倒计时程序会在以下时间点重启！

# 重启时间列表
reboot_time_weekdays = [datetime.time(7, 50),
                        datetime.time(8, 40),
                        datetime.time(9, 30),
                        datetime.time(10, 50),
                        datetime.time(11, 45),
                        datetime.time(14, 40),
                        datetime.time(15, 30),
                        datetime.time(16, 50),
                        datetime.time(17, 35),
                        datetime.time(19, 50)]

reboot_time_weekends = [datetime.time(10, 50),
                        datetime.time(11, 40),
                        datetime.time(14, 45),
                        datetime.time(15, 40),
                        datetime.time(16, 35),
                        datetime.time(17, 30)]


# 为了不妨碍上课，本程序可以在上课期间临时关闭程序，并在重启时间列表里的时间点重启
# 这是一个二维列表，记录了可以关闭的开始时间点和结束时间点！

# 允许临时关闭的时间二维列表：[start, end]
admit_close_time_weekdays = [[datetime.time(7, 59), datetime.time(8, 40)],
                             [datetime.time(8, 49), datetime.time(9, 30)],
                             [datetime.time(10, 59), datetime.time(11, 45)],
                             [datetime.time(14, 0), datetime.time(14, 40)],
                             [datetime.time(14, 49), datetime.time(15, 30)],
                             [datetime.time(16, 10), datetime.time(16, 50)],
                             [datetime.time(16, 59), datetime.time(17, 35)],
                             [datetime.time(18, 10), datetime.time(19, 50)]]

admit_close_time_weekends = [[datetime.time(10, 10), datetime.time(10, 50)],
                              [datetime.time(11, 0), datetime.time(11, 40)],
                              [datetime.time(14, 0), datetime.time(14, 45)],
                              [datetime.time(14, 55), datetime.time(15 ,40)],
                              [datetime.time(15, 50), datetime.time(16, 35)],
                              [datetime.time(16, 45), datetime.time(17, 30)]]

# 作者信息不能打开多个，设置flag
opened_info = False

# 初始化
today = datetime.datetime.today()
weekday = today.weekday()
if weekday == 5:
    reboot_schedule = reboot_time_weekends
    admit_close_schedule = admit_close_time_weekends
else:
    reboot_schedule = reboot_time_weekdays
    admit_close_schedule = admit_close_time_weekdays

# 打开txt文件
file_path = "content.txt"
with open(file_path, "r", encoding="utf-8") as file:
    # 读取文件内容并存储到列表中
    content = file.readlines()


# 模块1 计算时间差、按钮函数

# button_fresh用于按钮刷新信号
# 经测试发现：程序如果比系统时间程序启动得早的话，开启时有可能引起时间停留在前一天
# 故编写刷新函数重新获取时间。
# 来不及优化了，暂时编写成关闭再启动吧！后续会改
def button_fresh() -> None:
    global win
    win.destroy()
    create_win()

# 密码永久关闭程序    
def p_close_win() -> None:
    global win
    result = simpledialog.askstring('提示：', '          输入管理员密码关闭程序          ', show='*')
    if result is not None:
        p = bytes(result,'utf-8')
        p = base64.b64encode(p)
        if p == b'Z2Fva2FvamlheW91':
            win.destroy()
        else:
            messagebox.showerror('错误！', '密码错误！')
            
# 临时关闭程序
# 写得不好，1.2.0会改进！！！
def t_close_win() -> None:
    global admit_close_schedule, reboot_schedule
    
    current_time = datetime.datetime.now().time()
    for i in admit_close_schedule:
        if i[0] <= current_time <= i[1]:
            messagebox.showinfo('提示', '即将临时关闭，将在下课时重新开启')
            win.destroy()
            while True:
                current_time = datetime.datetime.now().time()
                current_time = datetime.time(current_time.hour, current_time.minute)
                if current_time in reboot_schedule:
                    create_win()
                    break
                time.sleep(1)
            break
    else:
        messagebox.showerror('错误', '下课期间禁止临时关闭程序！')
        
# 作者信息
def author_info():
    global opened_info
    if opened_info:  # 判断是否打开了窗口
        return  # 打开了窗口，避免重复打开，用return中断函数，不执行创建窗口的代码。
                # 简单的if判断，不用if - else，提高执行效率。
    opened_info = True
    
    # 嵌套函数，用于关闭win2时刷新flag的值
    def close_win2():
        global opened_info
        opened_info = False
        win2.destroy()

    win2 = tk.Tk()
    win2.geometry('250x250')
    win2.resizable(False, False)  # 禁止修改大小
    # 居中显示
    # 获取屏幕的宽度和高度
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()

    # 计算窗口的左上角坐标
    x = int((screen_width - 250) / 2)
    y = int((screen_height - 300) / 2)
    win2.geometry('+{}+{}'.format(x, y))

    t = tk.Text(win2, height=20, width=25)
    t.insert(tk.END, '高考计时器\nV：1.1.0\n作者：24届10班孙培煊\nQQ：2979987115\n有Bug及时反馈\n未经允许禁止转载！\n程序语言：python\nGUI库：tkinter')
    f = font.Font(size=5)
    t.configure(bg=win2.cget('bg'), font=f, state='disabled', borderwidth=0, highlightthickness=0)
    t.pack()

    win2.protocol("WM_DELETE_WINDOW", close_win2)
    win2.mainloop()



# 模块2 GUI及主要功能
# 写成函数，用于重启
def create_win():
    global win, path

    # 获取当前日期时间
    now = datetime.datetime.now()
    # 设置未来日期时间
    future = datetime.datetime(now.year, 6, 7, 0, 0, 0)
    # 如果在6月7日后使用倒计时，则计算明年倒计时
    if now > future:
        future = datetime.datetime(now.year + 1, 6, 7, 0, 0, 0)
        time_diff = future - now  # 计算时间差
        t = time_diff.days + 1
    else:
        time_diff = future - now  # 计算时间差
        t = time_diff.days + 1
    


    # 创建窗口
    win = tk.Tk()
    win.geometry('650x450')

    # 居中显示
    # 获取屏幕的宽度和高度
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()

    # 计算窗口的左上角坐标
    x = int((screen_width - 650) / 2)
    y = int((screen_height - 450) / 2)

    win.geometry('+{}+{}'.format(x, y))

    # 隐藏窗口的标题栏和边框
    win.overrideredirect(True)

    b1 = tk.Button(win, text='关闭', width=5, height=1, command=p_close_win)
    b2 = tk.Button(win, text='临时关闭', width=6, height=1, command=t_close_win)
    b3 = tk.Button(win, text='刷新', width=5, height=1, command=button_fresh)
    b4 = tk.Button(win, text='作者信息', width=6, height=1, command=author_info)
    b5 = tk.Button(win, text='设置', width=5, height=1)  # 功能未开发

    # 将按钮放置在右下角
    b1.pack(side='right', anchor='se')
    b2.pack(side='right', anchor='se')
    b3.pack(side='right', anchor='se')
    b4.pack(side='right', anchor='se')

    # 倒计时显示
    # “距离高考仅剩”文本
    text = tk.Text(win, height=2, width=12)
    font1 = font.Font(size=35)
    text.insert(tk.END, '距离高考仅剩')
    text.configure(bg=win.cget('bg'), font=font1, state='disabled', borderwidth=0, highlightthickness=0)

    # 使用place()方法设置文本的起始位置
    text.place(x=55, y=100)

    # 时间
    text2 = tk.Text(win, height=2, width=5)
    text2.insert(tk.END, str(t), 'red')
    tk.Text.tag_configure(text2, 'red', foreground='red')
    text2.configure(bg=win.cget('bg'), font=font1, state='disabled', borderwidth=0, highlightthickness=0)

    # 使用place()方法设置文本的起始位置
    text2.place(x=385, y=100)

    # “天”文本
    text3 = tk.Text(win, height=2, width=3)
    text3.insert(tk.END, '天')
    text3.configure(bg=win.cget('bg'), font=font1, state='disabled', borderwidth=0, highlightthickness=0)

    # 使用place()方法设置文本的起始位置
    text3.place(x=475, y=100)

    # 鼓励文本
    text4 = tk.Text(win, height=2, width=50)
    font2 = font.Font(size=15)
    text4.insert(tk.END, random.choice(content), 'red')
    tk.Text.tag_configure(text4, 'red', foreground='red')
    
    # 居中显示文本
    text4.tag_configure('center', justify='center')
    text4.tag_add('center', '1.0', 'end')
    text4.configure(bg=win.cget('bg'), font=font2, state='disabled', borderwidth=0, highlightthickness=0)

    # 使用place()方法设置文本的起始位置
    text4.place(x=30, y=250)

    # 提示文本
    text5 = tk.Text(win, height=2, width=50)
    text5.insert(tk.END, '提示：教师上课期间可以点击“临时关闭”关闭程序！')
    text5.configure(bg=win.cget('bg'), state='disabled', borderwidth=0, highlightthickness=0)
    
    # 使用place()方法设置文本的起始位置
    text5.place(x=100, y=350)

    
    win.protocol("WM_DELETE_WINDOW", p_close_win)
    win.mainloop()



create_win()
