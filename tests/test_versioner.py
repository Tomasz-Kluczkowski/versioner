import pytest

from versioner import Versioner


@pytest.fixture()
def versioner():

    return Versioner()


def test_get_version_with_no_parameters(versioner):
    """Tests if correct version is returned when no parameters are
        passed and default values are used."""

    assert versioner.get_version() == "1.02"


def test_get_version_with_incorrect_root(versioner):
    """Tests if exception is raised when root is not a valid directory."""

    with pytest.raises(ValueError,
                       message="Project's root must be a valid directory."):
        # noinspection SpellCheckingInspection
        versioner.get_version(root="/home/yolo420")


def test_get_version_with_absolute_path_to_root(versioner):
    """Tests if version number is returned when absolute path to
    projects root is given and default VERSION.txt is used a a file."""

    assert versioner.get_version(
        root="/home/tomasz_kluczkowski/Dev/versioner") == "1.02"


def test_get_version_searching_for_version_file(versioner):
    """Tests searching for the file containing version number starting
    from the root."""

    assert versioner.get_version(root="/home/tomasz_kluczkowski/Dev/versioner",
                                 file="test_version.txt") == "1.00"


def test_get_version_searching_for_invalid_version_file(versioner):
    """Tests exception is raised when searching for invalid file containing
    version number starting from the root."""

    with pytest.raises(ValueError,
                       message="Version file missing,"
                               " please check parameters / folders."):

        assert versioner.get_version(
            root="/home/tomasz_kluczkowski/Dev/versioner",
            file="blah_test_version.txt")


if __name__ == "__main__":
    pytest.main()
