#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_handoff.py — 项目沉淀结构机器校验（project-handoff-memory skill 配套）。

用法：
  python3 check_handoff.py <项目路径> [<项目路径>...]   校验指定项目
  python3 check_handoff.py                              扫描当前目录下所有含 AGENTS.md 的项目
                                                        （或设环境变量 HANDOFF_SCAN_ROOTS 指定根目录，
                                                         多个用系统分隔符 : 或 ; 隔开）

规则（红=违规致 exit 1，黄=提醒不拦截）：
  红  标准文件齐：AGENTS.md / CLAUDE.md / handoff.md(根) / docs/progress-log.md
  红  CLAUDE.md 只能是一行 @AGENTS.md（允许空行）
  红  遗留文件残留：docs/handoff.md、*交接*.md、*沉淀*.md
  红  标准 md 头部（前 5 行）缺 Status:
  黄  非标准 docs/*.md 缺 Status:
  黄  文档仍引用 docs/handoff.md（progress-log 历史条目除外）
  黄  handoff.md 比 docs/progress-log.md 旧超过 1 天（现状快照没跟上）
  黄  跨项目相对路径指针（../xx/…​.md）目标不存在
  黄  README.md 缺失（content-gated，允许暂缺）
"""
import os
import re
import sys

def default_scan_roots():
    """默认扫描根目录。

    - 若设置环境变量 HANDOFF_SCAN_ROOTS，按系统分隔符（: 或 ;）拆分使用；
      例如：export HANDOFF_SCAN_ROOTS="$HOME/Desktop/projA:$HOME/work"
    - 否则默认扫描当前目录 "."，对所有人通用（每个人的项目目录都不同）。
    """
    env = os.environ.get("HANDOFF_SCAN_ROOTS", "").strip()
    if env:
        return [os.path.expanduser(p) for p in env.split(os.pathsep) if p.strip()]
    return ["."]


NOISE_DIRS = {".git", "node_modules", "venv", ".venv", "__pycache__",
              "dist", "build", "cache", ".pytest_cache", ".mypy_cache"}
STANDARD_MD = {"AGENTS.md", "README.md", "handoff.md",
               "progress-log.md", "口径与数据源.md", "evidence.md", "open-questions.md"}
FRESHNESS_TOLERANCE = 86400  # handoff 落后 progress-log 超过 1 天才提醒


def head_has_status(path):
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            return any("Status:" in next(f, "") for _ in range(5))
    except OSError:
        return False


def read_text(path):
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            return f.read()
    except OSError:
        return ""


def project_md_files(root):
    out = []
    for base in (root, os.path.join(root, "docs")):
        if os.path.isdir(base):
            out += [os.path.join(base, n) for n in sorted(os.listdir(base))
                    if n.endswith(".md")]
    return out


def check_project(root):
    reds, yellows = [], []
    docs = os.path.join(root, "docs")

    # 标准文件齐
    for rel in ("AGENTS.md", "CLAUDE.md", "handoff.md", "docs/progress-log.md"):
        if not os.path.isfile(os.path.join(root, rel)):
            reds.append(f"缺标准文件：{rel}")
    if not os.path.isfile(os.path.join(root, "README.md")):
        yellows.append("README.md 缺失（content-gated，背景稳定后应补）")

    # CLAUDE.md 只能是一行指针
    claude = os.path.join(root, "CLAUDE.md")
    if os.path.isfile(claude):
        lines = [l.strip() for l in read_text(claude).splitlines() if l.strip()]
        if lines != ["@AGENTS.md"]:
            reds.append("CLAUDE.md 不是一行 @AGENTS.md（内容版属遗留，应迁移进标准文件）")

    # 遗留文件残留
    if os.path.isfile(os.path.join(docs, "handoff.md")):
        reds.append("遗留文件：docs/handoff.md（handoff.md 应在项目根目录）")
    for base in (root, docs):
        if not os.path.isdir(base):
            continue
        for n in sorted(os.listdir(base)):
            if n.endswith(".md") and ("交接" in n or "沉淀" in n):
                reds.append(f"遗留文件：{os.path.relpath(os.path.join(base, n), root)}（应迁移进标准结构后删除）")

    # Status 头
    for path in project_md_files(root):
        name = os.path.basename(path)
        if name == "CLAUDE.md":
            continue
        if not head_has_status(path):
            rel = os.path.relpath(path, root)
            if name in STANDARD_MD:
                reds.append(f"缺 Status: 头：{rel}")
            else:
                yellows.append(f"缺 Status: 头（非标准文件）：{rel}")

    # 旧路径引用 + 跨项目指针
    for path in project_md_files(root):
        rel = os.path.relpath(path, root)
        text = read_text(path)
        if "docs/handoff" in text and os.path.basename(path) != "progress-log.md":
            yellows.append(f"仍引用 docs/handoff.md：{rel}")
        for ref in set(re.findall(r"\.\./[^)\s`'\"，。；]+\.md", text)):
            target = os.path.normpath(os.path.join(os.path.dirname(path), ref))
            if not os.path.isfile(target):
                yellows.append(f"跨项目指针断链：{rel} → {ref}")

    # handoff 新鲜度
    hand, plog = os.path.join(root, "handoff.md"), os.path.join(root, "docs/progress-log.md")
    if os.path.isfile(hand) and os.path.isfile(plog):
        lag = os.path.getmtime(plog) - os.path.getmtime(hand)
        if lag > FRESHNESS_TOLERANCE:
            yellows.append(f"handoff.md 比 progress-log 旧 {lag / 86400:.1f} 天（现状快照可能没跟上）")

    return reds, yellows


def find_projects(scan_roots):
    found = []
    for base in scan_roots:
        if not os.path.isdir(base):
            continue
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames[:] = [d for d in dirnames if d not in NOISE_DIRS and not d.startswith(".")]
            if "AGENTS.md" in filenames:
                found.append(dirpath)
    return sorted(set(found))


def main():
    args = sys.argv[1:]
    projects = [os.path.abspath(a) for a in args] if args else find_projects(default_scan_roots())
    if not projects:
        print("未找到任何含 AGENTS.md 的项目目录")
        sys.exit(1)

    total_red = total_yellow = 0
    for root in projects:
        if not os.path.isdir(root):
            print(f"\n❌ {root}\n   路径不存在")
            total_red += 1
            continue
        reds, yellows = check_project(root)
        total_red += len(reds)
        total_yellow += len(yellows)
        mark = "❌" if reds else ("⚠️ " if yellows else "✅")
        print(f"\n{mark} {root}")
        for r in reds:
            print(f"   ❌ {r}")
        for y in yellows:
            print(f"   ⚠️  {y}")
        if not reds and not yellows:
            print("   全绿")

    print(f"\n==== 汇总：{len(projects)} 个项目，红 {total_red} 项，黄 {total_yellow} 项 ====")
    sys.exit(1 if total_red else 0)


if __name__ == "__main__":
    main()
