// static/js/linked_select.js
(function($) {
    $(document).ready(function() {
        console.log("linked_select.js loaded");
        function initializeLinkedSelect(element) {
            var parentField = $(element).data('parent-field');
            var ajaxUrl = $(element).data('ajax-url');
            var parent = $('#id_' + parentField);

            console.log("Initializing linked select for:", element);
            console.log("Parent field:", parentField);
            console.log("AJAX URL:", ajaxUrl);

            parent.on('change', function() {
                var parentId = $(this).val();
                console.log("Parent changed:", parentId);
                if (parentId) {
                    $.ajax({
                        url: ajaxUrl,
                        data: {
                            'parent_id': parentId
                        },
                        success: function(data) {
                            console.log("AJAX success:", data);
                            var options = '<option value="">--------</option>';
                            $.each(data, function(key, value) {
                                options += '<option value="' + value.id + '">' + value.name + '</option>';
                            });
                            $(element).html(options);
                        },
                        error: function(xhr, status, error) {
                            console.error("AJAX error:", error);
                        }
                    });
                } else {
                    $(element).html('<option value="">--------</option>');
                }
            });
        }

        // Initialize all linked selects on the page
        $('#id_city').each(function() {
            initializeLinkedSelect(this);
        });

        $('#id_barangay').each(function() {
            initializeLinkedSelect(this);
        });

        // Also handle dynamically added rows (for inlines)
        $(document).on('formset:added', function(event, $row, formsetName) {
            $row.find('#id_city').each(function() {
                initializeLinkedSelect(this);
            });
            $row.find('#id_barangay').each(function() {
                initializeLinkedSelect(this);
            });
        });
    });
})(django.jQuery);