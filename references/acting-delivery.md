# 表演与反应交付契约

适用：所有模型的编译输出，包括项目自写编译器及临时适配器。技能中的创作角色负责判断指令是否适用；交付检查只证明没有静默丢失，不能证明艺术质量或实际表演效果。

## 编译前先审适用性

1. 每个执行分画必须有稳定ID和在画演员表。区分在画、同场画外声音和仅被提及的人。
2. 对performance与reaction分别作决定：`included`或`not_applicable`，都填写reason。适用时提供实际text和actors；不适用时不附演员指令。
3. 环境空镜不要求画外旁白者出镜或张口。手部插入镜不强加脸部反应。隔门镜不消费门外人物的可见反应。
4. 分画拆分后重新判断，不能将拆分前的复合动作/全场人物任务直接复制到每个分画。动作复述应基于当前分画，旧文本保留为来源。
5. 对白拍明确当前可见表演及适用反应，不用同一句“保持构图”代替全部表演。允许设计上没有听者反打，禁止为了填字段发明动作或改对白。

## 机器可读接口

`model_compilation.acting_source_ids`枚举本次编译的全部执行分画ID；每个`shots[]`提供`visual_units`和同序`acting_beats`。每个beat至少包含：

```json
{
  "id": "V001",
  "visible_cast": ["listener"],
  "performance": {
    "status": "included",
    "text": "Stay inside the locked room.",
    "actors": ["listener"],
    "reason": "The speaker is outside; only the listener is visible."
  },
  "reaction": {
    "status": "not_applicable",
    "reason": "No separate visible reaction is specified for this beat."
  }
}
```

项目独立状态可将上述编译对象放在根层。统一渲染使用`scripts/acting_contract.py`中的`render_beat`或`render_beats`，同一份审阅后的内容进入导演稿与最终提示词。保留原始字段、适用决定及改写原因供追溯。

## 强制交付检查

```bash
python scripts/acting_contract.py --input project_state.json
```

检查源ID覆盖、顺序、每个字段的处置理由、在画演员范围，并逐条验证实际指令进入compiled_prompt。仅增加“表演/反应”标题不能通过；字段、正文或整拍静默丢失都会失败。不适用必须说明理由。

`prompt_assembler.assemble`在发现编译结果时执行此检查；`export_html.export_compilation`在导出前强制检查。旧编译产物若没有契约字段须先迁移，不应伪造reason或审核通过状态。

CI运行`python -m unittest discover -s tests -v`，覆盖正文被删除但标题保留、任一字段缺失、画外演员泄入、空镜合理不适用、原因缺失及源分画遗漏/重复。检查失败时修源数据或编译器，不能删除失败项来制造通过。
