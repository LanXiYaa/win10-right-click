import tkinter as tk
from tkinter import messagebox, ttk
import subprocess
import sys
import os
import webbrowser

def change_to_win10_style():
    """更改为Windows 10样式"""
    try:
        # 添加注册表项
        result = subprocess.run([
            'reg.exe', 'add', 
            'HKCU\\Software\\Classes\\CLSID\\{86ca1aa0-34aa-4e8b-a509-50c905bae2a2}\\InprocServer32', 
            '/f', '/ve'
        ], capture_output=True, text=True, check=True)
        
        # 重启资源管理器
        restart_explorer()
        
        messagebox.showinfo("成功", "已更改为Windows 10样式右键菜单")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("错误", f"执行命令时出错:\n{e.stderr}")

def revert_to_win11_style():
    """恢复为Windows 11模式"""
    try:
        # 删除注册表项
        result = subprocess.run([
            'reg.exe', 'delete', 
            'HKCU\\Software\\Classes\\CLSID\\{86ca1aa0-34aa-4e8b-a509-50c905bae2a2}', 
            '/f'
        ], capture_output=True, text=True, check=True)
        
        # 重启资源管理器
        restart_explorer()
        
        messagebox.showinfo("成功", "已恢复为Windows 11样式右键菜单")
    except subprocess.CalledProcessError as e:
        # 如果注册表项不存在，也算成功
        if "系统找不到指定的注册表项或值" in e.stderr:
            messagebox.showinfo("成功", "已恢复为Windows 11样式右键菜单")
        else:
            messagebox.showerror("错误", f"执行命令时出错:\n{e.stderr}")

def open_github():
    """打开GitHub项目页面"""
    webbrowser.open("https://github.com/LanXiYaa/win10-right-click")

def restart_explorer():
    """重启资源管理器"""
    try:
        # 结束explorer进程
        subprocess.run(['taskkill', '/f', '/im', 'explorer.exe'], check=True)
    except subprocess.CalledProcessError:
        # 即使taskkill失败，也尝试启动explorer
        pass
    
    # 启动新的explorer进程
    subprocess.Popen('explorer.exe')

def on_win10_style_click():
    """Windows 10样式按钮点击事件"""
    if messagebox.askyesno("确认", "确定要更改为Windows 10样式右键菜单吗？"):
        change_to_win10_style()

def on_win11_style_click():
    """Windows 11样式按钮点击事件"""
    if messagebox.askyesno("确认", "确定要恢复为Windows 11样式右键菜单吗？"):
        revert_to_win11_style()

def main():
    # 创建主窗口
    root = tk.Tk()
    root.title("Windows右键菜单样式切换工具")
    root.geometry("550x400")
    root.resizable(False, False)
    
    # 设置样式
    style = ttk.Style()
    style.configure('TFrame', background='#f0f0f0')
    style.configure('TLabel', background='#f0f0f0', font=('Arial', 12))
    style.configure('Title.TLabel', background='#f0f0f0', font=('Arial', 16, 'bold'))
    style.configure('TButton', font=('Arial', 12))
    style.configure('Info.TLabel', background='#f0f0f0', font=('Arial', 10))
    
    # 主框架
    main_frame = ttk.Frame(root, padding=20)
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # 标题
    title_label = ttk.Label(main_frame, text="修改右键菜单模式", style='Title.TLabel')
    title_label.pack(pady=10)
    
    # 说明文本
    desc_label = ttk.Label(main_frame, text="此工具允许您在Windows 10和Windows 11风格的右键菜单之间切换。")
    desc_label.pack(pady=10)
    
    # 按钮框架
    button_frame = ttk.Frame(main_frame)
    button_frame.pack(pady=30)
    
    # Windows 10样式按钮
    win10_button = ttk.Button(button_frame, text="更改为Windows 10样式", command=on_win10_style_click, width=25)
    win10_button.pack(pady=10)
    
    # Windows 11样式按钮
    win11_button = ttk.Button(button_frame, text="恢复为Windows 11模式", command=on_win11_style_click, width=25)
    win11_button.pack(pady=10)
    
    # 退出按钮
    exit_button = ttk.Button(button_frame, text="退出", command=root.destroy, width=25)
    exit_button.pack(pady=10)

    # 项目仓库按钮
    github_button = ttk.Button(
        button_frame, 
        text="项目仓库", 
        command=open_github, 
        width=25,
        style='Small.TButton'
    )
    github_button.pack(pady=5)
    
    # 信息文本
    info_label = ttk.Label(main_frame, text="注意：更改后会自动重启文件资源管理器，这可能会导致桌面短暂消失。", style='Info.TLabel')
    info_label.pack(side=tk.BOTTOM, pady=0)
    
    # 运行主循环
    root.mainloop()

if __name__ == "__main__":

    main()
