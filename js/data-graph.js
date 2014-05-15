long_short_data = [ 
  {
    key: 'Bachelet 2006',
    color: '#821E5F',
    values: [
      { 
        "label" : "Group A" ,
        "value" : 1.8746444827653
      } , 
      { 
        "label" : "Group B" ,
        "value" : 8.0961543492239
      } , 
      { 
        "label" : "Group C" ,
        "value" : 0.57072943117674
      } , 
      { 
        "label" : "Group D" ,
        "value" : 2.4174010336624
      } , 
      {
        "label" : "Group E" ,
        "value" : 0.72009071426284
      } , 
      { 
        "label" : "Group F" ,
        "value" : 0.77154485523777
      } , 
      { 
        "label" : "Group G" ,
        "value" : 0.90152097798131
      } , 
      {
        "label" : "Group H" ,
        "value" : 0.91445417330854
      } , 
      { 
        "label" : "Group I" ,
        "value" : 0.055746319141851
      }
    ]
  },
  {
    key: 'Piñera 2010',
    color: '#1795CF',
    values: [
      { 
        "label" : "Group A" ,
        "value" : 25.307646510375
      } , 
      { 
        "label" : "Group B" ,
        "value" : 16.756779544553
      } , 
      { 
        "label" : "Group C" ,
        "value" : 18.451534877007
      } , 
      { 
        "label" : "Group D" ,
        "value" : 8.6142352811805
      } , 
      {
        "label" : "Group E" ,
        "value" : 7.8082472075876
      } , 
      { 
        "label" : "Group F" ,
        "value" : 5.259101026956
      } , 
      { 
        "label" : "Group G" ,
        "value" : 0.30947953487127
      } , 
      { 
        "label" : "Group H" ,
        "value" : 0
      } , 
      { 
        "label" : "Group I" ,
        "value" : 0 
      }
    ]
  },
  {
    key: 'Bachelet 2014',
    color: '#F8981D',
    values: [
      { 
        "label" : "Group A" ,
        "value" : 25.307646510375
      } , 
      { 
        "label" : "Group B" ,
        "value" : 16.756779544553
      } , 
      { 
        "label" : "Group C" ,
        "value" : 18.451534877007
      } , 
      { 
        "label" : "Group D" ,
        "value" : 8.6142352811805
      } , 
      {
        "label" : "Group E" ,
        "value" : 7.8082472075876
      } , 
      { 
        "label" : "Group F" ,
        "value" : 5.259101026956
      } , 
      { 
        "label" : "Group G" ,
        "value" : 0.30947953487127
      } , 
      { 
        "label" : "Group H" ,
        "value" : 0
      } , 
      { 
        "label" : "Group I" ,
        "value" : 0 
      }
    ]
  }
];


var chart;
nv.addGraph(function() {
  chart = nv.models.multiBarHorizontalChart()
      .x(function(d) { return d.label })
      .y(function(d) { return d.value })
      .margin({top: 0, right: 0, bottom: 0, left: 60})
      .showValues(true)
      .tooltip(false)
    //   .tooltip(function(key, x, y, e, graph, n_promesas, link_ley) {
    //     var text_for_twitter = encodeURIComponent(y + '% de cumplimiento en ' + x + ',');
    //     return '<h5 class="'+x+'">' +  y + 'de Cumplimiento</h5>' +
    //            '<p> De las ' + e.point.n_promesas + ' promesas en ' + x + ' entre ' + key + '.</p>' +
    //            '<div><a target="_blank" href="'+ e.point.link_ley +'">¿Cómo cumple la promesa? </a></div>' +
    //            '<div style="float:right;"><a href="https://twitter.com/share?text='+text_for_twitter+'&via=ciudadanoi&hashtags=21mayo" target="_blank" class="twitter-share-button"><i class="fa fa-twitter"></i> Twittear</a></div>'
    // })
      .valueFormat(d3.format('%'))
      // .barColor(d3.scale.category20().range())
      .transitionDuration(250)
      .stacked(false)
      .showControls(false);

  chart.xAxis
      .showMaxMin(false)

  chart.yAxis
      .tickFormat(d3.format('%'));

  chart.forceY([0,1]);

  d3.select('#chart1 svg')
      .datum(long_short_data)
      .call(chart);

  nv.utils.windowResize(chart.update);

  chart.dispatch.on('stateChange', function(e) { nv.log('New State:', JSON.stringify(e)); });

  return chart;
});