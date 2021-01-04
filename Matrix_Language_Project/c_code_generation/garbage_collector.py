from frontend import symbol_table

class GarbageCollector:
    def __init__(self):
        self.reference_groups = []
        self.variables = {}

    def init_reference(self, name):
        self.reference_groups.append(set([name]))
        self.variables[name] = self.reference_groups[-1]

    def remove_reference(self, name):
        group = self.variables[name]
        del self.variables[name]
        group.remove(name)
        if group == set():
            return ''.join(['free_matrix(', name, ');\n'])

    def add_reference(self, name, ref):
        group = self.variables[ref]
        group.add(name)
        self.variables[name] = group

    def reassign_reference(self, name, ref, type_size, symbol_table: symbol_table.SymbolTable):
        remove_ret_val = self.remove_reference(name)
        self.add_reference(name, ref)
        symbol_table.get(name).type_info = type_size
        return remove_ret_val

    def reinit_reference(self, name, type_size, symbol_table: symbol_table.SymbolTable):
        remove_ret_val = self.remove_reference(name)
        self.init_reference(name)
        symbol_table.get(name).type_info = type_size
        return remove_ret_val

    def purify_curr_scope(self, curr_scope, indent):
        result = str()
        for var in [var_fltr for var_fltr in curr_scope[1] if var_fltr in self.variables]:
            retval = self.remove_reference(var)
            if retval is not None:
                result += '\t'*indent + retval
        return result

    

    