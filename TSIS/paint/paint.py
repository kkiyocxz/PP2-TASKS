import pygame as p
import math
from datetime import datetime

p.init()

try:
    icon = p.image.load("images/icon_paint.png")
    p.display.set_icon(icon)
except:
    pass

WIDTH, HEIGHT = 1000, 750
p.display.set_caption("Paint")
screen = p.display.set_mode((WIDTH, HEIGHT))
clock = p.time.Clock()
font = p.font.SysFont("Arial", 11, bold=True)
large_font = p.font.SysFont("Arial", 18, bold=True)

# --- Canvas ---
canvas_offset = (10, 110)
canvas = p.Surface((980, 630))
canvas.fill((255, 255, 255))

# --- State ---
color = (0, 0, 0)
brush_size = 3
tool = "draw"
drawing = False
start_pos = None
text_input = ""
text_pos = None
last_draw_pos = None

# --- Цвета палитры ---
COLORS = [
    ("black",  (0, 0, 0)),
    ("white",  (255, 255, 255)),
    ("red",    (220, 30, 30)),
    ("orange", (255, 140, 0)),
    ("yellow", (255, 220, 0)),
    ("green",  (30, 180, 30)),
    ("cyan",   (0, 210, 210)),
    ("blue",   (30, 80, 220)),
    ("purple", (140, 0, 200)),
    ("pink",   (255, 100, 180)),
    ("brown",  (140, 70, 20)),
    ("gray",   (150, 150, 150)),
]

# --- Строим btns ---
btns = {}

# Строка 1 (y=10): цвета + eraser + clear
x = 10
for name, clr in COLORS:
    btns[name] = {"rect": p.Rect(x, 10, 38, 38), "color": clr}
    x += 42

btns["eraser"] = {"rect": p.Rect(x, 10, 60, 38), "color": (255, 255, 255), "label": "eraser"}
x += 65
btns["clear"] = {"rect": p.Rect(x, 10, 55, 38), "label": "clear"}

# Строка 2 (y=58): инструменты + размер кисти
tool_items = [
    ("draw",     "pencil"),
    ("line",     "line"),
    ("square",   "rect"),
    ("circle",   "circle"),
    ("rect_tri", "r-tri"),
    ("eq_tri",   "e-tri"),
    ("rhombus",  "rhombus"),
    ("fill",     "fill"),
    ("text",     "text"),
]
x = 10
for tname, tlabel in tool_items:
    btns[tname] = {"rect": p.Rect(x, 58, 72, 38), "label": tlabel}
    x += 76

btns["minus"] = {"rect": p.Rect(x, 58, 38, 38), "label": "-"}
x += 42
btns["plus"]  = {"rect": p.Rect(x, 58, 38, 38), "label": "+"}


def flood_fill(surf, x, y, new_col):
    target_col = surf.get_at((x, y))
    if target_col[:3] == new_col[:3]:
        return
    stack = [(x, y)]
    w, h = surf.get_size()
    while stack:
        cx, cy = stack.pop()
        if 0 <= cx < w and 0 <= cy < h:
            if surf.get_at((cx, cy))[:3] == target_col[:3]:
                surf.set_at((cx, cy), new_col)
                stack.extend([(cx+1,cy),(cx-1,cy),(cx,cy+1),(cx,cy-1)])


def get_shape_points(shape_type, start, end):
    x1, y1 = start
    x2, y2 = end
    w, h = x2 - x1, y2 - y1
    if shape_type == "rect_tri":
        return [(x1, y1), (x1, y2), (x2, y2)]
    elif shape_type == "eq_tri":
        side = x2 - x1
        h_tri = (math.sqrt(3) / 2) * abs(side)
        return [(x1 + side/2, y1), (x1, y1 + h_tri), (x1 + side, y1 + h_tri)]
    elif shape_type == "rhombus":
        return [(x1 + w/2, y1), (x2, y1 + h/2), (x1 + w/2, y2), (x1, y1 + h/2)]
    return []


def draw_button(surf, name, info, active_tool, active_color):
    rect = info["rect"]
    is_color_btn = "color" in info and "label" not in info
    is_eraser = name == "eraser"

    # Фон кнопки
    if is_color_btn:
        bg = info["color"]
    elif name == active_tool or (is_eraser and active_tool == "draw" and active_color == (255,255,255)):
        bg = (255, 230, 0)  # активный инструмент — жёлтый
    else:
        bg = (220, 220, 220)

    p.draw.rect(surf, bg, rect, border_radius=5)
    p.draw.rect(surf, (80, 80, 80), rect, 1, border_radius=5)

    # Подпись
    if "label" in info:
        r, g, b = bg
        tc = (255,255,255) if (r*0.299 + g*0.587 + b*0.114) < 100 else (20, 20, 20)
        txt = font.render(info["label"], True, tc)
        surf.blit(txt, (rect.centerx - txt.get_width()//2,
                        rect.centery - txt.get_height()//2))

    # Рамка для активного цвета
    if is_color_btn and info["color"] == active_color:
        p.draw.rect(surf, (255, 255, 0), rect.inflate(4, 4), 3, border_radius=6)


# --- Главный цикл ---
running = True
while running:
    mx, my = p.mouse.get_pos()
    cw, ch = canvas.get_size()
    cx = mx - canvas_offset[0]
    cy = my - canvas_offset[1]

    for event in p.event.get():
        if event.type == p.QUIT:
            running = False

        if event.type == p.KEYDOWN:
            if event.key == p.K_1: brush_size = 2
            if event.key == p.K_2: brush_size = 5
            if event.key == p.K_3: brush_size = 10
            if event.key == p.K_s and (p.key.get_mods() & p.KMOD_CTRL):
                fname = f"paint_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                p.image.save(canvas, fname)
                print(f"Saved: {fname}")

            if tool == "text" and text_pos:
                if event.key == p.K_RETURN:
                    txt_surf = large_font.render(text_input, True, color)
                    canvas.blit(txt_surf, text_pos)
                    text_input, text_pos = "", None
                elif event.key == p.K_ESCAPE:
                    text_input, text_pos = "", None
                elif event.key == p.K_BACKSPACE:
                    text_input = text_input[:-1]
                else:
                    text_input += event.unicode

        if event.type == p.MOUSEBUTTONDOWN:
            clicked_ui = False
            for name, info in btns.items():
                if info["rect"].collidepoint(mx, my):
                    clicked_ui = True
                    if "color" in info:
                        color = info["color"]
                        if name != "eraser":
                            tool = "draw"  # возвращаем карандаш при выборе цвета
                    elif name == "eraser":
                        color = (255, 255, 255)
                        tool = "draw"
                    elif name == "plus":
                        brush_size = min(50, brush_size + 1)
                    elif name == "minus":
                        brush_size = max(1, brush_size - 1)
                    elif name == "clear":
                        canvas.fill((255, 255, 255))
                    else:
                        tool = name

            if not clicked_ui and 0 <= cx < cw and 0 <= cy < ch:
                if tool == "fill":
                    flood_fill(canvas, cx, cy, color)
                elif tool == "text":
                    text_pos = (cx, cy)
                    text_input = ""
                else:
                    drawing = True
                    start_pos = (cx, cy)
                    last_draw_pos = (cx, cy)

        if event.type == p.MOUSEBUTTONUP:
            if drawing:
                if tool == "line":
                    p.draw.line(canvas, color, start_pos, (cx, cy), brush_size)
                elif tool == "circle":
                    rad = int(math.hypot(cx - start_pos[0], cy - start_pos[1]))
                    if rad > 0:
                        p.draw.circle(canvas, color, start_pos, rad, brush_size)
                elif tool == "square":
                    side = max(abs(cx - start_pos[0]), abs(cy - start_pos[1]))
                    p.draw.rect(canvas, color, p.Rect(start_pos[0], start_pos[1], side, side), brush_size)
                elif tool not in ("draw",):
                    pts = get_shape_points(tool, start_pos, (cx, cy))
                    if len(pts) > 2:
                        p.draw.polygon(canvas, color, pts, brush_size)
                drawing = False
                start_pos = None

    # Рисование карандашом
    if drawing and tool == "draw":
        if 0 <= cx < cw and 0 <= cy < ch:
            p.draw.line(canvas, color, last_draw_pos, (cx, cy), brush_size)
            p.draw.circle(canvas, color, (cx, cy), brush_size // 2)
            last_draw_pos = (cx, cy)

    # --- Отрисовка ---
    screen.fill((200, 200, 200))

    # Кнопки
    for name, info in btns.items():
        draw_button(screen, name, info, tool, color)

    # Инфо: размер кисти и текущий цвет
    info_x = btns["plus"]["rect"].right + 15
    size_txt = large_font.render(f"Size: {brush_size}", True, (30, 30, 30))
    screen.blit(size_txt, (info_x, 63))

    # Текущий цвет — квадрат справа
    color_rect = p.Rect(WIDTH - 55, 58, 42, 38)
    p.draw.rect(screen, color, color_rect, border_radius=5)
    p.draw.rect(screen, (60, 60, 60), color_rect, 1, border_radius=5)

    # Разделительная линия
    p.draw.line(screen, (150, 150, 150), (0, 104), (WIDTH, 104), 1)

    # Холст
    screen.blit(canvas, canvas_offset)
    p.draw.rect(screen, (60, 60, 60),
                (canvas_offset[0]-1, canvas_offset[1]-1, cw+2, ch+2), 1)

    # Превью фигур при рисовании
    if drawing and start_pos and tool != "draw":
        ox, oy = canvas_offset
        ps = (start_pos[0] + ox, start_pos[1] + oy)
        if tool == "line":
            p.draw.line(screen, color, ps, (mx, my), brush_size)
        elif tool == "circle":
            rad = int(math.hypot(mx - ps[0], my - ps[1]))
            if rad > 0:
                p.draw.circle(screen, color, ps, rad, 1)
        elif tool == "square":
            side = max(abs(mx - ps[0]), abs(my - ps[1]))
            p.draw.rect(screen, color, (ps[0], ps[1], side, side), 1)
        else:
            pts = get_shape_points(tool, ps, (mx, my))
            if len(pts) > 2:
                p.draw.polygon(screen, color, pts, 1)

    # Превью текста
    if tool == "text" and text_pos:
        preview = large_font.render(text_input + "|", True, color)
        screen.blit(preview, (text_pos[0] + canvas_offset[0],
                               text_pos[1] + canvas_offset[1]))

    p.display.flip()
    clock.tick(120)

p.quit()