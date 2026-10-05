# Demo：release-check · 检查 phd-application-skills（2026-10-05）

- **Agent**：Codex（`codex exec -s read-only`），真实仓库，非测试 fixture；被检查仓库无改动
- **输入**：「按 release-check 检查这个仓库能不能发布，并告诉我对标头部仓库还差什么。只检查，不要修改任何文件。」
- **输出**：[codex-reply.md](codex-reply.md)，原样保存：3/8，不能发布；门槛表与脚本直接输出逐行一致
- **看点**：Codex 发现两个脚本其实有 `--selftest` 且通过，但脚本只认 `--selfcheck`；它按规则保留了脚本的判分，把分歧写在旁边
- **后续**：据此修了 `check_release.py`（两种写法都认），重跑结果：4/8
