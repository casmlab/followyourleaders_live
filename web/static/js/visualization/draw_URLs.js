    function draw_URLs(type, data, data2 = [], name1, name2 = []) {


        //define plot size
        var labelArea = 100;
        var chart,
            bar_height = 20;
        var widthBAR = type == 'compare' ? ((width) / 2 - labelArea) - 100 : (width) - labelArea - 100;
        var rightOffset = type == 'compare' ? widthBAR + 2 * labelArea + 100 : labelArea
        var rightText = type == 'compare' ? -20 + widthBAR + 2 * labelArea + 100 : -20 + labelArea

        // define scales
        var xScale = d3.scale.linear()
            .range([0, widthBAR]);

        var maxYbar;
        if (data2.length <= 0) {
            if (data.length > 0) {
                maxYbar = d3.max(data, function(d) {
                    return d.value
                });
            }

        } else {
            if (data.length > 0) {
                maxYbar = d3.max([d3.max(data, function(d) { return d.value }), d3.max(data2, function(d) { return d.value })]);
            } else {
                maxYbar = d3.max(data2, function(d) { return d.value });
            }
        }

        xScale.domain([0, maxYbar]);

        // define svg
        var svg = d3.select("#urls_chart")
            .append('svg')
            .attr('class', 'chart')
            .attr('width', width + margin.left + margin.right)
            .attr('height', height + margin.top + margin.bottom)

        // shift plot (margin)
        var chart = svg.append("g")
            .append("g")
            .attr("transform",
                "translate(" + margin.left + "," + margin.top + ")");

        // no data in single mode
        if (data.length <= 0 & type == 'single') {
            var textCenter = svg.append("text")
                .attr('class', 'no_show')
                .attr("x", '50%')
                .attr("y", '50%')
                .attr("text-anchor", "middle")
                .text('There is no data for this congress member');
            return
        }

        // no data in compare mode
        if (data.length <= 0 & data2.length <= 0 & type == 'compare') {
            var textCenter = svg.append("text")
                .attr('class', 'no_show')
                .attr("x", '50%')
                .attr("y", '50%')
                .attr("text-anchor", "middle")
                .text('There is no data for these 2 congress members');
            return

        }

        if (type == 'single') {
            drawRight(data,user_color[0])
        } else {
            // in compare mode
            drawRight(data2,user_color[1])
            drawLeft(data,user_color[0])
            if (data.length <= 0) { missingOne(svg,'25%')} 
            if (data2.length <= 0) { missingOne(svg,'75%')}
        }


        /// add lengend
        var legendlist = name1.concat(name2)
        var legend_g = svg.selectAll('.legends4')
            .data(legendlist)
            .enter().append('g')
            .attr("class", "legends4")
            .attr("transform", function(d, i) {
                return i == 0 ? "translate(" + (100 * legendlist.length) + "," + (margin.top / 2) + ")" :  "translate(" + (width - 100 * legendlist.length) + "," + (margin.top / 2) + ")"
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

        // function for creating text when missing one leader's data
        function missingOne(svg,x_position) {
            var textCenter = svg.append("text")
                    .attr('class', 'no_show')
                    .attr("x", x_position)
                    .attr("y", '35%')
                    .attr("text-anchor", "middle")

                textCenter.selectAll("tspan")
                    .data(['There is no data', 'for this congress', 'member.'])
                    .enter()
                    .append("tspan")
                    .attr("x", textCenter.attr("x"))
                    .attr("dy", "1em")
                    .text(function(d) {
                        return d;
                    });
        }

        // function for drawing right bars
        function drawRight(data,color) {
            var y = d3.scale.ordinal().rangeBands([20, height]);
            y.domain(data.map(function(d) { return d.label; }));
            var yPosByIndex = function(d) { return y(d.label); };

            chart.selectAll("text.name2")
                .data(data)
                .enter().append("text")
                .attr("x", rightText)
                .attr("y", function(d) {
                    return y(d.label) + y.rangeBand() / 2;
                })
                .attr("dy", ".20em")
                .attr("text-anchor", "end")
                .attr('class', 'name')
                .text(function(d) { return d.label.replace('www.', ''); });


            chart.selectAll("rect.right")
                .data(data)
                .enter().append("rect")
                .attr("x", rightOffset)
                .attr("y", yPosByIndex)
                .attr("class", "right")
                .attr("width", 0) //
                .on("click", function(d) { 
                    d3.select('#slide2').selectAll('.description').remove()
                        for (key in d.data) {
                            d3.select('#slide2')
                                .append("p")
                                .attr("class", "description")
                                .html(function() {
                                    return "<strong>"+d.data[key]['created_at'] +":</strong><br>" + 
                                        d.data[key]['text']+"<br><a target='_blank' href='"+'https://twitter.com/statuses/'+key+"'> View Live</a>"
                                });
                        }

                        if (d3.selectAll(".bar_active")[0].length == 0) {
                            slideShow()
                        } else {
                            firstF().then(secondF())
                        };
                    d3.selectAll(".bar_active").classed('bar_active', false);
                    d3.select(this).classed('bar_active', true)

                })
                .transition()
                .duration(1500)
                .attr("width", function(d) {
                    return xScale(+d['value']);
                })
                .attr("height", y.rangeBand())
                .attr("fill", color['main'])
                

            chart.selectAll("text.rightscore")
                .data(data)
                .enter().append("text")
                .attr('class', 'chartscore')
                .attr("x", function(d) {
                    return xScale(d['value']) + rightOffset + 40;
                })
                .attr("y", function(d) {
                    return y(d.label) + y.rangeBand() / 2;
                })
                .attr("dx", -5)
                .attr("dy", ".36em")
                .attr("text-anchor", "end")
                .attr('class', 'rightscore')
                .style('fill', 'gray')
                .text(function(d) { return d['value']; });
        }

        function drawLeft(data,color) {

            var y2 = d3.scale.ordinal().rangeBands([20, height]);
            y2.domain(data.map(function(d) {return d.label;}));
            var yPosByIndex2 = function(d) {return y2(d.label);};

            chart.selectAll("rect.left")
                    .data(data)
                    .enter().append("rect")
                    .attr("x", widthBAR)
                    .attr("y", yPosByIndex2)
                    .attr("class", "left")
                    .attr("width", 0) //
                    .on("click", function(d) { 

                         d3.select('#slide2').selectAll('.description').remove()

                         for (key in d.data) {
                            //d.data.key.text
                            d3.select('#slide2').append("p")
                             .attr("class", "description")
                             .html(function() {
                                return "<strong>"+d.data[key]['created_at'] +":</strong><br>" + 
                                    d.data[key]['text']+"<br><a target='_blank' href='"+'https://twitter.com/statuses/'+key+"'> View Live</a>"
                            });
                         }

                          if (d3.selectAll(".bar_active")[0].length == 0) {
                            slideShow()
                          } else {
                                firstF().then(secondF())
                                };
                         d3.selectAll(".bar_active").classed('bar_active', false);
                         d3.select(this).classed('bar_active', true)

                    })
                    .transition()
                    .duration(1500)
                    .attr("x", function(d) {

                        return widthBAR - xScale(d['value']);
                    })
                    .attr("width", function(d) {

                        return xScale(d['value']);
                    })
                    .attr("height", y2.rangeBand())
                    .attr("fill", color['main'])
                    
                chart.selectAll("text.leftscore")
                    .data(data)
                    .enter().append("text")
                    .attr("x", function(d) {
                        return widthBAR - xScale(d['value']) - 40;
                    })
                    .attr("y", function(d) {
                        return y2(d.label) + y2.rangeBand() / 2;
                    })
                    .attr("dx", "20")
                    .attr("dy", ".36em")
                    .attr("text-anchor", "end")
                    .attr('class', 'leftscore')
                    .text(function(d) { return d['value']; })
                    .style('fill', 'gray');

                chart.selectAll("text.name1")
                    .data(data)
                    .enter().append("text")
                    .attr("x", 20 + widthBAR)
                    .attr("y", function(d) {
                        return y2(d.label) + y2.rangeBand() / 2;
                    })
                    .attr("dy", ".20em")
                    .attr("text-anchor", "start")
                    .attr('class', 'name')
                    .text(function(d) { return d.label.replace('www.', ''); });
        }
        /// slide function //
        function slideShow() {
            $('#slide2').css('right', '5%')
            $('#slide2').css('opacity', '1')
        };

        function slideHide() {
            d3.selectAll(".bar_active").classed('bar_active', false);
            $('#slide2').css('right', '-50%')
            $('#slide2').css('opacity', '0')
        };

        function firstF() {
            var deferred = new $.Deferred();
            slideHide()
            return deferred.promise();
        };

        function secondF() { setTimeout(function() { slideShow(); }, 800); } ;


    }