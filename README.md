<div align="center">

# Humanities Essay

**让历史可考，让人物复杂，让文学表达有余韵。**

[![Validation](https://github.com/2023violet/humanities-essay/actions/workflows/validate.yml/badge.svg?branch=main)](https://github.com/2023violet/humanities-essay/actions/workflows/validate.yml)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue)](LICENSE)
![Version](https://img.shields.io/badge/version-3.1.0-informational)
![Python](https://img.shields.io/badge/test_tools-Python%203%20stdlib-lightgrey)

**简体中文** · [English](README.en.md)

</div>

`humanities-essay` 是基于开放 [Agent Skills](https://agentskills.io/) 目录格式的中文人文叙事写作 Skill。面向历史人物、古典诗文、文学比较、神话与文化意象，支持研究、构思、成稿、事实复核、只读审稿、最小修改与发布适配。

**它不是“复制爆款文风”的提示词。** 它要求作者的独特判断经得起证据、反证和编辑。好听不是事实，高分不是流量保证。

## 目录

- [功能](#功能) · [快速开始](#快速开始) · [创作流程](#创作流程) · [设计原则](#设计原则) · [验证](#验证) · [仓库结构](#仓库结构) · [文档](#文档) · [贡献](#贡献) · [许可证](#许可证)

## 功能

| 能力 | 说明 |
|---|---|
| **立意与构思** | 两条候选命题、题眼/入口问题分离、核心矛盾与必要反证 |
| **证据驱动写作** | F/I/A/R/D/U 六种证据状态，关键引文、时序、身份和因果检查 |
| **六类叙事架构** | 字句细读、版本比较、对照审判、意象考古、时间回声、诚实的观察研究 |
| **独立审稿** | 事实硬门禁、人物复杂度、场景必要性、结尾回响；只审不改是明确模式 |
| **最小修改** | 保留用户锁定的结构和关键句，批量列改动且只修必要处 |
| **单图视觉适配** | 默认单张封面＋配乐＋长简介，可切换木刻、肖像、空间、拼贴、文献等视觉方向 |
| **发布辅助** | 可运行的字符统计与平台指标比率脚本（不自动发布、不抓取后台） |

## 快速开始

### 安装 Skill

克隆或下载本仓库，把 `humanities-essay/` **完整复制**到所用 Agent 支持的 Skills 目录，不要只复制 `SKILL.md`：

```bash
git clone https://github.com/2023violet/humanities-essay.git
# Claude Code 项目示例：
mkdir -p .claude/skills
cp -R humanities-essay/humanities-essay .claude/skills/humanities-essay
```

Windows PowerShell（在仓库根目录执行）：

```powershell
New-Item -ItemType Directory -Force .claude\skills | Out-Null
Copy-Item -Recurse .\humanities-essay .\.claude\skills\
```

Codex / 其他支持 Agent Skills 的客户端可导入相同的 `humanities-essay/` 目录；实际安装位置与调用格式以对应客户端文档为准。

### 调用示例

```text
/humanities-essay 写一篇苏轼的原创人文长文，2800字以内，先核对引文，只要单图＋音乐＋长简介方案。

/humanities-essay 对这篇李斯稿只做独立审稿，不动正文；标出事实、论证、风格风险和保护线。

/humanities-essay 我批准四处句子级修改，其余冻结；输出对照与最终字符数。
```

### 发布长度检查

```bash
python humanities-essay/scripts/check_length.py path/to/post.txt --min 2500 --max 3000
```

工具同时报告 Unicode 码点与 UTF-16 单元计数，并以更保守的 UTF-16 作为默认门禁；实际平台编辑器口径仍需最终确认。

## 创作流程

**素材与来源 → 两种可辩护的立意 → 选择叙事发动机 → 场景与反证 → 写作 → 事实硬门禁 → 独立审稿 → 最小改稿 → 单图发布 → 数据复盘。**

五篇样本把这一流程具体化：项羽写武力的边界；刘邦写胜利的代价；韩信写才能与权位；李斯写位置与退出；苏轼写受限生活中的感受力。**案例分析只提取方法，不包含五篇完整文章或原始账户后台数据。**

## 设计原则

- **史料诚实**：原始文献的说法、历史解释、文学改编、作者想象分别标明；重大待核事实一票阻断。
- **人物完整**：伟业与代价共存；不为了同情写成免责，不为了攻击抹去人的复杂性。
- **反模板**：不强制“孤独天才/悲剧英雄/三到六场景”，让材料决定结构。
- **最小修改**：只审不改，授权后逐项修订；尊重冻结段落与意象。
- **单图优先但视觉多样**：一个清晰意象胜过七张不断转场的相似海报；同系列不必同画风。
- **观察不冒充因果**：四篇互动截图只能用于有限的趋势观察，不等于平台传播学实验。
- **数据本地处理**：自检脚本无第三方依赖、不联网、不需 API Key；没有自动发布或后台采集。

## 验证

```bash
python humanities-essay/scripts/quick_validate.py humanities-essay
python -m unittest discover -s tests -v
python humanities-essay/scripts/check_length.py --help
python humanities-essay/scripts/metrics_report.py --help
```

这套 CI 只证明目录与辅助脚本符合预期，不代表文章质量或史实正确性。更详细的四级门禁见 [验证策略](docs/VALIDATION.md)。

## 仓库结构

| 路径 | 说明 |
|---|---|
| `humanities-essay/SKILL.md` | 唯一 Skill 入口 |
| `humanities-essay/references/` | 六类叙事、事实协议、编辑检查、单图视觉与指标定义 |
| `humanities-essay/assets/` | 创作简报、证据台账、指标 CSV 模板 |
| `humanities-essay/evals/` | 跨题材验收用例与回归场景（需独立模型执行） |
| `humanities-essay/scripts/` | 完全本地、标准库的验证工具 |
| `tests/` | 确定性脚本单元测试 |
| `examples/` | 自编虚构测试案例（不含未获授权的第三方内容） |
| `docs/` | 架构、验证与后续计划 |

## 文档

| 主题 | 链接 |
|---|---|
| Skill 安装与调用 | [humanities-essay/README.md](humanities-essay/README.md) |
| 五篇案例的方法提炼 | [five-case-study.md](humanities-essay/references/five-case-study.md) |
| 单图封面视觉编辑 | [visual-editorial.md](humanities-essay/references/visual-editorial.md) |
| 数据复盘协议 | [measurement.md](humanities-essay/references/measurement.md) |
| 系统架构 | [ARCHITECTURE.md](docs/ARCHITECTURE.md) |
| 质量与 CI 门禁 | [VALIDATION.md](docs/VALIDATION.md) |
| 更新记录与计划 | [CHANGELOG.md](CHANGELOG.md) · [ROADMAP.md](docs/ROADMAP.md) |

## 发布到 GitHub

新建空白开源仓库与上传步骤见 [PUBLISH.md](PUBLISH.md)。现有工具不会自动创建仓库或修改其他仓库。

## 贡献

欢迎提交史料核验反例、跨题材评测、不同构图的视觉规范与错误修正。请先阅读 [CONTRIBUTING.md](CONTRIBUTING.md)；安全问题参见 [SECURITY.md](SECURITY.md)。

## 许可证

本仓库的原创 Skill 指令、脚本和文档以 [Apache License 2.0](LICENSE) 发布，参见 [NOTICE](NOTICE)。本许可证**不替其他作者的文章、插画、音乐或平台数据授权**。具体引用须遵循各自来源的授权与法律限制。
