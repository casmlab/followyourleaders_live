    // Function for transforming data format
    function makeArrayObject(objectI, keyName, valueName) {
        var op = [];
        Object.keys(objectI).forEach(function(key) {
            var obj = {};
            obj[keyName] = key;
            obj[valueName] = objectI[key];

            op.push(obj);

        })
        return op
    };

    function sortByDateAscending(a, b) {
        return a.date - b.date;
    }

    // function for drawing line chart



    // function for drawing pie chart
    function drawPie (selector,colorpanal,data) {

        var width = $(selector).width(),
        height = width*0.8,
        radius = Math.min(width, height) / 2;


    var outerRadius = radius-30,
        innerRadius = radius-70;

    // var pie = d3.layout.pie();
     var pie = d3.layout.pie()
        .sort(null)
        .padAngle(.02)
        .value(function(d) { return d.num; });


    var arc = d3.svg.arc()
        .padRadius(outerRadius);

    var arc2 = d3.svg.arc()
        .outerRadius(outerRadius)
        .innerRadius(innerRadius);

    var svgM = d3.select(selector).append("svg")
        .attr("width", width)
        .attr("height", height);

    var svg = svgM.append("g")
        .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

    var g= svg.selectAll("path")
        .data(pie(data))
      .enter()

      g.append("path")
        .each(function(d) { d.outerRadius = outerRadius - 20; })
        .attr("d", arc)
        .style("fill", function(d,i) { return color(i); })
        .on("mouseover", function(){ arcTween(outerRadius + 20, 0, this)(); })
        .on("mouseout", function(){ arcTween(outerRadius - 20, 150, this)(); })
        .transition().duration(1500)
        .attrTween('d', attrTween1)



    // adding text

    
    g.append("text")
        .attr("transform", function(d) { return "translate(" + arc2.centroid(d) + ")"; })
        .attr("dy", ".35em")
        .attr("class", "d3-label")
        .style("text-anchor", "middle")
        .style("font-size", "10px")
        .text(function(d) { 
          return d.data.num; });


    // adding legend

    var legendG = svgM.selectAll(".legend")
      .data(pie(data))
      .enter().append("g")
      .attr("transform", function(d,i){
        return "translate(" + (width - 110) + "," + (i * 15 + 20) + ")";
      })
      .attr("class", "legend");   
    
    legendG.append("rect")
      .attr("width", 10)
      .attr("height", 10)
      .attr("fill", function(d, i) {
        return color(i);
      });
    
    legendG.append("text")
      .text(function(d){
        return " "+d.data.type+" "+d.data.num
      })
      .style("font-size", 12)
      .attr("y", 10)
      .attr("x", 11);

      function attrTween1 (d, i) {
        var i = d3.interpolate(d.endAngle, d.startAngle);
        return function(t) {
                d.startAngle = i(t);
                return arc(d);
            };
    }


    function arcTween(outerRadius, delay, that) {
        console.log('here')
      return function() {
        var el = (that !== undefined ? that : this);
        d3.select(el).transition().delay(delay).attrTween("d", function(d) {
          var i = d3.interpolate(d.outerRadius, outerRadius);
          return function(t) { d.outerRadius = i(t); return arc(d); };
        });
      };
    }
    

    }



