// Function to Download PDF
function downloadPDF() {
    const element = document.getElementById('timetable-card');
    const opt = {
        margin:       0.5,
        filename:     'timetable.pdf',
        image:        { type: 'jpeg', quality: 0.98 },
        html2canvas:  { scale: 2 },
        jsPDF:        { unit: 'in', format: 'letter', orientation: 'landscape' }
    };
    // Uses html2pdf library included in base.html
    html2pdf().set(opt).from(element).save();
}

// Function to Share
function shareLink() {
    if (navigator.share) {
        navigator.share({
            title: document.title,
            text: 'Check out this college timetable:',
            url: window.location.href,
        })
        .then(() => console.log('Successful share'))
        .catch((error) => console.log('Error sharing', error));
    } else {
        // Fallback for desktop browsers
        navigator.clipboard.writeText(window.location.href);
        alert("Link copied to clipboard!");
    }
}