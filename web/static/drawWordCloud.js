function drawWordCloud(type, data1, data2, name1, name2) {

    var word_count = {},
        word_count2 = {};

    var word_entries = [],
        word_entries2 = [];

    // if user1 have hash data
    if (data1.length > 0) {
        for (i = 0; i < data1.length; i++) {
            word_count[data1[i].label] = data1[i].value
        }
        word_entries = d3.entries(word_count);
    }

    // if user 2 have hash data
    if (data2.length > 0) {
        for (i = 0; i < data2.length; i++) {
            word_count2[data2[i].label] = data2[i].value
        }

        word_entries2 = d3.entries(word_count2);
    }

    // find the maximun
    var Maximu = d3.max([d3.max(word_entries, function(d) { return d.value }), d3.max(word_entries2, function(d) { return d.value })]);


    // make a svg
    var svg = d3.select('#wcloud')
        .append("svg")
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
        .style({ 'border': '1px dotted #ccc' });

    var s = svg.append("g")
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");


    // if single mode has no data
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
            .text('There is no data for this congress member');
        return

    }

    // define color
    //https://gka.github.io/palettes/#colors=#fffde4,#005aa7|steps=12|bez=1|coL=1
    //https://uigradients.com/#EveningNight
    //var fill = d3.scale.category20();
    //var fill1 = ['#fffde4', '#eceddf', '#daddda', '#c8cdd4', '#b6bdcf', '#a3aec9', '#909fc4', '#7c91be', '#6882b8', '#5174b3', '#3767ad', '#005aa7'].reverse()
    //var fill2 = ['#ffffe0', '#ffe9b7', '#ffd196', '#ffb67f', '#ff9b6f', '#f98065', '#ee665d', '#e14d54', '#cf3548', '#bb1e37', '#a40921', '#8b0000'].reverse();
    var fill1 = user_color[0]['word_color']
    var fill2 = user_color[1]['word_color']

    // define scale
    var xScale = d3.scale.linear()
        .domain([0, Maximu])
        .range([15, 40]);

    // define location
    var wc1_postion = type == 'compare' ? [width * 3 / 4, height / 2] : [width * 1 / 2, height / 2];
    var wc2_postion = [width / 4, height / 2];

    // define wc size
    var wc_size = type == 'compare' ? [(width) / 2, height] : [width, height];



    // draw first one
    d3.layout.cloud().size(wc_size)
        .timeInterval(20)
        .words(word_entries)
        .fontSize(function(d) { return xScale(+d.value); })
        .text(function(d) { return d.key; })
        .rotate(function() { return ~~(Math.random() * 2) * 90; })
        .font("Impact")
        .on("end", function(d) { return draw(d, s, wc1_postion, xScale) })
        .start();

    // draw second one
    d3.layout.cloud().size(wc_size)
        .timeInterval(20)
        .words(word_entries2)
        .fontSize(function(d) { return xScale(+d.value); })
        .text(function(d) { return d.key; })
        .rotate(function() { return ~~(Math.random() * 2) * 90; })
        .font("Impact")
        .on("end", function(d) { return draw2(d, s, wc2_postion, xScale) })
        .start();
    if (type == 'compare') {
        if (data2.length <= 0) {
            var textCenter = svg.append("text")
                .attr('class', 'no_show')
                .attr("x", '25%')
                .attr("y", '35%')
                .attr("text-anchor", "middle")

                textCenter.selectAll("tspan")
                .data(['There is no data', 'for this congress','member.'])
                .enter()
                .append("tspan")
                .attr("x",textCenter.attr("x"))
                .attr("dy","1em")
                .text(function(d){
                    return d;
                });
        }
        if (data1.length <= 0) {
            var textCenter = svg.append("text")
                .attr('class', 'no_show')
                .attr("x", '75%')
                .attr("y", '35%')
                .attr("text-anchor", "middle")

                textCenter.selectAll("tspan")
                .data(['There is no data', 'for this congress','member.'])
                .enter()
                .append("tspan")
                .attr("x",textCenter.attr("x"))
                .attr("dy","1em")
                .text(function(d){
                    return d;
                });
        }
    }

    // add lengend

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




    // draw leader 1's wc (right)
    function draw(words, s, position, ) {


        s.append("g")
            .attr("transform", "translate(" + position + ")")
            .selectAll("text")
            .data(words)
            .enter().append("text")
            .style("font-size", function(d) { return xScale(d.value) + "px"; })
            .style("font-family", "Impact")
            .style("fill", function(d, i) { return fill1[i % fill1.length]; })
            .attr("text-anchor", "middle")
            .attr("transform", function(d) { return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")"; })
            .text(function(d) { return d.key; });
    }



    // draw leader 2 wc (left)
    function draw2(words, s, position) {


        s.append("g")
            .attr("transform", "translate(" + position + ")")
            .selectAll("text")
            .data(words)
            .enter().append("text")
            .style("font-size", function(d) { return xScale(d.value) + "px"; })
            .style("font-family", "Impact")
            .style("fill", function(d, i) { return fill2[i % fill2.length]; })
            .attr("text-anchor", "middle")
            .attr("transform", function(d) { return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")"; })
            .text(function(d) { return d.key; });
    }
    d3.layout.cloud().stop();
}