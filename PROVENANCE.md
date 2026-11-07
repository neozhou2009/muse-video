# 来源与仓库范围

- 原项目：https://github.com/LuoJiangYong/muse-video-skill
- 原许可证：MIT；LICENSE 中原版权声明完整保留。
- 当前安装技能版本：SKILL.md 中的 0.36.7。
- 本仓库从用户现有安装目录导入，不含原 Git 历史；无法凭此快照断言与上游某一提交逐字一致。
- 初始仓库调整：增加本来源说明，在中英文 README 中注明来源，并将本仓库的 Git 克隆命令指向 neozhou2009/muse-video。
- 本仓库不包含《百年遗忘》的剧本、导演稿、生成提示词、角色资产或生成记录；技能自带的示例与案例资料保留。
- 当前技能正式模型编译适配为 Seedance 2.0；项目里临时编写的 Seedance 2.5 编译脚本未混入技能源码。

## 本地检查

```bash
python -m compileall -q scripts
python scripts/build_index.py --check --deps
```

脚本依赖按原工作流安装 PyYAML、jsonschema；导出 Excel 时另需 openpyxl。示例 schema 检查按 .github/workflows/quality-gate.yml 执行。
