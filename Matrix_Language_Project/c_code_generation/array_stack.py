class ArrayStack:
    def __init__(self):
        self.counter = 0
        self.scopes = [[]]

    def init_scope(self):
        self.scopes.append([])

    def handle_request(self, ptr_type, array_repr):
        identifier = "dummy" + str(self.counter)
        self.counter += 1
        self.scopes[-1].append(' '.join([ptr_type, identifier + '[]', '=', array_repr + ';\n']))
        return identifier

    def resume_scope(self, indent):
        resumed = str()
        for array in self.scopes[-1]:
            resumed += '\t' * indent + array
        self.scopes.pop(-1)
        return resumed