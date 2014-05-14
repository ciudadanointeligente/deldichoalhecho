function showInfo(data, tabletop) {
  var cnt = fila = 0;

  $.each( tabletop.sheets(), function(i, sheet) 
  {
    var rows = sheet.all().length;
    for(i = 0; i < rows; i++ ) 
    {
      if(cnt == 0)
        $("#data-content").append("<div class='row fila"+fila+"'>");
      
      var promesa   = sheet.elements[i].promesa;
      var detalles  = sheet.elements[i].detalles;
      var tipo      = '';
      var tmp_tipo  = sheet.elements[i].tipo;
      var area      = sheet.elements[i].area;

      var cnt_tipo = tmp_tipo.split(',');

      if (cnt_tipo.length > 1)
      {
        for (x = 0; x < cnt_tipo.length; x++) 
        {
          tipo += '<li class="type-'+cnt_tipo[x].toLowerCase()+'">'+cnt_tipo[x]+'</li>';
        }
      } 
      else 
      {
        tipo = '<li class="type-'+tmp_tipo.toLowerCase()+'">'+tmp_tipo+'</li>';
      }
      
      var twitter = '<a href="#" onclick="window.open(\'https://twitter.com/share?url=http://deldichoalhecho.cl/&amp;via=ciudadanoi&amp;hashtags=deldichoalhecho&amp;text='+promesa+'\',\'twitter\',\'width=450, height=250\')">twitter</a>';

      $(".fila"+fila).append("<div class='col-md-3 cajita'><span class='area'>"+area+"</span><ul id='social'><li>"+twitter+"</li></ul><h2 id='title'>"+promesa+"</h2><p class='detail'>"+detalles+"</p><ul id='type'>"+tipo+"</ul></div>");

      cnt++;
      
      if(cnt == 4) 
      {
        $("#data-content").append("</div>");
        cnt = 0;
        fila++;
      }
    }
  });
}