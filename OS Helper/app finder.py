import os
import win32com.client


def resolve_shortcut(shortcut_path):
    if shortcut_path.lower().endswith((".lnk", ".url")):
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortcut(shortcut_path)
        target_path = os.path.abspath(shortcut.TargetPath)
        _, extension = os.path.splitext(target_path)

        # Исключаем unins000.exe и Uninstall.exe и setup.exe
        if extension.lower() == ".exe" and os.path.basename(target_path).lower() not in (
        "unins000.exe", "uninstall.exe", "setup.exe"):
            return target_path
    return None


def get_shortcuts_from_path(path):
    shortcuts = []
    for root, dirs, files in os.walk(path):
        for file in files:
            shortcut_path = os.path.join(root, file)
            shortcuts.append(shortcut_path)
    return shortcuts


def get_programs_from_start_menu_and_desktop():
    start_menu_path = os.path.join(os.environ['ProgramData'], 'Microsoft', 'Windows', 'Start Menu', 'Programs')
    desktop_path = os.path.join(os.environ['USERPROFILE'], 'Desktop')

    start_menu_shortcuts = get_shortcuts_from_path(start_menu_path)
    desktop_shortcuts = get_shortcuts_from_path(desktop_path)

    return start_menu_shortcuts + desktop_shortcuts


# Пример использования
programs = get_programs_from_start_menu_and_desktop()
for program in programs:
    exe_path = resolve_shortcut(program)
    if exe_path is not None:
        print(f"Ярлык: {program}, Путь к .exe: {exe_path}")