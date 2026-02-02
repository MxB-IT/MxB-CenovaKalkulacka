import sys
import os

class ResourcePather:
    @staticmethod
    def resource_path(relative_path: str) -> str:
        """
        method used to get relative paths to resources, even after compiled for the end user
        :param relative_path: relative path from the script to the requested resource
        :return: real path to the resource
        """
        try:
            base_path = sys._MEIPASS
        except Exception:
            current_file_dir = os.path.dirname(os.path.abspath(__file__))

            base_path = os.path.dirname(current_file_dir)

        return os.path.join(base_path, relative_path)