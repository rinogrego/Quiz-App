document.addEventListener("DOMContentLoaded", () => {

  // Hide all the questions first
  document.querySelectorAll('.test-container-for-questions').forEach( (question_container) => {
    question_container.setAttribute('style', 'display: none;')
  })
  document.querySelectorAll('.test-container-for-questions')[0].setAttribute('style', 'display: block')

  document.querySelector('#layout-footer').setAttribute('style', 'display: none;')


})

function switch_number (question_id) {

  question_id = parseInt(question_id);
  // Hide all the questions first
  document.querySelectorAll('.test-container-for-questions').forEach( (question_container) => {
    question_container.setAttribute('style', 'display: none;')
  })
  // Show the appropriate question
  document.querySelector(`#container-question-${question_id}`).setAttribute('style', 'display: block')

}