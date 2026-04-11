from JackTokenizer import Category


class SymbolTable:
    def __init__(self):
        self.tables = {
            Category.field: {},
            Category.static: {},
            Category.var: {},
            Category.arg: {},
            Category.aclass: {},
            Category.subroutine: {}
        }
        self.counters = {
            Category.field: 0,
            Category.static: 0,
            Category.var: 0,
            Category.arg: 0,
        }

    def add_identifier(self, name: str, category: Category):
        table = self.tables[category]
        if name in table:
            raise ValueError(f"{name} already exists for {category}")
        if category == Category.aclass or category == Category.subroutine:
            table[name] = -1 # why am I recording this again for class or subroutine? 
        else:
            table[name] = self.counters[category]
            self.counters[category] += 1

    # TODO: need to look in var, arg, then static and field... and is index sufficient, we need category down the line again? 
    def get_index(self, name: str, category: Category):
        return self.tables[category][name]
