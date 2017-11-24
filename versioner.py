import os
import sys
import platform


class Versioner(object):
    """Helper class allowing easy version number changes when building apps."""

    def __init__(self, root="", file=""):
        """Initialize object.

        Args:
            root (str): Project's root directory for the search (can be
                relative or absolute).
            file (str): File with the version number.
        """
        self.root = root
        self.file = file
        self._found = False
        """Status of the version file search."""
        self._true_path = ""
        """Confirmed path to the version file."""
        self._ver_num = None
        """Version number obtained from the version file."""

    def _search_file(self):
        """Attempts to find version file from path given in file or
        combination of root/file. If not possible will search for it
        recursively starting at the root.
        """
        # Sanity checks here.
        if not os.path.isdir(self.root):
            raise ValueError("Project's root must be a valid directory.")

        path = os.path.join(self.root, self.file)
        top_dir = self.root

        # Confirm if file is a valid path to the version file.
        if os.path.isfile(self.file):
            self._found = True
            self._true_path = self.file

        # Confirm if root/file is a valid path to the version file.
        elif os.path.isfile(path):
            self._found = True
            self._true_path = path

        # otherwise search for it
        else:
            for cur_root, dirs, files in os.walk(top_dir):
                for file in files:
                    if file == self.file:
                        self._found = True
                        self._true_path = os.path.join(cur_root, file)

        # if not found raise an exception
        if not self._found:
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

    def get_version(self, root="../", file="VERSION.txt", prompt=True):
        """Obtains version number from a file.

        Args:
            root (str): Project's root directory for the search (can be
                relative or absolute).
            file (str): File with the version number.
            prompt (bool): Check if user interaction should be enabled
                at initial stage of getting version number.

        Returns:
            ver_num (str): Version number.
        """
        self.root = root
        self.file = file

        self._search_file()
        self._ver_num = self._read_file(self._true_path)

        if prompt:
            if self.user():
                return self._ver_num
            else:
                pass
                sys.exit("Version number not accepted. User abort")

        return self._ver_num

    def user(self):
        """Allows interaction with the user.

        Returns:
            (bool):

        """
        if platform.system() == "Windows":
            command = "cls"
        else:
            command = "clear"
        while True:
            os.system(command)
            print("Path to your version file:\n{0}".format(self._true_path))
            print(
                "Version number in the file is: {0}".format(
                    self._ver_num))
            response = input(
                "Do you want to accept this version number? (y/n)").lower()
            if response not in ["y", "n"]:
                continue
            elif response.lower() == "y":
                return True
            else:
                return False

# Examples
# if __name__ == "__main__":
#     v = Versioner()
#     v.get_version(file="non_def_version.txt")
