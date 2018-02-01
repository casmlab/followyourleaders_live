   // function: make a array of unique value for attribute
    function getUnique(array,attribute_name) {
        var unique = {};
        var distinct = [];
        for(i = 0; i < array.length; i++){
         if( typeof(unique[array[i][attribute_name]]) == "undefined"){
          distinct.push(array[i][attribute_name]);
         }
         unique[array[i][attribute_name]] = 0;
        }
        return distinct
    }

    // function: for making leader dd
    function fun_makedd(dd_base,filter1,filter2,attr_1,attr_2,dd_id){

        // if both filter have chosen values
        if ($(filter1).val() != 'default' && $(filter2).val() != 'default') {
            make_dd=dd_base.filter(function (el) {return el[attr_1] == $(filter1).val() && el[attr_2] == $(filter2).val()})
        }

        // if filter 2 didnt choose value
        else if ($(filter1).val() != 'default' && $(filter2).val() == 'default') {
            make_dd=dd_base.filter(function (el) {return el[attr_1] == $(filter1).val()})
        }

        // if filter 1 didnt choose value
        else if ($(filter1).val() == 'default' && $(filter2).val() != 'default') {
            make_dd=dd_base.filter(function (el) {return el[attr_2] == $(filter2).val()})
        }
        // if both unchoose
        else {
            make_dd=[]
        }
        
        //////// start buiding dd
        var options = "<option value='default'>Select Title ...<\/option>";

        // is data inside
        for(i = 0; i < make_dd.length; i++){
            //console.log(make_dd[i])
            for (j= 0; j < make_dd[i]['leader'].length; j++) {
                //console.log(make_dd[i]['leader'][j])
                options += '<option value="' + make_dd[i]['leader'][j].bioguide + '">' + make_dd[i]['leader'][j].name + '<\/option>';
            }
        }
        $(dd_id).html(options);
    };

    // function: for making all dds
    function generatedropdown(dd_base, chamber_dd, party_dd,leader_select ) {
        (function($) {

            // for making party and chamber dropdown
            var party_temp=getUnique(all_filter,'party_cat')
            var chamber_temp=getUnique(all_filter,'chamber_car')
            var options_categories_chamber = "<option value='default'>Select Chamber ...<\/option>";
            var options_categories_party = "<option value='default'>Select Party ...<\/option>";

            $.each(party_temp, function(i, d) {
                options_categories_party += '<option value="' + d + '">' + d + '<\/option>';
            });

            $.each(chamber_temp, function(i, d) {
                options_categories_chamber += '<option value="' + d + '">' + d + '<\/option>';
            });

            $(chamber_dd).html(options_categories_chamber);
            $(party_dd).html(options_categories_party);

            $(chamber_dd).change(function() { 
                fun_makedd(dd_base,party_dd,chamber_dd,'party_cat','chamber_car',leader_select)
            });

            $(party_dd).change(function() {
                fun_makedd(dd_base,party_dd,chamber_dd,'party_cat','chamber_car',leader_select)
            });

        })(jQuery);
    }