var getCookies = (name) => {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
};

var csrf_token = getCookies("csrftoken");

function addToFavorites(centerId) {
    var button = document.getElementById(centerId);
    var favoriteImage = document.getElementById('favoriteImage');
    const formData = new FormData();
    formData.append('center_id', centerId);
    fetch('/map/favorites/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrf_token,
            "X-Requested-With": "XMLHttpRequest",
        },
        body: formData
    })

    .then(response => response.json())
        .then(data => {
             var currentImagePath = favoriteImage.src;
             if (data.status == 'created') {
                var newImagePath = '/static/img/dil.svg';
             } else {
                var newImagePath = '/static/img/dil-disable.svg';
             }
             button.innerHTML = '<img id="favoriteImage" src="' + newImagePath + '" alt="dil">';
        })
        .catch(error => console.error(error));

}


var removeButtons = document.querySelectorAll('.fav-center-remove');

removeButtons.forEach(function (button) {
    button.addEventListener('click', function () {
        var centerId = button.getAttribute('data-center-id');

        fetch("/account/remove_favorite_center/" + centerId + "/", {
            method: "POST",
            headers: {
                "X-CSRFToken": csrftoken,
                "X-Requested-With": "XMLHttpRequest",
            },
        })
        .then(function (response) {
                    return response.json();
                })
                .then(function (data) {
                    if (data.status === 'success') {
                        button.parentNode.remove();
                    } else {
                        console.error('Ошибка удаления из избранного:', data.message);
                    }
                })
                .catch(function (error) {
                    console.error('Ошибка при обработке ответа:', error);
                });
    });
});