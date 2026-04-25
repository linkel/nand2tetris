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

    def __str__(self):
        s = ''
        for k,v in self.tables.items():
            s += str(k)
            s += ", "
            s += str(v)
            s += "\n"
        for k,v in self.counters.items():
            s += str(k)
            s += ", "
            s += str(v)
            s += "\n"


        return s
    
    def add_identifier(self, name: str, category: Category):
        table = self.tables[category]
        if name in table:
            raise ValueError(f"{name} already exists for {category}")
        if category == Category.aclass or category == Category.subroutine:
            table[name] = -1 # why am I recording this again for class or subroutine? 
        else:
            table[name] = self.counters[category]
            self.counters[category] += 1

# static - scope class
# field - scope class
# argument - scope subroutine
# var - scope subroutine (method/function/constructor) 
# two separate hash tables, one for class scope and another for subroutine scope 
# you can clear the subroutine scope when a new subroutine is started? what about old one 

    # TODO: need to look in var, arg, then static and field... and is index sufficient, we need category down the line again? 
    def get_index(self, name: str, category: Category):
        try: 
            if category == Category.subroutine or category == Category.aclass:
                return self.tables[category][name]

            if name in self.tables[Category.var]:
                return self.tables[Category.var][name]
            elif name in self.tables[Category.arg]:
                return self.tables[Category.arg][name]
            elif name in self.tables[Category.static]:
                return self.tables[Category.static][name]
            elif name in self.tables[Category.field]:
                return self.tables[Category.field][name]
            
            raise TypeError("Can't find category")
        except KeyError:
            print(self)
            print(f"name: {name}, category: {category}")
            raise
            