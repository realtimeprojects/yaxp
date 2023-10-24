# Release notes

## v1.0.0

-   Reworked text handling:
    - `xpath.p(text='...')` will be converted to `//p[text()='...']`
    - `xpath.p(_text='...')` will be converted to `//p[@text='...']`
    - `xpath.p(_='...')` will be converted to `//p[.='...']`
