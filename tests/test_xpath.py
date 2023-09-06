import pytest
from yaxp import xpath as xp


testdata = [
    # basic xpath
    (xp.h1,                  '//h1'),
    (xp.div.h1,              '//div//h1'),

    # full class specification
    (xp.h2.by(_id="huhu"),        '//h2[@id="huhu"]'),

    # direct parent
    (xp.h2.by(_id="huhu", direct=True),        '/h2[@id="huhu"]'),

    # partial-match specification
    (xp.span(_id="*huhu"),  '//span[contains(@id, "huhu")]'),

    # text match exactly
    (xp.span(text="Hello"),  '//span[.="Hello"]'),

    # text match partial
    (xp.span(text="*World"),  '//span[contains(., "World")]'),

    # text match partial
    (xp.span(_id="myid").contains(text="Hello", _class="myclass"),  '//span[@id="myid"][contains(., "Hello")][contains(@class, "myclass")]'),

    # text match partial, _text will be interpreted as "contains the text", only for text attribute
    (xp.span(_text="Hello"),  '//span[contains(., "Hello")]'),

    # word-match specification
    (xp.div(_class="#part"),   '//div[contains(concat(" ", normalize-space(@class), " "), " part ")]'),

    # convert _ to -
    (xp.span(test_id="huhu"), '//span[@test-id="huhu"]'),

    # dont convert _ to -
    (xp.span(_test_id="huhu"), '//span[@test_id="huhu"]'),

    # special case "mixed mode"
    (xp.span(**{'_test_id-id': 'huhu'}), '//span[@test_id-id="huhu"]'),

    # multiple attributes
    (xp.span(_id="myid", value="v1"), '//span[@id="myid"][@value="v1"]'),

    # string as parent
    (xp.span(_id="myid", parent="/div"), '/div//span[@id="myid"]'),

    # xpath as  parent
    (xp.span(_id="myid", parent=xp.div()), '//div//span[@id="myid"]'),
    (xp.by(role="h1", parent=xp.div), '//div//h1'),

    # multiple chaining
    (xp.span(_id="myid", parent=xp.div(parent=xp.body())), '//body//div//span[@id="myid"]'),

    # using "has"
    (xp.span(_id="myid").has(xp.div(_class="bla")), '//span[@id="myid"][.//div[@class="bla"]]'),

    # using "has" with direct descendant
    (xp.span(_id="myid").has(xp.div(_class="bla", direct=True)), '//span[@id="myid"][./div[@class="bla"]]'),

    # using "following"
    (xp.div(_class="myclass").following(xp.span(_id="myid")),
        '//span[@id="myid"]/following-sibling::div[@class="myclass"]'),

    # chaining
    (xp.div().h1(_class="myclass"), '//div//h1[@class="myclass"]'),

    # short chaining
    (xp.div.h1(_class="myclass"), '//div//h1[@class="myclass"]'),

    # roles containing "."
    (xp.Android_Container(_id="huhu"), '//Android.Container[@id="huhu"]'),

    # tags containing "_"
    (xp.Android__Container(_id="huhu"), '//Android_Container[@id="huhu"]'),
]


@pytest.mark.parametrize("xp,xpath", testdata)
def test_xpath(xp, xpath):
    assert str(xp) == xpath
