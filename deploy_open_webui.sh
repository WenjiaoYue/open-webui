#!/bin/bash

# Step 1: Switch to superuser
sudo su

# Step 2: Activate the conda environment
conda activate open-webui

# Step 3: Set proxy environment variables
export https_proxy=http://child-ir.intel.com:912
export http_proxy=http://child-ir.intel.com:912

# Step 4: List installed packages and filter for open-webui
pip list | grep open-webui

# Step 5: Uninstall open-webui (will prompt for confirmation)
pip uninstall -y open-webui

# Step 6: Build the package
python -m build

# Step 7: Install the new version of open-webui
pip install dist/open_webui-0.5.12-py3-none-any.whl

# Step 8: Clear the proxy settings
export http_proxy=""
export https_proxy=""

# Step 9: Run the open-webui server
open-webui serve --port 80
