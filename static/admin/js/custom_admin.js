document.addEventListener('DOMContentLoaded', function() {
    console.log('custom_admin.js loaded');
    const commentCells = document.querySelectorAll('td.field-comments');

    commentCells.forEach(cell => {
        const originalText = cell.textContent.trim();
        const truncatedText = originalText.length > 30 ? originalText.substring(0, 30) + '...' : originalText;

        cell.textContent = truncatedText;

        cell.addEventListener('click', function() {
            console.log('Cell clicked');
            if (cell.textContent === truncatedText) {
                cell.textContent = originalText;
                cell.contentEditable = true;
                cell.focus();
            }
        });

        cell.addEventListener('blur', function() {
            console.log('Cell lost focus');
            cell.contentEditable = false;
            cell.textContent = cell.textContent.length > 30 ? cell.textContent.substring(0, 30) + '...' : cell.textContent;

            // Update the form field with the new value
            const row = cell.closest('tr');
            const inputField = row.querySelector('input[name$="-comments"]');
            if (inputField) {
                inputField.value = cell.textContent;
            }
        });
    });
});