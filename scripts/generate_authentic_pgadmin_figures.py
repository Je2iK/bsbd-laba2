import os
import re
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = r'e:\laba2\images'
os.makedirs(OUT_DIR, exist_ok=True)

# Fonts
FONT_UI = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 12)
FONT_UI_BOLD = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 12)
FONT_UI_TAB = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 13)
FONT_UI_TAB_BOLD = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 13)
FONT_SMALL = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 10)
FONT_SQL = ImageFont.truetype('C:/Windows/Fonts/consola.ttf', 13)
FONT_SQL_BOLD = ImageFont.truetype('C:/Windows/Fonts/consolab.ttf', 13)
FONT_MSG = ImageFont.truetype('C:/Windows/Fonts/consola.ttf', 12)

# Colors (pgAdmin 4 dark theme)
BG_EDITOR = (30, 30, 30)
BG_GUTTER = (30, 30, 30)
BG_TAB_BAR = (37, 37, 38)
BG_TOOLBAR = (37, 37, 38)
BG_GRID_HDR = (42, 45, 50)
BG_ROW_EVEN = (30, 30, 30)
BG_ROW_ODD = (34, 37, 42)
BORDER_COLOR = (55, 55, 55)
GUTTER_LINE = (45, 45, 45)
COLOR_GUTTER_NUM = (110, 118, 129)
COLOR_TAB_ACTIVE = (255, 255, 255)
COLOR_TAB_INACTIVE = (150, 150, 150)
COLOR_INDICATOR = (64, 158, 255)
COLOR_TEXT_MAIN = (212, 212, 212)
COLOR_TEXT_MUTED = (140, 140, 140)

# SQL syntax colors
COLOR_KW = (242, 119, 122)      # Red / Coral
COLOR_STR = (229, 192, 123)     # Yellow / Gold
COLOR_TYPE = (86, 182, 194)     # Cyan
COLOR_IDENT = (97, 175, 239)    # Light blue
COLOR_NUM = (209, 154, 102)     # Orange
COLOR_DEFAULT = (200, 200, 200)

KEYWORDS = {
    'SELECT', 'FROM', 'WHERE', 'INSERT', 'INTO', 'VALUES', 'UPDATE', 'SET',
    'DELETE', 'RETURNING', 'EXPLAIN', 'ANALYZE', 'RESET', 'ROLE', 'LIMIT',
    'ORDER', 'BY', 'DROP', 'TABLE', 'CASE', 'WHEN', 'THEN', 'ELSE', 'END',
    'AND', 'OR', 'NOT', 'IN', 'DATE', 'AS', 'INTERVAL', 'TIMESTAMPTZ'
}

def highlight_sql_line(line):
    # Tokens: keywords, strings, numbers, identifiers, punctuation
    pattern = re.compile(
        r"(\b(?:SELECT|FROM|WHERE|INSERT|INTO|VALUES|UPDATE|SET|DELETE|RETURNING|EXPLAIN|ANALYZE|RESET|ROLE|LIMIT|ORDER|BY|DROP|TABLE|CASE|WHEN|THEN|ELSE|END|AND|OR|NOT|IN|DATE|AS|INTERVAL|TIMESTAMPTZ)\b)"
        r"|('(?:''|[^'])*')"
        r"|(\b\d+(?:\.\d+)?\b)"
        r"|(\b[a-zA-Z_][a-zA-Z0-9_\.]*\b)"
        r"|([^\s\w]+|\s+)"
    )
    tokens = []
    for match in pattern.finditer(line):
        text = match.group(0)
        if match.group(1): # keyword
            tokens.append((text, COLOR_KW, FONT_SQL_BOLD))
        elif match.group(2): # string
            tokens.append((text, COLOR_STR, FONT_SQL))
        elif match.group(3): # number
            tokens.append((text, COLOR_NUM, FONT_SQL))
        elif match.group(4): # identifier
            tokens.append((text, COLOR_IDENT, FONT_SQL))
        else: # punctuation or space
            tokens.append((text, COLOR_DEFAULT, FONT_SQL))
    return tokens

def render_pgadmin(
    sql_text,
    result_mode='grid',      # 'grid', 'message', 'plan'
    grid_cols=None,          # list of (name, type_desc, width)
    grid_rows=None,          # list of list of str
    error_lines=None,        # list of str
    active_tab='Результат',  # 'Результат' or 'Сообщения'
    width=900,
    out_path=None
):
    sql_lines = [l for l in sql_text.strip().split('\n')]
    num_sql_lines = len(sql_lines)
    
    # Calculate heights
    top_tab_h = 36
    sql_line_h = 20
    sql_pane_h = max(110, num_sql_lines * sql_line_h + 24)
    mid_bar_h = 36
    
    if result_mode in ('grid', 'plan'):
        if grid_rows:
            row_h = 26
            hdr_h = 36
            bot_pane_h = hdr_h + len(grid_rows) * row_h + 12
        else:
            bot_pane_h = 80
    else: # message / error
        num_err = len(error_lines) if error_lines else 3
        bot_pane_h = max(90, num_err * 22 + 28)
        
    total_h = top_tab_h + sql_pane_h + mid_bar_h + bot_pane_h
    
    im = Image.new('RGB', (width, total_h), BG_EDITOR)
    draw = ImageDraw.Draw(im)
    
    # 1. Top Tab Strip
    draw.rectangle([0, 0, width, top_tab_h], fill=BG_TAB_BAR)
    draw.line([0, top_tab_h, width, top_tab_h], fill=BORDER_COLOR, width=1)
    
    # Tab: "Запрос"
    draw.text((16, 9), 'Запрос', fill=COLOR_TAB_ACTIVE, font=FONT_UI_TAB_BOLD)
    tw = draw.textlength('Запрос', font=FONT_UI_TAB_BOLD)
    draw.line([16, top_tab_h - 2, 16 + tw, top_tab_h - 2], fill=COLOR_INDICATOR, width=2)
    
    # Tab: "История запросов"
    draw.text((16 + tw + 24, 9), 'История запросов', fill=COLOR_TAB_INACTIVE, font=FONT_UI_TAB)
    
    # 2. SQL Pane
    gutter_w = 46
    draw.rectangle([0, top_tab_h, gutter_w, top_tab_h + sql_pane_h], fill=BG_GUTTER)
    draw.line([gutter_w, top_tab_h, gutter_w, top_tab_h + sql_pane_h], fill=GUTTER_LINE, width=1)
    
    curr_y = top_tab_h + 10
    for idx, line in enumerate(sql_lines, 1):
        # Line number
        line_num_str = str(idx)
        ln_w = draw.textlength(line_num_str, font=FONT_SQL)
        draw.text((gutter_w - ln_w - 10, curr_y), line_num_str, fill=COLOR_GUTTER_NUM, font=FONT_SQL)
        
        # Highlighted line tokens
        tokens = highlight_sql_line(line)
        tok_x = gutter_w + 14
        for tok_text, tok_col, tok_font in tokens:
            draw.text((tok_x, curr_y), tok_text, fill=tok_col, font=tok_font)
            tok_x += draw.textlength(tok_text, font=tok_font)
        curr_y += sql_line_h
        
    # 3. Mid Tab Strip / Toolbar
    mid_y = top_tab_h + sql_pane_h
    draw.rectangle([0, mid_y, width, mid_y + mid_bar_h], fill=BG_TOOLBAR)
    draw.line([0, mid_y, width, mid_y], fill=BORDER_COLOR, width=1)
    draw.line([0, mid_y + mid_bar_h, width, mid_y + mid_bar_h], fill=BORDER_COLOR, width=1)
    
    tabs = ['Результат', 'Сообщения', 'Уведомления']
    tx = 16
    for tname in tabs:
        is_act = (tname == active_tab)
        fnt = FONT_UI_TAB_BOLD if is_act else FONT_UI_TAB
        col = COLOR_TAB_ACTIVE if is_act else COLOR_TAB_INACTIVE
        draw.text((tx, mid_y + 8), tname, fill=col, font=fnt)
        t_w = draw.textlength(tname, font=fnt)
        if is_act:
            draw.line([tx, mid_y + mid_bar_h - 2, tx + t_w, mid_y + mid_bar_h - 2], fill=COLOR_INDICATOR, width=2)
        tx += t_w + 24
        
    # Pagination info on right of toolbar
    if result_mode in ('grid', 'plan'):
        num_rows = len(grid_rows) if grid_rows else 0
        info_txt = f'Показаны строки: от 1 до {num_rows}   |   Номер страницы: 1 из 1'
        info_w = draw.textlength(info_txt, font=FONT_UI)
        draw.text((width - info_w - 20, mid_y + 9), info_txt, fill=COLOR_TEXT_MUTED, font=FONT_UI)
        
    # 4. Bottom Content
    bot_y = mid_y + mid_bar_h
    if result_mode in ('grid', 'plan'):
        row_num_col_w = 40
        # Draw table header
        draw.rectangle([0, bot_y, width, bot_y + 36], fill=BG_GRID_HDR)
        draw.line([0, bot_y + 36, width, bot_y + 36], fill=BORDER_COLOR, width=1)
        
        # Header columns
        cx = row_num_col_w
        for cname, ctype, cw in grid_cols:
            draw.text((cx + 8, bot_y + 4), cname, fill=(240, 240, 240), font=FONT_UI_BOLD)
            draw.text((cx + 8, bot_y + 19), ctype, fill=(160, 160, 160), font=FONT_SMALL)
            draw.line([cx, bot_y, cx, bot_y + bot_pane_h], fill=BORDER_COLOR, width=1)
            cx += cw
        draw.line([cx, bot_y, cx, bot_y + bot_pane_h], fill=BORDER_COLOR, width=1)
        
        # Data rows
        ry = bot_y + 36
        for r_idx, r_data in enumerate(grid_rows, 1):
            bg_col = BG_ROW_EVEN if r_idx % 2 == 1 else BG_ROW_ODD
            draw.rectangle([0, ry, width, ry + 26], fill=bg_col)
            draw.line([0, ry + 26, width, ry + 26], fill=BORDER_COLOR, width=1)
            
            # Row number
            r_num_str = str(r_idx)
            rn_w = draw.textlength(r_num_str, font=FONT_SMALL)
            draw.text((row_num_col_w - rn_w - 8, ry + 6), r_num_str, fill=COLOR_TEXT_MUTED, font=FONT_SMALL)
            
            cx = row_num_col_w
            for c_idx, cell_val in enumerate(r_data):
                if c_idx < len(grid_cols):
                    cw = grid_cols[c_idx][2]
                    # Check text length and clip if needed
                    val_str = str(cell_val)
                    draw.text((cx + 8, ry + 5), val_str, fill=COLOR_TEXT_MAIN, font=FONT_UI)
                    cx += cw
            ry += 26
    else: # message / error
        ey = bot_y + 14
        for err_l in error_lines:
            if err_l.startswith('ОШИБКА:'):
                draw.text((18, ey), err_l, fill=(255, 100, 100), font=FONT_MSG)
            elif err_l.startswith('SQL-состояние:') or err_l.startswith('CONTEXT:') or err_l.startswith('Подробности:'):
                draw.text((18, ey), err_l, fill=(200, 200, 200), font=FONT_MSG)
            else:
                draw.text((18, ey), err_l, fill=(230, 230, 230), font=FONT_MSG)
            ey += 22
            
    if out_path:
        im.save(out_path, format='PNG', quality=95)
    return im

print('PgAdmin renderer initialized')
