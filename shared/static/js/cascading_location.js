// shared/static/js/cascading_location.js
(function($) {
    $(document).ready(function() {
        function updateDropdown(changer, dependent, url) {
            var changerValue = changer.val();
            if (changerValue) {
                $.ajax({
                    url: url,
                    data: {
                        parent_id: changerValue
                    },
                    success: function(data) {
                        dependent.empty().append('<option value="">---------</option>');
                        $.each(data, function(key, value) {
                            dependent.append($('<option></option>').attr('value', value.id).text(value.name));
                        });
                        dependent.trigger('change'); // Trigger change to update next dropdown
                    }
                });
            } else {
                dependent.empty().append('<option value="">---------</option>');
                dependent.trigger('change');
            }
        }

        var $province = $('#id_province');
        var $city = $('#id_city');
        var $barangay = $('#id_barangay');

        // Initial state (if editing an existing object)
        if ($province.val()) {
            updateDropdown($province, $city, '/api/tourism/get_cities/');
        }
        if ($city.val()) {
            updateDropdown($city, $barangay, '/api/tourism/get_barangays/');
        }

        // Event listeners
        $province.on('change', function() {
            updateDropdown($province, $city, '/api/tourism/get_cities/');
        });

        $city.on('change', function() {
            updateDropdown($city, $barangay, '/api/tourism/get_barangays/');
        });

        // Handle dynamically added inlines (if applicable)
        $(document).on('formset:added', function(event, $row, formsetName) {
            var $newProvince = $row.find('#id_province');
            var $newCity = $row.find('#id_city');
            var $newBarangay = $row.find('#id_barangay');

            $newProvince.on('change', function() {
                updateDropdown($newProvince, $newCity, '/api/tourism/get_cities/');
            });

            $newCity.on('change', function() {
                updateDropdown($newCity, $newBarangay, '/api/tourism/get_barangays/');
            });
        });
    });
})(django.jQuery);
