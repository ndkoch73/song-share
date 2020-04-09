function openModal(){
  $('.ui.modal').modal('show');
}

function closeError(){
    $('.message .close').on('click', function() {
      $(this).closest('.message').transition('fade');
    });
}