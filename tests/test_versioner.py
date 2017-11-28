import pytest

from unittest import mock
from versioner import Versioner


@pytest.fixture()
def versioner():
    return Versioner()


@pytest.fixture()
def mock_input_yes(monkeypatch):
    """Simulates user input character y."""
    mock_input = mock.Mock()
    mock_input.return_value = "y"
    monkeypatch.setattr("builtins.input", mock_input)


@pytest.fixture()
def mock_input_no(monkeypatch):
    """Simulates user input character n."""
    mock_input_n = mock.Mock()
    mock_input_n.return_value = "n"
    monkeypatch.setattr("builtins.input", mock_input_n)


@pytest.fixture()
def mock_open_fix(monkeypatch):
    """Helper for avoiding the real open()."""
    mock_open = mock.mock_open(read_data="1.02")
    monkeypatch.setattr("builtins.open", mock_open)


@pytest.fixture()
def mock_is_dir_true(monkeypatch):
    """Fake directory exists."""
    mock_is_dir = mock.Mock()
    mock_is_dir.return_value = True
    monkeypatch.setattr("versioner.os.path.isdir", mock_is_dir)


@pytest.fixture()
def mock_is_dir_false(monkeypatch):
    """Fake directory does not exist."""
    mock_is_dir = mock.Mock()
    mock_is_dir.return_value = False
    monkeypatch.setattr("versioner.os.path.isdir", mock_is_dir)


@pytest.fixture()
def mock_is_file_true(monkeypatch):
    """Confirm file exists."""
    mock_is_file = mock.Mock()
    mock_is_file.return_value = True
    monkeypatch.setattr("versioner.os.path.isfile", mock_is_file)


@pytest.fixture()
def mock_is_file_false(monkeypatch):
    """Confirm file does not exist."""
    mock_is_file = mock.Mock()
    mock_is_file.return_value = False
    monkeypatch.setattr("versioner.os.path.isfile", mock_is_file)


@pytest.fixture()
def mock_is_path_true(monkeypatch):
    """Confirm joined paths root/file exist."""
    mock_is_file = mock.Mock()
    mock_is_file.side_effect = [False, True]
    monkeypatch.setattr("versioner.os.path.isfile", mock_is_file)


@pytest.fixture()
def mock_os_walk(monkeypatch):
    """Return a valid result from a file search."""
    _mock_os_walk = mock.Mock()
    _mock_os_walk.return_value = [
        ("/home/tomasz_kluczkowski/Dev/versioner/", [],
         ["test_version.txt"]), ]
    monkeypatch.setattr("versioner.os.walk", _mock_os_walk)


# Tests without user interaction below.
def test_get_version_with_incorrect_root(versioner):
    """Tests if exception is raised when root is not a valid directory."""

    with pytest.raises(NotADirectoryError) as info:
        versioner.get_version(root="../yolo420", prompt=False)
    assert str(info.value) == "Project's root must be a valid directory."


def test_get_version_with_no_parameters(mock_open_fix, mock_is_dir_true,
                                        mock_is_file_true, versioner):
    """Tests if correct version is returned when no parameters are
        passed and default values are used."""

    assert versioner.get_version(prompt=False) == "1.02"


def test_get_version_with_valid_file_path(mock_open_fix, mock_is_dir_true,
                                          mock_is_file_true, versioner):
    """Tests if version is returned when full path to version file is
    given as the file parameter with the default root."""

    assert versioner.get_version(file="/home/tomasz_kluczkowski/Dev/versioner/"
                                      "version_dir/test_1/test_2/"
                                      "test_version.txt",
                                 prompt=False) == "1.02"


def test_get_version_with_absolute_path_to_root(mock_open_fix, mock_is_dir_true,
                                                mock_is_path_true, versioner):
    """Tests if version number is returned when absolute path to
    projects root is given and default VERSION.txt is used as a file."""

    assert versioner.get_version(
        root="/home/tomasz_kluczkowski/Dev/versioner", prompt=False) == "1.02"


def test_get_version_with_abs_path_to_root_and_non_def_file(mock_open_fix,
                                                            mock_is_dir_true,
                                                            mock_is_path_true,
                                                            versioner):
    """Tests if version number is returned when absolute path to
    projects root and a non default version file is given ."""

    assert versioner.get_version(
        root="/home/tomasz_kluczkowski/Dev/versioner/version_dir/test_1",
        file="non_def_version.txt", prompt=False) == "1.02"


def test_get_version_searching_for_version_file(mock_open_fix,
                                                mock_is_dir_true,
                                                mock_is_file_false,
                                                mock_os_walk,
                                                versioner):
    """Tests searching for the file containing version number starting
    from the root."""

    assert versioner.get_version(root="/home/tomasz_kluczkowski/Dev/versioner",
                                 file="test_version.txt",
                                 prompt=False) == "1.02"


def test_get_version_searching_for_invalid_version_file(mock_open_fix,
                                                        mock_is_dir_true,
                                                        mock_is_file_false,
                                                        mock_os_walk,
                                                        versioner):
    """Tests exception is raised when searching for invalid file containing
    version number starting from the root."""

    with pytest.raises(ValueError) as info:
        assert versioner.get_version(
            root="/home/tomasz_kluczkowski/Dev/versioner",
            file="blah_test_version.txt", prompt=False)
    assert str(
        info.value) == "Version file missing, please check parameters / folders."


# Test basic user interaction below.
def test_user_input_yes(versioner, mock_input_yes):
    """Tests user for response yes."""

    assert versioner.user() is True


def test_user_input_no(versioner, mock_input_no):
    """Tests user for response yes."""

    assert versioner.user() is False


# Test getting version number with user interaction below.
def test_get_version_with_user_input_yes(mock_open_fix,
                                         mock_is_dir_true, mock_is_file_true,
                                         mock_input_yes, versioner):
    """Tests get_version with user response = "y" Use default root and
    file."""

    assert versioner.get_version() == "1.02"


def test_get_version_user_abort(mock_open_fix,
                                mock_is_dir_true, mock_is_file_true,
                                mock_input_no, versioner):
    """Tests if script exits when user does not accept version number
    from the file found."""

    with pytest.raises(SystemExit) as info:
        versioner.get_version()

    assert str(info.value) == "Version number not accepted. User abort"


if __name__ == "__main__":
    pytest.main()
