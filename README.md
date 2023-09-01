# yet another xpath generator

Create an xpath with an chainable and intuitive API.

## Quickstart

Create the most simple xpath for a `div` element:

    ``` python
    from yaxp import xpath

    # //div
    xpath.div()
    ```

Any keyword argument you pass will add a filter for an
attribute with the name and value of the keyword:

    ``` python
    # //div[@role="cell"]
    xpath.div(role="cell")
    ```

An `_` at the beginning of the attribute name will be
removed, this is helpful for attributes that represents
python keywords like "class" or "id":


    ``` python
    # //div[@class="cell"][@id="myid"]
    xpath.div(_class="cell", _id="myid")
    ```

If the value of an attribute starts with an asteric (`*`), the xpath matches
any element that has the following text as a substring in this attribute

    ``` python
    # //div[contains(@class, 'mycl')]
    xpath.div(_class="*mycl")               
    ```

Alternatively, you can use the `contains()` function to filter for subtrings.
the following statement is equal to the above

    ``` python
    xpath.div().contains(_class="mycl")    # //div[contains(@class, 'mycl')]
    ```

xpath supports "nested predicates", i.e. you can filter for specific sub-elements,
while the xpath itself will point to the parent element (div in this example).

    ``` python
    # //div[./span[@class='mycl']]
    xpath.div().has(xpath.span(_class="mycl"))
    ```

Nested predicates are chainable:

    ``` python
    # //div[./span[@class='mycl'][./p[.="hello"]]]
    xpath.div().has(xpath.span(_class="mycl")).has(xpath.p(text="hello"))
    ```

If the value of an attribute starts with a hashtag (`#`), the xpath matches
any element that has the following text as a *full word* in this attribute.

    ``` python
    # //div[contains(concat(' ', normalize-space(@class), ' '), ' myclass ')]
    Xpath.div(_class="#myclass")
    ```

Any combination of the features are allowed:

    ``` python
    # //span[contains(@class, "mycl")][@placeholder="huhu"]
    Xpath.span(_class="*mycl", _placeholder='huhu')
    ```

## Further reading

- [The xpath cheat sheet](https://devhints.io/xpath)

