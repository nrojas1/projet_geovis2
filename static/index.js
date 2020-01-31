// Map set up
var map = L.map('map').setView([46.798333, 8.231944], 8);

map.setMaxBounds([[-85, -170], [85, 190]]);
map.setMinZoom(3);

var satImage = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/t\ile/{z}/{y}/{x}', {
    attribution: '&copy; <a href="https://www.esri.com">Esri</a>, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'
});
var topomap = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}', {
  attribution: 'Tiles © <a href="https://services.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer">ArcGIS</a>'
});
var stamenT = L.tileLayer('http://tile.stamen.com/toner/{z}/{x}/{y}.png', {
  attribution: ['Design by Shawn Allen at <a href="http://stamen.com/">Stamen</a>.',
                'Data courtesy of <a href="http://fuf.net/">FuF</a>,',
                '<a href="http://www.yellowcabsf.com/">Yellow Cab</a>',
                '&amp; <a href="http://sf-police.org/">SFPD</a>.']
});
var stamenWC = L.tileLayer(
  'http://tile.stamen.com/watercolor/{z}/{x}/{y}.jpg',{
    attribution:[
                'Design by Shawn Allen at <a href="http://stamen.com/">Stamen</a>',
                'Data courtesy of <a href="http://fuf.net/">FuF</a> ',
                '<a href="http://www.yellowcabsf.com/">Yellow Cab</a> ',
                '&amp; <a href="http://sf-police.org/">SFPD</a>.']
});
var osmNoirBlanc = L.tileLayer(
  'http://{s}.www.toolserver.org/tiles/bw-mapnik/{z}/{x}/{y}.png',{
    attribution: '&copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors'
});
topomap.addTo(map);

L.control.layers({
  "Stamen - Toner": stamenT,
  "Stamen - watercolor": stamenWC,
  "World Topographic": topomap,
  "Satelite": satImage,
  "OpenStreetMap B/W": osmNoirBlanc
}).addTo(map);

var cats = [
  'accordion', 'bass', 'clarinet', 'double-bass', 'drum-set', 'flute', 'guitar',
  'harmonica', 'harp', 'marimba', 'piano', 'saxophone', 'trombone',
  'trumpet', 'violin', 'vocal'
];

var icons = {};
for (var i=0; i < cats.length; i++){
  var c = cats[i];
  icons[c] = L.icon({
    iconUrl: 'static/icons/'+c+'.png',
    iconSize: [30, 30],
    iconAnchor:   [7, 7],
    popupAnchor:  [0, -7]
  });
};

var exprs = [
  'Composition/Arrangement', 'Improvisation/Jamm', 'Performance', 'Recording'
]
var genrs = [
  'Alternative', 'Blues', 'Brazilian', 'Classical', 'Country', 'Dance',
  'Gospel', 'Hip Hop/Rap', 'Indie', 'Jazz', 'Metal', 'Opera', 'Pop', 'Reggae',
   'Rhythm and Blues/Soul', 'Rock', 'Singer/Songwriter', 'World'
]
var marqueurs = [];
var instrpresent = [];
var instfilt = [];

function show_markers(){
  // first remove all existing markers on page
  for (var i=0; i < marqueurs.length; i++){
    map.removeLayer(marqueurs[i])
  }
  // empty out container
  marqueurs = [];
  instrpresent = [];

  var url = '/musicians.json';
  // json
  $.getJSON(url, function(data){
    var filtered = $('.unsel');
    instfilt = [];
    for (var i = 0; i < filtered.length; i++){ // each filtered instrument
      var filid = filtered[i].id;
      instfilt.push(parseInt(filid));
    }
    for (var i=0; i < data.length; i++){ // each musician
      var post = data[i];
      var mType = post.instrument_id;
      instrpresent.push(mType);
      if (!instfilt.includes(mType)){
        var mm = cats[mType-1];
        var m = L.marker(
          [post.x, post.y],
          {icon: icons[mm]}
        );
        m.addTo(map);
        m.info = post;
      }

      // display marker info
      m.on('click', function(e) {
        var xp = [exprs[e.target.info.skill_id1], exprs[e.target.info.skill_id2],
          exprs[e.target.info.skill_id3], exprs[e.target.info.skill_id4]]
        var stl = [genrs[e.target.info.genre_id1], genrs[e.target.info.genre_id2],
          genrs[e.target.info.genre_id3], genrs[e.target.info.genre_id4], genrs[e.target.info.genre_id5]]
        var html = '<table cellpadding="3" id="marker_info">';
        html += '     <tr>';
        html += '       <td><b>Name:</b></td>';
        html += '       <td>' + e.target.info.name.replace('{','').replace('}','') + '</td>';
        html += '     </tr>';
        html += '     <tr>';
        html += '       <td><b>Email:</b></td>';
        html += '       <td>' + e.target.info.email.replace('{','').replace('}','') + '</td>';
        html += '     </tr>';
        html += '     <tr>';
        html += '       <td><b>Experiences:</b></td>';
        html += '       <td>' + xp + '</td>';
        html += '     </tr>';
        html += '     <tr>';
        html += '       <td><b>Genres:</b></td>';
        html += '       <td>' + stl + '</td>';
        html += '     </tr>';
        // html += '     <tr>';
        // html += '       <td><button type="button" onclick="console.log(123);">Contact!</button></td>';
        // html += '     </tr>';
        html += '   </table>';
        $('#marker_info').remove();
        $('.info-box').html(html);
        $('#marker_info').insertAfter('#redirect-home');
        map.flyTo([e.target.info.x,e.target.info.y], 16);
      });
      marqueurs.push(m);
    }

    for (var i=0; i < 16; i++) { // each instrument for legend
      if(!instrpresent.includes(i)){
        var id = i;
        $('tr#'+id).attr('hidden','true');
      }
    }
  })
}

show_markers();

// Send map coordinates to form on [map] click
map.on('click', function(e){
  var coord = e.latlng;
  $('#lat').val(coord.lat.toFixed(4));
  $('#lng').val(coord.lng.toFixed(4));
});

// post data to app.py route which will update db!
function new_musician() {
  var post = $.post('/db_new_musician', function(data, status){
    alert("Data: " + data + "\nStatus: " + status);
  })
};

// form condition
$('[name="genre"]').on('change', function(e) {
  if($('[name="genre"]:checked').length >= 6) {
    alert('Thats alot of styles... How about a Top 5?');
    this.checked = false;
  };
});

// Event legent click
$('#instr tr').on('click', function(e){
  $(e.target).closest('tr').toggleClass('unsel');
  show_markers();
});

// button redirect_form
function redirect_form() {
  location.replace('/form');
}

// button redirect_form
function redirect_home() {
  location.replace('/');
}
