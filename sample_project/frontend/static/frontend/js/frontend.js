'use strict';

$(document).ready(function() {
});


function deleteRemoteObject(url, title, afterObjectDeleteCallback) {
    var modal = $('#modal_confirm');
    modal.find('.modal-title').text(title);
    modal.find('.btn-yes').off().on('click', function() {
        // User selected "Yes", so proceed with remote call
        $.ajax({
            type: 'GET',
            url: url
        }).done(function(data) {
            if (afterObjectDeleteCallback) {
                afterObjectDeleteCallback(data);
            }
        }).fail(function(jqXHR, textStatus, errorThrown) {
            alert('SERVER ERROR: ' + errorThrown);
        });
    });
    modal.modal('show');
}
