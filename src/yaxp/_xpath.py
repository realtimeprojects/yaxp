import copy


class XPG:
    """ Base class for generating xpathes.

        Usually, you don't use the constructor directly, but the xpath instance of the root element
        instead, like in the example in the class description. However, since this will call this
        constructor, all parameters (except role) can be passed like in the example of the class
        description.

        :param role:        role for the xpath, e.g. `span`, `h1`, etc.
        :param direct:      If set to `True`, the role must be a direct descendant of the parent element
                            otherwise it can be nested in any sub-element as well.
        :param parent:      If set, this is the xpath of the parent element to search from, otherwise
                            the search starts at the root element of the document. **parent** can either be
                            and x-path string or another `Xpath` object.
        :param **kwargs:    Additional attributes to filter for. The searched elements needs to match all
                            of the given attributes. See the example in the class description for further details.
                            An _ at the beginning will be removed. This allows to filter for reseved keywords
                            like `class` as attributes using:
                            `Xpath.h5(_class="#title")`
    """
    def __init__(self, role=None, parent=None):
        self._parent = str(parent) if parent else ""
        self._role = role
        self._filter = []
        self._direct = False

    def by(self, **kwargs):
        role = copy.copy(self._role) if self._role else "*"
        filter = copy.copy(self._filter)
        parent = copy.copy(self._parent)
        direct = copy.copy(self._direct)

        _xp = XPG(role, parent)
        _xp._filter = filter
        _xp._direct = direct
        _xp._add_filter(**kwargs)
        return _xp

    def __call__(self, **kwargs):
        self._add_filter(**kwargs)
        return self

    def _add_filter(self, **kwargs):
        filter = ""
        for arg, values in kwargs.items():
            if arg == "direct":
                self._direct = values
                continue
            if arg == "parent":
                self._parent = str(values)
                continue
            if arg == "role":
                self._role = values
                continue
            wildcard = False
            force_text = False
            if arg == "_text":
                force_text = True
            if arg[0] == "_":
                arg = arg[1:]
            else:
                arg = arg.replace("_", "-")
            arg = "." if arg == "text" and not force_text else f"@{arg}"
            if not values:
                continue
            if not isinstance(values, list):
                values = [values]
            for value in values:
                if wildcard:
                    filter += f'[contains({arg}, "{value}")]'
                elif value[0] == "*":
                    filter += f'[contains({arg}, "{value[1:]}")]'
                elif value[0] == "#":
                    filter += f'[contains(concat(" ", normalize-space({arg}), " "), " {value[1:]} ")]'
                else:
                    filter += f'[{arg}="{value}"]'
        self._filter.append(filter)

    @staticmethod
    def _by_xpath(xpath):
        return XPG(role=xpath)

    @property
    def xpath(self):
        return self._xpath()

    def get_xpath(self):
        """ :return: The generated xpath as string """
        _xp = str(self._parent) if self._parent else ""
        pre = "/" if self._direct else "//"
        _xp += pre + self._role if self._role else ""
        for _f in self._filter:
            _xp += _f
        return _xp

    def __repr__(self):
        return self.get_xpath()

    def has(self, *args):
        """ Nested predicates. Filter for an element that has a specific
            xpath as sub-element, while this xpath still points to the parent
            element.
        """
        _has = ["." + str(arg) for arg in args]
        self._filter.append("[" + " and ".join(_has) + "]")
        return self

    def following(self, xpath):
        return f"{xpath}/following-sibling::{self.get_xpath().lstrip('/')}"

    def contains(self, **kwargs):
        """ Adds a filter for the keyword attributes matching all values
            as a substring.
        """
        for key, value in kwargs.items():
            kwargs[key] = "*" + value
        self._add_filter(**kwargs)
        return self

    def __getattr__(self, name):
        if name[0] == "_":
            name = name[1:]
        name = name.replace("_", ".")
        name = name.replace("..", "_")

        return XPG(name, parent=self)
