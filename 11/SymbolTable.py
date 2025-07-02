from JackTokenizer import Category


class SymbolTable:
    def __init__(self):
        self.fields = {}
        self.fields_counter = 0
        self.statics = {}
        self.statics_counter = 0
        self.vars = {}
        self.vars_counter = 0
        self.args = {}
        self.args_counter = 0
        self.classes_or_subroutines = {}

    def add_to_dict_or_counter(self, name, dic: dict, counter: int = None):
        if name in dic:
            raise ValueError("Already exists!")
        if counter:
            dic[name] = counter
            prev_counter = counter
            counter += 1
            return prev_counter
        else:
            dic[name] = -1

    def add_identifier(self, name: str, category: Category):
        if category == Category.field:
            self.add_to_dict_or_counter(name, self.fields, self.fields_counter)
        elif category == Category.static:
            self.add_to_dict_or_counter(name, self.statics, self.statics_counter)
        elif category == Category.var:
            self.add_to_dict_or_counter(name, self.vars, self.vars_counter)
        elif category == Category.arg:
            self.add_to_dict_or_counter(name, self.vars, self.vars_counter)
        elif category == Category.aclass:
            self.add_to_dict_or_counter(name, self.vars)
        elif category == Category.subroutine:
            self.add_to_dict_or_counter(name, self.vars)
        else:
            raise ValueError("Category not found")

    def get_index(self, name: str, category: Category):
        if category == Category.field:
            return self.fields[name]
        elif category == Category.static:
            return self.statics[name]
        elif category == Category.var:
            # does this need to handle field, static or var??
            if name in self.fields:
                return self.fields[name]
            elif name in self.statics:
                return self.statics[name]
            elif name in self.vars:
                return self.vars[name]
            else:
                raise ValueError("should never get here")
        elif category == Category.arg:
            return self.args[name]
        # classes and subroutines don't have indexes
        elif category == Category.aclass:
            return self.classes_or_subroutines[name]
        elif category == Category.subroutine:
            return self.classes_or_subroutines[name]
        else:
            raise ValueError("Category not found")
