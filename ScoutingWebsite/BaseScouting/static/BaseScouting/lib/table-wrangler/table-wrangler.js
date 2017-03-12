(function($) {

    /**
     * Sort by and/or filter a column
     * @param fieldOptions - FilterTarget field options for the column to filter, with the addition
     * @param colname {string} - colname for the th on the row to sort
     * @param search - Search query
     * @param method - Type of comparrison to do
     -------------------------- OLD
     * @param options.type {string} - Content type, either number or custom
     * @param options.target - th of the column being filtered
     * @param options.sort {string} - Sort direction, either asc or desc
     * @param options.sortMethod {function(a,b)} - If passed, called and determines whether a is higher than b
     * @param options.search - Search query
     * @param options.searchMethod {string|function(o, search)} - Type of search to do (based on type),
     *                                                            or function returning whether o is displayed
     *                                                            for the given search
     * @param options.multi {boolean} - Whether or not there are multiple values in the cells for the column,
     *                                  triggering the related handling
     ---------------------------
     */
    function doFilter(fieldOptions, colname, search, method, sort, table) {

        var colIndex = $(table).find("[data-colname=" + colname + "]").index() + 1;

        // Filter
        $(table).find("tbody tr").each(function() {
            var $this = $(this);

            var value = $this.find("td:nth-child(" + colIndex + ")");
            if (fieldOptions.selector) value = value.find(fieldOptions.selector);
            value = fieldOptions.getVal ? fieldOptions.getVal(value) : value.text().trim();
            if (fieldOptions.type == "number" && search) {
                value = parseFloat(value);
                search = parseFloat(search);
            }

            var pass = false;
            switch (method) {
                case "eq":
                    if (value == search) pass = true
                    break;
                case "gt":
                    if (value > search) pass = true;
                    break;
                case "lt":
                    if (value < search) pass = true;
                    break;
                case "gteq":
                    if (value >= search) pass = true;
                    break;
                case "lteq":
                    if (value <= search) pass = true;
                    break;
                case "contains":
                    if (value.indexOf(search) != -1) pass = true;
                    break;
                case "oneof":
                    if (search.indexOf(value) != -1) pass = true;
                    break;
            }
            
            // TODO: Should probably make sure commas are escaped
            var filterID = "," + "-" + (fieldOptions.name||'');

            if (pass || search === '' || search === undefined || search.length === 0) {
                if ($this.data("filteredBy").indexOf(filterID) !== -1) {
                    $this.data("filteredBy", $this.data("filteredBy").replace(filterID, ''));
                    if (!$this.data("filteredBy")) $this.css("display", "");
                }
            } else {
                if (!$this.data("filteredBy")) $this.css("display", "none");
                if ($this.data("filteredBy").indexOf(filterID) === -1) {
                    $this.data("filteredBy", ($this.data("filteredBy")) + filterID);
                }
            }
        });
        
        if (sort === '' || sort === undefined) return;
        
        $(table).find("tbody td:nth-child(" + colIndex + ")").sortElements(function(a, b) {
            
            a = $(a);
            b = $(b);
            
            var oA = a.parent().find("td").eq(0).text();
            var oB = b.parent().find("td").eq(0).text();
            
            if (fieldOptions.selector) {
                a = a.find(fieldOptions.selector);
                b = b.find(fieldOptions.selector);
            }

            if (fieldOptions.getVal) {
                a = fieldOptions.getVal(a);
                b = fieldOptions.getVal(b);
            } else {
                a = a.text().trim();
                b = b.text().trim();
            }

            if (fieldOptions.type == "number") {
                a = parseFloat(a);
                b = parseFloat(b);
            }
            
            if (fieldOptions.type == "choice") {
                var aIndex = fieldOptions.choices.indexOf(a);
                var bIndex = fieldOptions.choices.indexOf(b);
                
                if (sort == "asc") {
                    return aIndex > bIndex ? 1 : -1;
                }
                if (sort == "desc") {
                    return aIndex < bIndex ? 1 : -1;
                }
            } else {
                if (sort == "asc") {
                    return a > b ? 1 : -1;
                }
                if (sort == "desc") {
                    return a < b ? 1 : -1;
                }
            }
            
        }, function() {
            return this.parentNode;
        });
    }

    /**
     * Base popover initialization
     * @param target {(string|element)} - jQuery selector for the element triggering the popover
     * @param title {(string|element)} - The content to be palced in the popover title
     * @param content {(string|element)} - The content to be placed in the popover
     * @param table {(string|element)} - jQuery selector for the table being filtered
     * @param onDisplay {function} - Function to be called for implementation-specific actions when target is clicked,
     *                               and after the popover is shown
     */
    function initPopover(target, title, content, table, onDisplay) {
        $(target).popover({
            trigger: "manual",
            html: true,
            animation: false,
            placement: "bottom",
            container: "body",
            title: title,
            content: content
        }).click(function() {
            // The content of bs.popover is the live popover object, and tip() returns the jQuery object of the popover
            var popover = $(this).data('bs.popover').tip();

            // Remove old popovers
            $('.popover').popover("hide");
            // Show popover
            $(this).popover("show");
            // On cancel
            popover.find(".btn-cancel").click(function() {
                $(target).popover('hide');
            });
            onDisplay(popover);
        });
    }

    /**
     * Initialize the popover for column selection
     * @param target {(string|element)} - jQuery selector for the element triggering the popover
     * @param content {(string|element)} - The content to be placed in the popover
     * @param table {(string|element)} - jQuery selector for the table being filtered
     */
    function initColSelect(target, content, table) {
        var title = '<div style="font-weight: bold;">Filter Columns</div>';

        initPopover(target, title, content, table, function(popover) {
            // Fill remembered values
            popover.find("input[type='checkbox']").each(function() {
                if ($(table).find("th[data-colname=" + $(this).data("target") + "]").css("display") != "none") {
                    $(this).prop("checked", true);
                }
            });

            // On apply - show/hide columns
            popover.find(".btn-apply").click(function() {
                popover.find("input[type='checkbox']").each(function() {
                    // Get column number of the header corresponding with the checkbox
                    var colnum = $(table).find("th[data-colname=" + $(this).data("target") + "]").index() + 1;

                    // Show/hide the given header and cells in the same column
                    if (!$(this).prop("checked")) {
                        $(table).find('td:nth-child(' + colnum + '),th:nth-child(' + colnum + ')').hide();
                    } else {
                        $(table).find('td:nth-child(' + colnum + '),th:nth-child(' + colnum + ')').show();
                    }
                });
                $(target).popover('hide');
            });
        }.bind(this));
    }

    /**
     * Initialize the popover for filter selection
     * @param target {(string|element)} - jQuery selector for the element triggering the popover
     * @param content {(string|element)} - The content to be placed in the popover
     * @param table {(string|element)} - jQuery selector for the table being filtered
     */
    function initFilter(target, content, targetOptions, table) {
        var title = '<div style="font-weight: bold">Filter ' + $(target).text() + '</div>';

        target.css("cursor", "pointer").css("cursor", "hand");

        initPopover(target, title, content, table, function(popover) {
            // Initialize bootstrap-select styling for select elements
            popover.find('.selectpicker').selectpicker({
                style: 'btn-default',
                size: false
            });

            // Only one sort option should be selected at a given time
            $('.selectpicker').on('hidden.bs.select', function(e) {
                $('.selectpicker[name^=sort-]').not(this).selectpicker('val', null);
            });
            
            // Radio buttons should be unselectable and update when the button is clicked
            popover.find(".btn-radio").click(function(e){
                if ($(this).hasClass("active")) {
                    $(this).removeClass('active').children("input").attr('checked', false);
                } else {
                    $(this).addClass('active').children("input").attr('checked', true);
                    $(this).siblings().removeClass('active').attr('checked', false);
                }
                e.preventDefault()
            });
            
            // Fill remembered values
            popover.find('[name]').each(function() {
                var $this = $(this);
                var oldVal = $(target).data("filter-previous-" + $this.prop("name"));
                //console.log("filter-previous-" + $this.prop("name"));
                if ($this.hasClass("selectpicker")) {
                    if ($this.prop("name").startsWith("sort-") && !$(target).data("filter-active-sort")) {
                        return;
                    }
                    $this.selectpicker('val', oldVal);
                } else if ($this.attr("type") == "radio") {
                    //console.log(this);
                    //console.log(oldVal);
                    //console.log($this.data("value"));
                    if (oldVal === $this.data("value")) {
                        $this.val(oldVal);
                        $this.parent().addClass("active");
                    }
                } else {
                    $this.val(oldVal);
                }
            });

            // On apply - filter/sort
            popover.find(".btn-apply").click(function() {
                
                var fields = targetOptions.multi || [targetOptions];
                for (var i = 0; i < fields.length; i++) {
                    var method;
                    var name = fields[i].name || '';
                    switch (fields[i].type) {
                        case "number":
                            method = popover.find("[name=method-" + name + "]").val();
                            break;
                        case "string":
                            method = "contains";
                            break;
                        case "boolean":
                            method = "eq";
                            break;
                        case "choice":
                            method = "oneof";
                            break;
                    }
                    
                    var search;
                    if (fields[i].type == "boolean") {
                        var checked = popover.find("[name='search-" + name + "']:checked");
                        search = checked.data("value") || '';
                    } else {
                        search = popover.find("[name='search-" + name + "']").val();
                    }
                    var sort = popover.find("[name='sort-" + name + "']").val();
                    
                    // Store old values
                    $(target).data("filter-previous-search-" + name, search);
                    $(target).data("filter-previous-sort-" + name, sort);
                    if (sort) {
                        $(target).data("filter-active-sort", true);
                        $(table).find("th").not($(target)).data("filter-active-sort", false);
                    }
                    doFilter(fields[i], targetOptions.colname, search, method, sort, table);
                }

                $(target).popover('hide');
            });
        }.bind(this));
    }



    /**
     * jQuery plugin to set up table to be filterable
     * @param options.colTarget {(string|element)} - jQuery selector for the element triggering the display of the
     *                                               column selection popover
     * @param options.colContent {(string|element)} - The content to be placed in the column selection popover
     * @param options.filterTarget {(object)} - Object providing colnames of headers and options for their columns
     * @param options.filterTarget.<colname> {string} - Key should correspond to the data-colname attribute of a given
     *                                                  th element
     * @param options.filterTarget.<colname>.type {string} - Content type, either number, string, boolean, or choice
     // TODO: Should this be able to be customized in the frontend, ie custom ordering?
     * @param options.filterTarget.<colname>.choices {array} - If type is choices, provides an array of possible values,
     *                                                         in the order they should be sorted in (lowest to highest)
     * @param options.filterTarget.<colname>.getVal {function(cell)} - Function run on the cell to get its value (optional)
     * @param options.filterTarget.<colname>.multi {array} - If there are multiple values in the cells provide info for each
     * @param options.filterTarget.<colname>.multi[n].name {string} - Name of the value
     * @param options.filterTarget.<colname>.multi[n].selector {(string|element)} - jQuery selector for the element containing
     *                                                                              the value, scoped to the td
     * @param options.filterTarget.<colname>.multi[n].type {string} - Same as  options.filterTarget.<colname>.type
     * @param options.filterTarget.<colname>.multi[n].choices {array} - Same as  options.filterTarget.<colname>.choices
     * @param options.filterTarget.<colname>.multi[n].getVal {function(element)} - Same as  options.filterTarget.<colname>.getVal,
     *                                                                             but using selector of multi[n]
     * @param options.filterTarget.<colname>.group {string} - Name of the group to be placed under in the column
     *                                                        selection UI
     * @param options.filterTarget.<colname>.required {boolean} - Set to true to not include the option to deselect
     *                                                               in the column selection UI
     * @param options.colContent {(string|element)} - The content to be placed in the filter popover
     */
    $.fn.tableWrangler = function(options) {
        options.colTarget = options.colTarget || "#col-select";
        options.colContent = options.colContent || $("#tem_column_selection").html();
        // TODO: Automatically determine column type
        //options.filterTargets = options.filterTargets || this.find("th");
        options.filterContent = options.filterContent || $("#tem_filter").html()

        // Create template data for column selection
        var colSelData = {
            groups: []
        };
        for (var i = 0; i < options.filterTargets.length; i++) {
            var targetOptions = options.filterTargets[i];

            // If it's a required column, don't include it
            if (targetOptions.required) {
                continue;
            }

            // If group doesn't exist yet, add it
            var group = $.grep(colSelData.groups, function(group) {
                return group.name === targetOptions.group
            })[0];
            if (!group) {
                colSelData.groups.push({
                    name: targetOptions.group,
                    // TODO: What happens when two escaped names evaluate to be the same?
                    "name-escaped": targetOptions.group.replace(/^[^A-Za-z]/, "s-").replace(/[^\w\d-:.]/g, "-"),
                    columns: []
                });
                group = colSelData.groups.slice(-1)[0];
            }
            // Add the column info to the group
            group.columns.push({
                colname: targetOptions.colname,
                // TODO: Make sure there isn't a case where someone would put some stuff in there that shouldn't be the title
                name: this.find("th[data-colname=" + targetOptions.colname + "]").text()
            });
        }

        initColSelect(options.colTarget, Mustache.render(options.colContent, colSelData), this);

        for (var i = 0; i < options.filterTargets.length; i++) {
            var targetOptions = options.filterTargets[i];
            var fields = targetOptions.multi || [targetOptions];

            var filterData = {
                fields: []
            };
            for (var field in fields) {
                filterData.fields.push({
                    name: fields[field].name,
                    type_number: fields[field].type === "number",
                    type_text: fields[field].type === "text",
                    type_boolean: fields[field].type === "boolean",
                    type_choice: fields[field].type === "choice",
                    choices: fields[field].choices
                })
            }

            initFilter(this.find("th[data-colname=" + targetOptions.colname + "]"), Mustache.render(options.filterContent, filterData), targetOptions, this);
        }
        
        // Initialize data property for filtering
        this.find("tbody tr").each(function(){
            $(this).data("filteredBy",'')
        })
        
        return this;
    };

}(jQuery));