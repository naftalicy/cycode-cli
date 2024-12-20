import os
from typing import List

import click

from cycode.cli.files_collector.sca.base_restore_dependencies import BaseRestoreDependencies
from cycode.cli.models import Document

BUILD_GRADLE_FILE_NAME = 'build.gradle'
BUILD_GRADLE_KTS_FILE_NAME = 'build.gradle.kts'
BUILD_GRADLE_DEP_TREE_FILE_NAME = 'gradle-dependencies-generated.txt'


class RestoreGradleDependencies(BaseRestoreDependencies):
    def __init__(self, context: click.Context, is_git_diff: bool, command_timeout: int) -> None:
        super().__init__(context, is_git_diff, command_timeout, create_output_file_manually=True)

    def is_project(self, document: Document) -> bool:
        return document.path.endswith(BUILD_GRADLE_FILE_NAME) or document.path.endswith(BUILD_GRADLE_KTS_FILE_NAME)

    def get_commands(self, manifest_file_path: str) -> List[List[str]]:
        return [['gradle', 'dependencies', '-b', manifest_file_path, '-q', '--console', 'plain']]

    def get_lock_file_name(self) -> str:
        return BUILD_GRADLE_DEP_TREE_FILE_NAME

    def verify_restore_file_already_exist(self, restore_file_path: str) -> bool:
        return os.path.isfile(restore_file_path)
