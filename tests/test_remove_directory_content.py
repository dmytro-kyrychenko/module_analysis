# Copyright The IETF Trust 2022, All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


__author__ = 'Slavomir Mazur'
__copyright__ = 'Copyright The IETF Trust 2022, All Rights Reserved'
__license__ = 'Apache License, Version 2.0'
__email__ = 'slavomir.mazur@pantheon.tech'

import os
import shutil
import subprocess
import unittest

import remove_directory_content as rdc


class TestRemoveDirectoryContent(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.resource_path = os.path.join(os.environ['VIRTUAL_ENV'], 'tests/resources/remove_directory_content')
        cls.script_path = os.path.join(os.environ['VIRTUAL_ENV'], 'bin/remove_directory_content.py')
        cls.subdir_path = os.path.join(cls.resource_path, 'subdir')
        cls.file_path = os.path.join(cls.resource_path, 'test_file.json')
        cls.symlink_src_file = os.path.join(cls.resource_path, 'test_symlink.json')
        cls.symlink_dst_file = os.path.join(cls.resource_path, 'test_symlink')

    def setUp(self):
        os.makedirs(self.resource_path, exist_ok=True)
        os.makedirs(self.subdir_path)
        open(self.file_path, 'w', encoding='utf-8').close()
        open(self.symlink_src_file, 'w', encoding='utf-8').close()
        os.symlink(self.symlink_src_file, self.symlink_dst_file)

    def tearDown(self) -> None:
        shutil.rmtree(self.resource_path, ignore_errors=True)

    def test_remove_directory_content(self):
        """Try to delete the content of a directory - it should be empty after script run."""
        self.assertNotEqual(os.listdir(self.resource_path), [])

        rdc.remove_directory_content(self.resource_path, 1)

        self.assertTrue(os.path.isdir(self.resource_path))
        self.assertEqual(os.listdir(self.resource_path), [])

    def test_rename_file_backup_from_console(self) -> None:
        """Run the script from the console by passing the arguments."""
        bash_command = f'python {self.script_path} --dir {self.resource_path} --debug 1'
        subprocess.run(bash_command, shell=True, capture_output=True, check=False).stdout.decode()

        self.assertTrue(os.path.isdir(self.resource_path))
        self.assertEqual(os.listdir(self.resource_path), [])


class TestRemoveDirectoryContentEmpty(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.resource_path = os.path.join(os.environ['VIRTUAL_ENV'], 'tests/resources/remove_directory_content')
        cls.non_existing_path = os.path.join(os.environ['VIRTUAL_ENV'], 'tests/resources/non_existing')

    def setUp(self):
        os.makedirs(self.resource_path, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.resource_path, ignore_errors=True)
        shutil.rmtree(self.non_existing_path, ignore_errors=True)

    def test_remove_directory_content_empty(self):
        """Try to delete the content of an empty directory."""
        rdc.remove_directory_content(self.resource_path)

        self.assertTrue(os.path.isdir(self.resource_path))
        self.assertEqual(os.listdir(self.resource_path), [])

    def test_remove_directory_content_non_existing_dir(self):
        """Try to delete the content of a directory that does not exist."""
        rdc.remove_directory_content(self.non_existing_path)

        self.assertTrue(os.path.isdir(self.non_existing_path))
        self.assertEqual(os.listdir(self.non_existing_path), [])

    def test_remove_directory_content_default(self):
        """Try to delete the content of a directory - using default value."""
        result = rdc.remove_directory_content('')

        self.assertEqual(result, None)


if __name__ == '__main__':
    unittest.main()
