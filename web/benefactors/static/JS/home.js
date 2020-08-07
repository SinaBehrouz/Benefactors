function expandSearchOpt() {
  var hint = document.getElementById('content');
  if (hint.classList.contains('adv-search-hidden')){
    hint.classList.remove('adv-search-hidden');
    hint.classList.add('adv-search-visible');
  }else{
    hint.classList.remove('adv-search-visible');
    hint.classList.add('adv-search-hidden');
  }
}

let autocomplete;
function initAutocomplete(){
  autocomplete = new google.maps.places.Autocomplete(
  document.getElementById('autocomplete','locality','(cities)'), {
    types: ['establishment'],
    componentRestrictions:{'country': ['CA']},
    fields: ['place_id', 'geometry', 'name', 'address_components', 'geometry', 'icon']
  });
}
