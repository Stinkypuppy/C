import os
import shutil
import zipfile

def find_installation_dir(extracted_dir):

    for root, dirs, files in os.walk(extracted_dir):
        for dir in dirs:
            if dir.endswith('.dist-info'):
                return os.path.join(root, dir)
    return None

def find_site_packages_dir():

    python_version = '.'.join(map(str, sys.version_info[:3]))
    site_packages_dir = os.path.join(sys.prefix, 'lib', 'python' + python_version, 'site-packages')
    if not os.path.exists(site_packages_dir):
        print("Error: Unable to locate the site-packages directory.")
        sys.exit(1)
    return site_packages_dir

def install_from_wheel(wheel_file_path):

    temp_dir = 'temp_wheel_extracted'
    os.makedirs(temp_dir, exist_ok=True)

    with zipfile.ZipFile(wheel_file_path, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)

    extracted_dir = os.path.join(temp_dir, os.listdir(temp_dir)[0])

    install_dir = find_installation_dir(extracted_dir)
    if not install_dir:
        print("Error: Unable to find installation directory in the wheel file.")
        shutil.rmtree(temp_dir)
        return

    site_packages_dir = find_site_packages_dir()

    for item in os.listdir(install_dir):
        source = os.path.join(install_dir, item)
        destination = os.path.join(site_packages_dir, item)
        if os.path.isdir(source):
            shutil.copytree(source, destination)
        else:
            shutil.copy(source, destination)

    print("Installation successful.")

    shutil.rmtree(temp_dir)

if __name__ == "__main__":
    wheel_file_path = input("Enter the path to the wheel file: ")
    if not os.path.exists(wheel_file_path):
        print("Error: File not found.")
    elif not wheel_file_path.endswith('.whl'):
        print("Error: Not a valid wheel file.")
    else:
        install_from_wheel(wheel_file_path)
