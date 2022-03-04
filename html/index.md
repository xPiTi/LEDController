#LED Controller

Addressable LED Strip controller on Raspberry Pi.  
Please see [wiki page](/help) for more details

#### List of commands:
*Click on a command to see example in action:*

Commands | Paramerters | Note
---------|-------------|------
[/](/a) | n/a | This page
[/help](/help) | n/a | Help page
[/setColor](/setColor?r=100&g=130&b=200&w=50) | [r, g, b, w] from 0 to 255 | Sets the whole strip to specified color values
[/setLeft](/setLeft?r=0&g=0&b=255&w=0) | [r, g, b, w] from 0 to 255 | Sets color to the left alcove
[/setRight](/setRight?r=0&g=255&b=0&w=0) | [r, g, b, w] from 0 to 255 | Sets color to the right alcove
[/setLedColor](/setLedColor?id=1&r=100&g=130&b=200&w=0) | [id] and [r, g, b, w] from 0 to 255| Sets led id to specified color
[/setRaw](/setRaw?data=_wAA_gAA_QAB_QAB) | [data] | String of color values, refer to [Raw color data](/help#raw-color-data) section
[/getColor](/getColor) | n/a | Returns JSON data with color

Made by Pawel Toborek