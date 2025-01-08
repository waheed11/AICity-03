function switchLanguage() {
    const questionId = document.getElementsByName("question_index")[0].value;  // Get question ID
    const currentUrlPath = window.location.pathname;
    const pathPattern = /\/([a-z]+)-([a-z]{2})/;
    const match = currentUrlPath.match(pathPattern);

    if (match) {
        const subject = match[1];
        const currentLanguage = match[2];
        const newLanguage = currentLanguage === 'en' ? 'ar' : 'en';

        // Redirect to the new path with the question ID included as a query parameter
        const newPath = `/${subject}-${newLanguage}?qid=${questionId}`;
        window.location.href = newPath;
    }
}