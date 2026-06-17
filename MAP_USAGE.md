# Map Solver Usage Guide

## 快速开始

### 1. 编辑 `map.txt`

在项目目录中编辑 `map.txt` 文件，记录当前的扫雷地图状态。

**格式说明：**
- `x` - 已确认的雷
- `y` 或 `0` - 周围0个雷（安全）
- `1-8` - 周围N个雷
- `?` - 未知格子

### 2. 运行求解器

```bash
python map_solver.py
```

## 示例

### 示例1：从安全格开始

map.txt:
```
y??
???
???
```

输出：
```
Current board:
  y??  (row 0)
  ???  (row 1)
  ???  (row 2)

Next safe cell to click: (0, 1)
  Row 0, Column 1
```

### 示例2：包含确认的雷和数字

map.txt:
```
x1?
1?1
???
```

输出：
```
Current board:
  x1?  (row 0)
  1?1  (row 1)
  ???  (row 2)

Confirmed mines:
  Position (0, 0)

Next safe cell to click: (1, 1)
  Row 1, Column 1
```

### 示例3：较大的地图

map.txt:
```
11y11
1?1?1
1?1?1
11y11
?????
```

## 程序流程

1. **加载地图** - 从 `map.txt` 读取当前扫雷状态
2. **验证格式** - 确保所有行长度相同
3. **查找已知雷** - 列出所有标记为 `x` 的确认雷
4. **求解下一步** - 使用约束满足算法找出下一个安全点击位置
5. **输出结果** - 显示下一个安全格子的坐标

## 坐标说明

输出的坐标格式为 (行, 列)，从0开始计数：
- (0, 0) 是左上角
- (0, 1) 是右上角第一个
- (1, 0) 是左上角下方

## 进阶使用

可以直接在Python中使用求解器：

```python
from map_solver import MapSolver

solver = MapSolver('map.txt')
if solver.load_map():
    next_move = solver.find_next_move()
    if next_move:
        r, c = next_move
        print(f"点击: ({r}, {c})")
```
