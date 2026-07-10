import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

# 数据：每个模型下 x / - / √ 的数量
counts = {
    "GPT-4o": { "-": 3, "x": 2, "√": 19},
    "Claude3.5": {"-": 1, "x": 2, "√": 21},
    "Deepseek-R1": {"-": 0, "x": 1, "√": 23},
}

models = list(counts.keys())
symbols = [ "-", "x", "√"]  # 组内顺序

# ---- 展平为 9 根棒棒糖，并记录每组的起止索引 ----
flat_sym = []
flat_model = []
values = []
group_bounds = []
for m in models:
    start = len(values)
    for s in symbols:
        flat_sym.append(s)
        flat_model.append(m)
        values.append(counts[m][s])
    end = len(values) - 1
    group_bounds.append((start, end))

values = np.array(values)
n = len(values)

# 让"纵轴挨得近"：缩小 x 步长
step = 0.18
x = np.arange(n) * step

# 学术风格颜色：使用柔和的学术配色
academic_colors = [
    '#2E86AB', '#A23B72', '#F18F01',  # 第一组：深蓝、深红、橙色
    '#C73E1D', '#7209B7', '#F77F00',  # 第二组：深红、紫色、橙色
    '#33658A', '#2F4858', '#F6AE2D',  # 第三组：蓝、绿、黄
]
colors = [academic_colors[i % len(academic_colors)] for i in range(n)]

# ---- 版式：主图 + 底部彩色带 ----
fig = plt.figure(figsize=(9.2, 4))
# 调整两个子图的高度比例，减少底部彩色带的高度，从而减少下方空白
gs = fig.add_gridspec(nrows=2, ncols=1, height_ratios=[20, 0.5], hspace=0.01)  # 减少底部彩色带比例，减小间距
ax = fig.add_subplot(gs[0])
ax_bar = fig.add_subplot(gs[1], sharex=ax)

# ---- 主图：棒棒糖 ----
for i, (xi, yi) in enumerate(zip(x, values)):
    # 增加线宽使棒棒糖杆更粗
    ax.vlines(xi, 0, yi, color=colors[i], linewidth=8, alpha=0.8)
    # 增加点的大小使棒棒糖头更大
    ax.scatter([xi], [yi], s=600, color=colors[i], zorder=5, alpha=0.9)

    # 顶部数值标注（竖排）- 增加字体大小和权重，调整位置
    ax.text(
        xi, yi + (values.max() * 0.03 + 1.5), f"{int(yi)}",  # 增加了偏移量
        color=colors[i], ha="center", va="bottom",
        rotation=0, fontsize=20, fontweight="bold",  # 增加字体大小和粗细
        alpha=1.0  # 完全不透明
    )

# y 轴设置
ax.set_ylabel("The number of cases", fontsize=20)
ax.set_ylim(0, values.max() * 1.25 + 2)  # 增加上边界空间以容纳更大的数字
ax.grid(axis="y", linestyle="--", alpha=0.9, color='gray')
ax.set_axisbelow(True)

# 不用默认 x tick，改用"符号 + 模型"两层标注
ax.set_xticks([])
ax.tick_params(axis="x", length=0)

# ---- 两层底部标注：每根下方是符号；每组下方居中写模型 ----
# 位置用 x 轴坐标系（x 用 data，y 用轴比例），y<0 放在轴下方
for i, xi in enumerate(x):
    # 检查是否是 "x" 或 "√" 符号，如果是则将位置向左偏移
    if flat_sym[i] in ["x", "√"]:
        offset = -0.02  # 向左偏移
    else:
        offset = 0

    ax.text(
        xi + offset, -0.07, flat_sym[i],
        transform=ax.get_xaxis_transform(),
        ha="center", va="top", fontsize=18, alpha=0.8
    )

for (start, end), m in zip(group_bounds, models):
    mid_x = (x[start] + x[end]) / 2
    ax.text(
        mid_x, -0.18, m,
        transform=ax.get_xaxis_transform(),
        ha="center", va="top", fontsize=18, fontweight="bold", alpha=0.9
    )
    # 组分隔线（可选）
    if end != group_bounds[-1][1]:
        ax.axvline((x[end] + x[end + 1]) / 2, color="0.7", linewidth=0.8, alpha=0.6)

# x 范围更紧凑
ax.set_xlim(x[0] - step * 0.5, x[-1] + step * 0.5)

# ---- 底部彩色带（每根对应一块）----
ax_bar.set_ylim(0, 1)
ax_bar.set_yticks([])
ax_bar.set_xticks([])
for spine in ax_bar.spines.values():
    spine.set_visible(False)

for i, xi in enumerate(x):
    ax_bar.add_patch(Rectangle((xi - step * 0.35, 0), step * 0.7, 1.0, color=colors[i], ec="none", alpha=0.8))

# 优化底部边距以适应减少的底部元素
plt.subplots_adjust(left=0.10, right=0.98, top=0.92, bottom=0.20)  # 减少底部边距
plt.savefig('lollipop_chart.pdf', format='pdf', bbox_inches='tight', dpi=300)

plt.show()




