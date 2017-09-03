"""
TOAHModel:  Model a game of Tour of Anne Hoy
Cheese:   Model a cheese with a given (relative) size
IllegalMoveError: Type of exceptions thrown when an illegal move is attempted
MoveSequence: Record of a sequence of (not necessarily legal) moves. You will
need to return MoveSequence object after solving an instance of the 4-stool
Tour of Anne Hoy game, and we will use that to check the correctness of your
algorithm.
"""


class TOAHModel:
    """ Model a game of Tour Of Anne Hoy.

    Model stools holding stacks of cheese, enforcing the constraint
    that a larger cheese may not be placed on a smaller one.
    """

    def __init__(self, number_of_stools):
        """ Create new TOAHModel with empty stools
        to hold stools of cheese.

        @param TOAHModel self:
            Initialise a TOAHModel
        @param int number_of_stools:
            Number of stools in a TOAHModel
        @rtype: None

        >>> M = TOAHModel(4)
        >>> M.fill_first_stool(5)
        >>> (M.get_number_of_stools(), M.number_of_moves()) == (4,0)
        True
        >>> M.get_number_of_cheeses()
        5
        """
        self._move_seq = MoveSequence([])
        self._stools = []
        counter = 0
        while counter < number_of_stools:
            self._stools.append([])
            counter += 1
        self.copy = []

    def __eq__(self, other):
        """ Return whether TOAHModel self is equivalent to other.

        Two TOAHModels are equivalent if their current
        configurations of cheeses on stools look the same.
        More precisely, for all h,s, the h-th cheese on the s-th
        stool of self should be equivalent the h-th cheese on the s-th
        stool of other

        @type TOAHModel self:
        @type TOAHModel other:
        @rtype: bool

        >>> m1 = TOAHModel(4)
        >>> m1.fill_first_stool(7)
        >>> m1.move(0, 1)
        >>> m1.move(0, 2)
        >>> m1.move(1, 2)
        >>> m2 = TOAHModel(4)
        >>> m2.fill_first_stool(7)
        >>> m2.move(0, 3)
        >>> m2.move(0, 2)
        >>> m2.move(3, 2)
        >>> m1 == m2
        True
        """

        return self.helper_eq() == other.helper_eq()

    def __str__(self):
        """
        Depicts only the current state of the stools and cheese.

        @param TOAHModel self:
        @rtype: str
        """
        all_cheeses = []
        for height in range(self.get_number_of_cheeses()):
            for stool in range(self.get_number_of_stools()):
                if self._cheese_at(stool, height) is not None:
                    all_cheeses.append(self._cheese_at(stool, height))
        max_cheese_size = max([c.size for c in all_cheeses]) \
            if len(all_cheeses) > 0 else 0
        stool_str = "=" * (2 * max_cheese_size + 1)
        stool_spacing = "  "
        stools_str = (stool_str + stool_spacing) * self.get_number_of_stools()

        def _cheese_str(size):
            # helper for string representation of cheese
            if size == 0:
                return " " * len(stool_str)
            cheese_part = "-" + "--" * (size - 1)
            space_filler = " " * int((len(stool_str) - len(cheese_part)) / 2)
            return space_filler + cheese_part + space_filler

        lines = ""
        for height in range(self.get_number_of_cheeses() - 1, -1, -1):
            line = ""
            for stool in range(self.get_number_of_stools()):
                cheese = self._cheese_at(stool, height)
                if isinstance(cheese, Cheese):
                    size = _cheese_str(int(cheese.size))
                else:
                    size = _cheese_str(0)
                line += size + stool_spacing
            lines += line + "\n"
        lines += stools_str

        return lines

    def fill_first_stool(self, number_of_cheeses):
        """
        Fill the first stool of a TOAHModel object with multiple Cheese objects
        specified by number_of_cheeses.

        @param TOAHModel self:
        @param int number_of_cheeses:
        @rtype: None

        >>> m1 = TOAHModel(5)
        >>> m1.fill_first_stool(4)
        >>> m1.fill_first_stool(5)
        >>> m1.get_number_of_cheeses()
        4
        """
        disk_size = 0
        num_cheeses = number_of_cheeses
        while disk_size < number_of_cheeses:
            cheese = Cheese(num_cheeses)
            if len(self._stools[0]) == 0 or \
                    cheese.size < self._stools[0][-1].size:
                self._stools[0].append(cheese)
            num_cheeses -= 1
            disk_size += 1

    def add(self, cheese, index):
        """
        Add a cheese object to a stool.

        @param TOAHModel self:
        @param Cheese cheese:
        @param int index:
        @rtype: None
        >>> m1 = TOAHModel(4)
        >>> c1 = Cheese(2)
        >>> c2 = Cheese(3)
        >>> m1.add(c1, 0)
        >>> m1.add(c2, 0)
        >>> len(m1.stools()[0]) == 1
        True
        """
        if len(self._stools[index]) == 0 or \
           cheese.size < self._stools[index][-1].size:
            self._stools[index].append(cheese)

    def move(self, origin, dest):
        """ Apply move from origin to destination in model. Is only to
        be used when a user manually wants to play the game.

        May raise an IllegalMoveError.

        @param TOAHModel self:
            model to modify
        @param int origin:
            stool number (index from 0) of cheese to move
        @param int dest:
            stool number you want to move cheese to
        @rtype: None

        >>> m1 = TOAHModel(4)
        >>> m1.fill_first_stool(3)
        >>> m1.move(0, 1)
        >>> m1.move(0, 2)
        >>> m1.move(0, 3)
        >>> m1.move(2, 3)
        >>> m1.move(1, 3)
        >>> m1.number_of_moves() == 5
        True
        >>> len(m1.stools()[0]) == 0
        True
        >>> m1.get_top_cheese(3).size == 1
        True
        """
        n_list = []
        for i in range(self.get_number_of_stools()):
            n_list.append(i)
        if origin in n_list and dest in n_list and origin != dest:
            if len(self._stools[origin]) >= 1:
                cheese = self.get_top_cheese(origin)
                if len(self._stools[dest]) == 0 \
                        or cheese.size < self._stools[dest][-1].size:
                    self._stools[dest].append(cheese)
                    self._stools[origin].pop()
                    self._move_seq.add_move(origin, dest)
                else:
                    raise IllegalMoveError("That move is not legal")
            else:
                raise IllegalMoveError("The stack you choose is empty")
        else:
            raise IllegalMoveError("Please choose a valid stool")

    def number_of_moves(self):
        """
        Return the number of moves completed in a game of TOAH.

        @param TOAHModel self:
        @rtype: int
        >>> m1 = TOAHModel(4)
        >>> m1.fill_first_stool(7)
        >>> m1.move(0, 1)
        >>> m1.move(0, 2)
        >>> m1.move(1, 2)
        >>> m1.number_of_moves()
        3
        """

        return self._move_seq.length()

    def get_cheese_location(self, cheese):
        """
        Return the index in which a Cheese object is located in a TOAHModel
        object self.

        @param TOAHModel self:
        @param Cheese cheese:
        @rtype: int
        >>> m1 = TOAHModel(4)
        >>> m1.fill_first_stool(5)
        >>> m1.get_cheese_location(m1.get_top_cheese(0))
        0
        """
        stool = 0
        for index in range(len(self._stools)):
            for index2 in range(len(self._stools[index])):
                if self._stools[index][index2] == cheese:
                    stool = index
        return stool

    def get_top_cheese(self, index):
        """
        Return the Cheese object at the top of a stool in a TOAHModel obejct.

        @param self: TOAHModel
        @param index: int
        @rtype: Cheese

        >>> m1 = TOAHModel(4)
        >>> m1.fill_first_stool(5)
        >>> (m1.get_top_cheese(0)).size == 1
        True
        """

        if len(self._stools[index]) != 0:
            return self._stools[index][-1]
        else:
            raise IllegalMoveError("The stack you choose is empty")

    def get_number_of_stools(self):
        """
        Return the number of stools in a TOAHModel object.

        @param TOAHModel self:
        @rtype: int

        >>> model = TOAHModel(0)
        >>> model.get_number_of_stools()
        0
        >>> model2 = TOAHModel(1)
        >>> model2.get_number_of_stools()
        1
        >>> model3 = TOAHModel(3)
        >>> model3 = TOAHModel(4)
        >>> model3.get_number_of_stools()
        4
        """

        return len(self._stools)

    def get_number_of_cheeses(self):
        """
        Return the number of Cheese objects present in a game of TOAH.

        @param self: TOAHModel
        @rtype: int

        >>> m1 = TOAHModel(4)
        >>> m1.get_number_of_cheeses()
        0
        >>> m1 = TOAHModel(4)
        >>> m1.fill_first_stool(7)
        >>> m1.get_number_of_cheeses()
        7
        """

        num_cheese = 0
        for index in range(len(self._stools)):
            num_cheese += len(self._stools[index])
        return num_cheese

    def _cheese_at(self, stool_index, stool_height):
        """ Return (stool_height)th from stool_index stool, if possible.

        @type self: TOAHModel
        @type stool_index: int
        @type stool_height: int
        @rtype: Cheese | None

        # >>> M = TOAHModel(4)
        # >>> M.fill_first_stool(5)
        # >>> M._cheese_at(0,3).size
        # 2
        # >>> M._cheese_at(0,0).size
        # 5
        """
        if 0 <= stool_height < len(self._stools[stool_index]):
            return self._stools[stool_index][stool_height]
        else:
            return None

    def stools(self):
        """Make a copy of self._stools

        @param TOAHModel self:
        @rtype: list

        >>> m1 = TOAHModel(3)
        >>> len(m1.stools()) == m1.get_number_of_stools()
        True
        """
        for index in range(len(self._stools[0])):
            self.copy.append(self._stools[0][index].size)
        return self._stools

    def get_move_seq(self):
        """ Return the move sequence

        @type self: TOAHModel
        @rtype: MoveSequence
        >>> toah = TOAHModel(2)
        >>> toah.get_move_seq() == MoveSequence([])
        True
        """
        return self._move_seq

    def helper_eq(self):
        """ Return a more readable form of self._stools

        @type self: TOAHModel
        @rtype: list

        >>> toah = TOAHModel(2)
        >>> toah.helper_eq()
        [[], []]
        """
        n_list2 = []
        for index in range(len(self._stools)):
            n_list = []
            for index2 in range(len(self._stools[index])):
                n_list.append(self._stools[index][index2].size)
            n_list2.append(n_list)
        return n_list2


class Cheese:
    """ A cheese for stacking in a TOAHModel

    === Attributes ===
    @param int size: width of cheese
    """

    def __init__(self, size):
        """ Initialize a Cheese to diameter size.

        @param Cheese self:
        @param int size:
        @rtype: None

        >>> c = Cheese(3)
        >>> isinstance(c, Cheese)
        True
        >>> c.size
        3
        """
        self.size = size

    def __eq__(self, other):
        """ Is self equivalent to other?

        We say they are if they're the same
        size.

        @param Cheese self:
        @param Cheese|Any other:
        @rtype: bool

        >>> ch = Cheese(1)
        >>> ch2 = Cheese(2)
        >>> ch == ch2
        False
        >>> ch3 = Cheese(2)
        >>> ch3 == ch2
        True
        """
        return self.size == other.size


class IllegalMoveError(Exception):
    """ Exception indicating move that violate TOAHModel
    """
    pass


class MoveSequence(object):
    """ Sequence of moves in Tower Of Anne Hoy game
    """

    def __init__(self, moves):
        """ Create a new MoveSequence self.

        @param MoveSequence self:
        @param list[tuple[int]] moves:
        @rtype: None
        """
        # moves - a list of integer pairs, e.g. [(0,1),(0,2),(1,2)]
        self._moves = moves

    def get_move(self, i):
        """ Return the move at position i in self

        @param MoveSequence self:
        @param int i:
        @rtype: tuple[int]

        >>> ms = MoveSequence([(1, 2)])
        >>> ms.get_move(0) == (1, 2)
        True
        """
        # Exception if not (0 <= i < self.length)
        return self.get_move_sequence()[i]

    def get_move_sequence(self):
        """ Return the move at position i in self

        @param MoveSequence self:
        @rtype: tuple[int]

        >>> ms = MoveSequence([(1, 2)])
        >>> ms.get_move(0) == (1, 2)
        True
        """
        return self._moves

    def __eq__(self, other):
        """ Return the move at position i in self

        @param MoveSequence self:
        @param MoveSequence other:
        @rtype: tuple[int]

        >>> m1 = MoveSequence([])
        >>> m2 = MoveSequence([])
        >>> m1 == m2
        True
        >>> m3 = MoveSequence([])
        >>> m3.add_move(0, 2)
        >>> model = TOAHModel(3)
        >>> model.fill_first_stool(5)
        >>> model.move(0, 2)
        >>> model.get_move_seq() == m3
        True
        """
        return self._moves == other.get_move_sequence()

    def __str__(self):

        return "{0}".format(self._moves)

    def add_move(self, src_stool, dest_stool):
        """ Add move from src_stool to dest_stool to MoveSequence self.

        @param MoveSequence self:
        @param int src_stool:
        @param int dest_stool:
        @rtype: None
        """
        self._moves.append((src_stool, dest_stool))

    def length(self):
        """ Return number of moves in self.

        @param MoveSequence self:
        @rtype: int

        >>> ms = MoveSequence([(1, 2)])
        >>> ms.length()
        1
        """
        return len(self._moves)

    def generate_toah_model(self, number_of_stools, number_of_cheeses):
        """ Construct TOAHModel from number_of_stools and number_of_cheeses
         after moves in self.

        Takes the two parameters for
        the game (number_of_cheeses, number_of_stools), initializes the game
        in the standard way with TOAHModel.fill_first_stool(number_of_cheeses),
        and then applies each of the moves in this move sequence.

        @param MoveSequence self:
        @param int number_of_stools:
        @param int number_of_cheeses:
        @rtype: TOAHModel

        >>> ms = MoveSequence([])
        >>> toah = TOAHModel(2)
        >>> toah.fill_first_stool(2)
        >>> toah == ms.generate_toah_model(2, 2)
        True
        """
        model = TOAHModel(number_of_stools)
        model.fill_first_stool(number_of_cheeses)
        for move in self._moves:
            model.move(move[0], move[1])
        return model


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
    import python_ta
    python_ta.check_all(config="toahmodel_pyta.txt")
