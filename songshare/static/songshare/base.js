function openModal(){
  $('.ui.modal').modal('show');
}

function closeError(){
    $('.message .close').closest('.message').transition('fade');
}