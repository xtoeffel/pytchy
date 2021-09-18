# How does it work?

Each _distinct_ color is converted to a symbol. 
The picture is then converted into a symbol plot where each pixel is a 
symbol (the symbol of the pixel color).

Different symbol-sets are supported:

- _default_ - Default symbols like geometric shapes and signs
- *letters* - Upper and lower case letters from `[A-Z][a-z]`
- *filled* - filled symbols
- *skinny* - skinny symbols

The number of supported colors equals the number of
symbols in the symbol set. How many colors a symbol
set supports
can be printed in the command line by:
```bash
./pytchy -s <symbol-set> -m
```
The GUI will show the number of supported colors as a
symbol set is selected.

## *PNG* File
Recommended is to reduce the number of colors to about
`16`, unless you want to challenge yourself.
[Gimp](https://www.gimp.org/) is a great tool for image manipulation just
in case you do not have a favorite yet.

> **Observe**: _Pytchy_ will fail or halt
if the *PNG* contains too many colors. Select
a different symbol-set which supports more colors or reduce the number colors.

As for the colors, the same applies to the size.
Anything above `200 x 200` (width x height) is most likely too big.
Again, unless you like the challenge.

## Output, Cross Stitch Pattern
Stitch pattern files are written in the directory
where the *PNG* file is located.

3 *HTML* files are generated from a *PNG* file:

- color plot
- stitch pattern
- legend (symbol to color)


## Example
The example is based on the *PNG* file `img/Pelican1.png` within
the `pytchy` folder. The file is prepared with colors reduced
to 15 and size set to `70 x 117`. Technically, it has 16 colors
as *transparent* is treated as a *RGBA* color.

This uses the *default* symbol set. For completeness,
first check that the number of supported colors is sufficient.
```bash
./pytchy -s default -m
```
The output reads:
> Maximum permitted number of colors is 64.

To generate the stitch pattern files call:
```bash
./pytchy -p img/Pelican1.png -s default
```
This writes the following files.:

- [img/Pelican1_color_plot.html](example/Pelican1_color_plot.html) - color plot
- [img/Pelican1_stitch_pattern.html](example/Pelican1_stitch_pattern.html) - stitch pattern with symbols
- [img/Pelican1_legend.html](example/Pelican1_legend.html) - color to symbol legend

> __Note__: The _HTML_ files will always be written in the folder of the 
> image file.
