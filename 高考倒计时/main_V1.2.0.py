import datetime, time  # 时间相关库
import random  # 随机数库，用于随机产生标语
import tkinter as tk  # GUI的相关库
from tkinter import simpledialog, messagebox, font  # 对话窗口的相关库
import base64  # 简单保护一下密码，对称性加密（够用了）
import json  # 处理json格式数据
import os, sys  # 用于获取文件路径
import traceback

# 程序变量
# 作者信息不能打开多个，设置flag
opened_info = False

path = os.path.dirname(sys.executable)
    

# 模块1 计算时间差、获取资源、按钮函数
# 初始化
def init_data() -> None:
    global password, schedule, days, skin_path, content

    # 获取配置资源
    if not os.path.exists('config.json'):
        messagebox.showinfo('提示', '未找到配置文件，将创建初始config文件，请勿删除！')
        config = {"adminPass": "", "schedule": {"normal": [], "special": {"state": "negtive", "active_days": [], "schedule": []}}, "skin": "skin/originalskin.json"}
    else:
        try:
            with open('config.json', 'r', encoding='utf-8') as config_file:
                config = json.load(config_file)
        except:
            tb = traceback.format_exc()
            messagebox.showerror('错误', '程序因无法正确读取和解析文件而发生如下错误无法正常运行，您可以将错误截图反馈给作者：2979987115@qq.com\n\n{0}\n此外，如果您具备相关知识，请根据以上错误修复文件\n\n\t\t！！！注意！！！\n由于此错误，你可以选择恢复到初始的配置文件。\n请在下一个弹窗中点击“确定”来更新文件，点击“取消”程序将保留出错的配置文件并退出。'.format(str(tb)))
            ques = messagebox.askyesno('', '是否恢复到初始的配置文件')
            if ques:
                config = {"adminPass": "", "schedule": {"normal": [], "special": {"state": "negtive", "active_days": [], "schedule": []}}, "skin": "skin/originalskin.json"}
            else:
                exit()

    # 配置变量
    try:
        password = config['adminPass']
        schedule = config['schedule']['special']['schedule'] if config['schedule']['special']['state'] == 'active' and datetime.datetime.today().today() in config['schedule']['special']['active_days'] else config['schedule']['normal']
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

    # 2、把时间表里的元素换成datetime对象
    try:
        for i in range(len(schedule)):
            schedule[i] = [datetime.time(int(schedule[i][0].split(',')[0]), int(schedule[i][0].split(',')[1])), datetime.time(int(schedule[i][1].split(',')[0]), int(schedule[i][1].split(',')[1]))]
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

    win.lower()

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
        messagebox.showerror('警告', '由于无法解析密码而发生以下错误，您可以将错误截图反馈给作者：2979987115@qq.com\n\n{0}\n此外，如果您具备相关知识，请根据以上错误修复文件\n\n\t\t！！！注意！！！\n由于此错误，密码将无效。\n请转到“设置”重新设置密码。')
        win.destroy()
        exit()

    return


# 临时关闭程序
# 相比1.1.2减少了循环、减少重启时间表、代码量
def t_close_win() -> None:
    global schedule, win

    current_time = datetime.datetime.now()
    for i in schedule:
        if i[0] <= current_time.time() <= i[1]:
            win.destroy()
            messagebox.showinfo('提示', '即将在下课时重启（重启窗口置于最底层，不会占用屏幕，请放心上课）')
            reboot_time = datetime.datetime.combine(datetime.datetime.today().date(), i[1])
            time.sleep((reboot_time - current_time).total_seconds())
            create_win()
            break
    else:
        messagebox.showerror('错误', '下课期间禁止临时关闭程序！')

        return


# 作者信息
def author_info():
    global opened_info
    
    if opened_info:  # 判断是否打开了窗口
        return  # 打开了窗口，避免重复打开，用return中断函数，不执行创建窗口的代码。

    opened_info = True

    # 嵌套函数，用于关闭win2时刷新flag的值
    def close_win2():
        global opened_info
        opened_info = False
        win2.destroy()

    win2 = tk.Tk()
    win2.geometry('250x325')
    win2.resizable(False, False)  # 禁止修改大小
    # 居中显示
    # 获取屏幕的宽度和高度
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()

    # 计算窗口的左上角坐标
    x = int((screen_width - 250) / 2)
    y = int((screen_height - 300) / 2)
    win2.geometry(f'+{x}+{y}')

    t = tk.Text(win2, height=20, width=25)
    t.insert(tk.END, '高考计时器\nV：1.2.0(2024.6.14)\n作者：孙培煊\nQQ：2979987115\n有Bug及时反馈\n未经允许禁止转载！\n程序语言：python\nGUI库：tkinter\n\n刷新按钮运行内存占用过高bug已修复！\n\n新版本1.2.0已发布！\n基础版本已完成，“设置”将在下一版本完成！')
    f = font.Font(size=5)
    t.configure(bg=win2.cget('bg'), font=f, state='disabled', borderwidth=0, highlightthickness=0)
    t.pack()

    win2.protocol("WM_DELETE_WINDOW", close_win2)
    win2.mainloop()

    return


# 设置（未开发）
def settings() -> None:
    global content, schedule
    
    win3 = tk.Tk()
    win3.title('设置')
    win3.geometry('500x400')
    screen_width, screen_height = win.winfo_screenwidth(), win.winfo_screenheight()
    x = int((screen_width - 500) / 2)
    y = int((screen_height - 400) / 2)
    win3.geometry(f'+{x}+{y}')

    messagebox.showinfo('提示', '功能未开发')

    win3.destroy()
    win3.mainloop()

# 模块2 GUI及主要功能
# 写成函数，用于重启
def create_win():
    global win, path, content, days, skin_path, refresh_list
    
    default_window_size = False  # 皮肤文件出错后使用默认大小
    refresh_list = []
    init_data()

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


        # 居中显示
        # 获取屏幕的宽度和高度
        screen_width, screen_height = win.winfo_screenwidth(), win.winfo_screenheight()

        # 计算窗口的左上角坐标并放置
        x = int((screen_width - width) / 2)
        y = int((screen_height - height) / 2)
        win.geometry(f'+{x}+{y}')

        # 隐藏窗口的标题栏和边框
        win.overrideredirect(True)

        # 显示在最底层
        win.lower()

        b1 = tk.Button(win, text='关闭', width=5, height=1, command=p_close_win)
        b2 = tk.Button(win, text='临时关闭', width=6, height=1, command=t_close_win)
        b3 = tk.Button(win, text='刷新', width=5, height=1, command=button_fresh)
        b4 = tk.Button(win, text='作者信息', width=6, height=1, command=author_info)
        b5 = tk.Button(win, text='设置', width=5, height=1, command=settings)  # 功能未开发

        # 将按钮放置在右下角
        b1.pack(side='right', anchor='se')
        b2.pack(side='right', anchor='se')
        b3.pack(side='right', anchor='se')
        b4.pack(side='right', anchor='se')
        b5.pack(side='right', anchor='se')

        # 路径文本
        text_path = tk.Text(win, height=1.3, width=50)
        text_path.insert(tk.END, f'程序路径：{path}', 'red')
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