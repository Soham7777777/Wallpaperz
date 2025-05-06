"use strict";

/**
 * Retrieves string constants from HTML elements whose IDs start with "constant-" and end with the specified name suffix.
 * @param {string} name - The id suffix
 * @returns {string} - The constant value
 */
function loadConstant(name) {
    let textContent = document.getElementById(`constant-${name}`).textContent;
    if (textContent === null)
        return '';
    return textContent;
}


/**
 * Retrives array of messages from paragraph elements inside div with id "messages".
 * @returns {Array<string>} - The array of messages
 */
function loadMessages() {
    let messages = [];
    document.querySelectorAll('div#messages > p').forEach((element) => {
        let textContent = element.textContent;
        if(textContent === null)
            messages.push('');
        else
            messages.push(textContent);
    });
    return messages;
}
