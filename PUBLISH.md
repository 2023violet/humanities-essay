# Publishing to GitHub / 首次上传指南

> 本文记录待执行的人工作业步骤；交付压缩包本身**不等于已经建立 GitHub 仓库**。

建议仓库：`2023violet/humanities-essay`，可见性：**Public**，默认分支：`main`，许可证：Apache-2.0（已随文件打包）。

## 使用 GitHub CLI

1. 进入本仓库包的根目录（含 README.md / humanities-essay/）。
2. 检查 `git status` 和本地内容，仅上传已经审核允许公开的文件。
3. 执行以下命令：

```bash
git init -b main
git add .
git commit -m "Initial release: humanities-essay"
gh auth login                  # 若尚未授权
gh repo create 2023violet/humanities-essay --public --source . --remote origin --push
```

注意：请使用**空白仓库**；不要在网站提前初始化 README/License，以免首次 push 出现不同历史。不要使用 `--force`。

## 浏览器方式

打开 https://github.com/new ，Owner 选择 2023violet，Repository name 填 `humanities-essay`，设为 Public，**不要勾选**初始化 README、.gitignore 或许可证（文件已经提供）。创建后按 GitHub 页面给出的“push an existing repository”指令上传。以上操作需要仓库创建权限。

## 验收

- 根目录有中英文 README、LICENSE、NOTICE、CONTRIBUTING、.github/workflows/validate.yml。
- `humanities-essay/SKILL.md` 的 name=humanities-essay, metadata.version=3.1.0。
- GitHub Actions 运行 `Validate Skill` 成功，再将其称为“远端 CI 通过”。
- 在真实目标模型上运行跨题材 eval 之前，不要在发布说明里写“生成质量已验证”。

> v3.2 及后续维护：优先在单独分支准备改动，通过 PR 和 CI 验证再合并；此初次创建说明不用于覆盖现有 main。
