"""DLC 輔助工具共用模組：找到 domain-memory Plugin，補上固定參數後呼叫 registry_tools.py。

直接執行時就是 dm.ps1／dm.sh 背後的命令前綴：

    py -3.13 -X utf8 tools/dmlib.py <plugin 指令> [參數...] [--save 檔案]

- 在 Repo 根目錄執行；自動補 `--registry-root domain-memory` 與 `--repo-root .`（若該指令接受且你沒給）。
- `--save 檔案`：把 JSON 輸出以 UTF-8 存檔（PowerShell 5.1 的 `>` 會存成 UTF-16，之後的工具讀不到）。
- Plugin 位置依序：`--plugin <路徑>`、環境變數 DOMAIN_MEMORY_PLUGIN、tools/ 旁的 vendor/domain-memory/。
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REGISTRY = "domain-memory"
ASSETS = ["contexts", "vocabulary", "aggregates", "rules", "contracts", "interactions", "decisions",
          "events", "capabilities", "value-objects", "dependency-policies"]
_VENDOR = [HERE.parent / "vendor" / name for name in ("domain-memory", "domain-memory-0.61.0")]
DEFAULT_PLUGIN_DIRS = [*_VENDOR, *(p / "domain-memory" for p in _VENDOR), HERE.parent / "plugin" / "domain-memory"]

# 依 Plugin 0.61.0 的 cli_parser.py 整理（只讀，不 import Plugin）；scripts/check_dlc_plugin_compat.py 逐一比對。
REGISTRY_REQUIRED = {
    "migrate-registry", "validate", "export", "coverage", "lookup", "resolve-terms", "get-context", "get-record",
    "analyze-boundary", "upsert-candidate", "retract-candidate", "apply-approved-updates",
    "demote-local-reviews", "probe", "verify-evidence", "migrate-evidence", "recover-registry-update",
    "confirm-sources", "refresh-sources", "refine-sources", "amend-policy", "verify-git-governance",
    "install-git-hitl-hook", "governance-readiness", "verify-audit", "submit-proposal", "verify-proposal",
    "attest-signed-commit", "boundary-impact", "promote-candidate", "recite", "record-test-result",
    "relocate-evidence", "harvest-candidates",
}
# 可選 --registry-root：只有 domain-memory/ 已存在時才補。
REGISTRY_OPTIONAL = {"readiness", "cite", "finalize-proposal", "validate-change-package", "init-change-package",
                     "change-coupling", "redraft-proposal", "supersede-proposal"}
REPO_ROOT = {
    "validate", "readiness", "upsert-candidate", "retract-candidate", "apply-approved-updates",
    "demote-local-reviews", "discover-sources", "verify-sources", "probe", "verify-evidence",
    "migrate-evidence", "init-domain-memory", "confirm-sources", "refresh-sources", "refine-sources",
    "init-signing-key", "scan-secrets", "verify-git-governance", "install-git-hitl-hook",
    "governance-readiness", "submit-proposal", "verify-proposal", "finalize-proposal", "quality-gates",
    "counterfactual", "cite", "attest-signed-commit", "audit-attestations", "boundary-impact", "recite",
    "record-test-result", "recover-registry-update", "relocate-evidence", "validate-change-package",
    "export", "compare-registry", "change-coupling", "harvest-candidates", "coverage", "promote-candidate",
    "redraft-proposal", "supersede-proposal",
}


def plugin_root(flag: str | None = None) -> Path:
    for candidate in (flag, os.environ.get("DOMAIN_MEMORY_PLUGIN"), *DEFAULT_PLUGIN_DIRS):
        if candidate and (Path(candidate) / "scripts" / "registry_tools.py").is_file():
            return Path(candidate).resolve()
    raise SystemExit(
        "找不到 domain-memory Plugin。請把 vendor/domain-memory-0.61.0.zip 解壓到 vendor/domain-memory/，"
        "或設定環境變數 DOMAIN_MEMORY_PLUGIN=<Plugin 資料夾>，或加 --plugin <Plugin 資料夾>。"
    )


def expand(args: list[str], registry_exists: bool | None = None) -> list[str]:
    """補上指令需要但使用者沒給的固定參數。"""
    if not args:
        return args
    command, rest = args[0], list(args[1:])
    if registry_exists is None:
        registry_exists = Path(REGISTRY).is_dir()
    if "--registry-root" not in rest and (
        command in REGISTRY_REQUIRED or (command in REGISTRY_OPTIONAL and registry_exists)
    ):
        rest += ["--registry-root", REGISTRY]
    if "--repo-root" not in rest and command in REPO_ROOT:
        rest += ["--repo-root", "."]
    if command == "verify-sources":
        if "--source-map" not in rest:
            rest += ["--source-map", f"{REGISTRY}/source-map.json"]
        if "--policy" not in rest:
            rest += ["--policy", f"{REGISTRY}/domain-memory-policy.json"]
    if command == "init-signing-key":
        if "--key-file" in rest[:-1]:
            key = Path(rest[rest.index("--key-file") + 1])
            if key.resolve().is_relative_to(Path.cwd().resolve()):
                raise SystemExit(
                    f"--key-file {key} 在 Repo 內（scan-secrets 會掃到私鑰）。請放 Repo 外，例如 " + (
                        'PowerShell "$env:USERPROFILE\\.dlc-keys\\<代號>\\signing-key"（PowerShell 不展開 %USERPROFILE%）。'
                        if os.name == "nt" else '"$HOME/.dlc-keys/<代號>/signing-key"。')
                )
        elif "--key-file" not in rest and "--principal" in rest[:-1]:
            # Plugin 預設 ~/.domain-memory/signing-key：兩人共用電腦會互相沿用，改放 ~/.dlc-keys/<principal>/。
            principal = re.sub(r"[^\w.@-]", "_", rest[rest.index("--principal") + 1])
            rest += ["--key-file", str(key_dir() / principal / "signing-key")]
    return [command, *rest]


def key_dir() -> Path:
    """DLC 簽章金鑰的預設資料夾：家目錄下的 .dlc-keys（Repo 外，不會被 scan-secrets 掃到）。"""
    return Path.home() / ".dlc-keys"


def env() -> dict[str, str]:
    return {**os.environ, "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"}


def command_line(args: list[str], plugin: str | None = None) -> list[str]:
    script = plugin_root(plugin) / "scripts" / "registry_tools.py"
    return [sys.executable, "-X", "utf8", str(script), *expand(args)]


def run(args: list[str], plugin: str | None = None, check: bool = True) -> subprocess.CompletedProcess:
    """呼叫 Plugin，回傳 CompletedProcess（stdout/stderr 為 UTF-8 文字）。"""
    done = subprocess.run(command_line(args, plugin), capture_output=True, text=True,
                          encoding="utf-8", errors="replace", env=env())
    if check and done.returncode != 0:
        raise SystemExit(f"Plugin 指令失敗（exit {done.returncode}）：{args[0]}\n{done.stdout}{done.stderr}")
    return done


def run_json(args: list[str], plugin: str | None = None):
    return json.loads(run(args, plugin).stdout)


def registry_documents(root: str | Path = REGISTRY, plugin: str | None = None) -> dict:
    """唯讀：Registry 每種資產的文件 {資產: 文件}，經 Plugin `export`。工具要讀 Registry 內容一律經這裡，
    不直接開檔（0.29 起是 OKF 版面 registry/<資產>/<id>.md，版面是 Plugin 的事）。寫入一律經 Plugin 指令。
    """
    return run_json(["export", "--registry-root", str(root)], plugin)


def read_json(path: str | Path):
    """讀 JSON，容忍 UTF-8 BOM 與 PowerShell 5.1 `>` 產生的 UTF-16。"""
    try:
        raw = Path(path).read_bytes()
        encoding = "utf-16" if raw[:2] in (b"\xff\xfe", b"\xfe\xff") else "utf-8-sig"
        return json.loads(raw.decode(encoding))
    except OSError as error:
        raise SystemExit(f"讀不到 {path}：{error}") from None
    except ValueError as error:
        raise SystemExit(f"{path} 不是有效的 JSON（{error}）。若是 --save 的輸出，先看它的內容是否為 ERROR 訊息。") from None


def write_json(path: str | Path, data) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def split_plugin_flag(argv: list[str]) -> tuple[str | None, list[str]]:
    if "--plugin" in argv:
        index = argv.index("--plugin")
        return argv[index + 1], argv[:index] + argv[index + 2:]
    return None, argv


def main(argv: list[str]) -> int:
    plugin, argv = split_plugin_flag(argv)
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    save = None
    if "--save" in argv:
        index = argv.index("--save")
        save, argv = argv[index + 1], argv[:index] + argv[index + 2:]
    cmd = command_line(argv, plugin)
    print("[dm] registry_tools.py " + " ".join(cmd[4:]), file=sys.stderr)
    if save is None:
        return subprocess.run(cmd, env=env()).returncode
    done = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", env=env())
    Path(save).parent.mkdir(parents=True, exist_ok=True)
    Path(save).write_text(done.stdout, encoding="utf-8")
    sys.stderr.write(done.stderr if done.returncode == 0 else done.stdout + done.stderr)  # Plugin 的 ERROR 印在 stdout
    print(f"[dm] 輸出已存到 {save}（exit {done.returncode}）", file=sys.stderr)
    return done.returncode


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
