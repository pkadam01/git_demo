import argparse
import os.path
import pytest
import shutil
import pathlib
import lattehhpel.about as about


TESTS_FOLDER = 'tests'
HTML_RESULTS_FILENAME = 'results.html'
QKIT_RESULTS_FOLDER = 'qkit_results'


def info_package():
    info = '\n'
    info += 'lattehhpel package\n'
    info += '====================\n'
    info += f'Name: {about.__package__}\n'
    info += f'Version: {about.__version__}\n'
    info += f'Author: {about.__author__}\n'
    info += f'Email: {about.__email__}\n'
    info += f'Description: {about.__description__}\n'
    info += f'URL: {about.__url__}\n'
    print(info)


def parse_parameters():
    parser = argparse.ArgumentParser(
        prog=about.__package__,
        description=about.__description__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument('--version', help='prints library information', action='store_true')
    parser.add_argument('--test', metavar='hhpelcfg.py', help='runs self test')

    args = parser.parse_args()

    if args.test:
        run_tests(os.path.abspath(args.test))
    elif args.version:
        info_package()
    else:
        parser.print_help()


def delete_folder(folder):
    if os.path.exists(folder):
        try:
            shutil.rmtree(folder)
            print(f'==> Deleted existing results folder {folder}\n')
        except OSError as error:
            print(f'Error deleting existing results folder {folder}')
            print(f'OS error: {error.strerror}')


def create_folder(folder_name):
    pathlib.Path(folder_name).mkdir(parents=True, exist_ok=True)


def copy_file(src_file_name, dest_path):
    dest_file_name = os.path.abspath(os.path.join(dest_path, 'config.py'))
    try:
        shutil.copy(src_file_name, dest_file_name)
        print('\n==> File {} copied to {}'.format(src_file_name, dest_file_name))
    except (IOError, OSError) as error:
        print('\nError copying file {} to {}, error {}'.format(src_file_name, dest_file_name, error))


def delete_file(file_name):
    try:
        os.remove(file_name)
    except OSError:
        pass


def wait_user():
    input('\n==> Programmable Electronic load must be powered on, and connected to your computer. '
          'Please ENTER to continue...')
    print()


def run_tests(user_config_file):
    # get current path for this package
    dir_path = os.path.dirname(__file__)
    config_file = os.path.abspath(os.path.join(dir_path, 'tests/config.py'))
    # delete tests/config.py if exists
    delete_file(config_file)
    # copy user config file to /tests/config.py folder inside the package
    tests_path = os.path.abspath(os.path.join(dir_path, 'tests'))
    copy_file(user_config_file, tests_path)
    # send notification to prepare setup
    wait_user()
    # build output folder path
    user_output_folder = os.path.abspath(f'./{QKIT_RESULTS_FOLDER}/{about.__package__}')
    # create output report folder
    delete_folder(user_output_folder)
    create_folder(user_output_folder)
    filepath_report = os.path.join(user_output_folder, HTML_RESULTS_FILENAME)
    ret_code = pytest.main([
        '-k qkit',
        '-s',
        '-x',
        '-W ignore::DeprecationWarning',
        f'--html={filepath_report}',
        os.path.join(dir_path, TESTS_FOLDER)
    ])

    if int(about.__version__.split('.')[0]) < 100:
        text = '\nWARNING: This library version is not safety qualified. For testing safety related ' \
               'functionality, please use a library with version 100.X.Y'
    elif ret_code == pytest.ExitCode.OK:
        text = f'\n==> All tests passed OK. Results stored in folder {user_output_folder}\n'
    elif ret_code == pytest.ExitCode.TESTS_FAILED:
        text = f'\n==> Some test failed, see results stored in folder {user_output_folder}.\n' \
               f'    This library can not be used for testing safety related functionality\n'
    else:
        text = f'\n==> Internal error {ret_code} when executing the tests\n'
    print(text)


if __name__ == '__main__':
    parse_parameters()
