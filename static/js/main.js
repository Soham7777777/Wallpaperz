var tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
var tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))

var collapseElementList = document.querySelectorAll('.collapse')
var collapseList = [...collapseElementList].map(collapseEl => new bootstrap.Collapse(collapseEl))
