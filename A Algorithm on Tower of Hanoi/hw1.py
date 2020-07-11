class AStarProblem(object):

    def calculate_G_Score(self, neighbour_states, current_state): # to calculate adjacent rod' s distance

        side_movement = 1
        pick_up = 5
        put_down = 3

        current_first_rod = current_state.getItem(0)
        current_second_rod = current_state.getItem(1)
        current_third_rod = current_state.getItem(2)

        neighbour_first_rod = neighbour_states.getItem(0)
        neighbour_second_rod = neighbour_states.getItem(1)
        neighbour_third_rod = neighbour_states.getItem(2)


        if (current_first_rod == neighbour_first_rod):
            side_movement = 1
        elif (current_second_rod == neighbour_second_rod):
            side_movement = 2
        elif (current_third_rod == neighbour_third_rod):
            side_movement = 1

        return pick_up + put_down + side_movement #1


    def reached_goal(self, point, goal):
        return point == goal


class PathNotFound(Exception):
    pass


def search_route(hanoi, start, goal):

    open_set = set()

    open_queue = list()

    closed_set = set()

    came_from = dict()

    g_score = dict()

    h_score = dict()

    def f_score(point):
        return g_score[point] + h_score[point]


    g_score[start] = 0
    h = hanoi.heuristic(start)
    h_score[start] = h
    open_set.add(start)
    open_queue.append((f_score(start), start))

    # search up to the end
    while open_set:

        open_queue.sort()# sort queue by disk' s numbers(f score)
        next_f, point = open_queue.pop(0)# f score and stack, and pop the lowest value in queue !!!!
        open_set.remove(point)

        if hanoi.reached_goal(point, goal):
            # reached goal
            path = [point]

            while point != start:
                point = came_from[point]
                path.append(point)
            path.reverse()
            F_score = (open_queue.pop(0)[0])
            return path, F_score

        closed_set.add(point)

        for neighbor in hanoi.neighbor_nodes(point):

            if not neighbor in closed_set:

                neighbor_g_score = g_score[point] + hanoi.calculate_G_Score(neighbor, point)

                if neighbor not in open_set:
                    # Look through the new field
                    came_from[neighbor] = point
                    g = neighbor_g_score
                    h = hanoi.heuristic(neighbor)
                    g_score[neighbor] = g
                    h_score[neighbor] = h
                    open_set.add(neighbor)
                    f = g + h

                    open_queue.append((f, neighbor))

                else: # in open set, but better g score

                    if neighbor_g_score < g_score[neighbor]:# there is a better path than before

                        came_from[neighbor] = point
                        g = neighbor_g_score
                        g_score[neighbor] = g
                        h = hanoi.heuristic(neighbor)
                        h_score[neighbor] = h
                        f = g + h


    raise PathNotFound("there is no path from "+ str(start) + " to" + str(goal) + ".")



class Rods(object):

    def __init__(self, rods):
        if isinstance(rods, Rods):
            self.rods = rods.rods
        else:
            self.rods = rods

    def getItem(self, index):
        return self.rods[index]


    @staticmethod
    def first_rod(number_of_rods, number_of_disks):

        rods_list = []
        for element in range(number_of_rods):
            rods_list.append([])
        if rods_list:
            rods_list[0] = range(number_of_disks, 0, -1)

        return Rods(rods_list)

    @staticmethod
    def third_rod(number_of_rods, number_of_disks):

        rods_list = []
        for element in range(number_of_rods):
            rods_list.append([])
        if rods_list:
            rods_list[-1] = range(number_of_disks, 0, -1)

        return Rods(rods_list)

    def copy(self) : #copy the same current rods

        return Rods([list(rod) for rod in self.rods])



    def is_legal(self): #TO DECIDE WHETHER THE DISK IS BIGGER THAN THE TOP ONE OR NOT
        for rod in self.rods:
            controller_disk = 1000
            for disk in rod:
                if disk >= controller_disk:
                    return False
                else:
                    controller_disk = disk

        return True

    def depth(self, index): #depth of a rod
        return len(self.rods[index])

    def move(self, from_index, to_index):
        new_rods = self.copy()
        from_rods = new_rods.rods[from_index]
        to_rods = new_rods.rods[to_index]
        to_rods.append(from_rods.pop())

        return Rods(new_rods)

    @staticmethod
    def print_movements(result, all_movements):

        first_counter = 0
        second_counter = 1

        while(1):

            if (second_counter == len(result)):
                print(all_movements)
                return

            result_1_first_rod = result[first_counter].getItem(0)
            result_1_second_rod = result[first_counter].getItem(1)
            result_1_third_rod = result[first_counter].getItem(2)

            result_2_first_rod = result[second_counter].getItem(0)
            result_2_second_rod = result[second_counter].getItem(1)
            result_2_third_rod = result[second_counter].getItem(2)

            side_movement = str(second_counter) + ". Step is: pickup - "



            if (result_1_first_rod == result_2_first_rod):
                if(len(result_2_second_rod) > len(result_1_second_rod)): # from 3. rod to 2. rod
                    side_movement += "left - "
                else:                                                      # from 2. rod to 3. rod
                    side_movement += "right - "
            elif (result_1_second_rod == result_2_second_rod):
                if (len(result_2_third_rod) > len(result_1_third_rod)): # from 1. rod to 3. rod
                    side_movement += "right - right - "
                else:
                    side_movement += "left - left - "
            elif (result_1_third_rod == result_2_third_rod):
                if (len(result_2_first_rod) > len(result_1_first_rod)):  # from 1. rod to 3. rod
                    side_movement += "left - "
                else:
                    side_movement += "right - "

            side_movement += "putdown \n "
            all_movements += side_movement

            first_counter += 1
            second_counter += 1


    def __repr__(self): # to return a printable version of an object
        return 'Rods(%s)' % repr(self.rods)


    def __hash__(self): # return the same value for objects that are equal
        return hash(repr(self))

    def __eq__(self, other): # compares the equality of two objects
        return repr(self) == repr(other)




class TowerOfHanoi(AStarProblem):
    def __init__(self, pegs=3):
        self.number_of_pegs = pegs

    def neighbor_nodes(self, rods): # calculates all possible ways where disks can be placed on
        neighbors = []

        for i in range(self.number_of_pegs):
            for j in range(self.number_of_pegs):
                if i != j and rods.depth(i) > 0:
                    neighbor = rods.move(i, j)

                    if neighbor.is_legal():
                        neighbors.append(neighbor)

        return neighbors

    def heuristic(self, position):

        # number of disks at the third rod
        heuristic = len(position.rods)

        # number of disks to the third rod
        heuristic_2 = len(position.rods[0]) + len(position.rods[1])

        # size of disks at third rod
        heuristic_3 = sum(position.rods[-1])

        # size of disks other than third rod
        heuristic_4 = sum(position.rods[0]) + sum(position.rods[1])

        # combination of them (distance of disks to the third rod)
        heuristic_5 = len(position.rods[0])*2 + len(position.rods[1])

        # combination of them (size of disks other than the third rod according to distance)
        heuristic_6 = sum(position.rods[0])*2 + sum(position.rods[1])


        final_heuristic = heuristic_6

        return final_heuristic


if __name__ == '__main__':

    g = raw_input("Enter the number of disk : ")

    number_of_rods = 3
    number_of_disks = int(g)
    hanoi = TowerOfHanoi(number_of_rods)

    start = Rods.first_rod(number_of_rods, number_of_disks)
    goal = Rods.third_rod(number_of_rods, number_of_disks)


    result, F_Score = search_route(hanoi, start, goal)

    all_movements = ""
    print("---")
    print("Solution movements are: \n")
    Rods.print_movements(result, all_movements)

    i = 0
    print("--")
    print("States of the rods at each step:\n ")
    for point in result:
        print (str((i+1)) + ". Step: " + str(point))
        i = i+1

    print("\nNumber of visited node is: ")
    print(len(result))
    print("Path cost is: ")
    print(F_Score)