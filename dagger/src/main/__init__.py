"""A generated module for Dagger functions.

This module has been generated via dagger init and serves as a reference to
basic module structure as you get started with Dagger.

Two functions have been pre-created. You can modify, delete, or add to them,
as needed. They demonstrate usage of arguments and return types using simple
echo and grep commands. The functions can be called from the dagger CLI or
from one of the SDKs.

The first line in this comment block is a short description line and the
rest is a long description with more detail on the module's purpose or usage,
if appropriate. All modules should have a short description.
"""

# NOTE: it's recommended to move your code into other files in this package
# and keep __init__.py for imports only, according to Python's convention.
# The only requirement is that Dagger needs to be able to import a package
# called "main" (i.e., src/main/).
#
# For example, to import from src/main/main.py:
# >>> from .main import Dagger as Dagger

import dagger
from dagger import dag, function, object_type

UV_VERSION: str = "0.4.16"


@object_type
class DaggerTest:
    """dagger test."""

    _uv_cache: dagger.CacheVolume = dag.cache_volume("uv_cache")

    @function
    async def lint(self, directory: dagger.Directory) -> None:
        """Linting python code.

        Args:
            directory: directory.

        """
        await self._create_package_container(directory).with_exec(
            ["uv", "run", "ruff", "check", "."]
        )

    @function
    async def format(self, directory: dagger.Directory) -> None:
        """Format python code.

        Args:
            directory: directory.

        """
        await self._create_package_container(directory).with_exec(
            ["uv", "run", "ruff", "format", "--diff", "."]
        )

    @function
    async def typo_check(self, directory: dagger.Directory) -> None:
        """Format python code.

        Args:
            directory: directory.

        """
        await self._create_package_container(directory).with_exec(
            ["uv", "run", "typos", "."]
        )

    @function
    async def test(self, directory: dagger.Directory) -> None:
        """Test python code.

        Args:
            directory: directory.

        """
        await self._create_package_container(directory).with_exec(
            ["uv", "run", "pytest", "."]
        )

    def _create_base_container(self) -> dagger.Container:
        uv_container = dag.container().from_(f"ghcr.io/astral-sh/uv:{UV_VERSION}")
        return (
            dag.container()
            .from_("ubuntu:22.04")
            .with_file("/usr/local/bin/uv", uv_container.file("/uv"))
            .with_mounted_cache("/root/.cache/uv", self._uv_cache)
            .with_env_variable("UV_LINK_MODE", "copy")
        )

    def _create_package_container(
        self,
        directory: dagger.Directory,
    ) -> dagger.Container:
        return (
            self._create_base_container()
            .with_mounted_directory("/project", directory)
            .with_workdir("/project")
            .with_exec(["uv", "sync"])
        )
