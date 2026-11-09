# OpenViking Compile 产品介绍

[OpenViking Compile 介绍视频](./video.mp4)

Compile 可以把分散的项目资料整理成 Wiki 或报告。以 Wiki 为例，它按 Skill 定义的规则读取文档、会议记录和反馈，把同一主题的信息汇集到一页，并保留来源引用，方便读者核对原文。[Compile 介绍文档](https://docs.openviking.ai/zh/context-compilation/01-overview)

## 基本用法

要把自己的项目资料整理成 Wiki，先启用 Compile Runtime，将资料导入 OpenViking，并安装 LLM Wiki Skill。准备步骤见[上下文编译入门](https://docs.openviking.ai/zh/getting-started/13-compile)。

将下面的 `project-docs` 换成已导入的资料目录名，将 `project-wiki` 换成准备存放 Wiki 的新目录名。

```bash
ov compile --from viking://resources/project-docs \
  --to viking://resources/project-wiki \
  --skill viking://agent/skills/llm-wiki \
  --instruction "请按主题整理这些资料，生成中文 Wiki，用 index.md 链接各主题页面，并在正文中引用原始资料的 viking:// URI。"
```

用返回的任务 ID 查询进度，例如 `ov task status cmp_...`。状态变为 `completed` 后，打开 Wiki 首页即可按主题浏览。

```bash
ov read viking://resources/project-wiki/index.md
```
