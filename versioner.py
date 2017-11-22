import os


class Versioner(object):
    """Helper class allowing easy version number changes when building apps."""

    def _search_file(self, proj_root,  path):
        """Attempts to read file given in path. If not possible will search for
         it recursively.

        Args:
            path (str):  Path to the file with the version number.
            proj_root (str): Project's root directory.

        Returns:
            ver_num (str) : Version number.

        """
        if os.path.isfile(path):
            self._read_file(path)

        # top_dir = "."
        #
        # for root, dirs, files in os.walk(top_dir):
        #     for file in files:
        #         if file == path:
        #             pass

    def _read_file(self, path):
        """Reads first line of the file containing version number.

        Args:
            path (str): Path to the file with the version number.

        Returns:
            ver_num (str):  Version number.

        """

        with open(path) as file:
            ver_num = file.read()

        return ver_num
