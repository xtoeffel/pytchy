# How does it work?

Each color is converted to a symbol. The picture is then converted into a 
symbol plot where each pixel is a symbol (the symbol of the pixel color).

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

> **Observe**: `Pytchy` will fail or halt
if the *PNG* contains too many colors. Select
a different symbol-set which supports more colors or reduce the number colors.

As for the colors, the same applies to the size.
Anything above `200 x 200` (width x height) is most likely too big.
Again, unless you like the challenge.

## Output, Cross Stitch Pattern
Stitch pattern files are written in the directory
where the *PNG* file is located.

3 *HTML* files are generated from a *PNG* file:
- color pattern
- stitch pattern
- legend (symbol to color)


## Example
The example is based on the *PNG* file `img/Pelican1.png` within
the `pytchy` folder. The file is prepared with colors reduced
to 15 and size set to `70 x 117`. Technically, it has 16 colors
as *transparent* is treated as a *RGBA* color.

This uses the *letters* symbol set. For completeness,
first check that the number of supported colors is sufficient.
```
./pytchy -s letters -m
```
The output reads:
> Maximum permitted number of colors is 52.

To generate the stitch pattern files call:
```
./pytchy -p img/Pelican1.png -s letters
```
This writes the following files:

- `img/Pelican1_color_pattern.html` - color plot
- `img/Pelican1_stitch_pattern.html` - stitch pattern with symbols
- `img/Pelican1_legend.html` - color to symbol legend
