document.addEventListener("DOMContentLoaded", function () {

  const addressInput = document.getElementById("faddress");

  addressInput.addEventListener("keydown", function (event) {
    console.log(event)
    if (event.key === "Enter") {
      event.preventDefault();
      const address = event.target.value;
      sendAddress(address);
    }
  });

  function sendAddress(address) {
    var noticeElement = document.querySelector('p.notice');

    const URL_BACKEND = 'http://0.0.0.0:8000'

    require(['axios'], function (axios) {
      const data = {
        address: address
      };

      axios.post(`${URL_BACKEND}/is_address`, JSON.stringify(data), {
        headers: {
          'Content-Type': 'application/json'
        }
      })
        .then(function (response) {
          if (response.data.status != 200) {
            noticeElement.textContent = response.data.data;
            noticeElement.style.color = '#FF0000';
          } else {
            noticeElement.textContent = response.data.data;
            noticeElement.style.color = '#39FF14';
            addressInput.value = '';
          }

        })
        .catch(function (error) {
          noticeElement.textContent = error.data.data;
          noticeElement.style.color = '#FF0000';
        });
    });
  }
})