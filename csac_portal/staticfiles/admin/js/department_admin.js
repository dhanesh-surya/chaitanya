(function($) {
    $(document).ready(function() {
        // Locate the fieldset with the heading text "Banner"
        var bannerFieldset = $('fieldset').filter(function() {
            return $(this).find('h2').text().trim() === 'Banner';
        });
        
        if (bannerFieldset.length && $('#departmentbanner-group').length) {
            // Move the inline multiple banner uploads right after the Banner fieldset
            $('#departmentbanner-group').insertAfter(bannerFieldset);
        }
    });
})(django.jQuery);
