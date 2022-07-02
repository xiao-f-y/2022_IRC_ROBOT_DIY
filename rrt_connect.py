import time
import math
import tqdm
import numpy as np

from tool import env, plotting, utils, Node


class RrtConnect:
    def __init__(self, start_point, end_point, step_length, sample_rate, max_iter, env_instance):
        '''
        :param start_point: start point of the robot
        :param end_point: end point of the robot
        :param step_length: step length of the robot
        :param sample_rate: sample rate for finding new node
        :param max_iter: maximum iteration
        :param env_instance:
        '''
        self.st_point = Node(start_point)
        self.ed_point = Node(end_point)
        self.step_length = step_length
        self.sample_rate = sample_rate
        self.max_iter = max_iter
        self.V1 = [self.st_point]
        self.V2 = [self.ed_point]
        self.nodes = [self.st_point]  # nodes of the tree

        # initialize the environment
        self.env = env_instance
        self.plotting = plotting.Plotting(start_point, end_point, self.env)
        self.utils = utils.Utils(self.env)
        self.utils.fix_random_seed()
        self.x_range = self.env.x_range
        self.y_range = self.env.y_range
        self.obs_circle = self.env.obs_circle
        self.obs_rectangle = self.env.obs_rectangle
        self.obs_boundary = self.env.obs_boundary

        # record
        self.iter_num = -1
        self.time_start = -1
        self.time_end = -1
        self.dist = -1

    def planning(self):
        path = None
        self.time_start = time.time()
        for i in tqdm.tqdm(range(self.max_iter)):
            node_rand = self.generate_random_node(self.ed_point, self.sample_rate)
            node_near = self.nearest_neighbor(self.V1, node_rand)
            node_new = self.new_state(node_near, node_rand)

            if node_new and not self.utils.is_collision(node_near, node_new):
                self.iter_num = i + 1
                self.V1.append(node_new)
                node_near_prim = self.nearest_neighbor(self.V2, node_new)
                node_new_prim = self.new_state(node_near_prim, node_new)

                if node_new_prim and not self.utils.is_collision(node_new_prim, node_near_prim):
                    
                    self.V2.append(node_new_prim)

                    while True:
                        node_new_prim2 = self.new_state(node_new_prim, node_new)
                        if node_new_prim2 and not self.utils.is_collision(node_new_prim2, node_new_prim):
                            
                            self.V2.append(node_new_prim2)
                            node_new_prim = self.change_node(node_new_prim, node_new_prim2)
                        else:
                            break

                        if self.is_node_same(node_new_prim, node_new):
                            break

                if self.is_node_same(node_new_prim, node_new):
                    return self.extract_path(node_new, node_new_prim)

            if len(self.V2) < len(self.V1):
                list_mid = self.V2
                self.V2 = self.V1
                self.V1 = list_mid
        self.time_end = time.time()
        return None

    @staticmethod
    def change_node(node_new_prim, node_new_prim2):
        node_new = Node((node_new_prim2.x, node_new_prim2.y))
        node_new.parent = node_new_prim

        return node_new

    @staticmethod
    def is_node_same(node_new_prim, node_new):
        if node_new_prim.x == node_new.x and \
                node_new_prim.y == node_new.y:
            return True

        return False

    def generate_random_node(self, sample_goal, sample_rate):
        delta = self.utils.delta

        if np.random.random() > sample_rate:
            return Node((np.random.uniform(self.x_range[0] + delta, self.x_range[1] - delta),
                         np.random.uniform(self.y_range[0] + delta, self.y_range[1] - delta)))

        return sample_goal

    @staticmethod
    def nearest_neighbor(node_list, n):
        return node_list[int(np.argmin([math.hypot(nd.x - n.x, nd.y - n.y)
                                        for nd in node_list]))]

    def new_state(self, node_start, node_end):
        dist, theta = self.get_distance_and_angle(node_start, node_end)

        dist = min(self.step_length, dist)
        node_new = Node((node_start.x + dist * math.cos(theta),
                         node_start.y + dist * math.sin(theta)))
        node_new.parent = node_start

        return node_new

    @staticmethod
    def extract_path(node_new, node_new_prim):
        path1 = [(node_new.x, node_new.y)]
        node_now = node_new

        while node_now.parent is not None:
            node_now = node_now.parent
            path1.append((node_now.x, node_now.y))

        path2 = [(node_new_prim.x, node_new_prim.y)]
        node_now = node_new_prim

        while node_now.parent is not None:
            node_now = node_now.parent
            path2.append((node_now.x, node_now.y))

        return list(list(reversed(path1)) + path2)

    @staticmethod
    def get_distance_and_angle(node_start, node_end):
        dx = node_end.x - node_start.x
        dy = node_end.y - node_start.y
        return math.hypot(dx, dy), math.atan2(dy, dx)

        self.time_end = time.time()
        # return final path
        # implement extract_path func maybe help
        # path = extract_path(..., ...)
        # self.dist = self.path_distance(path)
        return path

    # TODO: Backtrack the path from the end node to the start node to get the final path
    # def extract_path(self, ...):
    #     pass
    def path_distance(self, path):
        '''
        get the distance of the path
        :param path:
        :return:
        '''
        dist_sum = 0
        for i in range(len(path) - 1):
            dist_sum += np.linalg.norm([path[i + 1][0] - path[i][0], path[i + 1][1] - path[i][1]])
        return dist_sum


def env1_planning(eval_time=1):
    x_start = (5, 5)  # st node
    x_goal = (49, 16)  # end node

    # visualization
    if eval_time == 1:
        rrt = RrtConnect(x_start, x_goal, 0.5, 0.05, 10000, env.EnvOne())
        path = rrt.planning()
        if not path:
            print("No Path Found!")
        print("Time: {:.3f} s".format(rrt.time_end - rrt.time_start))
        print("Iteration:", rrt.iter_num)
        if path:
            print("Distance:{:.3f}".format(rrt.dist))
        rrt.plotting.animation_connect(rrt.V1, rrt.V2, path, "RRT_CONNECT_ENV1")
        return
    # evaluation
    time_sum = list()
    iter_sum = list()
    dist_sum = list()
    for i in range(eval_time):
        rrt = RrtConnect(x_start, x_goal, 0.5, 0.05, 10000, env.EnvOne())
        path = rrt.planning()
        if not path:
            print("No Path Found!")
        print("###### Evaluation: {} ######".format(i + 1))
        print("Time: {:.3f} s".format(rrt.time_end - rrt.time_start))
        print("Iteration:", rrt.iter_num)
        if path:
            print("Distance:{:.3f}".format(rrt.dist))
            dist_sum.append(rrt.dist)
        print("-----------------------------------------------------")
        time_sum.append(rrt.time_end - rrt.time_start)
        iter_sum.append(rrt.iter_num)

    # average time
    print("Average Time: {:.3f} s".format(np.mean(time_sum)))
    # average iteration
    print("Average Iteration: {:.0f}".format(np.mean(iter_sum)))
    # average distance
    if len(dist_sum) > 0:
        print("Average Distance: {:.3f}".format(np.mean(dist_sum)))


def env2_planning(eval_time=1):
    x_start = (5, 20)  # st node
    x_goal = (67, 40)  # end node

    # visualization
    if eval_time == 1:
        rrt = RrtConnect(x_start, x_goal, 0.5, 0.2, 10000, env.EnvTwo())
        path = rrt.planning()
        if not path:
            print("No Path Found!")
        print("Time: {:.3f} s".format(rrt.time_end - rrt.time_start))
        print("Iteration:", rrt.iter_num)
        if path:
            print("Distance:{:.3f}".format(rrt.dist))
        rrt.plotting.animation(rrt.nodes, path, "RRT_ENV2", True)
        return
    # evaluation
    time_sum = list()
    iter_sum = list()
    dist_sum = list()
    for i in range(eval_time):
        rrt = RrtConnect(x_start, x_goal, 0.5, 0.2, 10000, env.EnvTwo())
        path = rrt.planning()
        if not path:
            print("No Path Found!")
        print("###### Evaluation: {} ######".format(i + 1))
        print("Time: {:.3f} s".format(rrt.time_end - rrt.time_start))
        print("Iteration:", rrt.iter_num)
        if path:
            print("Distance:{:.3f}".format(rrt.dist))
            dist_sum.append(rrt.dist)
        print("-----------------------------------------------------")
        time_sum.append(rrt.time_end - rrt.time_start)
        iter_sum.append(rrt.iter_num)

    # average time
    print("Average Time: {:.3f} s".format(np.mean(time_sum)))
    # average iteration
    print("Average Iteration: {:.0f}".format(np.mean(iter_sum)))
    # average distance
    if len(dist_sum) > 0:
        print("Average Distance: {:.3f}".format(np.mean(dist_sum)))


def env3_planning(eval_time=1):
    x_start = (5, 2)  # st node
    x_goal = (18, 18)  # end node

    # visualization
    if eval_time == 1:
        rrt = RrtConnect(x_start, x_goal, 0.5, 0.2, 10000, env.EnvThree())
        path = rrt.planning()
        if not path:
            print("No Path Found!")
        print("Time: {:.3f} s".format(rrt.time_end - rrt.time_start))
        print("Iteration:", rrt.iter_num)
        print("Distance:{:.3f}".format(rrt.dist))
        rrt.plotting.animation(rrt.nodes, path, "RRT_ENV3", True)
        return
    # evaluation
    time_sum = list()
    iter_sum = list()
    dist_sum = list()
    for i in range(eval_time):
        rrt = RrtConnect(x_start, x_goal, 0.5, 0.2, 10000, env.EnvThree())
        path = rrt.planning()
        if not path:
            print("No Path Found!")
        print("###### Evaluation: {} ######".format(i + 1))
        print("Time: {:.3f} s".format(rrt.time_end - rrt.time_start))
        print("Iteration:", rrt.iter_num)
        if path:
            print("Distance:{:.3f}".format(rrt.dist))
            dist_sum.append(rrt.dist)
        print("-----------------------------------------------------")
        time_sum.append(rrt.time_end - rrt.time_start)
        iter_sum.append(rrt.iter_num)

    # average time
    print("Average Time: {:.3f} s".format(np.mean(time_sum)))
    # average iteration
    print("Average Iteration: {:.0f}".format(np.mean(iter_sum)))
    # average distance
    if len(dist_sum) > 0:
        print("Average Distance: {:.3f}".format(np.mean(dist_sum)))


if __name__ == '__main__':
    env1_planning(eval_time=1)
    # env2_planning(eval_time=1)
    # env3_planning(eval_time=1)
