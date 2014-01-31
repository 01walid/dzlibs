# jQuery.cloudGrid

* Licence: `MIT`. 
* [See Example](http://rawgithub.com/pinterest/cloudgrid/master/example/index.html)

`jQuery.cloudGrid` is a lightweight [`jQuery`](http://jquery.com) plugin that positions elements within a grid.

The grid follows a matrix model in which each cell has the same height and width (`gridSize`). The distance between each cell is the same across the grid (`gridGutter`).

An element in the grid can be more than one cell wide and/or be more than one cell tall but is always rectangular; for example, the dimensions 1x2, 2x1, and 3x3 are all valid. The grid will make a best effort at fitting in all elements but drops elements if keeping them would leave empty cells in the grid. These elements are hidden but not removed from the DOM.  Resizing the grid such that those elements would fit brings them back into view.
     
It's rare that elements will be hidden, but tends to happen more frequently if elements are very wide. For example:

```
+-----------------------------------------------------------+
|                                                           |
|  +----------+  +----------+  +----------+  +----------+   |
|  |          |  |          |  |          |  |          |   |
|  |          |  |          |  |          |  |          |   |
|  |          |  |          |  |          |  |          |   |
|  |          |  |          |  |          |  |          |   |
|  |          |  |          |  +----------+  |          |   |        
|  |          |  |          |                |          |   |
|  |          |  |          |                |          |   |
|  |          |  |          |                |          |   |
|  |          |  |          |                |          |   |
|  +----------+  +----------+                +----------+   |
|                                                           |
|  +--------------------------------------+                 |
|  |  This child does not fit without     |                 |
|  |  leaving white spaces, so it will    |                 |
|  |  be removed.                         |                 |        
|  |                                      |                 |
|  +--------------------------------------+                 |
+-----------------------------------------------------------+
```

## Requires

* UnderscoreJs: http://underscorejs.org/
* jQuery: http://jquery.com

## Instructions

All you need to do is instantiate a new grid and pass it a valid option:

For example: 

```html
<div class="grid">
	<div class="gridItem"></div>
	<div class="gridItem"></div>
	...
</div>
```

```js
var $grid = $('.grid');
$grid.cloudGrid({
	gridSize: 60,
	gridGutter: 13,
	children: $grid.children('.gridItem')
});
```

Each item in the grid needs to have its dimensions (`grid-rows`, `grid-columns`) specified. You can either attach the number of columns and rows using data attributes (`data-grid-grows`, `data-grid-columns`) or attach them to the DOM element directly by using `[$.data](http://api.jquery.com/jQuery.data/)`.


## Options

### children

Type: `$`

All the elements that the grid will attempt to display.

### gridSize

Type: `number`

The width/height of each grid cell in CSS pixels (a grid cell is always a square). This is also the width of each grid column.

### gridGutter

Type: `number`

The distance between cells in CSS pixels.

### setChildPosition

Type: `function(child: Element, cssProperties: {top: Number, left: Number, display: string}, childIndex: number)` Default: `null`

Used to position children. By default children are positioned using the standard jQuery css method. 

__Note:__

After calculating the position of a child, the element is immediately positioned. If you want to apply an animation, or any other treatment, on how the child is being positioned, you can override the grid option `setChildPosition`.

### setChildProperties

Type: `function(child: Element, properties: {width: number, height: number}, childIndex: number)` Default: `null`

Used to initialize the width and height of the children.


## Methods

### reflowContent

Reflow the content of the grid. For performance reasons, the grid does not listen to changes in the window size. If you want the grid to resize and reflow its contents when the user resizes the window, you will need to attach an event in your application and request the grid to reflow.

Example:  

```js
$(window).on('resize', function() {
	$grid.cloudGrid('reflowContent');		
});
```

## Author

* Michael Ortali ([@xethorn](https://github.com/xethorn))
