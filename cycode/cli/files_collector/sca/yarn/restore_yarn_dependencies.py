import os
from typing import List

import click

from cycode.cli.files_collector.sca.base_restore_dependencies import BaseRestoreDependencies
from cycode.cli.models import Document

YARN_PROJECT_FILE_EXTENSIONS = ['.json']
YARN_LOCK_FILE_NAME = 'yarn.lock'
YARN_MANIFEST_FILE_NAME = 'package.json'
YARN_PACKAGES_FOLDER_NAME = 'node_modules'


class RestoreYarnDependencies(BaseRestoreDependencies):
    def __init__(self, context: click.Context, is_git_diff: bool, command_timeout: int) -> None:
        super().__init__(context, is_git_diff, command_timeout)

    def is_project(self, document: Document) -> bool:
        return any(document.path.endswith(ext) for ext in YARN_PROJECT_FILE_EXTENSIONS)

    def get_command(self, manifest_file_path: str) -> List[str]:
        return [
            'yarn',
            '--cwd',
            self.prepare_manifest_file_path_for_command(manifest_file_path),
            '&&',
            'rm',
            '-rf',
            self.prepare_packages_folder_path_for_command(manifest_file_path),
        ]

    def get_lock_file_name(self) -> str:
        return YARN_LOCK_FILE_NAME

    def verify_restore_file_already_exist(self, restore_file_path: str) -> bool:
        return os.path.isfile(restore_file_path)

    def prepare_manifest_file_path_for_command(self, manifest_file_path: str) -> str:
        return manifest_file_path.replace(os.sep + YARN_MANIFEST_FILE_NAME, '')

    def prepare_packages_folder_path_for_command(self, manifest_file_path: str) -> str:
        return manifest_file_path.replace(os.sep + YARN_MANIFEST_FILE_NAME, os.sep + YARN_PACKAGES_FOLDER_NAME)
