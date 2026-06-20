# Minesweeper Solver with Rule Support

A constraint satisfaction solver for Minesweeper that supports multiple rule sets.

## 📋 Rules

### Rule V - Standard Minesweeper (默认)
Standard minesweeper rules where each number indicates the exact count of mines in 8 neighbors.

### Rule M - Multi-mine with Checkerboard Coloring 
Cells are colored in a checkerboard pattern (black/white). Top-left (0,0) is a colored (black) cell. 
**Rule: Colored cells count mines as double.**

- Colored cell: `(r + c) % 2 == 0` (top-left is colored)
- A number "n" on a colored cell actually means "2n" mines nearby
- A number "n" on a non-colored cell means "n" mines nearby

Example:
```
Rule M board:
2??
???
???

(0,0) is colored, "2" = 4 mines nearby
(0,1) is not colored, "?" = unknown
```

## 📁 Files

- `config.txt` - Rule specification (one per line, e.g., "V", "M")
- `map.txt` - Current minesweeper board state
- `solver.py` - Core algorithm supporting rule-based constraint propagation
- `map_solver.py` - Main program to read config and map, output next safe cell

## 🚀 Usage

1. Edit `config.txt` to specify rules (default: V)
   ```
   V
   ```
   or
   ```
   M
   ```

2. Edit `map.txt` with current board
   ```
   y??
   ???
   ???
   ```

3. Run:
   ```bash
   python map_solver.py
   ```

## 🧪 Testing

No dedicated unit test scripts are included in this distribution (debug/test scripts were removed to keep the repository minimal). To run the core program:

```bash
python map_solver.py
```

## 🗑️ 缓存清理（Cache cleanup）

- 已删除: `__pycache__/` 目录及所有 `*.pyc` 缓存文件。
- 原因: Python 的字节码缓存是平台/环境相关的，提交到 git 会增加噪音并可能引起平台差异问题。

请确保本地开发时不要将缓存文件加入版本控制（见下文 `.gitignore` 建议）。

## 🧠 设计思路（Design rationale）

- 仓库只保留核心可运行程序：`map_solver.py`, `solver.py`, `map.txt`, `config.txt`, 文档等。
- 所有临时、调试或生成的文件（如日志、调试输出、枚举结果、缓存）不应纳入版本控制，以保持仓库整洁和可复现性。
- 编码/环境相关的本地规则或配置（例如本地的编码说明文件）应保持为本地私有文件，并在 `.gitignore` 中列明，**不要上传到远程仓库**。
- 在需要共享的实现细节中，优先将设计思路写入 `RULES.md` 或 `README.md`，而不是通过生成的中间文件共享。

## .gitignore 建议

请在仓库根目录添加 `.gitignore`，至少包含下列条目：

```
__pycache__/
*.pyc
# 本地编码/环境规则文件（示例名，实际命名请根据本地情况替换）
encoding_rules.txt
encoding.*
```

上述 `encoding_rules.txt`（或类似命名）应当只存在于本地开发环境，并且不会被提交到 git。

## Git 提交建议

在确认 `.gitignore` 配置无误后，将剩余核心文件提交到 git：

```bash
git init        # 如尚未初始化仓库
git add .
git commit -m "Keep core solver files; ignore cache and local encoding rules"
```

如需将仓库推送到远端，请按常规配置 `git remote add` 和 `git push`。
