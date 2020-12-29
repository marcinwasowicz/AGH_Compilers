
class VariableSymbol:
    def __init__(self, name, type_info):
        self.name = name
        self.type_info = type_info

class SymbolTable:
    def __init__(self):
        self.scope_list = [["global", {}]]
   
    def put(self, name, type_info): 
        for scope in reversed(self.scope_list):
            if name in scope[1]:
                scope[1][name] = VariableSymbol(name, type_info)
                return
        self.scope_list[0][1][name] = VariableSymbol(name, type_info)
    
    def get(self, name): 
        for scope in reversed(self.scope_list):
            if name in scope[1]:
                return scope[1][name]
        return None
    
    def getCurrScope(self):
        return self.scope_list[0]
    
    def pushScope(self, name):
        self.scope_list.insert(0, [name, {}])
    
    def popScope(self):
        self.scope_list.pop(0)

    def searchScopeOfName(self, names):
        for scope in reversed(self.scope_list):
            if scope[0] in names:
                return scope
        return None
