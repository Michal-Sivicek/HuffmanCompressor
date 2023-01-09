class Node:
    def __init__(self, char, freq):
        """
        :param char: the character
        :param freq: the frequency of the character
        """
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        """
        :param other: the other node
        :return: True if the frequency of the current node is less than the frequency of the other node
        """
        return self.freq < other.freq

    def __eq__(self, other):
        """
        :param other: the other node
        :return: True if the character of the current node is equal to the character of the other node
        """
        if other == None:
            return False
        if not isinstance(other, Node):
            return False
        return self.freq == other.freq

    def __str__(self):
        return f"Node({self.char}, {self.freq})"

    def __repr__(self):
        return f"Node({self.char}, {self.freq})"

    def __hash__(self):
        return hash(self.char)

