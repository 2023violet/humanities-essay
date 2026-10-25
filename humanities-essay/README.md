# humanities-essay v3.1.0 · Skill 安装说明

仓库总览请参阅仓库根目录的 README.md / README.en.md；单独安装本 Skill 时不需要它们。

**目录本身就是 Skill**：`SKILL.md` 为入口，`references/` 按需读，`assets/` 提供模板，`scripts/` 提供可选的本地校验辅助工具。支持 Agent Skills 格式的客户端通常可以读取此目录，但唤起语法和路径可能不同。

## 安装

- Claude Code 项目目录：复制整个 `humanities-essay/` 到 `<project>/.claude/skills/humanities-essay/`。
- 个人目录（兼容客户端）：放入对应的 Skills 根目录，保持子目录名称和 `SKILL.md` 同级。
- Codex：复制到所用 Codex 客户端的 Skills 目录，保留可选的 `agents/openai.yaml`。实际安装命令以客户端说明为准。

## 示例

```text
使用 humanities-essay 写一篇约2800字符的人物志，指定单图＋配乐＋长简介，先核查重要原始文献。

使用 humanities-essay 只审不改这篇稿件，只指出事实风险、解释欲、首尾意象与可执行修改清单。

使用 humanities-essay 将已锁稿的文章做一张不限于水墨画风的封面，不修改正文、不自动拆轮播。
```

校验：`python scripts/quick_validate.py .`。工具可运行不代表模型写作质量已经通过实测。
