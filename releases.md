# Release notes

## v1.0.1
> 2024-04-27

-   Fix xpath error when vaues contain a quote (`"`):
    -   Use `'` as delimeter if values contain a quote
    -   Raise an error if values contain both, a single-quote and a double-quote,
        since this is not supported by xpath 1.x

## v1.0.0
> 2023-11-14

-   Reworked text handling:
    - `xpath.p(text='...')` will be converted to `//p[text()='...']`
    - `xpath.p(_text='...')` will be converted to `//p[@text='...']`
    - `xpath.p(_='...')` will be converted to `//p[.='...']`
-   Partual matching: Use pattern `//p[@attribute[contains(., '...')]]` since this
    is more reliable (e.g. for text matching)
