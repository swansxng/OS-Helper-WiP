import win32gui
import win32ui
import win32con
import struct


def extract_icon(exe_path, save_path="icon.ico"):
    large, small = win32gui.ExtractIconEx(exe_path, 0)
    if large:
        hicon = large[0]
    elif small:
        hicon = small[0]
    else:
        raise Exception("Не удалось извлечь иконку")

    hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))
    hbmp = win32ui.CreateBitmap()
    hdc_mem = hdc.CreateCompatibleDC()

    info = win32gui.GetIconInfo(hicon)
    hbmp.CreateCompatibleBitmap(hdc, 32, 32)
    hdc_mem.SelectObject(hbmp)
    win32gui.DrawIconEx(hdc_mem.GetSafeHdc(), 0, 0, hicon, 32, 32, 0, None, win32con.DI_NORMAL)

    hbmp.SaveBitmapFile(hdc, save_path)
    win32gui.DestroyIcon(hicon)


extract_icon(r"C:\Program Files\FACEIT AC\faceitclient.exe", "faceit.ico")
exe_path = r"C:\Users\xolo\AppData\Local\JetBrains\PyCharm Community Edition 2024.2.3\bin\pycharm64.exe"