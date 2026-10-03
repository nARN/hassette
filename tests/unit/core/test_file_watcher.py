"""Unit tests for FileWatcherService."""

from unittest import mock

from hassette.core import file_watcher
from tests.support import mock_hassette


async def test_disabled_watcher_stays_ready_until_shutdown() -> None:
    """A disabled watcher stays ready without watching files and shuts down cleanly."""
    hassette = mock_hassette.make_mock_hassette(sealed=False, file_watcher={"watch_files": False})
    watcher = file_watcher.FileWatcherService(hassette)

    with mock.patch.object(file_watcher, "awatch") as awatch:
        try:
            await watcher.initialize()
            await watcher.wait_ready(timeout=5)
            assert watcher.is_ready()
            assert watcher.is_running()
            awatch.assert_not_called()
        finally:
            report = await watcher.shutdown()

    assert report.is_restart_safe
    assert not watcher.is_running()
    assert not watcher.is_ready()
