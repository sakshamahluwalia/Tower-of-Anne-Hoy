"""
functions to run TOAH tours.
"""


# Copyright 2013, 2014, 2017 Gary Baumgartner, Danny Heap, Dustin Wehr,
# Bogdan Simion, Jacqueline Smith, Dan Zingaro
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
# Copyright 2013, 2014 Gary Baumgartner, Danny Heap, Dustin Wehr


# you may want to use time.sleep(delay_between_moves) in your
# solution for 'if __name__ == "main":'
import time
from toah_model import TOAHModel, IllegalMoveError


def optimal_moves(num_disks):
    """Helper function to find the optimal moves for a given number of disks

     @param int num_disks:
        number of disks
    """
    n_list = []
    n_list2 = []
    if num_disks == 1:
        return 1
    else:
        for i in range(1, num_disks):
            result = (2 * optimal_moves(num_disks - i) + (2 ** i) - 1)
            n_list.append(result)
            n_list2.append(i)
    return min(n_list)


def optimal_i(disks):
    """Helper function to find the optimal i for a given number of disks

     @param int disks:
        number of disks
    """
    n_list = []
    n_list2 = []
    if disks == 1:
        return 1
    else:
        for i in range(1, disks):
            result = (2 * optimal_moves(disks - i) + (2 ** i) - 1)
            n_list.append(result)
            n_list2.append(i)
    return n_list2[n_list.index(min(n_list))]


def optimal_i_two(num_disk):
    """Helper function to find the optimal i for a given number of disks.

     @param int num_disk:
        number of disks
    """
    n_list = [[1, 2], [3, 4, 5], [6, 7, 8, 9], [10, 11, 12, 13, 14],
              [15, 16, 17, 18, 19, 20]]
    n_list2 = [1, 2, 3, 4, 5]
    optimum_i = 0
    for index in range(5):
        for disk in range(len(n_list[index])):
            if num_disk == n_list[index][disk]:
                optimum_i = n_list2[index]
    return optimum_i


def move_for_tour(model, origin, destination, animate):
    """ Apply move from origin to destination in model. Is used by
    a program to solve the puzzle.

    Will not raise an IllegalMoveError.

    @param TOAHModel model:
        model to modify
    @param list origin:
        stool number (index from 0) of cheese to move
    @param list destination:
        stool number you want to move cheese to
    @param bool animate:
        Tells us if the user wants to print the model
    @rtype: None
    """

    destination.append(origin.pop())
    model.get_move_seq().add_move(model.stools().index(origin),
                                  model.stools().index(destination))
    if animate:
        print(model)


def move_tower2(model, num_disk, tup, delay, animate):
    """ Apply move from origin to destination in model. Is only to
    be used

    May raise an IllegalMoveError.

    @param TOAHModel model:
        model to modify.
    @param int num_disk:
        Number of disks in source.
    @param tuple tup:
        Tuple containing stools.
    @param bool animate:
        Tells us if the user wants to print the model.
    @param float delay:
        delays the function call by the specified amount of time.
    @rtype: None
    """
    source, target, helper = tup
    if num_disk > 0:
        move_tower2(model, num_disk-1, (source, helper, target),
                    delay, animate)
        time.sleep(delay)
        move_for_tour(model, source, target, animate)
        move_tower2(model, num_disk-1, (helper, target, source),
                    delay, animate)


def tour_of_four_stools(model, delay_btw_moves=0.5, animate=False):
    """Move a tower of cheeses from the first stool in model to the fourth.

    @type model: TOAHModel
        TOAHModel with tower of cheese on first stool and three empty
        stools
    @type delay_btw_moves: float
        time delay between moves if console_animate is True
    @type animate: bool
        animate the tour or not
    """
    if len(model.stools()[0]) > 0:
        num_disks = model.copy[0]
        source = model.stools()[0]
        helper = model.stools()[1]
        helper2 = model.stools()[2]
        target = model.stools()[3]
    else:
        raise IllegalMoveError("Need at least 1 cheese to start the game")
    if animate:
        print(model)
    move_tower(model, num_disks, (source, helper, helper2, target),
               delay_btw_moves, animate)


def move_tower(model, num_disks, tup_, delay_btw_moves, animate):
    """
    Move the tower starting at the nth disk from the source peg to the target,
    using the helper peg following the towers of anne hoy rulers

    @param TOAHModel model:
        model to modify
    @param int num_disks:
        Number of disks in source
    @param tuple tup_:
        Tuple containing stools
    @param bool animate:
        Tells us if the user wants to print the model
    @param float delay_btw_moves:
        delays the function call by the specified amount of time
    @rtype: None
    """
    source, helper, helper2, target = tup_
    if num_disks in range(7, 21):
        i = optimal_i_two(num_disks)
    else:
        i = optimal_i(num_disks)
    if num_disks == 1:
        time.sleep(delay_btw_moves)
        move_for_tour(model, source, target, animate)
    if num_disks >= 2:
        move_tower(model, num_disks-i, (source, helper, target, helper2),
                   delay_btw_moves, animate)
        move_tower2(model, i, (source, target, helper),
                    delay_btw_moves, animate)
        move_tower(model, num_disks-i, (helper2, source, helper, target),
                   delay_btw_moves, animate)

if __name__ == '__main__':
    num_cheeses = 10
    delay_between_moves = 0
    console_animate = True

    # DO NOT MODIFY THE CODE BELOW.
    four_stools = TOAHModel(4)
    four_stools.fill_first_stool(number_of_cheeses=num_cheeses)
    tour_of_four_stools(four_stools,
                        animate=console_animate,
                        delay_btw_moves=delay_between_moves)
    print(four_stools.number_of_moves())
