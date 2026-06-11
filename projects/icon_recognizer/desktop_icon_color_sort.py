import ctypes
import ctypes.wintypes as wintypes
import colorsys
import sys

import win32con
import win32gui


LVM_FIRST = 0x1000
LVM_GETITEMCOUNT = LVM_FIRST + 4
LVM_GETITEMPOSITION = LVM_FIRST + 16
LVM_SETITEMPOSITION = LVM_FIRST + 15
LVM_SETITEMPOSITION32 = LVM_FIRST + 49
LVM_GETITEMTEXTW = LVM_FIRST + 115
LVM_GETITEMW = LVM_FIRST + 75
LVM_GETIMAGELIST = LVM_FIRST + 2
LVM_GETITEMSPACING = LVM_FIRST + 53
LVSIL_NORMAL = 0
LVIF_TEXT = 0x0001
LVIF_IMAGE = 0x0002
ILD_NORMAL = 0x00000000
DIB_RGB_COLORS = 0


def _find_desktop_listview():
    def find_folder_view(parent):
        shell_view = win32gui.FindWindowEx(parent, 0, "SHELLDLL_DefView", None)
        if shell_view:
            hwnd = win32gui.FindWindowEx(shell_view, 0, "SysListView32", "FolderView")
            if hwnd:
                return hwnd
        return None

    progman = win32gui.FindWindow("Progman", "Program Manager")
    if progman:
        hwnd = find_folder_view(progman)
        if hwnd:
            return hwnd

    desktop_hwnd = win32gui.FindWindow("Progman", None)
    if desktop_hwnd:
        hwnd = find_folder_view(desktop_hwnd)
        if hwnd:
            return hwnd

    found = []

    def enum_windows(hwnd, lparam):
        if win32gui.IsWindowVisible(hwnd) and win32gui.GetClassName(hwnd) == "WorkerW":
            hwnd2 = find_folder_view(hwnd)
            if hwnd2:
                found.append(hwnd2)
                return False
        return True

    win32gui.EnumWindows(enum_windows, None)
    if found:
        return found[0]

    def enum_children(hwnd, lparam):
        if win32gui.GetClassName(hwnd) == "SysListView32":
            found.append(hwnd)
            return False
        return True

    win32gui.EnumChildWindows(progman or desktop_hwnd or 0, enum_children, None)
    return found[0] if found else None


class POINT(ctypes.Structure):
    _fields_ = [("x", wintypes.LONG), ("y", wintypes.LONG)]


class LVITEMW(ctypes.Structure):
    _fields_ = [
        ("mask", wintypes.UINT),
        ("iItem", wintypes.INT),
        ("iSubItem", wintypes.INT),
        ("state", wintypes.UINT),
        ("stateMask", wintypes.UINT),
        ("pszText", wintypes.LPWSTR),
        ("cchTextMax", wintypes.INT),
        ("iImage", wintypes.INT),
        ("lParam", wintypes.LPARAM),
        ("iIndent", wintypes.INT),
        ("iGroupId", wintypes.INT),
        ("cColumns", wintypes.UINT),
        ("puColumns", wintypes.LPVOID),
        ("piColFmt", wintypes.LPVOID),
        ("iGroup", wintypes.INT),
    ]


class ICONINFO(ctypes.Structure):
    _fields_ = [
        ("fIcon", wintypes.BOOL),
        ("xHotspot", wintypes.DWORD),
        ("yHotspot", wintypes.DWORD),
        ("hbmMask", wintypes.HBITMAP),
        ("hbmColor", wintypes.HBITMAP),
    ]


class BITMAPINFOHEADER(ctypes.Structure):
    _fields_ = [
        ("biSize", wintypes.DWORD),
        ("biWidth", wintypes.LONG),
        ("biHeight", wintypes.LONG),
        ("biPlanes", wintypes.WORD),
        ("biBitCount", wintypes.WORD),
        ("biCompression", wintypes.DWORD),
        ("biSizeImage", wintypes.DWORD),
        ("biXPelsPerMeter", wintypes.LONG),
        ("biYPelsPerMeter", wintypes.LONG),
        ("biClrUsed", wintypes.DWORD),
        ("biClrImportant", wintypes.DWORD),
    ]


class BITMAPINFO(ctypes.Structure):
    _fields_ = [
        ("bmiHeader", BITMAPINFOHEADER),
        ("bmiColors", wintypes.DWORD * 3),
    ]


class BITMAP(ctypes.Structure):
    _fields_ = [
        ("bmType", wintypes.LONG),
        ("bmWidth", wintypes.LONG),
        ("bmHeight", wintypes.LONG),
        ("bmWidthBytes", wintypes.LONG),
        ("bmPlanes", wintypes.WORD),
        ("bmBitsPixel", wintypes.WORD),
        ("bmBits", wintypes.LPVOID),
    ]


def _get_icon_image_list_handle(hwnd):
    return win32gui.SendMessage(hwnd, LVM_GETIMAGELIST, LVSIL_NORMAL, 0)


def _get_item_image_index(hwnd, index):
    buffer = ctypes.create_unicode_buffer(260)
    item = LVITEMW()
    item.mask = LVIF_IMAGE
    item.iItem = index
    item.iSubItem = 0
    item.iImage = 0
    res = ctypes.windll.user32.SendMessageW(hwnd, LVM_GETITEMW, index, ctypes.byref(item))
    if res == 0:
        return None
    return item.iImage


def _get_item_text(hwnd, index):
    buffer = ctypes.create_unicode_buffer(260)
    item = LVITEMW()
    item.mask = LVIF_TEXT
    item.iItem = index
    item.iSubItem = 0
    item.pszText = ctypes.cast(buffer, wintypes.LPWSTR)
    item.cchTextMax = len(buffer)
    ctypes.windll.user32.SendMessageW(hwnd, LVM_GETITEMTEXTW, index, ctypes.byref(item))
    return buffer.value


def _get_item_position(hwnd, index):
    point = POINT()
    res = ctypes.windll.user32.SendMessageW(hwnd, LVM_GETITEMPOSITION, index, ctypes.byref(point))
    if res == 0:
        return None
    return point.x, point.y


def _set_item_position(hwnd, index, x, y):
    lparam = (y << 16) | (x & 0xFFFF)
    ctypes.windll.user32.SendMessageW(hwnd, LVM_SETITEMPOSITION32, index, lparam)


def _extract_average_icon_color(hicon):
    if not hicon:
        return None
    width = 32
    height = 32
    hdc = ctypes.windll.user32.CreateCompatibleDC(0)
    if not hdc:
        return None

    bmi = BITMAPINFO()
    bmi.bmiHeader.biSize = ctypes.sizeof(BITMAPINFOHEADER)
    bmi.bmiHeader.biWidth = width
    bmi.bmiHeader.biHeight = -height
    bmi.bmiHeader.biPlanes = 1
    bmi.bmiHeader.biBitCount = 32
    bmi.bmiHeader.biCompression = win32con.BI_RGB
    bmi.bmiHeader.biSizeImage = width * height * 4

    bits_ptr = ctypes.c_void_p()
    hbitmap = ctypes.windll.gdi32.CreateDIBSection(hdc, ctypes.byref(bmi), DIB_RGB_COLORS, ctypes.byref(bits_ptr), None, 0)
    if not hbitmap:
        ctypes.windll.user32.DeleteDC(hdc)
        return None

    prev_obj = ctypes.windll.gdi32.SelectObject(hdc, hbitmap)
    if not prev_obj:
        ctypes.windll.gdi32.DeleteObject(hbitmap)
        ctypes.windll.user32.DeleteDC(hdc)
        return None

    try:
        if not ctypes.windll.user32.DrawIconEx(hdc, 0, 0, hicon, width, height, 0, 0, win32con.DI_NORMAL):
            return None

        buf = ctypes.create_string_buffer(width * height * 4)
        lines = ctypes.windll.gdi32.GetDIBits(hdc, hbitmap, 0, height, buf, ctypes.byref(bmi), DIB_RGB_COLORS)
        if lines == 0:
            return None

        data = buf.raw
        r_sum = g_sum = b_sum = count = 0
        for i in range(0, len(data), 4):
            b = data[i]
            g = data[i + 1]
            r = data[i + 2]
            a = data[i + 3]
            if a == 0:
                continue
            r_sum += r
            g_sum += g
            b_sum += b
            count += 1
        if count == 0:
            return None
        return (r_sum // count, g_sum // count, b_sum // count)
    finally:
        ctypes.windll.gdi32.SelectObject(hdc, prev_obj)
        ctypes.windll.gdi32.DeleteObject(hbitmap)
        ctypes.windll.user32.DeleteDC(hdc)
        ctypes.windll.user32.DestroyIcon(hicon)


def _get_icon_average_color(hwnd, index, ime_handle):
    image_index = _get_item_image_index(hwnd, index)
    if image_index is None or image_index < 0:
        return None
    image_list_get_icon = ctypes.windll.comctl32.ImageList_GetIcon
    image_list_get_icon.restype = wintypes.HICON
    image_list_get_icon.argtypes = [wintypes.HANDLE, ctypes.c_int, wintypes.UINT]
    hicon = image_list_get_icon(ime_handle, image_index, ILD_NORMAL)
    return _extract_average_icon_color(hicon)


def _color_name_from_rgb(rgb):
    if rgb is None:
        return "unknown"
    r, g, b = [v / 255.0 for v in rgb]
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    h_deg = h * 360
    if v < 0.15 or s < 0.2:
        return "unknown"
    if h_deg >= 330 or h_deg < 15:
        return "red"
    if h_deg < 45:
        return "orange"
    if h_deg < 75:
        return "yellow"
    if h_deg < 165:
        return "green"
    if h_deg < 195:
        return "cyan"
    if h_deg < 255:
        return "blue"
    return "purple"


def _get_desktop_icons(hwnd):
    count = win32gui.SendMessage(hwnd, LVM_GETITEMCOUNT, 0, 0)
    imagelist = _get_icon_image_list_handle(hwnd)
    icons = []
    for index in range(count):
        text = _get_item_text(hwnd, index)
        pos = _get_item_position(hwnd, index)
        avg_rgb = _get_icon_average_color(hwnd, index, imagelist) if imagelist else None
        color = _color_name_from_rgb(avg_rgb)
        icons.append({
            "index": index,
            "text": text,
            "pos": pos,
            "rgb": avg_rgb,
            "color": color,
        })
    return icons


COLOR_ORDER = ["red", "orange", "yellow", "green", "cyan", "blue", "purple", "unknown"]


def _sort_icons(icons):
    return sorted(
        icons,
        key=lambda item: (
            COLOR_ORDER.index(item["color"]) if item["color"] in COLOR_ORDER else len(COLOR_ORDER),
            item["color"],
            item["text"].lower(),
        ),
    )


def _get_grid_spacing(hwnd):
    mx = ctypes.windll.user32.SendMessageW(hwnd, LVM_GETITEMSPACING, 0, 0)
    if mx == 0:
        return 100, 100
    x = mx & 0xFFFF
    y = (mx >> 16) & 0xFFFF
    return x, y


def _rearrange_icons(hwnd, icons):
    if not icons:
        return
    spacing_x, spacing_y = _get_grid_spacing(hwnd)
    base_x = min((item["pos"][0] for item in icons if item["pos"] is not None), default=0)
    base_y = min((item["pos"][1] for item in icons if item["pos"] is not None), default=0)
    columns = max(1, int(1200 / spacing_x))
    for position, item in enumerate(icons):
        row = position // columns
        col = position % columns
        x = base_x + col * spacing_x
        y = base_y + row * spacing_y
        _set_item_position(hwnd, item["index"], x, y)


def main():
    hwnd = _find_desktop_listview()
    if not hwnd:
        print("找不到桌面图标列表窗口，请确保这是 Windows 桌面。")
        return

    icons = _get_desktop_icons(hwnd)
    if not icons:
        print("桌面上没有找到图标。")
        return

    sorted_icons = _sort_icons(icons)
    print("检测到桌面图标：")
    for icon in sorted_icons:
        print(f"{icon['text']} -> {icon['color']} ({icon['rgb']})")

    _rearrange_icons(hwnd, sorted_icons)
    if win32gui.IsWindow(hwnd):
        win32gui.InvalidateRect(hwnd, None, True)
        win32gui.UpdateWindow(hwnd)
    print("桌面图标已按颜色排序并重新排列。")


if __name__ == "__main__":
    if sys.platform != "win32":
        print("此脚本仅在 Windows 上运行。")
    else:
        main()
