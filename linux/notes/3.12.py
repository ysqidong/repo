from collections.abc import Sequence
from typing import Any
class SetInsert:
    """
    A class that represents the set insert operation in Python. It takes a set as an argument and allows you to insert elements into the set using the insert method.
    """
    def insert_item(self, my_set: set, item: Any) -> None:
        """
        Inserts an item into the set.

        Parameters:
        my_set (set): The set to insert the item into.
        item (Any): The item to be inserted into the set.
        """
        my_set.add(item)