function makeRequest(url, method, data={}, callback) {
  let requestOptions = {
    method: method,
    headers: {
      'Content-Type': 'application/json'
    }
  };

  if (method === 'GET') {
    const params = new URLSearchParams(data);
    url += '?' + params;
  } else {
    requestOptions.body = JSON.stringify(data);
  }

  fetch(url, requestOptions)
    .then(response => response.json())
//    .then(response => response.text())
    .then(result => callback(result))
    .catch(error => console.error(error));
}

const searchCity = () => {
    q = document.getElementById('city').value;
    weather_div = document.getElementById('weather');
    makeRequest(
        "/search",
        "GET",
        {q: q},
        function(data) {
            output = '';
            loc = data.location;
            output += `<h3>Координаты</h3><p>Широта: ${loc['lat']}, Долгота: ${loc['lon']}</p><p>${loc['location']}</p>`;
            weather = data.weather;
            output += `<p>Погода в: ${weather.name}</p>
            <p>Температура: ${weather.main.temp}, ощущается как ${weather.main.feels_like}</p>`;
            output += `<p>Описание: `;
            weather.weather.forEach(el => {
                output += `${el.description}&nbsp;<img src="https://openweathermap.org/img/wn/${el.icon}@2x.png"><br />`;
            });
            output += `</p>`;
            output += `<p>Ветер: ${weather.wind.deg}&deg;, скорость ${weather.wind.speed}`;
            if (weather.wind.gust != undefined) {
                output += ` - ${weather.wind.gust}`;
            }
            output += ` м/с</p>`;
            weather_div.innerHTML = output;
        }
    );
}

document.addEventListener('DOMContentLoaded', () => {

    btnSearchCity = document.querySelector("#search-city");
    if (btnSearchCity) {
        btnSearchCity.addEventListener('click', searchCity);
    }

});