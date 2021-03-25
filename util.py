
class Node:
    def __init__(self, state, parent, action):
        # the state attribute is a coordinate for the node in the maze
        self.state = state
        # the parent attribute is an object (node) of Node class
        self.parent = parent
        # the action attribute is a string (up, down, left, right)
        self.action = action


class StackFrontier:
    def __init__(self):
        self.frontier = [] # creating an empty frontier with a list data structure

    def add(self, node):
        self.frontier.append(node)

    # checks if the passsed state is existent in the frontier (True) or not (False)
    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    # no args; when invoked would return True if the frontier is empty and False otherwise
    def empty(self):
        return len(self.frontier) == 0

    # no args: raises an Exception when the frontier is empty otherwise the last node in the frontier is returned
    def remove(self):
        if self.empty():
            raise Exception("frontier is empty")
        else:
            node = self.frontier[-1]
            # del self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node

class QueueFrontier(StackFrontier):
    # Q1 = how can I access frontier attribute in line 41 without invoking the superclass's constructor (__init__).
    def remove(self):
        if self.empty():
            raise Exception("frontier is empty")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node
