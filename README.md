# yet another xpath generator

Create an xpath with an chainable and intuitive API.

## Quickstart

Create the most simple xpath for a `div` element:

``` python
from yaxp import xpath

# //div
xpath.div
```

xpath objects are chainable:

``` python
# //div//h1
xpath.div.h1
```

Any keyword argument you pass will add a filter for an
attribute with the name and value of the keyword:

``` python
# //div[@role="cell"]
xpath.div(role="cell")
```

Alternatively, use the `by()` method to specify attributes:

``` python
# //*[@class="main"]
xpath.by(_class="main")
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
the following statement is equal to the above:

``` python
# //div[contains(@class, 'mycl')]
xpath.div.contains(_class="mycl")
```

xpath supports "nested predicates", i.e. you can filter for specific sub-elements,
while the xpath itself will point to the parent element (div in this example):

``` python
# //div[./span[@class='mycl']]
xpath.div.has(xpath.span(_class="mycl"))
```

Nested predicates are chainable:

``` python
# //div[./span[@class='mycl'][./p[text()="hello"]]]
xpath.div.has(xpath.span(_class="mycl")).has(xpath.p(text="hello"))
```

As you can see in the example above, a text attribute will be converted to "text()".
In order to avoid this, use "_":

``` python
# //p[@text="hello"]]]
xpath.p(_text="hello"))
```

An "_" attrbute will be converted to ".":

``` python
# //p[contains(., "world")]
xpath.p(_="*world")
```

If the value of an attribute starts with a hashtag (`#`), the xpath matches
any element that has the following text as a *full word* in this attribute:

``` python
# //div[contains(concat(' ', normalize-space(@class), ' '), ' myclass ')]
xpath.div(_class="#myclass")
```

Any combination of the features are allowed:

``` python
# //span[contains(@class, "mycl")][@placeholder="huhu"]
xpath.span(_class="*mycl", _placeholder='huhu')
```

An `_` in the role will be converted to a ".":

``` python
# //Android.Container[@id="huhu"]
xp.Android_Container(_id="huhu")
```

Use double `__` if you need an `_`:

``` python
# //Android_Container[@id="huhu"]
xp.Android__Container(_id="huhu")
```

## Further reading

- [The xpath cheat sheet](https://devhints.io/xpath)

