let currentYear;
let currentMonth;
let events = [];

document.addEventListener('DOMContentLoaded', function() {
    const currentDate = new Date();
    currentYear = currentDate.getFullYear();
    currentMonth = currentDate.getMonth() + 1;

    document.querySelector('.calendar__title').textContent = `${getMonthName(currentMonth)}, ${currentYear}`;

    updateCalendar(currentYear, currentMonth);

    document.getElementById('prev-month').addEventListener('click', function() {
        changeMonth(-1);
    });

    document.getElementById('next-month').addEventListener('click', function() {
        changeMonth(1);
    });

    events = {{ events | safe }};
});

function changeMonth(offset) {
    currentMonth += offset;

    if (currentMonth > 12) {
        currentMonth = 1;
        currentYear++;
    } else if (currentMonth < 1) {
        currentMonth = 12;
        currentYear--;
    }

    document.querySelector('.calendar__title').textContent = `${getMonthName(currentMonth)}, ${currentYear}`;
    updateCalendar(currentYear, currentMonth);
}

function updateCalendar(year, month) {
    const calendarContainer = document.getElementById('calendar-container');

    calendarContainer.innerHTML = '';

    const lastDay = new Date(year, month, 0).getDate();

    let firstDayOfWeek = new Date(year, month - 1, 1).getDay();

    firstDayOfWeek = (firstDayOfWeek === 0) ? 6 : (firstDayOfWeek - 1);

    for (let i = 0; i < firstDayOfWeek; i++) {
        const emptyCell = document.createElement('div');
        emptyCell.classList.add('calendar__month-cell', 'calendar__month-cell--empty');
        calendarContainer.appendChild(emptyCell);
    }

    for (let day = 1; day <= lastDay; day++) {
        const cell = document.createElement('div');
        cell.classList.add('calendar__month-cell');

        const span = document.createElement('span');
        span.classList.add('calendar__month-day');
        span.textContent = day;

        const eventForDay = getEventsForDay(day);
        if (eventForDay) {
        const eventContainer = document.createElement('div');
        eventContainer.classList.add('calendar__event-container');

        const eventText = document.createElement('div');
        eventText.classList.add('calendar__event-text');
        eventText.textContent = eventForDay.title;

        const eventLink = document.createElement('a');
        eventLink.classList.add('calendar__event-link', 'link');
        eventLink.href = eventForDay.get_absolute_url;
        eventLink.innerHTML = '<span>Подробнее</span><img src="images/arrow.svg" alt="icon">';

        eventContainer.appendChild(eventText);
        eventContainer.appendChild(eventLink);
        cell.appendChild(eventContainer);
    }

        cell.appendChild(span);
        calendarContainer.appendChild(cell);
    }
}

function getEventsForDay(day) {
    const eventForDay = events.find(event => event.event && event.event.data && event.event.data.getDate() === day);
    if (eventForDay) {
    }
    return eventForDay ? eventForDay.event : null;
}

function createEventCell(event) {
    const eventCell = document.createElement('div');
    eventCell.classList.add('calendar__month-cell', 'event-cell');

    return eventCell;
}

function getMonthName(month) {
    const monthNames = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'];
    return monthNames[month - 1];
}