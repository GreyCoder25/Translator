class ParseTreeNode(object):
    def __init__(self, text, type):
        self.text = text
        self.type = type
        self.descendants = []
        self.ancestor = None


class ParseTree(object):
    def __init__(self):
        self.root = None
        self.current_node = None

    def add(self, text, type):
        if self.root is None:
            self.current_node = ParseTreeNode(text, type)
            self.root = self.current_node
        else:
            ancestor_node = self.current_node
            new_node = ParseTreeNode(text, type)
            new_node.ancestor = ancestor_node
            self.current_node.descendants.append(new_node)
            self.current_node = new_node

    def delete_last(self):
        if self.level_up():
            self.current_node.descendants.pop()

    def level_up(self):
        if self.current_node.ancestor is not None:
            self.current_node = self.current_node.ancestor
            return True
        return False

    def _print(self, root, level):
        if root is None:
            return
        print(level*'--' + root.text)
        if len(root.descendants) != 0:
             for descendant in root.descendants:
                 self._print(descendant, level + 1)

    def print(self):
        self._print(self.root, 0)