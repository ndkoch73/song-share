function openModal(identifier){
  $('.ui.modal'+'.'+identifier).modal('show');
}

function closeError(){
    $('.message .close').closest('.message').transition('fade');
}