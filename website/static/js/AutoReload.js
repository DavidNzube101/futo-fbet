function autoReload(element) {
    function saveTagState(innerHTML) {
        localStorage.setItem('tag_state', `${innerHTML}`);
    }

    const currentTagState = element.innerHTML;
    const previousTagState = localStorage.getItem('tag_state');

    if (currentTagState !== previousTagState) {
        saveTagState(currentTagState);
        location.reload();
        console.log(currentTagState);
    }
// }