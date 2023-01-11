from typing import List


class Content:

    def __init__(self, app_type: str = "application/json"):
        """

        :param app_type: The response application type
        """
        ...

    def schema(self, type: str, items: List[str]):
        """

        """