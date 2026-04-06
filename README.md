# 并行审查系统 (Parallel Review System)

为 Claude Code 提供的三阶段并行审查协议，在执行任务时自动启动多个并行 Agent 进行方案评审、资料查询和完成检查。

## 工作流程

```
用户提出任务
    │
    ▼
┌─────────────────────────────────┐
│  阶段一：方案评审                 │
│  3个并行Agent审查工作方案          │
│  ├ Agent1: 完整性审查            │
│  ├ Agent2: 风险评估              │
│  └ Agent3: 优化建议              │
└──────────┬──────────────────────┘
           │ 用户确认后执行
           ▼
┌─────────────────────────────────┐
│  阶段二：并行资料查询（按需触发）   │
│  多源信息时并行Agent分别查询       │
└──────────┬──────────────────────┘
           │
           ▼
┌─────────────────────────────────┐
│  阶段三：完成检查                 │
│  3个并行Agent验证结果             │
│  ├ Agent1: 需求符合度            │
│  ├ Agent2: 代码/文档质量          │
│  └ Agent3: 方案建议回顾           │
└─────────────────────────────────┘
```

## 安装

### 1. 复制 CLAUDE.md 到全局配置

```bash
cp CLAUDE.md ~/.claude/CLAUDE.md
```

> 如果已有 `~/.claude/CLAUDE.md`，请将内容合并进去。

### 2. 复制 Hook 脚本

```bash
cp hooks/parallel_review_reminder.py <你的hooks目录>/
```

### 3. 配置 settings.json

编辑 `~/.claude/settings.json`，在 `hooks.SessionStart` 数组中添加：

```json
{
  "type": "command",
  "command": "python <你的hooks目录>/parallel_review_reminder.py",
  "timeout": 3
}
```

参考 `config/settings.template.json` 中的模板。

### 4. 重启 Claude Code

新会话将自动加载并行审查协议。

## 文件说明

```
├── CLAUDE.md                              # 全局指令（三阶段协议完整规则）
├── hooks/
│   └── parallel_review_reminder.py         # SessionStart Hook（会话提醒）
├── config/
│   └── settings.template.json              # settings.json 配置模板
└── README.md                               # 本文件
```

## 豁免规则

以下任务自动跳过审查，不会影响执行速度：

- 单行代码修改 / typo 修复
- 纯信息查询（读文件、搜索）
- 用户明确要求跳过评审

## 自定义

你可以编辑 `CLAUDE.md` 来调整：

- 并行 Agent 的数量（默认 3 个）
- 每个审查维度的具体内容
- 豁免条件
- 评审报告的输出格式
