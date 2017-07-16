# Hermes
Hermes is a markdown to pdf converter designed with customization in mind. It is planned that the user will be able to easily create their own document theme using python. This package is written using python and handles pdf output using reportlab. This enables easy drawing and styles, as well as allowing the user to do more complex manipulation if they require. Currently this is still in heavy development.

## Why Hermes?
Hermes was the greek messenger for the gods, and people use pdfs to store and send information from one another. And this package allows users that ability.

## Running
To run Hermes, simply install reportlab and clone this repo. Then from within cloned directory run:
```shell
./hermes.py filename.md
```
Where `filename.md` is the location of the file. At the current point in time, the output file will be test.pdf and Hermes will use the default template. Support for other templates and file output is planned

# To-do list
- [x] Headers
- [x] Plain Text
- [x] Bullet points
- [x] Internal Links
- [x] External Links
- [x] Title Page
- [x] TOC
- [x] Opening document options
- [ ] Load external files
- [x] Images
- [x] Number Points
- [ ] Control Output File
- [x] BlockQuotes
- [x] Tables
- [x] Captions
- [x] Checklist
- [x] Bold
- [x] Italics
- [x] Inline Code Blocks
- [x] Code Blocks
- [ ] Add wiki pages for how to create custom templates
- [ ] Add wiki pages for markdown
- [x] Header and footer
- [x] Color Text
- [x] Add note block
- [ ] Add support for plantuml