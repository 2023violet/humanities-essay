# Contributing to Humanities Essay

感谢参与。请先阅读 `humanities-essay/SKILL.md` 与 [验证策略](docs/VALIDATION.md)。

## 贡献原则

- 提交新的叙事方法时，说明适用场景、不适用边界和至少一个反例；不要只添加漂亮金句。
- 修改核查协议时，附可核对来源；无证据的历史细节不可作为测试正确答案。
- 用户批准“只审不改”时，不得改动正文。新 PR 不要顺便重构无关文件。
- 禁止提交未经授权的创作全文、私有抖音后台数据、受版权限制的插图、音乐、他人隐私。
- 公开贡献按 Apache-2.0 Section 5 的规则处理，保留必要署名与原授权说明。

## 提交前验证

```bash
python humanities-essay/scripts/quick_validate.py humanities-essay
python -m unittest discover -s tests -v
```

在 PR 中填写：变更目标、与 v3.0 行为差异、测试结果、人工文学/史实审稿状态（可写未运行）。不要把脚本 PASS 夸大为模型生成效果已通过。
