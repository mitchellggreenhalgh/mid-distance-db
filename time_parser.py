import re

class TimeParser:
    def parse_time(self, time: str) -> float:
        """Parse a time string in the format 'MM:SS' and return the total seconds as a float.

        Args:
            time (str): A string representing time in 'MM:SS' format.

        Returns:
            float: Total seconds.
        
        Raises:
            ValueError: If the input string is not in the correct 'MM:SS' format.
        """
        # Validate the input using a regular expression
        if not re.match(r'^\d{2}:\d{2}$', time):
            raise ValueError("Input must be in 'MM:SS' format.")

        # Use str.split and list unpacking for efficiency
        minutes, seconds = time.split(":")
        return 60 * int(minutes) + int(seconds)