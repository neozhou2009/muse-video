# 产出验证清单 — Verification Checklist

> **用途**：Phase 7 组装完成后、交付用户前的最终验证。Director 逐项检查。
> **执行时机**：`prompt_assembler.py` 运行后，导出前。

---

## 必须通过（CRITICAL — 任一失败则不可交付）

- [ ] Project State JSON 完整——所有 phase 的 `_meta.director_approved` = true
- [ ] 每个角色产出有 `_meta` 追溯（role + revision）
- [ ] 无缺失字段——所有必填字段已填写，无 `TODO` 占位符
- [ ] 案例引用已加载（如果用户提到了风格参考）

## 应该通过（SUGGESTION — 影响质量但不阻塞交付）

- [ ] Director 全程参与审核，无跳过阶段
- [ ] 色调全局一致性——所有场景主色色相偏差 ≤ 30°
- [ ] 分镜 panel 数量覆盖所有关键场景
- [ ] 角色对白风格与 character_bible[].voice 一致（如有角色）
- [ ] 字幕条目 panel_id 皆对应已存在 panel（无悬挂；Phase 7 选项 B 重排后复核）
- [ ] source=dialogue 的字幕文本与 scenes[].dialogue 一致（或显式标注改写）
- [ ] 双语条目的语言模式与文本匹配（language_mode 与 text_zh / text_en 双填一致）

## 按需检查（NITPICK）

- [ ] 导出格式已按用户需求生成（HTML / Excel）
- [ ] Creative Pack 文件路径可访问


## 编译产物表演交付门禁

- 每个源执行分画都有 performance/reaction 的适用决定及理由。
- 源拍、在画演员与最终指令一一可追溯，指令实际进入 compiled_prompt。
- 编译预览导出前 `scripts/acting_contract.py --input project_state.json` 通过；不得只核字段存在。
- 空镜、旁白、手部插入镜及拆分分画不套用旧整场反应。
