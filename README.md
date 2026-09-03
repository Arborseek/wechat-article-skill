# WeChat Article Skill

一个面向 **Codex、OpenClaw、Hermes Agent 和 WorkBuddy** 的微信公众号创作与 HTML 排版技能。它不只写提示词，而是把创作拆成“内容判断 + 联网研究 + 文章契约 + 配图决策 + 确定性渲染 + 自动检查 + 浏览器验收”。

仓库地址：<https://github.com/Arborseek/wechat-article-skill>

## 平台支持

| 平台 | 支持程度 | 推荐安装方式 | 技能调用方式 |
| --- | --- | --- | --- |
| Codex | 完整支持 | 在聊天中让 `$skill-installer` 从 GitHub 安装 | `$wechat-article-skill` |
| OpenClaw | 完整支持 | `openclaw skills install git:...` | `$wechat-article-skill` 或自然语言 |
| Hermes Agent | 完整支持 | 聊天中 `/skills install <SKILL.md URL>` | `/wechat-article-skill` 或自然语言 |
| WorkBuddy | 完整技能包 | 生成兼容 ZIP，在技能市场的创建对话中上传 | 在会话中选择/调用已安装技能 |

完整功能需要 Python 3 和 `beautifulsoup4>=4.12,<5`。联网研究、图片搜索与图片生成取决于宿主智能体是否提供对应工具；没有这些工具时，技能仍可完成已有正文的分类、排版、渲染和检查。

> 安装第三方技能前应先查看仓库内容。技能本身不会自动写数据库；只有用户明确批准后，宿主智能体才应执行数据库替换。

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

下面每个平台都同时给出“直接发消息安装”和“手动安装”。对话式安装要求当前智能体拥有联网、终端和技能目录写入权限；如果权限不足，使用对应的手动方式。

### Codex

#### 直接发消息安装（推荐）

把下面这段原样发给 Codex：

```text
请使用 $skill-installer 安装这个 GitHub 技能：
https://github.com/Arborseek/wechat-article-skill

安装完成后，请根据仓库 requirements.txt 安装 Python 依赖，并告诉我技能安装到了哪个目录。不要修改仓库文件，也不要执行任何数据库操作。
```

安装后新开一个对话，或在下一轮直接这样使用：

```text
使用 $wechat-article-skill，把这篇草稿排版成纯白背景的微信公众号 HTML，先生成预览，不修改数据库。
```

#### 手动安装

```bash
git clone https://github.com/Arborseek/wechat-article-skill.git \
  ~/.codex/skills/wechat-article-skill
python3 -m pip install -r \
  ~/.codex/skills/wechat-article-skill/requirements.txt
```

如果设置了 `CODEX_HOME`，请将 `~/.codex` 替换为该目录。安装后重新开始一次 Codex 会话，使技能列表刷新。

更新：

```bash
git -C ~/.codex/skills/wechat-article-skill pull --ff-only
```

Codex 技能说明：[官方文档](https://developers.openai.com/codex/skills/)。

### OpenClaw

#### 直接发消息安装

把下面这段发给具有终端权限的 OpenClaw 智能体：

```text
请先检查下面 GitHub 仓库中的 SKILL.md 和脚本，再把它作为全局技能安装：
https://github.com/Arborseek/wechat-article-skill

请执行 OpenClaw 的 Git 技能安装流程，技能名保持 wechat-article-skill；随后安装 requirements.txt 中的 Python 依赖。完成后验证技能可见，但不要运行文章任务，也不要修改任何数据库。
```

#### 命令安装（推荐、最确定）

全局安装，供本机所有 OpenClaw 智能体使用：

```bash
openclaw skills install \
  git:Arborseek/wechat-article-skill@main \
  --global
python3 -m pip install -r \
  ~/.openclaw/skills/wechat-article-skill/requirements.txt
```

只安装到当前工作区：

```bash
openclaw skills install git:Arborseek/wechat-article-skill@main
python3 -m pip install -r \
  ./skills/wechat-article-skill/requirements.txt
```

Git 安装不会被 `openclaw skills update` 自动跟踪；更新时重新执行同一条安装命令。新会话中可这样调用：

```text
$wechat-article-skill 请根据这个主题写一篇公众号文章，视觉主题自动，配图策略 hybrid，先输出 HTML 预览。
```

OpenClaw 技能安装说明：[官方文档](https://github.com/openclaw/openclaw/blob/main/docs/tools/skills.md#installing-from-clawhub)。

### Hermes Agent

#### 在聊天中安装（推荐）

在 Hermes 会话里发送：

```text
/skills install https://raw.githubusercontent.com/Arborseek/wechat-article-skill/main/SKILL.md --name wechat-article-skill --now
```

Hermes 会从 `SKILL.md` URL 安装技能及其中引用的支持文件。`--now` 会立即刷新当前会话的技能缓存；也可以省略它，然后执行 `/reset` 或开始新会话。

如果当前版本未完整取得 `scripts/`、`references/` 等目录，请使用下面的整仓手动安装方式：

```bash
git clone https://github.com/Arborseek/wechat-article-skill.git \
  ~/.hermes/skills/wechat-article-skill
python3 -m pip install -r \
  ~/.hermes/skills/wechat-article-skill/requirements.txt
```

验证并调用：

```text
/skills search wechat-article-skill
/wechat-article-skill 把这篇文章整理成适合手机阅读的微信公众号 HTML，先给预览。
```

也可以使用自然语言：

```text
请使用 wechat-article-skill，根据“人形机器人行为世界模型”研究并撰写公众号文章，背景纯白，主题自动选择。
```

Hermes 技能安装说明：[官方文档](https://hermes-agent.nousresearch.com/docs/guides/work-with-skills#installing-from-the-hub)。

### WorkBuddy

WorkBuddy 的技能上传结构和元数据与 Codex 略有不同。不要直接上传 GitHub 自动生成的源码 ZIP；先生成专用包：

```bash
git clone https://github.com/Arborseek/wechat-article-skill.git
cd wechat-article-skill
python3 scripts/build_workbuddy_package.py
```

产物位置：

```text
dist/wechat-article-skill-workbuddy.zip
```

打包脚本会生成 WorkBuddy 要求的 `skills/wechat-article-skill/` 目录，并加入 `description_zh`、`description_en`、`version`、`author` 等元数据，同时保持根目录的 Codex 标准 `SKILL.md` 不变。

#### 通过创建技能对话安装

1. 进入 WorkBuddy 左侧的“专家 · 技能 · 连接器”。
2. 打开“技能市场”，点击右上角“添加技能 → 创建技能”。
3. 上传刚生成的 `wechat-article-skill-workbuddy.zip`。
4. 在创建技能的对话中发送：

```text
请导入我上传的 wechat-article-skill-workbuddy.zip，保留其中的 SKILL.md、references、scripts、schemas 和 examples。

请将它创建为“微信公众号智能创作与排版”技能，允许用户主动调用；确认运行环境支持 Bash、Python 3，并安装 requirements.txt 中的依赖。创建完成后只做结构校验，不要执行文章生成，也不要访问或修改任何数据库。
```

5. 创建完成后安装该技能，再在普通会话里发送：

```text
请使用“微信公众号智能创作与排版”技能，把我上传的文章整理为纯白背景的微信公众号 HTML，先输出预览文件。
```

如果该技能以后发布到 WorkBuddy 技能市场，普通用户只需进入技能市场，点击技能卡片右上角的 `+` 安装，无需上传 ZIP。

WorkBuddy 技能结构说明：[官方文档](https://open.workbuddy.cn/en/docs/skill)。

### 通用手动安装

对于其他兼容 Agent Skills / `SKILL.md` 的智能体，可以把完整仓库克隆到其技能目录：

```bash
git clone https://github.com/Arborseek/wechat-article-skill.git \
  /path/to/agent/skills/wechat-article-skill
python3 -m pip install -r \
  /path/to/agent/skills/wechat-article-skill/requirements.txt
```

必须复制完整仓库，不能只复制 `SKILL.md`，因为确定性排版、文章契约、渲染和检查依赖 `scripts/`、`references/`、`schemas/` 与 `examples/`。

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
