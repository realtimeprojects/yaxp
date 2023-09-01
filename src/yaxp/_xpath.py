class XPG:
    """ Base class for generating xpathes.

        Usually, you don't use the constructor directly, but the xpath instance of the root element
        instead, like in the example in the class description. However, since this will call this
        constructor, all parameters (except tag) can be passed like in the example of the class
        description.

        :param tag:         Tag for the xpath, e.g. `span`, `h1`, etc.
        :param direct:      If set to `True`, the tag must be a direct descendant of the parent element
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
    def __init__(self, tag="*", direct=False, parent=None, **kwargs):
        self._xpath = str(parent) if parent else ""
        self._xpath += "/" if direct else "//"
        self._xpath += tag
        self._xpath += XPG._filter(**kwargs)

    @staticmethod
    def _filter(**kwargs):
        filter = ""
        for arg, values in kwargs.items():
            wildcard = False
            if arg == "_text":
                arg = "text"
                wildcard = True
            if arg[0] == "_":
                arg = arg[1:]
            else:
                arg = arg.replace("_", "-")
            arg = "." if arg == "text" else f"@{arg}"
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
        return filter

    @staticmethod
    def _by_xpath(xpath):
        xp = XPG()
        xp._xpath = xpath
        return xp

    @property
    def xpath(self):
        """ :return: The generated xpath as string """
        return self._xpath

    def __repr__(self):
        return self.xpath

    def has(self, *args):
        """ Nested predicates. Filter for an element that has a specific
            xpath as sub-element, while this xpath still points to the parent
            element.
        """
        _has = ["." + arg.xpath for arg in args]
        return XPG._by_xpath(self.xpath + "[" + " and ".join(_has) + "]")

    def following(self, xpath):
        return f"{xpath}/following-sibling::{self.xpath.lstrip('/')}"

    def contains(self, **kwargs):
        """ Adds a filter for the keyword attributes matching all values
            as a substring.
        """
        for key, value in kwargs.items():
            kwargs[key] = "*" + value
        return XPG._by_xpath(self.xpath + self._filter(**kwargs))

    def __getattr__(self, name):
        if name[0] == "_":
            return super().__getattr__(name)

        def constructor(**kwargs):
            if 'parent' in kwargs:
                parent = str(kwargs['parent']) + self.xpath
                del kwargs['parent']
            else:
                parent = self.xpath
            return XPG(tag=name, parent=parent, **kwargs)

        return constructor
