# OpenViking Compile 介绍片

上下文编译（Compile）能力的中文产品介绍视频，HyperFrames（HTML/CSS → 视频）工程。1920×1080、30 fps，约 67.9 秒，带旁白、配乐和音效。

- 版本：V4（2026-11-09），需求方 富嘉杰，review 刘智恒。
- 成片：https://blog.openviking.ai/video/openviking-compile.mp4 （不入库）
- 旁白：豆包 seed-tts-2.0，音色 `zh_male_liufei_uranus_bigtts`（刘飞），台词见 `voiceover/lines.json`，生成脚本 `tools/doubao_tts.py`（凭证从 env 读取）。
- 配乐：ElevenLabs Music 生成的器乐垫乐 `project/assets/music/bed.mp3`；音效来自 HyperFrames 自带 Pixabay 音效（可商用免署名）。
- Logo：OpenViking 官方 `docs/images/brand-lockup-light.svg`，未改动。强调色为橙红落日渐变，不用 indigo。
- 界面参照设计稿重绘，示例目录和文件名为虚构的“星海科技 / 产品知识 Wiki”。

## 镜头

| 时间 | 内容 |
|---|---|
| 0–6s | 零散资料聚合成结构化 Wiki，标题 OpenViking Compile |
| 6–16s | 控制台：选 Wiki、写需求、勾选产品文档 / 会议纪要 / 客服工单 |
| 16–31s | VikingBot 对话：查看资料、调用 openviking_tree，表单选择编译 Skill、目标目录、更新策略，确认后开始编译；Wiki 写回上下文树 |
| 27–43s | 冲突检测与看板：冲突列表，展开“退款时效”冲突详情并填写修复方案解决 |
| 43–57s | 换 Skill 产出日报、团队经验；定时更新、增量编译、版本管理 |
| 57–64s | 结尾卡 |

## 重建

需要 Node.js、FFmpeg。先下载 Noto Sans SC 到 `project/assets/fonts/NotoSansSC.ttf`（Google Fonts，OFL）。

```sh
cd products/openviking/compile-introduction/project
npx --yes hyperframes@0.9.8 render --crf 20
```

## English version (`project-en/`)

Separate HyperFrames project; the Chinese build in `project/` is untouched.

- Final cut: https://blog.openviking.ai/video/openviking-compile-en.mp4 (not checked in), about 73.1 s.
- Narration: Doubao seed-tts-2.0 with voice `en_male_tim_uranus_bigtts`. Generated one paragraph at a time at the default rate (no speech_rate speed-up), then sliced into lines at word timestamps (`tools/doubao_tts_en.py`, `tools/slice_en.py`) and normalized to about −16 LUFS. Script: `voiceover-en/lines.json`.
- On-screen text was translated with `tools/en_map.py` + `tools/en_apply.py`. The English narration runs longer, so each composition adds `EN_HOLDS` and `tools/en_timing.py` shifts the root timing to match.
