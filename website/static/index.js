function deleteNote(noteID){ // Take noteID
    // Send a request in javascript -> fetch()
    fetch('/delete-note',{
        method: 'POST',
        body: JSON.stringify({ noteID: noteID })
    }).then((_res) => {
        window.location.href = "/";
    });
    /*
    This is going to take the 'noteID' that It was passed, send a POST request to the delete note end point
    After it gets response from this delete note end point, it's going to reload the window.
    'window.location.href = "/"' means redirect to the homepage, refresh the page
    JSON.stringify({ noteID: noteID }) turns data into a string
    */
}