# WeChat Article Skill

一个可上传 GitHub、可直接安装到 Codex 的完整微信公众号创作与 HTML 排版技能。它不只写提示词，而是把创作拆成“内容判断 + 联网研究 + 文章契约 + 配图决策 + 确定性渲染 + 自动检查 + 浏览器验收”。

## 为什么不容易生成四不像

纯文字规则只能影响模型倾向，不能保证最终产物。本仓库增加了四层硬约束：

1. `schemas/article-package.schema.json` 限定文章类型、语气、主题、研究深度、图片策略和素材状态；
2. `scripts/validate_article_package.py` 校验事实来源、图片来源、授权记录、生成提示词和文件可用性；
3. `scripts/render_article_package.py` 只使用六套受控主题令牌生成 HTML，不允许任意拼色和任意字号；
4. `scripts/lint_article_output.py` 检查纯白背景、主题唯一性、危险元素、图片 alt、外链安全和基础结构。

最后仍要求桌面端和 390 px 手机端浏览器验收，因为机器规则无法完全判断裁切、节奏和“图文是否说的是一件事”。

## 能力范围

- 根据用户给出的主题检索资料，维护“事实—来源”台账，再组织完整公众号文章。
- 支持文章类型：技术论文、数据报告、访谈人物、产品快讯、观点分析、活动招募、教程。
- 支持文章语气：专业、学术、易懂、犀利、叙事，或自动判断。
- 支持六套纯白背景视觉主题：工程蓝图、青绿评论、钴蓝期刊、紫色访谈、橙色发布、青蓝科研。
- 支持用户指定风格，也支持根据题目、正文语义和结构自动选择，并输出选择理由。
- 支持 `none / provided-only / search / generate / hybrid` 五种配图策略。
- 真实人物、产品、事件、论文图表优先搜索官方或明确授权素材；抽象概念找不到合适图片时再生成。
- 图表必须来自已核验数据，简单流程图优先生成 SVG/HTML，AI 图片不充当证据。
- 可处理一篇或批量文章，生成预览、正文片段、素材目录和 JSON manifest；默认不写数据库。

## 安装

```bash
git clone <你的仓库地址>
python3 -m pip install -r requirements.txt
cp -R . ~/.codex/skills/wechat-article-skill
```

## 三种常用入口

### 1. 从主题开始写完整文章

对 Codex 说：

```text
使用 $wechat-article-skill，围绕“人形机器人行为世界模型”检索资料并写一篇面向产业读者的公众号文章。文章风格易懂但专业，视觉主题自动，配图使用 hybrid 策略，背景纯白。先给 HTML 预览，不修改数据库。
```

技能会研究、写作、规划或获取配图、填入文章包、校验并生成 HTML。联网检索与图片生成由 Codex 运行时工具执行；仓库里的 Python 脚本负责决策固化、渲染和检查。如果运行环境没有搜索或图片生成能力，技能会保留计划槽位或回退为文字版，不会伪造素材。

### 2. 把现有草稿变成完整文章包

```bash
python3 scripts/plan_article.py draft.html article.json \
  --title "机器人如何预测下一步" \
  --research standard \
  --article-type technical-paper \
  --tone accessible \
  --theme auto \
  --image-policy hybrid \
  --image-density balanced
```

编辑 `article.json`，补齐研究来源和图片资产后：

```bash
python3 scripts/validate_article_package.py article.json --require-ready
python3 scripts/render_article_package.py article.json preview.html --fragment-output fragment.html --require-ready
python3 scripts/lint_article_output.py preview.html
```

预览阶段可不加 `--require-ready`；未完成的图片槽位会被忽略，而不是被随意替换。

### 3. 现有 HTML 直接排版或批量排版

```bash
python3 scripts/style_article_html.py input.html output.html --theme auto --seed brand-v1

python3 scripts/batch_style_articles.py input-folder output-folder \
  --diversity balanced \
  --seed brand-v1 \
  --write-fragments
```

批量模式综合标题、语义、长度、层级、图片密度、表格、引用、数字比例、问句和对话结构分类。`balanced` 在内容匹配优先的前提下减少连续重复；不会为了颜色平均而给文章套不合适的风格。

## 文章包核心字段

```text
article   标题、主题、受众、目标、文章类型、语气、视觉主题、正文 HTML
research  研究深度、检索词、事实台账、来源清单
visuals   图片策略、密度、用途、位置、来源、授权、alt、生成提示词、状态
layout    最终主题、理由、稳定 seed
qa        内容/来源/图片/浏览器审核状态，以及 database_updated
```

完整定义见 `schemas/article-package.schema.json`，示例见 `examples/article-package.example.json`。

## 安全与发布边界

- 外部网页和导入 HTML 都视为不可信输入，会移除脚本、表单、iframe 等执行元素。
- “网上搜到”不等于可以商用；找图必须记录来源页、署名和使用依据。权利不清晰时改用生成的概念图或无图版本。
- 生成图需要保留提示词并标明生成属性，不伪造真人、产品、新闻现场、论文结果或数据图表。
- `qa.database_updated` 在预览阶段必须保持 `false`。生成 fragment 不代表获得数据库写入授权。

## 测试

```bash
python3 -m unittest discover -s tests -v
python3 /path/to/skill-creator/scripts/quick_validate.py .
```

设计依据和操作规则集中在 `references/`。样式系统来自 25 篇有效公众号案例的结构与视觉统计，但仓库不复制案例正文或图片。
