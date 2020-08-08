let autocomplete;
function initAutocomplete(){
  autocomplete = new google.maps.places.Autocomplete(
  document.getElementById('autocomplete'), {
    types: ['establishment'],
    fields: ['place_id', 'geometry', 'name']
  });
  autocomplete.addListener('place_changed', onPlaceChanged);
}
function onPlaceChanged(){
  update()
}
function update(){
  var place = autocomplete.getPlace();
  if (!place.geometry){ //whether user actually clicked a prediction or entered some text that did not result in predictions
    document.getElementById('autocomplete').placeholder = "Search Items based on Locations";
  }
  let sites = 'https://www.google.com/maps/embed/v1/search?key=AIzaSyCZ2UdTtgsGg7Jbx7UmtnGPFh_pVRi2n4U&q=' + place.name
  document.getElementById('map').src = sites;
  }
