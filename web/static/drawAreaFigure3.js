function drawLineplot(type, data1, data2 = [], name1, name2 = []) {

    /*-- find minimums and maximums for axis --*/
    var minY, maxY, mindate, maxdate;
    if (data2.length <= 0) {
        if (data1.length > 0) {
            minY = d3.min(data1, function(d) { return d.number_post });
            maxY = d3.max(data1, function(d) { return d.number_post });
            mindate = d3.extent(data1, function(d) { return d.date; })[0];
            maxdate = d3.extent(data1, function(d) { return d.date; })[1];
        }

    } else {
        if (data1.length > 0) {
            minY = d3.min([d3.min(data1, function(d) { return d.number_post }), d3.min(data2, function(d) { return d.number_post })]);
            maxY = d3.max([d3.max(data1, function(d) { return d.number_post }), d3.max(data2, function(d) { return d.number_post })]);
            var Date1 = d3.extent(data1, function(d) { return d.date; }),
                Date2 = d3.extent(data2, function(d) { return d.date; });
            mindate = Date1[0] < Date2[0] ? Date1[0] : Date2[0];
            maxdate = Date1[1] > Date2[1] ? Date1[1] : Date2[1];
        } else {
            minY = d3.min(data2, function(d) { return d.number_post });
            maxY = d3.max(data2, function(d) { return d.number_post });
            mindate = d3.extent(data2, function(d) { return d.date; })[0];
            maxdate = d3.extent(data2, function(d) { return d.date; })[1];
        }
    }
    // define scales for axises
    var scaleX = d3.time.scale()
        .domain([mindate, maxdate])
        .range([0, width])

    var scaleY = d3.scale.linear()
        .range([height, 0])
        .domain([0, maxY])

    /*-- adding svg --*/
    var svg = d3.select('#graphic').append("svg").attr({
        'width': width + margin.left + margin.right,
        'height': height + margin.top + margin.bottom,
    });
    var s = svg.append("g")
        .append("g")
        .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");

    /*-- define line: X represents date, Y represents number of post --*/
    var line = d3.svg.line()
        .x(function(d) {
            return scaleX(d.date);
        }).y(function(d) {
            return scaleY(d.number_post);
        });

    /*-- define area : X represents date, Y represents number of post --*/
    var area = d3.svg.area()
        .x(function(d) { return scaleX(d.date); })
        .y0(height)
        .y1(function(d) { return scaleY(d.number_post); });

    /*-- Define the div for the tooltip --*/
    var div = d3.select("body").append("div")
        .attr("class", "tooltip")
        .style("opacity", 0);
    var tip = d3.tip()
        .attr('class', 'd3-tip')
        .offset([-10, 0])
        .html(function(d) {
            return "<br><strong>Date:</strong> <span><b>" + d3.time.format("%b-%Y") (d.date) + "</b></span>" +
                "<br>" + "<strong>Number of Tweets:</strong> <span>" + d.number_post + "</span>";
        })
    svg.call(tip);


    // if there is no data in the single mode // return 
    if (data1.length <= 0 & type == 'single') {
        var textCenter = svg.append("text")
            .attr('class', 'no_show')
            .attr("x", '50%')
            .attr("y", '50%')
            .attr("text-anchor", "middle")
            .text('There is no data for this congress member');
        return
    }

    // if there is no data in the compare mode // return 
    if (data1.length <= 0 & data2.length <= 0 & type == 'compare') {
        var textCenter = svg.append("text")
            .attr('class', 'no_show')
            .attr("x", '50%')
            .attr("y", '50%')
            .attr("text-anchor", "middle")
            .text('There is no data for this 2 congress members');
        return
    }

    //define gradient color
    svg.append("linearGradient")
        .attr("id", "area-gradient")
        .attr("gradientUnits", "userSpaceOnUse")
        .attr("x1", 0).attr("y1", scaleY(0))
        .attr("x2", 0).attr("y2", scaleY(50))
        .selectAll("stop")
        .data([
            { offset: "0%", color: user_color[0]['light'] },  
            { offset: "100%", color: user_color[0]['main'] }
        ])
        .enter().append("stop")
        .attr("offset", function(d) { return d.offset; })
        .attr("stop-color", function(d) {
            return d.color;
        });

    svg.append("linearGradient")
        .attr("id", "area-gradient2")
        .attr("gradientUnits", "userSpaceOnUse")
        .attr("x1", 0).attr("y1", scaleY(0))
        .attr("x2", 0).attr("y2", scaleY(50))
        .selectAll("stop")
        .data([
            { offset: "0%", color: user_color[1]['light'] },  
            { offset: "100%", color: user_color[1]['main']}
        ])
        .enter().append("stop")
        .attr("offset", function(d) { return d.offset; })
        .attr("stop-color", function(d) {
            return d.color;
        });

    // animation of area
    var startData = data1.map(function(d) {
        return {
            date: d.date,
            number_post: 0
        };
    });

    if (data1.length>0) {
        s.append("path")
            .data([startData])
            .attr("class", "areaChart")
            .attr("d", area)
            .on('mouseover', function(d) { d3.select(this).style("opacity", "1"); 
                d3.select('.areaChart2').style("opacity", "0");
                d3.selectAll('.linedot2').style("opacity", "0");
            })
            .on('mouseout', function(d) { d3.select(this).style("opacity", "0.8"); 
                d3.select('.areaChart2').style("opacity", "0.8");
                d3.selectAll('.linedot2').style("opacity", "1");
            })
            .transition().duration(1500)
            .attrTween('d', tween(data1, area))
            .each('end', function(d) { drawCircles(data1, user_color[0]['main'] ,'1') });
    };

    /* if it is a compare mode */
    if (data2.length>0) {
        var startData2 = data2.map(function(d) {
            return {
                date: d.date,
                number_post: 0
            };
        });
        s.append("path")
            .data([startData2])
            .attr("class", "areaChart2")
            .attr("d", area)
            .on('mouseover', function(d) { 
                d3.select(this).style("opacity", "1");
                d3.select('.areaChart').style("opacity", "0");
                d3.selectAll('.linedot1').style("opacity", "0");
             })
            .on('mouseout', function(d) { d3.select(this).style("opacity", "0.8"); 
                d3.select('.areaChart').style("opacity", "0.8");
                d3.selectAll('.linedot1').style("opacity", "1");
            })
            .transition().duration(1500)
            .attrTween('d', tween(data2, area))
            .each('end', function(d) { drawCircles(data2, user_color[1]['main'] ,'2') });
    }

    /* draw axises */
    var axisX = d3.svg.axis().scale(scaleX)
        .orient("bottom").ticks(10).tickFormat(d3.time.format("%b-%Y"));

    var axisY = d3.svg.axis().scale(scaleY)
        .orient("left").ticks(5);
    // define grid
    var axisXGrid = d3.svg.axis()
        .scale(scaleX)
        .orient("bottom")
        .ticks(10)
        //.tickFormat(d3.time.format('%Y-%m-%d'))
        .tickFormat(d3.time.format(""))
        .tickSize(-height, 0);

    var axisYGrid = d3.svg.axis()
        .scale(scaleY)
        .orient("left")
        .ticks(10)
        .tickFormat("")
        .tickSize(-width, 0);

    /* draw grid */
    s.append('g')
    .call(axisXGrid)
    .attr({
        'fill': 'none',
        'stroke': 'rgba(0,0,0,.1)',
        'transform': 'translate(0,' + height + ')'
    });

    s.append('g')
    .call(axisYGrid)
    .attr({
        'fill': 'none',
        'stroke': 'rgba(0,0,0,.1)',
        // 'transform': 'translate(35,20)'
    });

    // add axis
    s.append('g')
    .call(axisX)
    .attr({
        'fill': 'none',
        'stroke': '#000',
        'transform': 'translate(0,' + height + ')'
    }).selectAll('text')
    .attr({
        'fill': '#000',
        'stroke': 'none',
    })
    .attr("transform", function(d) {
        return "translate(" + this.getBBox().height * -2 + "," + this.getBBox().height + ")rotate(-45)";
    }).style({
        'font-size': '15px'
    });

    s.append('g')
    .call(axisY)
    .attr({
        'fill': 'none',
        'stroke': '#000',
        // 'transform': 'translate(35,20)'
    }).selectAll('text')
    .attr({
        'fill': '#000',
        'stroke': 'none',
    }).style({
        'font-size': '20px'
    });

    // function for drawing circles
    function drawCircles(data, color,sequence) {
        s.selectAll("linedot")
            .data(data)
            .enter().append("circle")
            .attr("class", "linedot linedot"+sequence)
            .attr("r", 7)
            .attr("cx", function(d) { return scaleX(d.date); })
            .attr("cy", function(d) { return scaleY(d.number_post); })
            .attr("fill", color)
            .style("opacity", 0)
            .on("click", function(d) {
                //clean the description
                d3.select('#slide1').selectAll('.description').remove()

                for (i = 0; i < d.values.length; i++) {
                    for (key in d.values[i].dataSingle) {
                        d3.select('#slide1').append("p")
                            .attr("class", "description")
                            .html(function() {
                                return "<strong>"+d.values[i].dataSingle[key].created_at +":</strong><br>" + d.values[i].dataSingle[key].tweet_text+"<br><a target='_blank' href='"+'https://twitter.com/statuses/'+key+"'> View Live</a>"
                            });

                        if (d3.selectAll(".circle_active")[0].length == 0) { slideShow();
                        } else { firstF().then(secondF());}

                        d3.selectAll(".circle_active").classed('circle_active', false);
                        d3.select(this).classed('circle_active', true)

                    }

                }
            })
            .on('mouseover', tip.show)
            .on('mouseout', tip.hide)
            .transition()
            .delay(function(d, i) {
                return i * 30
            })
            .style("opacity", 1);
    }


        /// add lengend
        var legendlist = name1.concat(name2)
        var legend_g = svg.selectAll('.legends4')
            .data(legendlist)
            .enter().append('g')
            .attr("class", "legends4")
            .attr("transform", function(d, i) {
                return i == 0 ? "translate(" + (width - 100 * legendlist.length) + "," + (margin.top / 2) + ")" :  "translate(" + (100 * legendlist.length) + "," + (margin.top / 2) + ")"
            });

        legend_g.append('rect')
        .attr("x", 0)
        .attr("y", 0)
        .attr("width", 10)
        .attr("height", 10)
        .style("fill", function(d, i) {
            return i == 0 ? user_color[0]['main'] : user_color[1]['main']
        });

        legend_g.append('text')
        .attr("x", 20)
        .attr("y", 10)
        .text(function(d, i) {
            return d
        })
        .attr("class", "textselected")
        .style("text-anchor", "start")
        .style("font-size", 15)


        svg.append("text")
        .attr("text-anchor", "middle") // this makes it easy to centre the text as the transform is applied to the anchor
        .attr("transform", "translate(" + (margin.left - 50) + "," + (height / 2 + margin.top) + ")rotate(-90)") // text is drawn off the screen top left, move down and out and rotate
        .text("Number of Tweets")
        .style("font-size", 20);
        }

    /// slide function //
    function slideShow() {
        $('#slide1').css('right', '5%')
        $('#slide1').css('opacity', '1')
    };

    function slideHide() {
        d3.selectAll(".circle_active").classed('circle_active', false);
        $('#slide1').css('opacity', '0')
        $('#slide1').css('right', '-100%')
    };

    function firstF() {
        var deferred = new $.Deferred();
        slideHide()
        return deferred.promise();
    };

    function secondF() { setTimeout(function() { slideShow(); }, 300); }

    function tween(b, callback) {
        return function(a) {
            var i = d3.interpolateArray(a, b);

            return function(t) {
                return callback(i(t));
            };
        };
    }