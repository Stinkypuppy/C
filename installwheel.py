import os
import sys
import shutil
import zipfile
import glob

def extract_wheel_contents(wheel_file_path):
    temp_dir = 'wheel_extracted'
    os.makedirs(temp_dir, exist_ok=True)

    with zipfile.ZipFile(wheel_file_path, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)

    return temp_dir

def find_install_dir(extracted_dir):
    dist_info_dirs = glob.glob(os.path.join(extracted_dir, '*.dist-info'))
    if not dist_info_dirs:
        print("Error: Unable to find installation directory in the wheel file.")
        return None
    else:
        return dist_info_dirs[0]

def find_site_packages_dir():
    python_version = 'python' + '.'.join(map(str, sys.version_info[:2]))
    paths_to_check = [
        os.path.join('/'.join(sys.executable.split('/')[:-2]), 'lib', python_version, 'site-packages'),
        os.path.join(sys.prefix, 'lib', python_version, 'site-packages'),
        os.path.join(sys.prefix, 'lib', 'site-packages'),
    ]

    for path in paths_to_check:
        if os.path.exists(path):
            return path

    print("Error: Unable to locate the site-packages directory.")
    return None

def copy_files_to_site_packages(install_dir, site_packages_dir):
    for item in os.listdir(install_dir):
        source = os.path.join(install_dir, item)
        destination = os.path.join(site_packages_dir, item)
        if os.path.isdir(source):
            shutil.copytree(source, destination)
        else:
            shutil.copy(source, destination)

def cleanup(temp_dir):
    shutil.rmtree(temp_dir)

def install_wheel(wheel_file_path):
    extracted_dir = extract_wheel_contents(wheel_file_path)

    install_dir = find_install_dir(extracted_dir)
    if not install_dir:
        cleanup(extracted_dir)
        return

    site_packages_dir = find_site_packages_dir()
    if not site_packages_dir:
        cleanup(extracted_dir)
        return

    copy_files_to_site_packages(install_dir, site_packages_dir)

    print("Installation successful.")

    cleanup(extracted_dir)

if __name__ == "__main__":
    wheel_file_path = input("Enter the path to the wheel file: ")
    if not os.path.exists(wheel_file_path):
        print("Error: File not found.")
    elif not wheel_file_path.endswith('.whl'):
        print("Error: Not a valid wheel file.")
    else:
        install_wheel(wheel_file_path)
