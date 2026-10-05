# AGENTS.md — <项目名>

<一句话定位；做什么、不做什么。git 情况。>

## 先读
1. `docs/project/mainline.md` — 方向与常驻约束
2. `docs/project/kanban.md` — 进度
3. `docs/tasks/current.md` — 当前唯一工作单元
4. `docs/README.md` — 文档索引

## 权限与标记
- Boss 决定：产品方向、范围、数据/隐私、发布与删除。Agent 只提案。
- 后果性陈述标注：**[已验证事实]** · **[Agent 提案]** · **[Boss 决定]**。

## 默认工作方式
- 默认 `manager-harness` 担任 Manager，只做 `current.md` 里的工作单元。
- 状态同步用 `project-sync`。

## 何时让 Boss 介入（必须暂停）
- 工作单元结束
- 改变定位 / 范围
- 发布、推送、改 remote
- 删除内容或历史；大规模重构
- 连续两次方向判断不确定，或结论与 mainline 冲突

## 汇报格式
1. 现在能做什么（链接） 2. 怎么验证 3. 还缺什么 4. 唯一下一步（等批准）

## 文档规则
- product + develop 各一份（< 60 行），细节只登记链接；所有文档进 `docs/README.md`。
- 进度只写 kanban，方向只写 mainline，当前任务只写 current。

## Git 与工程规范
- 分支：`main` 保持可用；功能用短分支 `feat/<x>`、`fix/<x>`，新长期分支需 Boss 批准。
- 提交：[Conventional Commits](https://www.conventionalcommits.org/zh-hans/)（`feat:` `fix:` `docs:` `refactor:` `test:` `chore:`），一次提交一件事。
- 版本：SemVer；发布打 tag `vX.Y.Z`，同时更新 `CHANGELOG.md`（只写 Boss 验收过的变化）。
- 提交前：跑测试 / `check_docs.py`；不提交凭据、数据、大文件、生成产物。
- 推送、PR、发布、改 remote 需 Boss 批准。

## 关键命令
- <安装 / 运行 / 测试>

## 红线与安全
- <凭据文件>：禁止读取、打印、提交。
