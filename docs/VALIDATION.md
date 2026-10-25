# Validation / 验证策略

## Gate 0：发布包与依赖

- `python humanities-essay/scripts/quick_validate.py humanities-essay` 检查目录、SKILL 元数据、UTF-8、相对链接、占位符与版本。
- `python -m unittest discover -s tests -v` 检查工具行为与负例。
- `python scripts/check_length.py --help` 和 `python scripts/metrics_report.py --help` 是可执行辅助工具，不依赖第三方包。

## Gate 1：事实阻断（人工/模型）

参照 `humanities-essay/references/evidence-protocol.md`，对引用、年代、人物身份、因果链逐项列举证据。重大 U/D 争议没有解决时，状态只能是 **HOLD**。

## Gate 2：文学编辑（人工/模型）

根据语料选择至少一篇情节型、一篇诗词细读、一篇版本比较和一个“只审不改”案例；参考 `humanities-essay/evals/`。计分用于找问题，**不是质量或流量保证**。

## Gate 3：发布格式

`python scripts/check_length.py <txt> --min 2500 --max 3000`：同时报告码点和 UTF-16 计数；保守校验按 UTF-16。抖音平台实际编辑器仍须再核对。音乐、插画版权独立检查。

## 验收状态

`STATIC_PASS` 表示安装包结构和脚本测试通过；`FACT_REVIEWED` 表示史料有逐项审查；`MODEL_EVAL_PASS` 表示指定模型、固定测试集和记录通过；`PUBLISHED` 需要真实发布回执。不得把一种状态当作另一种。
