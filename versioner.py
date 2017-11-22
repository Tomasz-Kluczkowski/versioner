import os


class Versioner(object):
    """Helper class allowing easy version number changes when building apps."""

    def _search_file(self, root, file):
        """Attempts to read file given in path. If not possible will search for
         it recursively.

        Args:
            root (str): Project's root directory.
            file (str): Path to the file with the version number.

        Returns:
            ver_num (str) : Version number.

        """
        # sanity checks here
        if not os.path.isdir(root):
            raise ValueError("Project's root must be a valid directory.")

        path = os.path.join(root, file)

        # if root/file is a valid version file, use it to get the ver_num.
        if os.path.isfile(path):
            ver_num = self._read_file(path)

            return ver_num

        # otherwise search for it
        top_dir = root

        for cur_root, dirs, _files in os.walk(top_dir):
            for _file in _files:
                if _file == file:
                    path = os.path.join(cur_root, _file)
                    ver_num = self._read_file(path)

                    return ver_num

        # if not found raise an exception

        raise ValueError(
            "Version file missing, please check parameters / folders.")

    @staticmethod
    def _read_file(path):
        """Reads first line of the file containing version number.

        Args:
            path (str): Path to the file with the version number.

        Returns:
            ver_num (str):  Version number.

        """

        with open(path) as file:
            ver_num = file.read()

        return ver_num

    def get_version(self, root="../", file="VERSION.txt"):
        """

        Args:
            root (str): Project's root directory for the search (can be
                relative or absolute).
            file (str): File with the version number.

        Returns:
            ver_num (str): Version number.
        """

        ver_num = self._search_file(root, file)

        return ver_num

