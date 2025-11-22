# Standard Colors Documentation

## Overview

This documentation page presents the 8-bit color palette supported by terminals in the Rich library (version 14.1.0).

## Key Information

The page includes a comprehensive table displaying 256 colors organized by:
- **Color Number** (0-255)
- **Color Name** (e.g., "black," "red," "bright_blue")
- **Hexadecimal Value** (e.g., #000000, #ff0000)
- **RGB Representation** (e.g., rgb(0,0,0))

## Important Note

The documentation emphasizes that "the first 16 colors are generally defined by the system or your terminal software, and may not display exactly as rendered here." This means the appearance of colors 0-15 varies depending on terminal configuration.

## Color Ranges

The palette consists of:
- **Colors 0-15**: Basic colors (black, red, green, yellow, blue, magenta, cyan, white, and bright variants)
- **Colors 16-231**: Extended 216-color cube with named variations (navy_blue, dodger_blue, chartreuse, etc.)
- **Colors 232-255**: Grayscale gradient from "grey3" (#080808) through "grey100" (#ffffff)

This reference enables developers to use specific color names or numbers when styling terminal output in Rich applications.
