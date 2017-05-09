class ParseTreeNode(object):
    def __init__(self, rule_num):
        self.rule = rule_num
        self.descendants = []
        self.ancestor = None


class ParseTreeLeaf(ParseTreeNode):
    def __init__(self, lex_code):
        ParseTreeNode.__init__(self, None)
        self.lex_code = lex_code


class ParseTree(object):
    def __init__(self, grammar_file):
        self.root = None
        self.current_node = None
        self.rules = []
        with open(grammar_file) as f:
            for rule in f:
                self.rules.append(rule.rstrip())

    def add(self, data):
        if isinstance(data, int):
            if self.root is None:
                self.current_node = ParseTreeNode(data)
                self.root = self.current_node
            else:
                ancestor_node = self.current_node
                new_node = ParseTreeNode(data)
                new_node.ancestor = ancestor_node
                self.current_node.descendants.append(new_node)
                self.current_node = new_node
        elif isinstance(data, str):
            ancestor_node = self.current_node
            new_node = ParseTreeLeaf(data)
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
        for i in range(1, level):
            print('      ', end='')
        if root.rule is not None:
            print(self.rules[root.rule - 1])

            if len(root.descendants) != 0:
                for descendant in root.descendants:
                    self._print(descendant, level + 1)
        else:
            print(root.lex_code)

    def print(self):
        self._print(self.root, 1)