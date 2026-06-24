#!/usr/bin/env python3
"""生成因子介绍 PPT — 简约三栏布局 + 顶部层级图"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# ── 配色 ──────────────────────────────────────────────
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
BG = RGBColor(0xFA, 0xFA, 0xFA)
TEXT = RGBColor(0x2C, 0x2C, 0x2C)
TEXT_LIGHT = RGBColor(0x66, 0x66, 0x66)
ACCENT_RED = RGBColor(0xC0, 0x39, 0x2B)

FUND = RGBColor(0x6B, 0x4E, 0xA8)      # 基本面 · 紫
PRICE = RGBColor(0xE8, 0x7A, 0x2E)       # 量价 · 橙
ALT = RGBColor(0x9B, 0x3A, 0x6B)         # 另类 · 玫红

FUND_LIGHT = RGBColor(0xF3, 0xEF, 0xFA)
PRICE_LIGHT = RGBColor(0xFD, 0xF0, 0xE4)
ALT_LIGHT = RGBColor(0xFA, 0xEC, 0xF2)

FONT = "PingFang SC"  # macOS; fallback handled by PowerPoint


def set_bg(slide, color=BG):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_textbox(slide, left, top, width, height, text="", size=12, bold=False,
                color=TEXT, align=PP_ALIGN.LEFT, font=FONT, anchor=MSO_ANCHOR.TOP):
    tb = slide.shapes.add_textbox(left, top, width, height)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(size)
    p.font.bold = bold
    p.font.color.rgb = color
    p.font.name = font
    p.alignment = align
    return tb, tf


def add_para(tf, text, size=11, bold=False, color=TEXT, space_before=0, space_after=4):
    p = tf.add_paragraph()
    p.text = text
    p.font.size = Pt(size)
    p.font.bold = bold
    p.font.color.rgb = color
    p.font.name = FONT
    p.space_before = Pt(space_before)
    p.space_after = Pt(space_after)
    return p


def rounded_pill(slide, left, top, width, height, text, border_color, fill_color=WHITE,
                 text_size=13, text_bold=True, text_color=None):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    shape.line.color.rgb = border_color
    shape.line.width = Pt(1.5)
    tf = shape.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(text_size)
    p.font.bold = text_bold
    p.font.color.rgb = text_color or border_color
    p.font.name = FONT
    p.alignment = PP_ALIGN.CENTER
    return shape


def vertical_pill(slide, left, top, width, height, text, border_color, fill_color=WHITE):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    shape.line.color.rgb = border_color
    shape.line.width = Pt(1.2)
    tf = shape.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    # 竖排：每字一行
    p.text = "\n".join(text)
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = border_color
    p.font.name = FONT
    p.alignment = PP_ALIGN.CENTER
    p.line_spacing = 1.0
    return shape


def connector_line(slide, x1, y1, x2, y2, color=RGBColor(0xCC, 0xCC, 0xCC)):
    connector = slide.shapes.add_connector(1, x1, y1, x2, y2)  # straight
    connector.line.color.rgb = color
    connector.line.width = Pt(0.75)
    return connector


def add_factor_block(slide, left, top, width, hook, example, definition, accent):
    """单个因子：钩子句 + 例 + 核心定义"""
    _, tf = add_textbox(slide, left, top, width, Inches(2.2))
    p = tf.paragraphs[0]
    p.text = hook
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = accent
    p.font.name = FONT
    p.space_after = Pt(6)

    add_para(tf, f"例：{example}", size=10, color=TEXT_LIGHT, space_after=6)
    add_para(tf, f"核心定义：{definition}", size=10, color=TEXT, bold=False)


def slide_cover(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide, WHITE)

    add_textbox(slide, Inches(1.5), Inches(2.2), Inches(7), Inches(1),
                "因子投资 · 入门指南", size=36, bold=True, align=PP_ALIGN.CENTER)
    add_textbox(slide, Inches(1.5), Inches(3.2), Inches(7), Inches(0.6),
                "基本面 · 量价 · 另类", size=16, color=TEXT_LIGHT, align=PP_ALIGN.CENTER)

    # 底部色条
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, Inches(5.0), Inches(10), Inches(0.08))
    bar.fill.solid()
    bar.fill.fore_color.rgb = FUND
    bar.line.fill.background()
    bar2 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, Inches(5.08), Inches(10), Inches(0.08))
    bar2.fill.solid()
    bar2.fill.fore_color.rgb = PRICE
    bar2.line.fill.background()
    bar3 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, Inches(5.16), Inches(10), Inches(0.08))
    bar3.fill.solid()
    bar3.fill.fore_color.rgb = ALT
    bar3.line.fill.background()


def slide_overview(prs):
    """全景一页：顶部层级图 + 底部三栏详解"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide, WHITE)

    add_textbox(slide, Inches(0.6), Inches(0.35), Inches(8), Inches(0.5),
                "因子全景", size=22, bold=True)

    # ── 顶部三大类 pill ──
    cat_w, cat_h = Inches(2.4), Inches(0.55)
    y_cat = Inches(1.0)
    cats = [
        (Inches(0.9), "基本面因子", FUND, FUND_LIGHT),
        (Inches(3.8), "量价因子", PRICE, PRICE_LIGHT),
        (Inches(6.7), "另类因子", ALT, ALT_LIGHT),
    ]
    centers = []
    for x, label, color, fill in cats:
        rounded_pill(slide, x, y_cat, cat_w, cat_h, label, color, fill, text_size=14)
        centers.append(x + cat_w / 2)

    # ── 连接线 + 子因子竖 pill ──
    y_sub = Inches(1.85)
    sub_h = Inches(1.5)
    sub_w = Inches(0.42)
    subs = [
        [(centers[0] - Inches(0.55), "成长因子"), (centers[0] + Inches(0.15), "价值因子")],
        [(centers[1] - Inches(0.55), "动量因子"), (centers[1] + Inches(0.15), "反转因子")],
        [(centers[2] - Inches(0.75), "情绪因子"), (centers[2], "供应链"), (centers[2] + Inches(0.75), "卫星数据")],
    ]
    colors = [FUND, PRICE, ALT]
    fills = [FUND_LIGHT, PRICE_LIGHT, ALT_LIGHT]
    for i, group in enumerate(subs):
        cx = centers[i]
        connector_line(slide, cx, y_cat + cat_h, cx, y_sub - Inches(0.05))
        for x, name in group:
            vertical_pill(slide, x, y_sub, sub_w, sub_h, name, colors[i], fills[i])
            mid_x = x + sub_w / 2
            connector_line(slide, cx, y_sub - Inches(0.05), mid_x, y_sub)

    # ── 分隔线 ──
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(3.55), Inches(8.8), Pt(0.75))
    line.fill.solid()
    line.fill.fore_color.rgb = RGBColor(0xE8, 0xE8, 0xE8)
    line.line.fill.background()

    # ── 底部三栏内容 ──
    col_w = Inches(2.85)
    col_y = Inches(3.75)
    col_xs = [Inches(0.65), Inches(3.55), Inches(6.45)]

    # 基本面
    add_textbox(slide, col_xs[0], col_y, col_w, Inches(0.35),
                "基本面因子", size=13, bold=True, color=FUND)
    add_factor_block(
        slide, col_xs[0], col_y + Inches(0.38), col_w,
        "成长因子：过去扩张快，未来还会快？",
        "奶茶品牌去年10家店、今年30家，营收利润双增，处于高速扩张期。",
        "用营收、利润增速衡量扩张能力，捕捉高增长机会。",
        FUND,
    )
    add_factor_block(
        slide, col_xs[0], col_y + Inches(1.55), col_w,
        "价值因子：现在卖得便宜，未来更划算？",
        "两家店利润相当，B店市值明显偏低，更像被低估，安全边际更高。",
        "用 BP 衡量股价是否低于内在价值，捕捉「便宜买好货」机会。",
        FUND,
    )

    # 量价
    add_textbox(slide, col_xs[1], col_y, col_w, Inches(0.35),
                "量价因子", size=13, bold=True, color=PRICE)
    add_factor_block(
        slide, col_xs[1], col_y + Inches(0.38), col_w,
        "动量因子：过去涨得猛，未来还会涨？",
        "网红奶茶店上月排队2小时，本月大概率仍排长队，热度有惯性。",
        "量化价格趋势延续性，捕捉「强者恒强」现象。",
        ACCENT_RED,
    )
    add_factor_block(
        slide, col_xs[1], col_y + Inches(1.55), col_w,
        "反转因子：涨过头了，会回摆？",
        "明星打卡排队从10分钟飙到3小时，一个月后缩回15分钟。",
        "盛极而衰、否极泰来，捕捉均值回归机会。",
        PRICE,
    )

    # 另类
    add_textbox(slide, col_xs[2], col_y, col_w, Inches(0.35),
                "另类因子", size=13, bold=True, color=ALT)
    add_factor_block(
        slide, col_xs[2], col_y + Inches(0.38), col_w,
        "另类因子：停车场能预判业绩？",
        "卫星数百货停车场车辆，车流下滑往往早于财报披露。",
        "从非传统数据（文本、情绪、供应链）提取投资信号。",
        ALT,
    )


def slide_detail_cards(prs):
    """第二页：卡片式展开，每类一屏更易阅读（演讲用）"""
    categories = [
        {
            "title": "基本面因子",
            "color": FUND,
            "light": FUND_LIGHT,
            "factors": [
                ("成长因子", "过去扩张快，未来还会快？",
                 "奶茶品牌去年10家店、今年30家，营收利润双增。",
                 "用营收、利润增速衡量扩张能力。"),
                ("价值因子", "现在卖得便宜，未来更划算？",
                 "两家店利润相当，B店市值偏低，更像被低估。",
                 "用 BP 衡量股价是否低于内在价值。"),
            ],
        },
        {
            "title": "量价因子",
            "color": PRICE,
            "light": PRICE_LIGHT,
            "factors": [
                ("动量因子", "过去涨得猛，未来还会涨？",
                 "网红奶茶店上月排队2小时，本月大概率仍排长队。",
                 "量化趋势延续性，捕捉「强者恒强」。"),
                ("反转因子", "涨过头了，会回摆？",
                 "明星打卡排队飙到3小时，一个月后缩回15分钟。",
                 "捕捉均值回归，盛极而衰、否极泰来。"),
            ],
        },
        {
            "title": "另类因子",
            "color": ALT,
            "light": ALT_LIGHT,
            "factors": [
                ("情绪因子", "舆论风向能领先股价？",
                 "社交媒体负面情绪升温，常早于股价反应。",
                 "从文本、舆情等非结构化数据提取信号。"),
                ("供应链因子", "上游异动能预警下游？",
                 "供应商出货放缓，或预示品牌方下季承压。",
                 "用产业链数据辅助基本面判断。"),
            ],
        },
    ]

    for cat in categories:
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        set_bg(slide, WHITE)

        # 左侧色条标题区
        band = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(0.12), Inches(5.625))
        band.fill.solid()
        band.fill.fore_color.rgb = cat["color"]
        band.line.fill.background()

        add_textbox(slide, Inches(0.55), Inches(0.45), Inches(4), Inches(0.5),
                    cat["title"], size=26, bold=True, color=cat["color"])

        card_w = Inches(4.1)
        card_h = Inches(1.85)
        for i, (name, hook, example, definition) in enumerate(cat["factors"]):
            y = Inches(1.35) + i * Inches(2.05)
            card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                                          Inches(0.55), y, card_w, card_h)
            card.fill.solid()
            card.fill.fore_color.rgb = cat["light"]
            card.line.color.rgb = cat["color"]
            card.line.width = Pt(0.75)

            _, tf = add_textbox(slide, Inches(0.8), y + Inches(0.18), Inches(3.6), card_h)
            p = tf.paragraphs[0]
            p.text = name
            p.font.size = Pt(15)
            p.font.bold = True
            p.font.color.rgb = cat["color"]
            p.font.name = FONT

            add_para(tf, hook, size=12, bold=True, color=TEXT, space_before=4)
            add_para(tf, f"例：{example}", size=10, color=TEXT_LIGHT, space_before=6)
            add_para(tf, f"核心定义：{definition}", size=10, color=TEXT, space_before=4)


def main():
    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(5.625)  # 16:9

    slide_cover(prs)
    slide_overview(prs)
    slide_detail_cards(prs)

    out = "/workspace/因子投资介绍.pptx"
    prs.save(out)
    print(f"已生成：{out}")


if __name__ == "__main__":
    main()
