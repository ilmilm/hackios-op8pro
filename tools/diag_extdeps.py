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

build_env, shell_env = sde.BootstrapEnvironment(root, scopes, None)
for d in build_env.extdeps:
    print("== extdep:", d.name)
    print("   version:", d.version)
    print("   descriptor_location:", d.descriptor_location)
    print("   contents_dir:", d.contents_dir)
    print("   state_file_path:", d.state_file_path)
    print("   published_path:", d.published_path)
    try:
        r = d.verify(shell_env)
    except Exception as e:
        r = f"EXCEPTION {e}"
    print("   verify:", r)
