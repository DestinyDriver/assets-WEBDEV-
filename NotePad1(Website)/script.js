// script.js

// Save the note content to localStorage
function saveNote() {
  const noteContent = document.getElementById("note").value;
  localStorage.setItem("note", noteContent);
}

// Load the saved note on page load
window.onload = function () {
  const savedNote = localStorage.getItem("note");
  if (savedNote) {
    document.getElementById("note").value = savedNote;
  }
};

// Auto-save the note whenever it's edited
document.getElementById("note").addEventListener("input", saveNote);
