# Project Handoff Memory

给 AI 装上「长期项目记忆」的一个 Agent Skill。让 Codex、Claude Code 等 AI 助手把项目记忆**沉淀成项目里的文件**,而不是锁在某一次聊天里——这样换窗口、换模型、换工具、隔了一个月回来,下一个 AI 都能接着干。

> A reusable agent skill that keeps long-term project memory in **files inside the project**, not only in chat — so the next agent (Codex, Claude Code, or any other) can pick the work up across sessions, models, and tools.

---

## 解决什么问题

用 AI 做一个稍微长一点的项目,几乎都会遇到:

- 聊天窗口一长,AI 开始「变笨」,旧方案、废弃判断混进当前任务;
- 一换新对话 / 新模型 / 新工具,AI 又什么都不记得,你得从头解释一遍;
- 关键决定、数据口径、下一步计划散落在聊天记录里,过一阵子自己也找不回。

这个 skill 的思路很简单:**把该长期记住的东西,从聊天里搬到项目文件里**,并且让每个项目都用**同一套标准结构**,任何 AI 打开都认得。

## 它会产出什么(标准结构)

在项目根目录维护一套统一的记忆文件,任何 agent 打开即用:

```
项目根/
├── AGENTS.md          # 唯一入口 / 启动协议:读取顺序、口径铁律、避坑、冲突仲裁规则
├── CLAUDE.md          # 只有一行 @AGENTS.md —— 让 Claude Code 自动加载同一份记忆
├── README.md          # 业务背景:项目是什么、为什么、边界
├── handoff.md         # 现状快照:一句话状态 / 目标 / 产物 / 最近决策 / 下一步(一屏)
└── docs/
    ├── progress-log.md      # 编年史,按日期追加,不改历史
    ├── open-questions.md    # 悬而未决、影响结论的问题
    ├── 口径与数据源.md       # (分析类)数据源 / 口径 / 校验钩子
    └── evidence.md          # (数据报告)结论 → 证据映射,每个数字可溯源
```

核心设计取舍:

- **两个入口文件,一个源头**:`AGENTS.md` 写全部指令,`CLAUDE.md` 只写 `@AGENTS.md` 指过去。Claude Code 读 `CLAUDE.md`、其他 agent 读 `AGENTS.md`,自动同步,永远只维护一份,不会两份漂移。
- **骨架先行,按需生长**:第一遍只建最小骨架,其余文件等真有内容了再拆出来,绝不预建空壳。
- **冲突仲裁有优先级**:同一事实打架时,信任顺序 `脚本实时计算 > 口径/reference > handoff > README/背景 > progress-log/归档`。
- **沉淀要留反例**:每条沉淀 = 决定 + 为什么 + **被否决的方案** + 怎么复验。
- **状态标签**:每个记忆文件头部标 `Status: current | reference | append-only | archived`,历史不会被误当成现状。

## 安装

### Claude Code

把本仓库放进你的 skills 目录(或软链接过去):

```bash
git clone https://github.com/yangliangyl/project-handoff-memory.git \
  ~/.claude/skills/project-handoff-memory
```

之后在会话里说「沉淀」「交接」「更新项目记忆」「收尾」,或切换会话 / agent 时,Claude Code 会自动触发这个 skill。

### Codex / 其他 agent

同样把目录放到你的 skills / 自定义指令位置即可;`agents/openai.yaml` 提供了 Codex 侧的展示名与默认提示词。

## 使用

进入你的项目,直接对 AI 说:

> 帮我更新这个项目的 handoff,让下一个 agent 能接着做。

或在任何一次实质性改动(代码、SQL、分析、内容、结构、关键决策)之后触发。它会:

1. 定位项目根目录;
2. **扫描整个项目树**(不只看聊天上下文),跳过 `.git`、`node_modules`、大文件等噪声;
3. 读已有的交接信号,按项目类型(analysis / product / content / skill / knowledge)决定该强调什么;
4. 建立或更新标准结构,迁移遗留命名的交接文件(不并行保留);
5. 跑校验脚本,红项修完再收工。

## 结构校验脚本

`scripts/check_handoff.py` 用来机器校验项目沉淀结构是否合规(标准文件齐全、`CLAUDE.md` 是纯指针、无遗留文件、Status 头、跨项目指针不断链、handoff 新鲜度等):

```bash
# 校验指定项目
python3 scripts/check_handoff.py /path/to/your/project

# 不带参数:默认扫描当前目录下所有含 AGENTS.md 的项目
python3 scripts/check_handoff.py

# 想固定扫描自己的几个项目根目录,设环境变量(多个用 : 或 ; 隔开):
export HANDOFF_SCAN_ROOTS="$HOME/Desktop/projA:$HOME/work"
python3 scripts/check_handoff.py
```

红项(缺标准文件、`CLAUDE.md` 不是纯指针、遗留文件残留等)会让脚本 `exit 1`;黄项只提醒。

## 仓库结构

```
project-handoff-memory/
├── SKILL.md                       # skill 主定义(触发条件 + 工作流)
├── agents/openai.yaml             # Codex 侧展示名与默认提示词
├── references/                    # 工作流引用的规则细则
│   ├── file-contract.md           #   每个文件的职责、更新模式、生长触发表
│   ├── project-types.md           #   五类项目各自强调什么、该建哪些文件
│   ├── handoff-template.md        #   handoff.md 模板
│   ├── tree-scan.md               #   项目树扫描规则
│   └── update-checklist.md        #   收尾前自查清单
├── scripts/check_handoff.py       # 结构合规机器校验
├── README.md
├── LICENSE
└── .gitignore
```

## License

[MIT](LICENSE) © 2026 阿亮 (liangyls)
