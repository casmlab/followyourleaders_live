    function format_timelines_data(data)  {

        data_line=[]
        for (key in data.dates){
            data_line.push({'date':parseDate(key),'dataSingle':data.dates[key]});
        }

        // function sortByDateAscending(a, b) {return a.date - b.date;}
        // aggregaate by month

        data_line=d3.nest()
          .key(function(d){ return d3.time.month(d.date); })
          .entries(data_line);

        // // change data Fomart
        data_line.forEach(function(d) {
            d.date = new Date(d.key);
            d.number_post_Day=d.values.length;
            count=0

            for (i = 0; i < d.values.length; i++) {
                 count=count+Object.keys(d.values[i].dataSingle).length;
                }

            d.number_post=count

            delete d.key
        });

        return data_line

    };


    function format_hashtags_data(data)  {
        temp=[]
        for (key in data.hashtags) {
            var obj = {};
            //console.log(data['hashtags'][key]['tweets'])
            obj['label'] = key;
            obj['value'] = Object.keys(data['hashtags'][key]['tweets']).length;
            obj['data'] = data['hashtags'][key]['tweets'];
            temp.push(obj);
        }

        temp.sort(function(a, b){
            return b.value-a.value
        })


        return temp
    }


    // defined url
    function format_urls_data(data)  {
        temp=[]
        for (key in data.urls) {
            var obj = {};
            //console.log(data['hashtags'][key]['tweets'])
            obj['label'] = unicodeToChar(key.replace("\u002e", "."));
            obj['value'] = Object.keys(data['urls'][key]['tweets']).length;
            obj['data'] = data['urls'][key]['tweets'];
            temp.push(obj);
        }

        temp.sort(function(a, b){
            return b.value-a.value
        })


        return temp
    }


function unicodeToChar(text) {
   return text.replace(/\\u[\dA-F]{4}/gi, 
          function (match) {
               return String.fromCharCode(parseInt(match.replace(/\\u/g, ''), 16));
          });
}