"""Dump extdep descriptors, their state files, and run verify() per dependency."""
import json
import logging
import os
from pathlib import Path

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s %(message)s")
for noisy in ("urllib3", "git"):
    logging.getLogger(noisy).setLevel(logging.INFO)

import importlib.util
from edk2toolext.environment import self_describing_environment as sde
from edk2toolext.environment import environment_descriptor_files as edf

spec = importlib.util.spec_from_file_location(
    "devicebuild", "Platforms/OnePlus/instantnoodlepPkg/DeviceBuild.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

sm = mod.SettingsManager()
root = sm.GetWorkspaceRoot()
scopes = sm.GetActiveScopes()
print("workspace:", os.path.abspath(root))
print("scopes:", scopes)

build_env, shell_env = sde.BootstrapEnvironment(root, scopes, None)
for d in build_env.extdeps:
    print("== extdep dict ==")
    print(json.dumps(d, indent=1, default=str))
    dep = edf.ExtDepFactory(d)
    try:
        r = dep.verify(shell_env)
        print("== verify() returned:", r)
    except Exception as e:
        print("== verify() raised:", repr(e))
    contents = Path(d.get("descriptor_file", "x/x")).parent / (d.get("name", "?") + "_extdep")
    state = contents / "extdep_state.yaml"
    print("   computed state file:", state, "exists:", state.is_file())
    if state.is_file():
        print("   content:", state.read_text())
    print()
