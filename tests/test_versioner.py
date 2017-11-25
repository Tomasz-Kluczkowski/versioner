import pytest
import os

from unittest import mock
from versioner import Versioner

root = "../"
test_dir_root = "version_dir"
test_dir_1 = os.path.join(root, test_dir_root, "test_1")
test_dir_2 = os.path.join(test_dir_1, "test_2")


@pytest.fixture()
def versioner():
    return Versioner()


@pytest.fixture()
def mock_input_yes():
    mock_input = mock.Mock()
    mock_input.return_value = "y"

    return mock_input


@pytest.fixture()
def mock_input_no():
    mock_input = mock.Mock()
    mock_input.return_value = "n"

    return mock_input


@pytest.fixture()
def mock_open_fix(monkeypatch):
    """Helper for avoiding the real open()."""
    _mock_open = mock.mock_open(read_data="1.02")
    monkeypatch.setattr("builtins.open", _mock_open)


# Tests without user interaction below
def test_get_version_with_no_parameters(monkeypatch, mock_open_fix, versioner):
    """Tests if correct version is returned when no parameters are
        passed and default values are used."""

    versioner._found = True
    assert versioner.get_version(prompt=False) == "1.02"


def test_get_version_with_valid_file_path(versioner):
    """Tests if version is returned when full path to version file is
    given as the file parameter with the default root."""

    assert versioner.get_version(file="/home/tomasz_kluczkowski/Dev/versioner/"
                                      "version_dir/test_1/test_2/"
                                      "test_version.txt",
                                 prompt=False) == "1.02"


# def test_get_version_with_incorrect_root(versioner):
#     """Tests if exception is raised when root is not a valid directory."""
#
#     with pytest.raises(ValueError,
#                        message="Project's root must be a valid directory."):
#         versioner.get_version(root="/home/yolo420", prompt=False)
#
#
# def test_get_version_with_absolute_path_to_root(versioner):
#     """Tests if version number is returned when absolute path to
#     projects root is given and default VERSION.txt is used a a file."""
#
#     assert versioner.get_version(
#         root="/home/tomasz_kluczkowski/Dev/versioner", prompt=False) == "1.02"
#
#
# def test_get_version_with_absolute_path_to_root_and_non_default_file(versioner):
#     """Tests if version number is returned when absolute path to
#     projects root and a non default version file is given ."""
#
#     assert versioner.get_version(
#         root="/home/tomasz_kluczkowski/Dev/versioner/version_dir/test_1",
#         file="non_def_version.txt", prompt=False) == "2.01"
#
#
# def test_get_version_searching_for_version_file(versioner):
#     """Tests searching for the file containing version number starting
#     from the root."""
#
#     assert versioner.get_version(root="/home/tomasz_kluczkowski/Dev/versioner",
#                                  file="test_version.txt",
#                                  prompt=False) == "1.00"
#
#
# def test_get_version_searching_for_invalid_version_file(versioner):
#     """Tests exception is raised when searching for invalid file containing
#     version number starting from the root."""
#
#     with pytest.raises(ValueError,
#                        message="Version file missing,"
#                                " please check parameters / folders."):
#         assert versioner.get_version(
#             root="/home/tomasz_kluczkowski/Dev/versioner",
#             file="blah_test_version.txt", prompt=False)
#
#
# # Test basic user interaction below
# def test_user_input_yes(monkeypatch, versioner, mock_input_yes):
#     """Tests user for response yes."""
#
#     monkeypatch.setattr("builtins.input", mock_input_yes)
#     assert versioner.user() is True
#
#
# def test_user_input_no(monkeypatch, versioner, mock_input_no):
#     """Tests user for response yes."""
#
#     monkeypatch.setattr("builtins.input", mock_input_no)
#     assert versioner.user() is False
#
#
# # Test getting version number with user interaction below
# def test_get_version_with_user_input_yes(monkeypatch, versioner,
#                                          mock_input_yes):
#     """Tests get_version with user response = "y"."""
#
#     monkeypatch.setattr("builtins.input", mock_input_yes)
#     assert versioner.get_version() == "1.02"
#     assert versioner.get_version(file="/home/tomasz_kluczkowski/Dev/versioner/"
#                                       "version_dir/test_1/test_2/"
#                                       "test_version.txt") == "1.00"
#     assert versioner.get_version(
#         root="/home/tomasz_kluczkowski/Dev/versioner") == "1.02"
#     assert versioner.get_version(root="/home/tomasz_kluczkowski/Dev/versioner",
#                                  file="test_version.txt") == "1.00"
#
#
# def test_get_version_user_abort(monkeypatch, versioner, mock_input_no):
#     """Tests if script exits when user does not accept version number
#     from the file found."""
#
#     monkeypatch.setattr("builtins.input", mock_input_no)
#     with pytest.raises(SystemExit) as my_exit:
#
#         versioner.get_version()
#         assert my_exit.type == SystemExit
#         assert my_exit.exception.args[0] == "Version number not accepted. User abort"


if __name__ == "__main__":
    pytest.main()
