        const countryData = JSON.parse(document.getElementById("country-data").textContent);

        function updateCities() {
            const countrySelect = document.getElementById("country");
            const citySelect = document.getElementById("city");
            const selectedCountry = countrySelect.value;

            citySelect.innerHTML = '';
            if (countryData[selectedCountry]) {
                countryData[selectedCountry].forEach(city => {
                    const option = document.createElement("option");
                    option.value = city;
                    option.textContent = city;
                    citySelect.appendChild(option);
                });
            }
        }

        // Populate on load if country was already selected
        document.addEventListener("DOMContentLoaded", () => {
            updateCities();

            // Reselect previously chosen city
            const selectedCity = "{{ selected_city|escapejs }}";
            if (selectedCity) {
                const citySelect = document.getElementById("city");
                for (const option of citySelect.options) {
                    if (option.value === selectedCity) {
                        option.selected = true;
                        break;
                    }
                }
            }
        });