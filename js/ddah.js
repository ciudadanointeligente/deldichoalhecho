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
      var detail    = sheet.elements[i].detalles;
      var min_detail= sheet.elements[i].detalles.substr(0,215);
      var tipo      = '';
      var tmp_tipo  = sheet.elements[i].tipo;
      var area      = sheet.elements[i].area;
      var view_more = ''

      var cnt_tipo = tmp_tipo.split(',');

      if (cnt_tipo.length > 1)
      {
        for (x = 0; x < cnt_tipo.length; x++) 
        {
          tipo += '<li class="type-'+cnt_tipo[x].toLowerCase()+'">&nbsp;</li>';
        }
      } 
      else 
      {
        tipo = '<li class="type-'+tmp_tipo.toLowerCase()+'">&nbsp;</li>';
      }

      if(detail.length > 215)
        view_more = '...<a href="#" data-toggle="modal" data-target="#myModal-'+i+'">ver más</a>'
      
      var twitter = '<a href="#" onclick="window.open(\'https://twitter.com/share?url=http://deldichoalhecho.cl/&amp;via=ciudadanoi&amp;hashtags=deldichoalhecho&amp;text='+promesa+'\',\'twitter\',\'width=450, height=250\')"><i class="fa fa-twitter"></i> twitter</a>';
      var modal = '<div class="modal fade" id="myModal-'+i+'" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true"><div class="modal-dialog"><div class="modal-content"><div class="modal-header"><button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button><h4 class="modal-title" id="myModalLabel">'+promesa+'</h4></div><div class="modal-body">'+detail+'</div><div class="modal-footer"><button type="button" class="btn btn-default" data-dismiss="modal">Cerrar</button></div></div></div></div>';
      var filter_class = area.replace(/[Áá]/g,"a").replace(/[Éé]/g,"e").replace(/[Íí]/g,"i").replace(/[Óó]/g,"o").replace(/[Úú]/g,"u").replace(/[,]/g,"").replace(/[\s]/g,"-").toLowerCase();

      $(".fila"+fila).append("<div class='col-md-3 "+filter_class+"'><div class='cajita'><span class='area'>"+area+"</span><h4 id='title'>"+promesa+"</h4><ul id='social'><li>"+twitter+"</li></ul><p class='detail'>"+min_detail+view_more+"</p><ul id='type'>"+tipo+"</ul></div>"+modal+"</div>");

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