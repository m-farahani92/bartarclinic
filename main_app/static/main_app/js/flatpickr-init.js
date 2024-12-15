document.addEventListener('DOMContentLoaded', function() {
    flatpickr(".flatpickr-input", {
        enableTime: true,
        noCalendar: true,
        dateFormat: "H:i",
        time_24hr: true
    });
});
