from pathlib import Path
import pytest
from openbb_terminal import loggers
from openbb_terminal.core.log.generation.settings import (
    Settings,
    AppSettings,
    AWSSettings,
    LogSettings,
)

settings = Settings(
    app_settings=AppSettings(
        commit_hash="MOCK_COMMIT_HASH",
        name="MOCK_COMMIT_HASH",
        identifier="MOCK_COMMIT_HASH",
        session_id="MOCK_SESSION_ID",
    ),
    aws_settings=AWSSettings(
        aws_access_key_id="MOCK_AWS_ACCESS_KEY_ID",
        aws_secret_access_key="MOCK_AWS",  # pragma: allowlist secret
    ),
    log_settings=LogSettings(
        directory=Path("."),
        frequency="H",
        handler_list="file",
        rolling_clock=False,
        verbosity=20,
    ),
)


def throw_os_error():
    raise OSError("This is a test error")


def throw_os_error_30():
    e = OSError()
    e.errno = 30
    raise e


def throw_generic():
    raise Exception("This is a test error")


@pytest.mark.parametrize(
    "to_mock", [None, throw_os_error, throw_os_error_30, throw_generic]
)
def test_get_app_id(to_mock, mocker):
    if to_mock:
        mocker.patch("openbb_terminal.loggers.get_log_dir", to_mock)
        with pytest.raises(Exception):
            value = loggers.get_app_id()
    else:
        value = loggers.get_app_id()
        assert value


@pytest.mark.parametrize("git", [True, False])
def test_get_commit_hash(mocker, git):
    mocker.patch("openbb_terminal.loggers.WITH_GIT", git)
    value = loggers.get_commit_hash()
    assert value


def test_get_commit_hash_obff(mocker):
    mocker.patch("openbb_terminal.loggers.obbff")
    value = loggers.get_commit_hash()
    assert value


def test_add_stdout_handler():
    loggers.add_stdout_handler(settings)


def test_add_stderr_handler():
    loggers.add_stderr_handler(settings)


def test_add_nopp_handler():
    loggers.add_noop_handler(settings)


def test_add_file_handler():
    loggers.add_file_handler(settings)


def test_setup_handlers():
    loggers.setup_handlers(settings)


def test_setup_logging(mocker):
    mocker.patch("openbb_terminal.loggers.os")
    loggers.setup_logging(settings)
