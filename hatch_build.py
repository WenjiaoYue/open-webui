# noqa: INP001
import os
import shutil
import subprocess
from sys import stderr

from hatchling.builders.hooks.plugin.interface import BuildHookInterface


class CustomBuildHook(BuildHookInterface):
    def initialize(self, version, build_data):
        super().initialize(version, build_data)
        stderr.write(">>> Building DCAI小智 frontend\n")
        npm = shutil.which("npm")
        if npm is None:
            raise RuntimeError(
                "NodeJS `npm` is required for building DCAI小智 but it was not found"
            )
        stderr.write("### Installing onnxruntime-node\n")
        subprocess.run([npm, "install", "onnxruntime-node", "--onnxruntime-node-install-cuda=skip"], check=True)  # noqa: S603
        
        ort_version = "1.20.1"
        ort_url = f"https://github.com/microsoft/onnxruntime/releases/download/v{ort_version}/onnxruntime-linux-x64-gpu-{ort_version}.tgz"
        
        stderr.write(f"### Downloading onnxruntime binaries from {ort_url}\n")
        subprocess.run(["curl", "-L", ort_url, "-o", f"onnxruntime-linux-x64-gpu-{ort_version}.tgz"], check=True)  # noqa: S603
        
        stderr.write("### npm install\n")
        subprocess.run([npm, "install"], check=True)  # noqa: S603

        stderr.write("\n### npm run build\n")
        os.environ["APP_BUILD_HASH"] = version
        subprocess.run([npm, "run", "build"], check=True)  # noqa: S603