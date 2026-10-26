# LeetCode HOT 100 · 算法通关手册

面向面试复习的中文交互式学习站。内容按力扣官方「LeetCode 热题 100」当前专题顺序组织，每题包含题意转述、解题信号、推导步骤、复杂度、易错点与 Python 3 实现。

## 在线访问

[打开 LeetCode HOT 100 · 算法通关手册](https://qianyuan1437.github.io/leetcode-hot100-study/)

## 本地预览

```powershell
python -m http.server 4173 --directory dist
```

访问 `http://127.0.0.1:4173/`。

## 内容校验

```powershell
python tools/build_content.py
python tools/check_content.py
python tools/test_solutions.py
```

站点无构建依赖，`dist/` 可直接部署。

`tools/browser_check.mjs` 支持将待测网址作为第四个参数传入，可对本地预览或线上部署执行完整浏览器交互冒烟测试。

仓库同时包含 GitHub Pages 工作流：推送到 `main` 后，在仓库 Settings → Pages 中选择 GitHub Actions，即可自动校验并发布 `dist/`。

## 主要交互

- 题号、标题、专题与关键词全文搜索；
- 学习状态、难度、17 个专题筛选；
- 折叠式推导、KaTeX 公式、Python 3 代码复制；
- 完成进度、收藏、最近阅读与深浅主题本地持久化；
- 随机一题、专注模式、键盘快捷键与移动端布局；
- 学习记录 JSON 导出与一键重置。

题单名称、题号与顺序核对自[力扣官方学习计划](https://leetcode.cn/studyplan/top-100-liked/)。题意均为摘要转述，讲解与 Python 3 实现为本项目独立整理。

