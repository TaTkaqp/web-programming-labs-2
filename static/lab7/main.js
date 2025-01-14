function fillFilmList() {
    fetch('/lab7/rest-api/films/')
    .then(function (data) {
        return data.json();
    })
    .then(function (films) {
        let tbody = document.getElementById('film-list');
        tbody.innerHTML = '';
        for(let i = 0; i<films.length; i++) {
            let tr = document.createElement('tr');

            let tdTitleRus = document.createElement('td');
            let tdTitle = document.createElement('td');
            let tdYear = document.createElement('td');
            let tdAction = document.createElement('td');

            tdTitleRus.innerText = films[i].title_ru;
            let originalTitle = document.createElement('span');
            originalTitle.innerText = films[i].title === films[i].title_ru ? '' : films[i].title;
            originalTitle.style.fontStyle = 'italic';
            originalTitle.innerText = originalTitle.innerText ? ` (${originalTitle.innerText})` : '';
            tdTitle.appendChild(originalTitle);
            tdYear.innerText = films[i].year;

            let editButton = document.createElement('button');
            editButton.innerText = 'Редактировать';
            

            editButton.onclick = function() {
                editFilm(i);
            }

            let delButton = document.createElement('button');
            delButton.innerText = 'Удалить';


            delButton.onclick = function() {
                deleteFilm(i, films[i].title_ru);
            }

            tdAction.append(editButton);
            tdAction.append(delButton);

            tr.append(tdTitleRus);
            tr.append(tdTitle);
            tr.append(tdYear);
            tr.append(tdAction);

            tbody.append(tr);
        }
    })
}

function deleteFilm(id, title) {
    if(! confirm(`Вы точно хотите удалить фильм? "${title}"?`))
        return;

    fetch(`/lab7/rest-api/films/${id}`, {method: 'DELETE'})
        .then(function () {
            fillFilmList();
        });
}

function sendFilm() {
    const id = document.getElementById('id').value;
    const film = {
        title: document.getElementById('title').value || '',
        title_ru: document.getElementById('title-ru').value || '',
        year: document.getElementById('year').value || '',
        description: document.getElementById('description').value || ''
    }

    const url = id === '' ? '/lab7/rest-api/films/' : `/lab7/rest-api/films/${id}`;
    const method = id === '' ? 'POST' : 'PUT';

    fetch(url, {
        method: method,
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(film)
    })
    .then(function(resp) {
        if(resp.ok) {
            fillFilmList();
            hideModal();
            return; 
        }
        return resp.json();
    })
    .then(function(errors) {
        document.getElementById('year-error').innerText = errors.year || '';
        document.getElementById('description-error').innerText = errors.description || '';
        document.getElementById('titleru-error').innerText = errors.title_ru || '';
        document.getElementById('title-error').innerText = errors.title || '';
    });
}


function editFilm(id) {
    fetch(`/lab7/rest-api/films/${id}`)
    .then(function (data) {
        return data.json();
    })
    .then(function (film) {
        document.getElementById('id').value = id;
        document.getElementById('title').value = film.title;
        document.getElementById('title-ru').value = film.title_ru;
        document.getElementById('year').value = film.year;
        document.getElementById('description').value = film.description;
        showModal();
    });
}

function showModal() {
    document.querySelector('div.modal').style.display = 'block';
    document.getElementById('description-error').innerText = '';
    document.getElementById('titleru-error').innerText = '';
    document.getElementById('title-error').innerText = '';
    document.getElementById('year-error').innerText = '';
}

function hideModal() {
    document.querySelector('div.modal').style.display = 'none';
}

function cancel() {
    hideModal();
}

function addFilm() {
    document.getElementById('id').value = '';
    document.getElementById('title').value = '';
    document.getElementById('title-ru').value = '';
    document.getElementById('year').value = '';
    document.getElementById('description').value = '';
    showModal();
}