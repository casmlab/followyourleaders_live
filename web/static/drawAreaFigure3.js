function drawLineplot(type, data1, data2 = [], name1, name2 = []) {

    // making axis
    // individual mode
    console.log(type, data1, data2)
    var minY, maxY, mindate, maxdate;

    // if data2 has no data or it is a single plot
    if (data2.length <= 0) {
        // if data 1 is not empty
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



    // Define the div for the tooltip
    var div = d3.select("body").append("div")
        .attr("class", "tooltip")
        .style("opacity", 0);


    //define line: X represents date, Y represents number of post
    var line = d3.svg.line()
        .x(function(d) {
            return scaleX(d.date);
        }).y(function(d) {
            return scaleY(d.number_post);
        });

    //define area : X represents date, Y represents number of post
    var area = d3.svg.area()
        .x(function(d) { return scaleX(d.date); })
        .y0(height)
        .y1(function(d) { return scaleY(d.number_post); });



    // adding svg
    var svg = d3.select('#graphic').append("svg").attr({
        'width': width + margin.left + margin.right,
        'height': height + margin.top + margin.bottom,
    }).style({
        'border': '1px dotted #ccc'
    });

    var tip = d3.tip()
        .attr('class', 'd3-tip')
        .offset([-10, 0])
        .html(function(d) {
            return "<br><strong>Date:</strong> <span style='color:red'>" + d3.time.format("%x")(d.date) + "</span>" +
                "<br>" + "<strong>Number of Tweets:</strong> <span style='color:red'>" + d.number_post + "</span>";
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

    var scaleX = d3.time.scale()
        .domain([mindate, maxdate])
        .range([0, width])

    var scaleY = d3.scale.linear()
        .range([height, 0])
        .domain([0, maxY]);

    //define gradient color
    svg.append("linearGradient")
        .attr("id", "area-gradient")
        .attr("gradientUnits", "userSpaceOnUse")
        .attr("x1", 0).attr("y1", scaleY(0))
        .attr("x2", 0).attr("y2", scaleY(50))
        .selectAll("stop")
        .data([
            { offset: "0%", color: user_color[0]['light'] },
            // {offset: "30%", color: "red"},    
            // {offset: "45%", color: "black"},      
            // {offset: "55%", color: "black"},      
            // {offset: "60%", color: "lawngreen"},  
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
            //{ offset: "0%", color: "#ff9a9e" },
            //{ offset: "100%", color: "#fad0c4" }
            //#ff8177 0%, #ff867a 0%, #ff8c7f 21%, #f99185 52%, #cf556c 78%, #b12a5b
            { offset: "0%", color: user_color[1]['light'] },
            // {offset: "20%", color: "#ff867a"},    
            // {offset: "40%", color: "#ff8c7f"},      
            // {offset: "60%", color: "#f99185"},      
            // {offset: "80%", color: "#cf556c"},  
            { offset: "100%", color: user_color[1]['main']}
        ])
        .enter().append("stop")
        .attr("offset", function(d) { return d.offset; })
        .attr("stop-color", function(d) {
            return d.color;
        });

    // shift plot (margin)
    var s = svg.append("g")
        .append("g")
        .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");


    // animation of area

    var startData = data1.map(function(d) {
        return {
            date: d.date,
            number_post: 0
        };
    });

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
            // .attr("fill", 'rgba(0,150,255,.1)')
            .transition().duration(1500)
            .attrTween('d', tween(data1, area))
            .each('end', function(d) { drawCircles(data1, user_color[0]['main'] ,'1') })



            if (data2 != null) {
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
                    // .attr("fill", 'rgba(0,150,255,.1)')
                    .transition().duration(1500)
                    .attrTween('d', tween(data2, area))
                    .each('end', function(d) { drawCircles(data2, user_color[1]['main'] ,'2') });
            }

            //start plotting
            // if (data1 != []) {

            //     linepath = s.append('path')
            //         .attr({
            //             'd': line(data1),
            //             'stroke': '#6bb7c7',
            //             'fill': 'none',
            //             // 'transform': 'translate(35,20)'
            //         })
            //         .style('stroke-width', 'px')
            // }

            // if (data2 != []) {
            //     linepath2 = s.append('path')
            //         .attr({
            //             'd': line(data2),
            //             'stroke': '#6bb7c7',
            //             'fill': 'none',
            //         })
            //         .style('stroke-width', 'px');
            // }


            // animation of Line
            // var totalLength = linepath.node().getTotalLength();
            // linepath
            //     .attr("stroke-dasharray", totalLength + " " + totalLength)
            //     .attr("stroke-dashoffset", totalLength)
            //     .transition()
            //     .duration(1500)
            //     .delay(1500 / 2)
            //     .ease("linear")
            //     .attr("stroke-dashoffset", 0)
            //     .each('end', function(d) { drawCircles(data1, 'steelblue') });


            // if (data2 != null) {
            //     var totalLength2 = linepath.node().getTotalLength();
            //     linepath2
            //         .attr("stroke-dasharray", totalLength2 + " " + totalLength2)
            //         .attr("stroke-dashoffset", totalLength2)
            //         .transition()
            //         .duration(1500)
            //         .delay(1500 / 2)
            //         .ease("linear")
            //         .attr("stroke-dashoffset", 0)
            //         .each('end', function(d) { drawCircles(data2, 'red') });

            // }


            // define axis
            var axisX = d3.svg.axis().scale(scaleX)
                .orient("bottom").ticks(10).tickFormat(d3.time.format('%Y-%m-%d'));

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

            // add grid
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
                'font-size': '11px'
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
                'font-size': '10px'
            });

            // adding dot

            function drawCircles(data, color,sequence) {
                s.selectAll("linedot")
                    .data(data)
                    .enter().append("circle")
                    .attr("class", "linedot linedot"+sequence)
                    //.attr("class", "linedot"+sequence)
                    .attr("r", 7)
                    .attr("cx", function(d) { return scaleX(d.date); })
                    .attr("cy", function(d) { return scaleY(d.number_post); })
                    .attr("fill", color)
                    .style("opacity", 0)
                    .on("click", function(d) {
                        //clean the description
                        d3.selectAll('.description').remove()
                        count = 0

                        for (i = 0; i < d.values.length; i++) {
                            //console.log(d.values[i].dataSingle)
                            for (key in d.values[i].dataSingle) {


                                d3.select('#slide').append("p")
                                    .attr("class", "description")
                                    .html(function() {

                                        return "Twitter text: " + d.values[i].dataSingle[key].tweet_text
                                    });



                                if (d3.selectAll(".circle_active")[0].length == 0) {
                                    slideShow()
                                } else {
                                    firstF().then(secondF())
                                }

                                d3.selectAll(".circle_active").classed('circle_active', false);
                                d3.select(this).classed('circle_active', true)

                            }

                            count = count + 1

                            if (count >= 5) { break }

                        }
                    })
                    .on('mouseover', tip.show)
                    .on('mouseout', tip.hide)
                    .transition()
                    // .duration(1000)
                    .delay(function(d, i) {
                        return i * 30
                    })
                    .style("opacity", 1)
            }


            /// add lengend
            var legendlist = name1.concat(name2)

            var dataL = 0;
            var offset = 120;

            var legend_g = svg.selectAll('.legends4')
                .data(legendlist)
                .enter().append('g')

                .attr("class", "legends4")
                .attr("transform", function(d, i) {
                    if (i === 0) {
                        dataL = d.length + offset
                        return "translate(" + (width - 100 * legendlist.length) + "," + (margin.top / 2) + ")"
                    } else {
                        var newdataL = dataL
                        dataL += d.length + offset
                        return "translate(" + (width - 100 * legendlist.length + newdataL) + "," + (margin.top / 2) + ")"
                    }
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
            //.attr("dy", ".35em")
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
        $('#slide').css('right', '5%')
        $('.slide').css('box-shadow', "-31px 8px 180px 2px rgba(14, 16, 33, 0.5)")
    };

    function slideHide() {
        d3.selectAll(".circle_active").classed('circle_active', false);
        $('#slide').css('right', '-35%')
        // $('#slide').css('opacity', "0")
        // $('.slide').css('box-shadow', "-31px 8px 180px 2px rgba(14, 16, 33, 0.5)")
    };

    function firstF() {
        var deferred = new $.Deferred();
        slideHide()
        return deferred.promise();
    };

    function secondF() { setTimeout(function() { slideShow(); }, 800); }

    function tween(b, callback) {
        return function(a) {
            var i = d3.interpolateArray(a, b);

            return function(t) {
                return callback(i(t));
            };
        };
    }