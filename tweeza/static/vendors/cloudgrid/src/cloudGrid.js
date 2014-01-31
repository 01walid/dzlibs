(function() {
    /**
     * Enable .cloudGrid on jQuery objects.
     *
     * If the grid is being initialized, `gridArgs` is a dictionary of options
     * that defines how the grid should behave and be displayed.
     *
     * If the grid has already been initialized, `gridArgs` is a string that is
     * the name of the method to be called on the grid. The arguments passed to
     * that method are the remaining arguments passed to this method.
     *
     * All the references to the grid are stored in the variable `grid` (defined
     * below).
     *
     * @params {Object} gridArgs The arguments sent to the grid.
     */
    $.fn.cloudGrid = function(gridArgs) {
        if (typeof(arguments[0]) === 'string') {
            var _arguments = arguments;
            this.each(function() {
                var grid = grids[uniqueGridId(this)];
                if (grid) {
                    grid[gridArgs].apply(grid,
                        Array.prototype.slice.call(_arguments, 1));
                }
            });
        } else {
            this.each(function() {
                gridArgs.container = this;
                grids[uniqueGridId(this)] = new CloudGrid(gridArgs);
            });
        }
        return this;
    };

    /**
     * Grid class.
     *
     * The grid follows a matrix model in which each cell has the same height
     * and width (`gridSize`). The distance between each cell is the same across
     * the grid (`gridGutter`).
     *
     * An element in the grid can use more than one cell but is always
     * rectangular; for example, the dimensions 1x2, 2x1, and 3x3 are all
     * valid. The grid will make a best effort at fitting in all elements but
     * drops elements if keeping them would leave empty cells in the grid. These
     * elements are hidden but not removed from the DOM, and resizing the grid
     * such that those elements would fit brings them back into view.
     *
     * It's rare that elements will be hidden, but tends to happen more
     * frequently if elements are very wide.
     *
     * @params {{
     *      container: (Element),
     *      children: (Array.<Element>),
     *      gridSize: (number),
     *      gridGutter: (number),
     *      setChildPosition: (Function|null|undefined),
     *      setChildProperties: (Function|null|undefined)
     * }} options .container The element that contains the grid. This element
     *                  is set automatically.
     *            .children All the elements that the grid will attempt to
     *                  display.
     *            .gridSize The width/height of each grid cell (a grid cell is
     *                  always a square). This is also the width of each grid
     *                  column.
     *             .gridGutter The distance between cells, which is also the
     *                  distance between elements in the grid and between
     *                  columns.
     *             .setChildPosition Optional method used to position
     *                  children. By default children are positioned using the
     *                  standard jQuery css method.
     *             .setChildProperties Optional method used to change the width
     *                  and height of the children.
     * @constructor
     */
    var CloudGrid = function(options) {
        this.options = {
            $container: $(options.container),
            children: options.children,
            gridSize: options.gridSize,
            gridGutter: options.gridGutter,
            setChildPosition: options.setChildPosition,
            setChildProperties: options.setChildProperties
        };

        if (this.options.children.length) {
            this.reflowContent();
        }

        if (options.onInitialized) {
            var self = this;
            _.defer(function() {
                options.onInitialized.apply(self);
            });
        }
    };

    /**
     * Reflow the content of the grid.
     *
     * Note: For performance reasons, the grid does not listen to changes in the
     * window size. If you want the grid to resize and reflow its contents when
     * the user resizes the window, you will need to attach an event in your
     * application and request the grid to reflow.
     *
     * @code
     *      $(window).on('resize', _.bind(function() {
     *          $('.container').grid('reflowContent');
     *      }, 10));
     */
    CloudGrid.prototype.reflowContent = function() {
        this._createColumns();

        for (var i=0; i < this.options.children.length; i++) {
            this._positionChild(this.options.children[i], i);
        }

        var containerHeight = 0;
        var height;
        for (var i=0; i < this._columns.length; i++) {
            height = this._columns[i].height;
            if (height > containerHeight) {
                containerHeight = height;
            }
        }

        this.options.$container.css({'height': containerHeight});
    };

    /**
     * Create columns and resize the container.
     *
     * The number of columns is calculated based on the width of the
     * container. After calculating the number of columns, the container is
     * shrunk to fit the columns.
     *
     * @private
     */
    CloudGrid.prototype._createColumns = function() {
        // Remove the applied width to the container so the calculation of the
        // width is based on the width the element can actually use.
        this.options.$container.css({'width': 'auto'});

        var containerWidth = this.options.$container.width();
        var columnCount = Math.floor(containerWidth / (this.options.gridSize + this.options.gridGutter));
        this.options.$container.css({
            width: columnCount * (this.options.gridSize + this.options.gridGutter) - this.options.gridGutter
        });

        this._columns = [];
        this._currentColumn = 0;
        for(var i=0; i < columnCount; i++) {
            this._columns[i] = new CloudGridColumn(i, this);
        }
    };

    /**
     * Position a child.
     *
     * A child can be displayed over more than one column, so the logic
     * remembers several sets of columns that would be a match (they share the
     * same height). Once we have looped over all our columns, we analyze the
     * set of columns and find the one that has the smallest height.
     *
     * @param {Element} child The reference to the child element.
     * @param {number} childIndex The child index within the grid.
     * @private
     */
    CloudGrid.prototype._positionChild = function(child, childIndex) {
        var columnMatches = [[]];
        var columnMatchesCursor = 0;
        var columnCount = this._columns.length;
        var currentColumnHeight = this._columns[this._currentColumn].height;
        var requiredColumns = $.data(child, 'grid-columns') || 1;
        var i;

        for (i=this._currentColumn; i < (columnCount + this._currentColumn); i++) {
            var index = i % columnCount;

            // If we go from the last column to the first column, we empty the
            // current set of columns.
            if (index === 0) {
                columnMatches[columnMatchesCursor] = [];
            }

            // Columns sharing the same height should be added to the current
            // match.  If the number of columns in the match correspond to the
            // number of columns necessary to display the item, we create a new
            // set.
            if (this._columns[index].height == currentColumnHeight) {
                if (columnMatches[columnMatchesCursor].length < requiredColumns) {
                    columnMatches[columnMatchesCursor].push(this._columns[index]);
                }

                if (columnMatches[columnMatchesCursor].length == requiredColumns) {
                    columnMatchesCursor++;
                    columnMatches[columnMatchesCursor] = [];
                }
            } else {
                columnMatches[columnMatchesCursor] = [this._columns[index]];
                currentColumnHeight = this._columns[index].height;
            }
        }

        // Find the best match in our set of columns. The best match will be the set
        // of columns that has the smallest height.
        var bestColumnMatch = columnMatches[0];
        for (i=1; i < columnMatches.length; i++) {
            if (columnMatches[i].length !== requiredColumns) {
                continue;
            }

            if (columnMatches[i][0].height < bestColumnMatch[0].height) {
                bestColumnMatch = columnMatches[i];
            }
        }

        // If the required number of columns doesn't match - we early return. There are no
        // easy solution at the moment, and this issue only happens when an element has a
        // number of required columns too big.
        if (bestColumnMatch.length != requiredColumns) {
            $(child).hide();
            return;
        }

        // Add the element into the columns.
        for (var columnIndex=0; columnIndex < bestColumnMatch.length; columnIndex++) {
            bestColumnMatch[columnIndex].addChild(child, columnIndex  === 0, childIndex);
        }

        this._setChildProperties(child, childIndex);
        this._recalculateSmallestColumn();
    };

    /**
     * Set the visual properties of a child.
     *
     * If you want to apply animations, or any kind of treatment, you can do it by
     * overriding the `setChildProperty` option.
     *
     * @param {Element} child The child element.
     * @param {number} childIndex The position of the child within the grid.
     */
    CloudGrid.prototype._setChildProperties = function(child, childIndex) {
        var gridColumnAttr = 'grid-columns';
        var gridRowsAttr = 'grid-rows';

        var properties = {
            width: this._getDimensionFromSize(
                $.data(child, gridColumnAttr) || $(child).attr('data-' + gridColumnAttr)) || 1,
            height: this._getDimensionFromSize(
                $.data(child, gridRowsAttr) || $(child).attr('data-' + gridRowsAttr)) || 1
        };

        if (this.options.setChildProperties) {
            this.options.setChildProperties(child, properties, childIndex);
        }
        else {
            $(child).css(properties);
        }
    };

    /**
     * Get the dimension from a size.
     *
     * @param {number} size The size that will be used to calculate the dimension.
     * @return {number}
     */
    CloudGrid.prototype._getDimensionFromSize = function(size) {
        return size * this.options.gridSize + (size - 1) * this.options.gridGutter;
    };

    /**
     * Recalculate the smallest column.
     *
     * @private
     */
    CloudGrid.prototype._recalculateSmallestColumn = function() {
        this._currentColumn = 0;

        var columnCount = this._columns.length;
        var smallestColumn = this._columns[this._currentColumn];

        for (var id = 1; id < columnCount; id++) {
            if (this._columns[id].height < this._columns[this._currentColumn].height) {
                this._currentColumn = id;
            }
        }
    };

    /**
     * Change/alter the options.
     *
     * @code
     *      $('.gridContainer').grid('setOptions', {...options...});
     *
     * @param {Object.<string, *>} options The new options.
     */
    CloudGrid.prototype.setOptions = function(options) {
        _.each(options, function(fn, key) {
            this.options[key] = fn;
        }, this);
    };

    /**
     * Representation of a column in the grid.
     *
     * @param {number} id The grid id.
     * @param {Grid} grid The reference to the grid that contains the column.
     * @constructor
     */
    var CloudGridColumn = function(id, grid) {
        /**
         * Index of the column.
         *
         * @type {number}
         */
        this.id = id;

        /**
         * Children that are contained in the column.
         *
         * @type {Array.<Element>}
         */
        this.children = [];

        /**
         * Current height of the column.
         *
         * @type {number}
         */
        this.height = 0;

        /**
         * Reference to the grid parent.
         *
         * @type {Grid}
         */
        this.grid = grid;
    };

    /**
     * Add a child to the column.
     *
     * If this column is the first column for the child, then the child is
     * positioned in the screen.
     *
     * If you want to apply an animation, or any other treatment, on how the
     * child is being positioned, you can override the grid option
     * `setChildPosition`.
     *
     * @param {Element} child The child to add to the element.
     * @param {boolean} position Flag if the element needs to be positioned or just
     *      need to be added to the grid.
     */
    CloudGridColumn.prototype.addChild = function(child, position, childIndex) {
        var gridOptions = this.grid.options;
        this.children.push(child);

        if (position) {
            var cssPosition = {
                'left': this.id * (gridOptions.gridSize + gridOptions.gridGutter),
                'top': this.height,
                'display': 'block'
            };

            if (gridOptions.setChildPosition) {
                gridOptions.setChildPosition(child, cssPosition, childIndex);
            } else {
                $(child).css(cssPosition);
            }
        }

        this.height = this.height + this.calculateElementHeight(child) + gridOptions.gridGutter;
    };

    /**
     * Calculate the height of a child element.
     *
     * @param {Element} child The child element.
     * @return {number}
     */
    CloudGridColumn.prototype.calculateElementHeight = function(child) {
        var gridOptions = this.grid.options;
        var columns = $.data(child, 'grid-rows');
        return columns * gridOptions.gridSize + gridOptions.gridGutter * (columns - 1);
    };

    /**
     * Reference to all the grids currently set.
     *
     * @type {Object.<number, CloudGrid>}
     */
    var grids = {};

    /**
     * Retrieve the unique id of an element that contains a grid.
     *
     * @param {Element} el The element that contains the grid.
     * @return {number}
     */
    var uniqueGridId = function(el) {
        var $el = $(el);
        var gridId = $el.attr('grid-id');
        if (gridId === undefined) {
            gridId = _.size(grids.length);
            $el.attr('grid-id', gridId);
        }
        return gridId;
    };
}());