"""
ConsoleController: User interface for manually solving
Anne Hoy's problems from the console.
"""


# Copyright 2014, 2017 Dustin Wehr, Danny Heap, Bogdan Simion,
# Jacqueline Smith, Dan Zingaro
# Distributed under the terms of the GNU General Public License.
#
# This file is part of Assignment 1, CSC148, Winter 2017.
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this file.  If not, see <http://www.gnu.org/licenses/>.


from toah_model import TOAHModel, IllegalMoveError


def move(model, origin, destination):
    """ Apply move from origin to destination in model.

    May raise an IllegalMoveError.

    @param TOAHModel model:
        model to modify
    @param int origin:
        stool number (index from 0) of cheese to move
    @param int destination:
        stool number you want to move cheese to
    @rtype: None
    """

    model.move(origin, destination)


class ConsoleController:
    """ Controller for text console.

    ==Attribute==
    @param TOAHModel model: a list version of the TOAHModel
    """

    def __init__(self, number_of_cheeses, number_of_stools):
        """ Initialize a new ConsoleController self.

        @param ConsoleController self:
        @param int number_of_cheeses:
        @param int number_of_stools:
        @rtype: None
        """
        self.model = TOAHModel(number_of_stools)
        self.model.fill_first_stool(number_of_cheeses)

    def play_loop(self):
        """ Play Console-based game.

        @param ConsoleController self:
        @rtype: None

        TODO:
        -Start by giving instructions about how to enter moves (which is up to
        you). Be sure to provide some way of exiting the game, and indicate
        that in the instructions.
        -Use python's built-in function input() to read a potential move from
        the user/player. You should print an error message if the input does
        not meet the specifications given in your instruction or if it denotes
        an invalid move (e.g. moving a cheese onto a smaller cheese).
        You can print error messages from this method and/or from
        ConsoleController.move; it's up to you.
        -After each valid move, use the method TOAHModel.__str__ that we've
        provided to print a representation of the current state of the game.
        """

        print("> To move a stack, first enter which tower number it's "
              "currently on followed by a space and then the tower number you "
              "want to move the stack to. \n \n"
              "> The first tower is tower number 1 and each tower number"
              " after that goes up by one (ie. the second tower is tower"
              " number 2). \n \n"
              "> To exit the game simply type 'exit' (as an isolated word"
              ") in the input command. \n \n"
              "> The objective of the game is to move all pieces from the"
              " initial tower, to the last tower. \n \n"
              "> The game's rules are: \n \n"
              "1. You can never move a bigger piece on a smaller piece. \n"
              "2. You can only move one piece at a time \n"
              "3. All disks must only be moved to viable towers \n")
        print(self.model)
        move_input = input("Enter a move or command: ").split()
        while 'exit' not in move_input:
            if len(move_input) == 2 and move_input[0].isdigit() and\
                 move_input[1].isdigit():
                try:
                    source = int(move_input[0])-1
                    destination = int(move_input[1])-1
                    self.model.move(source, destination)
                    print(self.model)
                except IllegalMoveError as error:
                    print(error)
                move_input = input("Enter a move or command: ").split()
            else:
                move_input = \
                    input("Please enter a legal move or command: ").split()

if __name__ == '__main__':
    controller = ConsoleController(3, 4)
    controller.play_loop()
    import python_ta
    python_ta.check_all(config='consolecontroller_pyta.txt')
    python_ta.check_errors(config='consolecontroller_pyta.txt')
