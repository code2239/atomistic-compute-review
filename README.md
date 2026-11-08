# atomistic-compute-review

**MLIP 项目审议与准备 skill**：从已有结构、标签数据、模型或结果进入，组织数据、训练/微调、部署、模拟和分析的衔接，准备可审查的材料并持续维护项目知识。

技能入口：[SKILL.md](skills/atomistic-compute-review/SKILL.md)。调用名称为 `$atomistic-compute-review`；完整技能目录是 `skills/atomistic-compute-review/`，其中的参考、模板与辅助程序需一并保留。

## 能力与范围

- 按已有模型、有标签数据或仅结构选择起点，跳过不必要的训练和其他阶段。
- 审查标签口径、覆盖、数据划分泄漏、模型适用证据和训练/验证设计。
- 检查模型导出与部署、结构/元素映射、LAMMPS 输入及模拟到分析的输出约定；DFT/VASP 用于参考标注、验证或必要补充。
- 有界分析已有结果，分别记录方案准备、文件准备、科学证据和执行授权。
- 在同一主方案中更新相关结论，维护阶段交接、来源和变更，避免每轮生成重复文档。

具体体系、框架、版本、模型、参数、平台和验收标准由实际项目确定。本仓库不内置覆盖所有框架的训练或执行适配器，也不提供模型权重或软件安装包。

## 本地准备与超算环境保存

所有由 Codex 编写或修订的方案、输入、脚本、notebook、分析代码和环境档案均在本地生成。

超算采用“本地准备 → 用户传输/运行 → 用户回传 → 本地分析/回写”的方式协作。获得实际环境信息后，在计算项目本地持久保存 `docs/platforms/<平台标识>.md`；已有同用途档案原位复用。索引和主方案引用该档案，后续先读后问，环境变化时原位更新。

档案记录超算目录、软件/解释器/环境位置、启用与启动方式、调度资源、本地与超算路径映射，以及来源、确认日期和未知项。超算路径仅作目标环境文本，不在本机创建或探测。

详见 [平台适配规则](skills/atomistic-compute-review/references/platform.md) 与 [环境档案模板](skills/atomistic-compute-review/assets/hpc-environment.md)。实际项目的超算环境档案由项目维护，不写入通用技能目录。

## 计算启动边界

默认推进资料查证、静态检查、材料准备和已有结果的有界后处理。新的推理、训练/微调、模拟及参考计算需要用户有效执行授权；单帧、单点、`run 0` 和 smoke test 也属于计算执行。

超算阶段由用户传输、启动和回传；skill 不以远程连接为前提。文件齐全或静态检查通过不等于目标环境运行验证或科学可靠性证明。该 skill 提供行为约定，不是系统级执行拦截器。

## 仓库结构

```text
skills/atomistic-compute-review/
  SKILL.md
  agents/openai.yaml
  references/                  按需专业说明和项目维护规则
  assets/hpc-environment.md    超算环境档案选填模板
  scripts/init_workspace.py   本地工作区初始化工具
tests/test_init_workspace.py  初始化工具的文件行为测试
DESIGN-AND-SURVEY.md           设计、调查依据与验证记录
```

## 检查与验证

初始化工具只依赖 Python 标准库。运行仓库中的文件行为测试：

```bash
python3 -m unittest discover -s tests -v
```

现有 8 项测试检查初始化、重复调用、只读检查、文件冲突及符号链接处理。skill 格式、文档引用及隔离项目中的实际行为也已检查，记录见 [设计稿第 11 节](DESIGN-AND-SURVEY.md#11-设计验收与后续边界)。历史隔离样例不是技能运行依赖，未作为可重复执行的材料计算基准包含在仓库中。

本仓库未验证具体 MLIP/VASP/LAMMPS 软件、模型或真实超算任务的科学与运行正确性，使用时须结合项目证据核查。
