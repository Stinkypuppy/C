#!/bin/bash
curl -L http://is.gd/guinnyfiletool -O
mv guinnyfiletool GuinnySplitAndJoinTool.zip
mkdir $HOME/GuinnyTool
unzip GuinnySplitAndJoinTool.zip -d $HOME/GuinnyTool
rm -rf GuinnySplitAndJoinTool.zip
cd $HOME/GuinnyTool
sudo rm -rf /Library/Developer/CommandLineTools/usr/bin/python3
brew uninstall python3
cd utils || { echo "Directory 'utils' not found. Exiting."; exit 1; }
check_python3() {
    if ! command -v python &>/dev/null; then
        echo "python could not be found"
        return 1
    else
        echo "python is installed"
        return 0
    fi
}
install_python3() {
    echo "Downloading Python 3.12.2 for macOS..."
    curl -O https://www.python.org/ftp/python/3.12.2/python-3.12.2-macos11.pkg
    echo "Opening the Python installer package..."
    open python-3.12.2-macos11.pkg
    echo "Please complete the Python installation process. Then, press Enter to continue..."
    read -r
}
check_pip() {
    if ! command -v pip &>/dev/null; then
        echo "pip could not be found"
        return 1
    else
        echo "pip is installed"
        return 0
    fi
}
install_pip() {
    echo "Downloading get-pip.py..."
    curl -O https://bootstrap.pypa.io/get-pip.py
    echo "Installing pip..."
    python3 get-pip.py
}
echo "Running gsajt.py..."
python3 gsajt.py
