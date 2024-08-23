import datetime, time  # 时间相关库
import random  # 随机数库，用于随机产生标语
import tkinter as tk  # GUI的相关库
from tkinter import ttk
from tkinter import simpledialog, messagebox, font  # 对话窗口的相关库
import base64  # 简单保护一下密码
import json  # 处理json格式数据
import os, sys  # 用于获取文件路径
import traceback

# 程序所用的变量
# 窗口不能重复打开，设置flag
opened_info = False
opened_settings = False
opened_main = False



# 模块1 计算时间差、获取资源、按钮函数

# 初始化
def init_data(need: bool=True) -> None:
    global password, schedule, days, skin_path, content, config, is_special, schedule_view_page1, schedule_view_page2, now_view

    if not need:
        return

    # 获取配置资源
    if not os.path.exists('config.json'):
        messagebox.showinfo('提示', '未找到配置文件，将创建初始config文件，请勿删除！')
        config = {"adminPass": "", "schedule": {"normal": [], "special": {"state": "negtive", "activeDays": [], "schedule": []}}, "skin": "skin/originalskin.json", "desktopMode":False}
    else:
        try:
            with open('config.json', 'r', encoding='utf-8') as config_file:
                config = json.load(config_file)
        except:
            tb = traceback.format_exc()
            messagebox.showerror('错误', '程序因无法正确读取和解析文件而发生如下错误无法正常运行，您可以将错误截图反馈给作者：2979987115@qq.com\n\n{0}\n此外，如果您具备相关知识，请根据以上错误修复文件\n\n\t\t！！！注意！！！\n由于此错误，你可以选择恢复到初始的配置文件。\n请在下一个弹窗中点击“确定”来更新文件，点击“取消”程序将保留出错的配置文件并退出。'.format(str(tb)))
            ques = messagebox.askyesno('', '是否恢复到初始的配置文件')
            if ques:
                config = {"adminPass": "", "schedule": {"normal": [], "special": {"state": "negtive", "activeDays": [], "schedule": []}}, "skin": "skin/originalskin.json", "desktopMode":False}
            else:
                exit()

    # 配置变量
    try:
        password = config['adminPass']
        schedule_view_page1 = config['schedule']['normal']
        schedule_view_page2 = config['schedule']['special']['schedule']
        skin_path = config['skin']
    except:
        tb = traceback.format_exc()
        messagebox.showerror('错误', '程序因无法正确读取和解析文件而发生如下错误无法正常运行，您可以将错误截图反馈给作者：2979987115@qq.com\n\n{0}\n此外，如果您具备相关知识，请根据以上错误修复文件\n\n\t\t！！！注意！！！\n由于此错误，程序即将退出。请重新下载配置正确文件！'.format(str(tb)))
        exit()

    # 需要处理的变量
    # 1、时间
    # 获取当前日期时间
    now = datetime.datetime.now()
    # 设置未来日期时间
    future = datetime.datetime(now.year, 6, 7, 0, 0, 0)
    # 如果在6月7日后使用倒计时，则计算明年倒计时
    if now > future:
        future = datetime.datetime(now.year + 1, 6, 7, 0, 0, 0)
        time_diff = future - now  # 计算时间差
        days = time_diff.days + 1
    else:
        time_diff = future - now  # 计算时间差
        days = time_diff.days + 1
    days = str(days)

    # 2、把每个时间表里的元素换成datetime对象，并把使用的时间表赋值给schedule
    try:
        for i in range(len(schedule_view_page1)):
            schedule_view_page1[i] = [datetime.time(int(schedule_view_page1[i][0].split(',')[0]), int(schedule_view_page1[i][0].split(',')[1])), datetime.time(int(schedule_view_page1[i][1].split(',')[0]), int(schedule_view_page1[i][1].split(',')[1]))]
        for i in range(len(schedule_view_page2)):
            schedule_view_page2[i] = [datetime.time(int(schedule_view_page2[i][0].split(',')[0]), int(schedule_view_page2[i][0].split(',')[1])), datetime.time(int(schedule_view_page2[i][1].split(',')[0]), int(schedule_view_page2[i][1].split(',')[1]))]
        if config['schedule']['special']['state'] == 'active' and datetime.datetime.today().today() in config['schedule']['special']['activeDays']:
            schedule = now_view = schedule_view_page2
            is_special = True
        else:
            schedule = now_view = schedule_view_page1
            is_special = False
    except:
        tb = traceback.format_exc()
        messagebox.showerror('错误', '程序因无法正确读取和解析文件而发生如下错误无法正常运行，您可以将错误截图反馈给作者：2979987115@qq.com\n\n{0}\n此外，如果您具备相关知识，请根据以上错误修复文件\n\n\t\t！！！注意！！！\n由于此错误，程序即将退出。请重新下载配置正确文件！'.format(str(tb)))
        exit()

    # 3、读取content.txt，获取文本
    try:
        with open('content.txt', 'r', encoding='utf-8') as f:
            content = f.readlines()
    except:
        messagebox.showwarning('警告', '无法读取content.txt文件，可能文件不存在或损坏，将新建文件，请勿删除！')
        messagebox.showwarning('警告', '由于无法读取content.txt文件内容，如果皮肤中设置了鼓励文本，将无法显示！\n请转到“设置”录入文本！')
        content = [None]

    return


# button_fresh用于按钮刷新信号
# 经测试发现：程序如果比系统时间程序启动得早的话，开启时有可能引起时间停留在前一天
# 故编写刷新函数重新获取时间。
def button_fresh() -> None:
    global refresh_list, win, days, content

    # 获取当前日期时间
    now = datetime.datetime.now()
    # 设置未来日期时间
    future = datetime.datetime(now.year, 6, 7, 0, 0, 0)
    # 如果在6月7日后使用倒计时，则计算明年倒计时
    if now > future:
        future = datetime.datetime(now.year + 1, 6, 7, 0, 0, 0)
        time_diff = future - now  # 计算时间差
        days = time_diff.days + 1
    else:
        time_diff = future - now  # 计算时间差
        days = time_diff.days + 1
    days = str(days)

    for i in range(len(refresh_list)):
        refresh_list[i][1].destroy()
        if refresh_list[i][0] == '$days':
            text = tk.Text(win, height=int(refresh_list[i][2]['size'].split(',')[0]), width=int(refresh_list[i][2]['size'].split(',')[1]))
            text.insert(tk.END, days, refresh_list[i][2]['color'])
            tk.Text.tag_configure(text, refresh_list[i][2]['color'], foreground=refresh_list[i][2]['color'])
            text.configure(bg=win.cget('bg'), font=font.Font(size=refresh_list[i][2]['fontsize']), state='disabled', borderwidth=0, highlightthickness=0)
            text.place(x=int(refresh_list[i][2]['pos'].split(',')[0]), y=int(refresh_list[i][2]['pos'].split(',')[1]))
            del text
        elif refresh_list[i][0] == '$couragements':
            text = tk.Text(win, height=int(refresh_list[i][2]['size'].split(',')[0]), width=int(refresh_list[i][2]['size'].split(',')[1]))
            text.insert(tk.END, random.choice(content), refresh_list[i][2]['color'])
            text.tag_configure('center', justify='center')
            text.tag_add('center', '1.0', 'end')
            tk.Text.tag_configure(text, refresh_list[i][2]['color'], foreground=refresh_list[i][2]['color'])
            text.configure(bg=win.cget('bg'), font=font.Font(size=refresh_list[i][2]['fontsize']), state='disabled', borderwidth=0, highlightthickness=0)
            text.place(x=int(refresh_list[i][2]['pos'].split(',')[0]), y=int(refresh_list[i][2]['pos'].split(',')[1]))
            del text

    win.attributes('-topmost', False)

    return


# 密码永久关闭程序
def p_close_win() -> None:
    global win, password

    if password == '':
        win.destroy()
        return
    
    try:
        result = simpledialog.askstring('提示：', '          输入管理员密码关闭程序          ', show='*')
        if result is not None:
            input_password = bytes(result, 'utf-8')
            if input_password == base64.b64decode(bytes(password, 'utf-8')):
                win.destroy()
            else:
                messagebox.showerror('错误！', '密码错误！')
    except:
        tb = traceback.format_exc()
        messagebox.showerror('警告', '由于无法解析密码而发生以下错误，您可以将错误截图反馈给作者：2979987115@qq.com\n\n{0}\n此外，如果您具备相关知识，请根据以上错误修复文件\n\n\t\t！！！注意！！！\n由于此错误，密码将无效。\n请转到“设置”重新设置密码。'.format(tb))
        win.destroy()
        exit()

    return


# 临时关闭程序
# 相比1.1.2减少了循环、减少重启时间表、代码量
# 可能会比上一版本慢零点几秒，无大碍
def t_close_win() -> None:
    global schedule, win

    current_time = datetime.datetime.now()
    for i in schedule:
        if i[0] <= current_time.time() <= i[1]:
            win.destroy()
            messagebox.showinfo('提示', '即将在下课时重启（重启窗口置于最底层，不会占用屏幕，请放心上课）')
            reboot_time = datetime.datetime.combine(datetime.datetime.today().date(), i[1])
            time.sleep((reboot_time - current_time).total_seconds())
            create_win(False)
            break
    else:
        messagebox.showwarning('提示', '下课期间禁止临时关闭程序！')

        return


# 作者信息
def author_info() -> None:
    global opened_info

    # 关闭窗口逻辑
    if opened_info:  # 判断是否打开了窗口
        return  # 用return中断函数，不执行创建窗口的代码。

    opened_info = True

    # 嵌套函数，用于关闭win2时刷新flag的值
    def close_win2():
        global opened_info

        opened_info = False
        win2.destroy()

    win2 = tk.Tk()
    win2.geometry(f'250x375+{int((win2.winfo_screenwidth() - 250) / 2)}+{int((win2.winfo_screenheight() - 375) / 2)}')
    win2.resizable(False, False)  # 禁止修改大小

    t = tk.Text(win2, height=20, width=25)
    t.insert(tk.END, '高考计时器\nV：1.3.0(2024.8.31)\n作者：孙培煊\nQQ：2979987115\n有Bug及时反馈\n未经允许禁止转载！\n程序语言：python\nGUI库：tkinter\n\n新版本1.3.0已发布！\n更新内容：\n1.部分“设置”功能，包括密码修改、时间表的增、删、改、修改特殊时间表及触发日期。\n2.对临时关闭功能算法小修改。\n3.现在可以通过修改配置文件以及皮肤文件对程序做出改动，详情请看“开发须知.txt”文件。\n\n更新计划（画饼）\n1.继续完成设置功能\n2.做皮肤编辑器\n3.开发者模式（调试、运行日志）\n4.更新日志')
    f = font.Font(size=5)
    t.configure(bg=win2.cget('bg'), font=f, state='disabled', borderwidth=0, highlightthickness=0)
    t.pack()

    win2.protocol('WM_DELETE_WINDOW', close_win2)
    win2.mainloop()

    return

# 设置
def settings() -> None:
    global opened_settings, schedule, is_special, now_view

    # 关闭窗口的逻辑
    if opened_settings:  # 判断是否打开了窗口
        return  # 用return中断函数，不执行创建窗口的代码。

    opened_settings = True

    def close_win_settings():
        global opened_settings

        opened_settings = False
        win_settings.destroy()
    
    # ==========================================================================================================
    # 第一部分：GUI、控件放置
    win_settings = tk.Tk()
    win_settings.title('设置')
    screen_width, screen_height = win_settings.winfo_screenwidth(), win_settings.winfo_screenheight()
    x = int((screen_width - 500) / 2)
    y = int((screen_height - 200) / 2)
    win_settings.geometry(f'+{x}+{y}')

    # Frame部分
    frame_setting = ttk.Frame(win_settings, width=500, height=200)
    frame_setting.pack()
    frame_change_pwd = ttk.Frame(win_settings, width=400, height=300)
    frame_change_schedule = ttk.Frame(win_settings, width=400, height=500)

    # Button部分
    # setting界面的
    btn_change_pwd = ttk.Button(frame_setting, text='修改密码')
    btn_change_pwd.place(relx=0.1, rely=0.2)
    btn_change_schedule = ttk.Button(frame_setting, text='修改时间表')
    btn_change_schedule.place(relx=0.1, rely=0.7)

    # 修改密码界面的
    btn_change_pwd_sure = ttk.Button(frame_change_pwd, text='确认')
    btn_change_pwd_sure.place(x=145, y=190)
    btn_change_pwd_return = ttk.Button(frame_change_pwd, text='返回')
    btn_change_pwd_return.place(x=350, y=270, width=50, height=30)

    # 修改时间表界面的
    btn_change_schedule_return = ttk.Button(frame_change_schedule, text='返回')
    btn_change_schedule_return.place(x=350, y=470, width=50, height=30)
    btn_change_schedule_view_changer = ttk.Button(frame_change_schedule, text='查看日常时间表' if is_special else '查看特殊时间表' )
    btn_change_schedule_view_changer.place(x=50, y=310)
    btn_change_schedule_schedule_changer = ttk.Button(frame_change_schedule, text='修改选中的时间段')
    btn_change_schedule_schedule_changer.place(x=260, y=50, width=125)
    btn_change_schedule_schedule_adder = ttk.Button(frame_change_schedule, text='添加一个时间段')
    btn_change_schedule_schedule_adder.place(x=260, y=100, width=125)
    btn_change_schedule_schedule_remover = ttk.Button(frame_change_schedule, text='删除选中的时间段')
    btn_change_schedule_schedule_remover.place(x=260, y=150, width=125)
    btn_change_schedule_schedule_import = ttk.Button(frame_change_schedule, text='批量导入')
    btn_change_schedule_schedule_import.place(x=260, y=200, width=125)
    btn_change_schedule_schedule_all_remover = ttk.Button(frame_change_schedule, text='删除全部')
    btn_change_schedule_schedule_all_remover.place(x=260, y=250, width=125)

    # 其它控件
    # 修改密码界面的
    label_change_pwd_new_text = ttk.Label(frame_change_pwd, text='新密码', justify=tk.CENTER)
    label_change_pwd_new_text.place(x=120, y=80)
    label_change_pwd_sure_text = ttk.Label(frame_change_pwd, text='确认密码', justify=tk.CENTER)
    label_change_pwd_sure_text.place(x=120, y=130)
    entry_change_pwd_new_pwd = ttk.Entry(frame_change_pwd, show='●')
    entry_change_pwd_new_pwd.place(x=120, y=100)
    entry_change_pwd_sure_pwd = ttk.Entry(frame_change_pwd, show='●')
    entry_change_pwd_sure_pwd.place(x=120, y=150)

    # 修改时间表界面的
    label_change_schedule_text = ttk.Label(frame_change_schedule, text='当前程序可以在以下时间段临时关闭', justify=tk.CENTER)
    label_change_schedule_text.place(x=50, y=25)
    table_change_schedule = ttk.Treeview(frame_change_schedule, show='headings', columns=('start_time', 'end_time'))
    table_change_schedule.column('start_time', width=100, anchor='center')
    table_change_schedule.column('end_time', width=100, anchor='center')
    table_change_schedule.heading('start_time', text='开始时间')
    table_change_schedule.heading('end_time', text='结束时间')
    for i in range(len_schedule := len(now_view)):
        table_change_schedule.insert('', i + 1, values=now_view[i])
    table_change_schedule.place(x=50, y=50, height=len_schedule * 25 if 0 < len_schedule * 25 < 300 else 300)

    # ==========================================================================================================
    # 第二部分：按钮、主要逻辑及事件
    # 控件函数
    # 设置窗口的
    # 打开修改密码设置按钮函数
    def change_pwd() -> None:
        win_settings.wm_title('修改密码')
        x = int((screen_width - 400) / 2)
        y = int((screen_height - 300) / 2)
        win_settings.geometry(f'+{x}+{y}')
        frame_change_pwd.pack()
        frame_setting.pack_forget()
        return

    btn_change_pwd.configure(command=change_pwd)

    # 打开调整时间表设置按钮函数
    def change_schedule() -> None:
        win_settings.wm_title('设置时间表')
        x = int((screen_width - 400) / 2)
        y = int((screen_height - 500) / 2)
        win_settings.geometry(f'+{x}+{y}')
        frame_change_schedule.pack()
        frame_setting.pack_forget()
        return

    btn_change_schedule.configure(command=change_schedule)


    # 其它窗口共有的
    # 返回按钮函数
    def return_to_main_frame(frame: tk.Frame) -> None:
        win_settings.wm_title('设置')
        x = int((screen_width - 500) / 2)
        y = int((screen_height - 200) / 2)
        win_settings.geometry(f'+{x}+{y}')
        frame_setting.pack()
        frame.pack_forget()
        return

    btn_change_pwd_return.configure(command=lambda: return_to_main_frame(frame_change_pwd))
    btn_change_schedule_return.configure(command=lambda: return_to_main_frame(frame_change_schedule))

    # 修改密码界面的
    # 确定按钮函数
    def sure() -> None:
        global content, schedule, password, config, win

        if  entry_change_pwd_new_pwd.get() == entry_change_pwd_sure_pwd.get():
            messagebox.showinfo('提示', '密码设置成功！')
            return_to_main_frame(frame_change_pwd)
            password = base64.b64encode(bytes(entry_change_pwd_new_pwd.get(), 'utf-8')).decode('utf-8')
            config['adminPass'] = password

            win.lower()
        else:
            messagebox.showerror('错误', '输入的密码不同！')
            win.lower()

    btn_change_pwd_sure.configure(command=sure)

    # 修改时间表界面的
    # 时间表转换查看按钮函数
    def change_schedule_view_changer() -> None:
        global schedule_view_page1, schedule_view_page2, now_view

        if now_view == schedule_view_page2:
            now_view = schedule_view_page1
            btn_change_schedule_view_changer.configure(text='查看特殊时间表')
            for i in table_change_schedule.get_children():
                table_change_schedule.delete(i)
            for i in range(len_schedule := len(schedule_view_page1)):
                table_change_schedule.insert('', i + 1, values=schedule_view_page1[i])
            table_change_schedule.place(x=50, y=50, height=len_schedule * 25 if 0 < len_schedule * 25 < 300 else 300)
            
        else:
            now_view = schedule_view_page2
            btn_change_schedule_view_changer.configure(text='查看日常时间表')
            for i in table_change_schedule.get_children():
                table_change_schedule.delete(i)
            for i in range(len_schedule := len(schedule_view_page2)):
                table_change_schedule.insert('', i + 1, values=schedule_view_page2[i])
            table_change_schedule.place(x=50, y=50, height=len_schedule * 25 if 0 < len_schedule * 25 < 300 else 300)
            

    btn_change_schedule_view_changer.configure(command=change_schedule_view_changer)

    # 时间表修改按钮函数
    def change_schedule_schedule_changer(action) -> None:
        global schedule_view_page1, schedule_view_page2, now_view
        selected_item = table_change_schedule.selection()
        if selected_item:
            item_index = table_change_schedule.index(selected_item[0])
            if action == 'add':

                win_change_schedule_schedule_adder = tk.Tk()
                win_change_schedule_schedule_adder.title = '添加一个时间段'
                win_change_schedule_schedule_adder.geometry()
            elif action == 'remove':
                pass
            elif action == 'import':
                pass
            elif action == 'remove_all':
                pass
            elif action == 'change':
                pass

            print(item_index)

    btn_change_schedule_schedule_changer.configure(command=lambda: change_schedule_schedule_changer('change'))
    btn_change_schedule_schedule_adder.configure(command=lambda: change_schedule_schedule_changer('add'))
    btn_change_schedule_schedule_remover.configure(command=lambda: change_schedule_schedule_changer('remove'))
    btn_change_schedule_schedule_import.configure(command=lambda: change_schedule_schedule_changer('import'))
    btn_change_schedule_schedule_all_remover.configure(command=lambda: change_schedule_schedule_changer('remove_all'))
    # ==========================================================================================================

    win_settings.protocol('WM_DELETE_WINDOW', close_win_settings)
    win_settings.mainloop()

# 模块2 GUI及主要功能
# 写成函数，用于重启
def create_win(init: bool=True) -> None:
    global win, content, days, skin_path, refresh_list
    
    default_window_size = False  # 皮肤文件出错后使用默认大小
    refresh_list = []
    init_data(init)

    try:
        with open(skin_path, 'r', encoding='utf-8') as skin_file:
            skin = json.load(skin_file)
        
        background = skin['backgrounds']
        size = skin['size']
        elements = skin['elements']
    except:
        tb = traceback.format_exc()
        messagebox.showerror('错误', '程序因无法正确读取和解析皮肤文件而发生如下错误无法正常运行，您可以将错误截图反馈给作者：2979987115@qq.com\n\n{0}\n此外，如果您具备相关知识，请根据以上错误修复文件\n\n\t\t！！！注意！！！\n由于此错误，程序即将退出。请重新下载配置正确的皮肤文件或选择皮肤文件！'.format(str(tb)))
        messagebox.showwarning('注意', '由于皮肤文件损坏，将无法显示，请点击“设置”更换皮肤或修复文件！\n程序将以默认大小创建窗口！')
        default_window_size = True

    finally:
        # 根据皮肤文件创建窗口
        # 创建窗口
        win = tk.Tk()
        if default_window_size:
            width, height = 650, 450
            win.geometry('650x450')
        else:
            try:
                win.geometry(size)
                width, height = int(size.split('x')[0]), int(size.split('x')[1])
            except:
                tb = traceback.format_exc()
                messagebox.showerror('错误', '程序因无法正确读取和解析皮肤文件而发生如下错误无法正常运行，您可以将错误截图反馈给作者：2979987115@qq.com\n\n{0}\n此外，如果您具备相关知识，请根据以上错误修复文件\n\n\t\t！！！注意！！！\n由于此错误，程序将以默认大小显示窗口。请重新下载配置正确的皮肤文件或选择皮肤文件！'.format(str(tb)))
                width, height = 650, 450
                win.geometry('650x450')

        # 创建背景
        try:
            if background['type'] == 'color':
                if background['color'] != None:
                    win.configure(background=background['color'])
            elif background['type'] == 'img':
                photo = tk.PhotoImage(filename=background['pic_path'])
                bklabel = tk.Label(win, image=photo)
                bklabel.pack(fill='both', expand=True)
                bklabel.image = photo
        except:
            tb = traceback.format_exc()
            messagebox.showerror('错误', '程序因无法正确读取和解析皮肤文件而发生如下错误无法正常运行，您可以将错误截图反馈给作者：2979987115@qq.com\n\n{0}\n此外，如果您具备相关知识，请根据以上错误修复文件\n\n\t\t！！！注意！！！\n由于此错误，程序将不会显示皮肤。请重新下载配置正确的皮肤文件或选择皮肤文件！'.format(str(tb)))
            messagebox.showinfo('提示', '可以根据以下提示修复：\n1、检查图片文件是否存在\n2、检查config.json文件是否完整或被篡改')

        # 计算窗口的左上角坐标并放置
        win.geometry(f'+{int((win.winfo_screenwidth() - width) / 2)}+{int((win.winfo_screenheight() - height) / 2)}')

        # 隐藏窗口的标题栏和边框
        win.overrideredirect(True)

        # 显示在最底层
        win.lower()

        b1 = ttk.Button(win, text='关闭', padding=(1, 1), width=5, command=p_close_win)
        b2 = ttk.Button(win, text='临时关闭', padding=(1, 1), width=7, command=t_close_win)
        b3 = ttk.Button(win, text='刷新', padding=(1, 1), width=5, command=button_fresh)
        b4 = ttk.Button(win, text='作者信息', padding=(1, 1), width=7, command=author_info)
        b5 = ttk.Button(win, text='设置', padding=(1, 1), width=5, command=settings)

        # 将按钮放置在右下角
        b1.pack(side='right', anchor='se')
        b2.pack(side='right', anchor='se')
        b3.pack(side='right', anchor='se')
        b4.pack(side='right', anchor='se')
        b5.pack(side='right', anchor='se')

        # 路径文本
        text_path = tk.Text(win, height=1.3, width=50)
        text_path.insert(tk.END, f'程序路径：{os.path.dirname(sys.executable)}', 'red')
        tk.Text.tag_configure(text_path, 'red', foreground='red')
        text_path.configure(bg=win.cget('bg'), state='disabled', borderwidth=0, highlightthickness=0)

        # 设置文本位置左下角
        text_path.pack(side='left', anchor='se')

        # 根据皮肤文件设置控件
        try:
            for i in elements:
                if i['type'] == 'text':
                    text = tk.Text(win, height=int(i['size'].split(',')[0]), width=int(i['size'].split(',')[1]))
                    text.insert(tk.END, i['contents'], i['color'])
                    tk.Text.tag_configure(text, i['color'], foreground=i['color'])
                    text.configure(bg=win.cget('bg'), font=font.Font(size=i['fontsize']), state='disabled', borderwidth=0, highlightthickness=0)
                    text.place(x=int(i['pos'].split(',')[0]), y=int(i['pos'].split(',')[1]))
                elif i['type'] == '$days':
                    text = tk.Text(win, height=int(i['size'].split(',')[0]), width=int(i['size'].split(',')[1]))
                    refresh_list.append(('$days', text, i))
                    text.insert(tk.END, days, i['color'])
                    tk.Text.tag_configure(text, i['color'], foreground=i['color'])
                    text.configure(bg=win.cget('bg'), font=font.Font(size=i['fontsize']), state='disabled', borderwidth=0, highlightthickness=0)
                    text.place(x=int(i['pos'].split(',')[0]), y=int(i['pos'].split(',')[1]))
                elif i['type'] == '$couragements':
                    text = tk.Text(win, height=int(i['size'].split(',')[0]), width=int(i['size'].split(',')[1]))
                    refresh_list.append(('$couragements', text, i))
                    text.insert(tk.END, random.choice(content), i['color'])
                    text.tag_configure('center', justify='center')
                    text.tag_add('center', '1.0', 'end')
                    tk.Text.tag_configure(text, i['color'], foreground=i['color'])
                    text.configure(bg=win.cget('bg'), font=font.Font(size=i['fontsize']), state='disabled', borderwidth=0, highlightthickness=0)
                    text.place(x=int(i['pos'].split(',')[0]), y=int(i['pos'].split(',')[1]))
        except IndexError:
            pass
        except:
            tb = traceback.format_exc()
            messagebox.showerror('错误', '程序因无法正确读取和解析皮肤文件而发生如下错误无法正常运行，您可以将错误截图反馈给作者：2979987115@qq.com\n\n{0}\n此外，如果您具备相关知识，请根据以上错误修复文件\n\n\t\t！！！注意！！！\n由于此错误，程序将不会显示皮肤。请重新下载配置正确的皮肤文件或选择皮肤文件！'.format(str(tb)))
        
        win.protocol("WM_DELETE_WINDOW", p_close_win)
        win.mainloop()

    return


create_win()