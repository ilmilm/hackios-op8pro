"""Dump every external dependency the active scopes see: exact paths, versions,
verify() results -- so the CI state can be seeded to satisfy them."""
import importlib.util
from pathlib import Path

from edk2toolext.environment import self_describing_environment as sde

spec = importlib.util.spec_from_file_location(
    "devicebuild", "Platforms/OnePlus/instantnoodlepPkg/DeviceBuild.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

sm = mod.SettingsManager()
root = sm.GetWorkspaceRoot()
scopes = sm.GetActiveScopes()
print("workspace:", os.path.abspath(root) if (os := __import__("os")) else root)
print("scopes:", scopes)

import json
build_env, shell_env = sde.BootstrapEnvironment(root, scopes, None)
for d in build_env.extdeps:
    print("== extdep dict ==")
    print(json.dumps(d, indent=1, default=str))
