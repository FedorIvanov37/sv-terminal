from typing import ForwardRef


l = list[ForwardRef("Cl2")]


class Cl1:
    ...

class Cl2:
    ...


lst: l = [Cl1()]
