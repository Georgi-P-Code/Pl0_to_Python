class Scope:

    def __init__(self, parent=None, name=None):

        self.identifiers = {}
        self.inner = []
        self.parent = parent
        self.name = name

        if not parent:
            self.level = 1
        else:
            self.level = parent.level + 1


    def add_identifier(self, identifier_name, identifier_type):
        self.identifiers[identifier_name] = identifier_type


    def add_scope(self, new_scope):
        self.inner.append(new_scope)


    def is_visible(self, identifier_name: str, scope="default"):
        if scope == "default":
            scope = self

        #print(f'is_visible: {identifier_name} in {scope.name}')

        result = self.is_in_scope(identifier_name, scope)

        if result:
            return result

        if scope.parent is None:
            return False

        return self.is_visible(identifier_name, scope.parent)


    def is_in_scope(self, identifier_name: str, scope="default"):
        if scope == "default":
            scope = self

        identifier_type = scope.identifiers.get(identifier_name)

        if identifier_type:
            return {identifier_name: identifier_type}
        else:
            return False


    def _indentation(self):
        return (self.level-1) * "\t"


    def __repr__(self):

        out = {"_": ""}

        def add_line(text: str):
            out["_"] += f"{self._indentation()}{text}\n"

        add_line(f"Name: {self.name} (Level: {self.level})")

        if self.identifiers.keys():
            add_line(f"Identifiers: {self.identifiers}")

        if self.inner:
            add_line(f"Inner: [")
            out["_"] += "\n".join([repr(scope) for scope in self.inner])
            out["_"] += f"{self._indentation()}]\n"

        return out["_"]


if __name__ == '__main__':
    a = Scope(name="global")
    a.add_identifier("zzz", "constant")
    b = Scope(parent=a, name="f1")
    a.add_scope(b)
    c = Scope(parent=b, name="f2")
    b.add_scope(c)

    c.add_identifier("asd", "variable")

    print(a)
    print(c.is_visible("zzz"))
