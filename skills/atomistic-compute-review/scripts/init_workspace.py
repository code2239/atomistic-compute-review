#!/usr/bin/env python3
"""Initialize an atomistic planning workspace without overwriting existing files."""

import argparse
import json
from pathlib import Path


CORE_DIRECTORIES = ("docs", "notebook", "analyse", "input", "output")
INDEX_CONTENT = """# 项目索引

当前方案：待登记。优先链接已有主方案；没有时，在形成实际方案内容后创建。

## 工作区入口

- [Notebook](../notebook/)：交互分析文件，生成不代表已执行。
- [分析程序](../analyse/)：分析、绘图与后处理代码。
- [输入](../input/)：体系、运行配置与输入草稿。
- [输出](../output/)：已有运行结果、日志和数值分析产物。

专题建立后在此登记路径和范围；详细结论在所属文档中持续维护。
准备状态与执行授权分别记录，目录和文件齐全不代表已获启动批准。
"""


def initialize_workspace(root: Path, check_only: bool = False) -> dict:
    root = root.expanduser().resolve()
    if not root.is_dir():
        raise ValueError(f"项目根目录必须已经存在且为目录：{root}")

    # Validate every destination before making changes. Existing symlinks may
    # represent another layout; do not silently follow or replace them.
    missing = []
    kept = []
    for name in CORE_DIRECTORIES:
        destination = root / name
        if destination.is_symlink():
            raise ValueError(f"目标是符号链接，请先核实项目布局：{destination}")
        if destination.exists():
            if not destination.is_dir():
                raise ValueError(f"目录名已被其他文件占用：{destination}")
            kept.append(name)
        else:
            missing.append(name)

    index = root / "docs" / "index.md"
    if index.is_symlink() or (index.exists() and not index.is_file()):
        raise ValueError(f"索引路径有冲突，不会覆盖：{index}")
    index_action = "kept" if index.exists() else "create"

    if not check_only:
        for name in missing:
            (root / name).mkdir(exist_ok=True)
        if index_action == "create":
            try:
                with index.open("x", encoding="utf-8") as handle:
                    handle.write(INDEX_CONTENT)
                index_action = "created"
            except FileExistsError:
                # Another writer may have created the index since inspection.
                # Exclusive creation keeps their content intact.
                index_action = "kept"

    return {
        "root": str(root),
        "check_only": check_only,
        "directories_to_create" if check_only else "directories_created": missing,
        "directories_kept": kept,
        "index": {"path": "docs/index.md", "action": index_action},
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path, help="已有计算项目的根目录")
    parser.add_argument("--check", action="store_true", help="只检查和报告，不写入")
    args = parser.parse_args()
    try:
        result = initialize_workspace(args.root, check_only=args.check)
    except (ValueError, OSError) as error:
        parser.exit(1, f"初始化未完成：{error}\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
