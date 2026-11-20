# 音乐下载器

一个基于 PyQt5 的桌面音乐搜索与下载工具：输入歌名后抓取搜索结果列表，双击任意一条即可把音频文件保存到本地。

## 功能

- 按歌名搜索，列表展示「歌名 - 歌手 - 专辑」
- 支持翻页加载更多结果
- 双击列表项下载音频，保存到 `下载/` 目录（自动创建）
- 多线程并发解析每首歌的音频直链，列表刷新更快
- 支持用 PyInstaller 打包成单文件 exe

## 环境依赖

```
Python 3.8+
PyQt5
requests
beautifulsoup4
```

安装：

```bash
pip install -r requirements.txt
```

## 运行

```bash
python main_v1.py
```

## 打包

```bash
pyinstaller main_v1.spec
```

打包产物在 `dist/main_v1.exe`，无控制台窗口。

## 文件说明

| 文件 | 说明 |
| --- | --- |
| `main_v1.py` | 程序入口，界面逻辑 + 下载逻辑 |
| `get_info.py` | 搜索页抓取、音频直链解析 |
| `音乐下载器.ui` | Qt Designer 界面文件 |
| `音乐下载器.py` | 由 .ui 生成的界面代码 |
| `main_v1.spec` | PyInstaller 打包配置 |
| `py.ico` | 程序图标 |

## 说明

本项目为个人学习 PyQt5 / 爬虫 的练手项目，请勿用于大规模抓取或商业用途。下载的音频文件版权归原作者及版权方所有，仅供本地学习试听，请勿传播。
