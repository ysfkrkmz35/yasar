$(document).ready(function(){
    var hoverTimeout;
    $('.meeting-name').hover(function() {
        var element = $(this);
        hoverTimeout = setTimeout(function(){
            // İlgili URL'ye preview parametresini ekleyelim:
            var pdfUrl = element.data('pdf-url') + '?preview=1';
            $('#pdfPreviewFrame').attr('src', pdfUrl);
            $('#pdfPreviewModal').modal('show');
        }, 500); // 500 ms gecikme
    }, function() {
        clearTimeout(hoverTimeout);
        // İsterseniz mouse ayrıldığında modal'in kapanmasını sağlayabilirsiniz.
        // $('#pdfPreviewModal').modal('hide');
    });

    $('#pdfPreviewModal').on('hidden.bs.modal', function () {
        $('#pdfPreviewFrame').attr('src', '');
    });
});
