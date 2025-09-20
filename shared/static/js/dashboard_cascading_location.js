document.addEventListener("DOMContentLoaded", function() {
    const provinceSelect = document.getElementById("id_province");
    const citySelect = document.getElementById("id_city");
    const barangaySelect = document.getElementById("id_barangay");

    if (provinceSelect) {
        provinceSelect.addEventListener("change", function() {
            const provinceId = this.value;
            if (provinceId) {
                fetch(`/admin_dash/get-cities/?province_id=${provinceId}`)
                    .then(response => response.json())
                    .then(data => {
                        citySelect.innerHTML = '<option value="">---------</option>';
                        data.forEach(city => {
                            const option = new Option(city.name, city.id);
                            citySelect.add(option);
                        });
                    });
            } else {
                citySelect.innerHTML = '<option value="">---------</option>';
                barangaySelect.innerHTML = '<option value="">---------</option>';
            }
        });
    }

    if (citySelect) {
        citySelect.addEventListener("change", function() {
            const cityId = this.value;
            if (cityId) {
                fetch(`/admin_dash/get-barangays/?city_id=${cityId}`)
                    .then(response => response.json())
                    .then(data => {
                        barangaySelect.innerHTML = '<option value="">---------</option>';
                        data.forEach(barangay => {
                            const option = new Option(barangay.name, barangay.id);
                            barangaySelect.add(option);
                        });
                    });
            } else {
                barangaySelect.innerHTML = '<option value="">---------</option>';
            }
        });
    }
});
