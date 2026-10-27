# LeetCode HOT 100 · 算法通关手册

面向面试复习的中文交互式学习站。内容按力扣官方「LeetCode 热题 100」当前专题顺序组织，每题包含完整题意转述、全部输入/输出示例、约束条件、解题信号、推导步骤、复杂度、易错点、Python 3 实现及代码所用 Python API 的逐项说明。

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

维护者可在已登录 GitHub CLI 的环境中重新抓取结构化题面资料：

```powershell
python tools/fetch_problem_details.py
```

站点无构建依赖，`dist/` 可直接部署。

`tools/browser_check.mjs` 支持将待测网址作为第四个参数传入，可对本地预览或线上部署执行完整浏览器交互冒烟测试。

仓库同时包含 GitHub Pages 工作流：推送到 `main` 后，在仓库 Settings → Pages 中选择 GitHub Actions，即可自动校验并发布 `dist/`。

## 主要交互

- 题号、标题、专题与关键词全文搜索；
- 学习状态、难度、17 个专题筛选；
- 完整题意、全部输入/输出示例与数据范围；
- 折叠式推导、KaTeX 公式、Python 3 代码复制及 API 说明；
- 完成进度、收藏、最近阅读与深浅主题本地持久化；
- 随机一题、专注模式、键盘快捷键与移动端布局；
- 电脑版采用固定专题侧栏、双列题单和双栏题意；手机版采用横向专题滑轨、单列卡片、紧凑进度卡及底部快捷导航；
- 学习记录 JSON 导出与一键重置。

## 数据来源与授权

题单名称、题号与顺序核对自[力扣官方学习计划](https://leetcode.cn/studyplan/top-100-liked/)。示例与约束参考 [doocs/leetcode](https://github.com/doocs/leetcode) 并按其 [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) 授权标注来源；题意经过本站整理转述。中文推导、Python 3 实现与 API 说明为本项目独立整理。详见 [DATA_LICENSE.md](DATA_LICENSE.md)。

