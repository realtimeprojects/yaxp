# Release notes

## v1.0.0
>   v1.1.0a1

-   Reworked text handling:
    - `xpath.p(text='...')` will be converted to `//p[text()='...']`
    - `xpath.p(_text='...')` will be converted to `//p[@text='...']`
    - `xpath.p(_='...')` will be converted to `//p[.='...']`
-   Partual matching: Use pattern `//p[@attribute[contains(., '...')]]` since this
    is more reliable (e.g. for text matching)
