# Validation / 验证策略

## Gate 0：发布包与依赖

- `python humanities-essay/scripts/quick_validate.py humanities-essay` 检查目录、SKILL 元数据、UTF-8、相对链接、占位符与版本。
- `python -m unittest discover -s tests -v` 检查工具行为与负例。
- `python scripts/check_length.py --help` 和 `python scripts/metrics_report.py --help` 是可执行辅助工具，不依赖第三方包。

## Gate 1：事实阻断（人工/模型）

参照 `humanities-essay/references/evidence-protocol.md`，对引用、年代、人物身份、因果链逐项列举证据。重大 U/D 争议没有解决时，状态只能是 **HOLD**。

## Gate 2：文学编辑（人工/模型）

根据语料选择至少一篇历史情节型、一篇诗词细读、一篇现代亲历随笔、一篇版本比较和一个“只审不改”案例；参考 `humanities-essay/evals/`。计分用于找问题，**不是质量或流量保证**。

三层语言结果独立报告：规范（错别字、句法、标点功能）、语流（前后连贯、重复解释）、文学表现（有必要的停顿与人物节奏）。不得依据句号数量认定质量变化。

## Gate 2B：作者确认与停笔

真实私人经历、心理表达、“我／我们”范围应由作者确认；锁定句子的字面一致性逐项核对；作者已认可、无硬伤时不为了审稿人另一种审美强制改写。

## Gate 3：发布格式

`python scripts/check_length.py <txt> --min 2500 --max 3000`：同时报告码点和 UTF-16 计数；保守校验按 UTF-16。抖音平台实际编辑器仍须再核对。音乐、插画版权独立检查。

## 验收状态

`STATIC_PASS` 表示安装包结构和脚本测试通过；`AUTHOR_READY` 表示可供作者最终确认；`AUTHOR_APPROVED` 表示作者已认可明确版本；`FACT_REVIEWED` 表示史料有逐项审查；`MODEL_EVAL_PASS` 表示指定模型、固定测试集和记录通过；`PUBLISHED` 需要真实发布回执。不得把一种状态当作另一种。
