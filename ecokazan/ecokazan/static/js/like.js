const getCookie = (name) => {
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

const csrftoken = getCookie("csrftoken");

const likeButtons = document.querySelectorAll('.shop__favorite');

likeButtons.forEach(button => {
    button.addEventListener('click', event => {
        const storeId = parseInt(button.dataset.store);
        const formData = new FormData();
        var likeImage = document.getElementById('likeImage');
        formData.append('store_id', storeId);
        fetch("/store/like/", {
            method: "POST",
            headers: {
                "X-CSRFToken": csrftoken,
                "X-Requested-With": "XMLHttpRequest",
            },
            body: formData
        }).then(response => response.json())
        .then(data => {
             var currentImagePath = likeImage.src;
             if (data.status == 'created') {
                var newImagePath = '/static/img/dil.svg';
             } else {
                var newImagePath = '/static/img/dil-disable.svg';
             }
             button.innerHTML = '<img src="' + newImagePath + '" alt="dil">';
        })
        .catch(error => console.error(error));
    });
});

const ratingInputs = document.querySelectorAll('.shop__rate-input');

ratingInputs.forEach(input => {
    input.addEventListener('click', event => {
        const value = input.value;
        const storeId = parseInt(input.dataset.storeId);
        input.innerHTML = '';
        const formData = new FormData();
        formData.append('store_id', storeId);
        formData.append('value', value);
        formData.append('data_id', input.dataset.storeId)
        fetch("/store/rating/", {
            method: "POST",
            headers: {
                "X-CSRFToken": csrftoken,
                "X-Requested-With": "XMLHttpRequest",
            },
            body: formData
        }).then(response => response.json())
        .catch(error => console.error(error));
    });
});

var removeButtons = document.querySelectorAll('.fav-store-remove');

removeButtons.forEach(function (button) {
    button.addEventListener('click', function () {
        var storeId = button.getAttribute('data-store-id');

        fetch("/account/remove_favorite_store/" + storeId + "/", {
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



const saveButtons = document.querySelectorAll('.save-event');

saveButtons.forEach(button => {
    button.addEventListener('click', event => {
        const eventId = parseInt(button.dataset.event);
        const formData = new FormData();
        formData.append('event_id', eventId);
        fetch("/forum/save/", {
            method: "POST",
            headers: {
                "X-CSRFToken": csrftoken,
                "X-Requested-With": "XMLHttpRequest",
            },
            body: formData
        }).then(response => response.json())
        .then(data => {
            if (data.status == 'created') {
                button.textContent = 'В каленаре';
            }
            if (data.status == 'deleted') {
                button.textContent = 'Добавить в мой календарь';
            }
        })
        .catch(error => console.error(error));
    });
});