from configparser import ConfigParser


class ConfigParse:
    def __init__(self):
        """
        Initialize the ConfigParse object.
        """
        self.config = ConfigParser()

    def read_config(self, file):
        """
        Read and parse a configuration file.

        Reads the specified configuration file using the ConfigParser object.
        If the file is 'config.cfg', it is parsed and the ConfigParser object
        is returned.
        For any other file, None is returned.

        Args:
            file (str): The path or name of the configuration file.

        Returns:
            configparser.ConfigParser | None: The parsed ConfigParser object
            if the file is 'config.cfg', else None.
        """
        try:
            if file == 'config.cfg':
                self.config.read(file)
                return self.config
            else:
                return None
        except KeyError:
            return None
