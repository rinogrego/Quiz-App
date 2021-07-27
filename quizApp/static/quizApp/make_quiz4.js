
function generate_questions() {
  const generate_btn = document.querySelector('#generate-button');
  generate_btn.value = "Re-Generate";

  var number = document.querySelector('#num-generate').value;


  // Generate Info
  const topic_container = document.querySelector('#topic-container')
  const title_container = document.querySelector('#title-container')
  const num_container = document.querySelector('#num-container')

  topic_container.style.display = 'block';
  title_container.style.display = 'block';
  num_container.style.display = 'block';

  const num_input = document.getElementById('num');
  num_input.setAttribute('value', `${number}`);
  // Generate Info


  // Delete Pre-Populated Questions, Options, Answers, and Buttons
  try {
    x = document.querySelector('#questions-button-container');
    x.remove();
  } catch(err) {
    // alert(err.message);
  }


  // Delete Pre-Populated Questions, Options, Answers, and Buttons

  // Form
  const form_container = document.querySelector('#make-quiz-form')

  const questions_button_container = document.createElement('div');
  questions_button_container.setAttribute('id', 'questions-button-container');
  form_container.appendChild(questions_button_container)
  
  for (i=1; i <= number; i++) {

    // i = number of questions
    const question_container = document.createElement('div');
    question_container.setAttribute('id', `question-${i}-container`);
    question_container.setAttribute('class', `border-top border-danger pb-2 mt-3`);
    questions_button_container.appendChild(question_container);


    // Question_Q
    const question_q_container = document.createElement('div');
    question_q_container.setAttribute('class', 'mb-5 pt-3');
    question_container.appendChild(question_q_container);

      const question_label = document.createElement('label');
      question_label.setAttribute(`for`, `q-${i}`);
      question_label.setAttribute(`class`, `form-label make-a-quiz-quesion-q-label bg-dark p-2`);
      question_label.innerHTML = `Question ${i}:`;
      question_q_container.appendChild(question_label);

      const question_input = document.createElement('input');
      question_input.setAttribute('type', `text`);
      question_input.setAttribute('name', `q-${i}`);
      question_input.setAttribute('id', `q-${i}`);
      question_input.setAttribute('placeholder', `Input your question here`);
      question_input.setAttribute('class', `form-control bg-dark text-light border-custom-121212`);
      question_q_container.appendChild(question_input);
    // Question Q


    // Options
    // j = number of options
    const options_container = document.createElement('div');
    options_container.setAttribute('class', 'mb-3');
    question_container.appendChild(options_container);
    
    for (j=1; j <= 5; j++) {
      console.log(`constructing question-${i}-option-${j}`);
      const option_container = document.createElement('div');
      option_container.setAttribute('class', 'mb-1');
      
        const option_label = document.createElement('label');
        option_label.setAttribute('for', 'num');
        option_label.setAttribute('class', 'form-label');
        option_label.innerHTML = `Option ${j}:`;

        const option_input = document.createElement('input');
        option_input.setAttribute('type', `text`);
        option_input.setAttribute('name', `q-${i}-opt-${j}`);
        option_input.setAttribute('id', `q-${i}-opt-${j}`);
        option_input.setAttribute('placeholder', `Input your option here`);
        option_input.setAttribute('class', `form-control bg-dark text-light border-custom-121212`);
        option_input.setAttribute('onfocusout', `fillOption(this);`);

        option_container.appendChild(option_label);
        option_container.appendChild(option_input);

      options_container.appendChild(option_container);
    }
    

    // Answer
    const answer_label = document.createElement('label');
    answer_label.setAttribute('for', `q-${i}-answer`);
    answer_label.setAttribute('class', `form-label mt-3`);
    answer_label.innerHTML = 'Answer:';
    question_container.appendChild(answer_label);

    const answer_select = document.createElement('select');
    answer_select.setAttribute('name', `q-${i}-answer`);
    answer_select.setAttribute('id', `q-${i}-answer`);
    answer_select.setAttribute('class', `form-select mb-3 bg-dark text-light border-custom-121212`);
    question_container.appendChild(answer_select);
    // Answer


    // j = number of options for ANSWER
    for (j=0; j <= 5; j++) {

      if (j == 0) {
        const answer_option = document.createElement('option');
        answer_option.setAttribute('id', `q-${i}-opt-${j}-answer`);
        answer_option.value = "Answer-Not-Chosen";
        answer_option.innerHTML = "Enter your options above and after then you can choose the answer properly"
        answer_select.appendChild(answer_option);
        continue
      }
      
      console.log(`constructing question-${i}-option-${j}-for-answer`);
      const answer_option = document.createElement('option');
      answer_option.setAttribute('id', `q-${i}-opt-${j}-answer`);
      answer_option.value = "";

      answer_select.appendChild(answer_option);
    }
    
  }

  // Submit Button
  const button_container = document.createElement('div');
  button_container.setAttribute('class', 'mt-5 d-flex justify-content-end');
  questions_button_container.appendChild(button_container);

    // Without Modal
    // const button_input = document.createElement('input');
    // button_input.setAttribute(`type`, `submit`);
    // button_input.setAttribute(`value`, `Create New Quiz`);
    // button_input.setAttribute(`class`, `btn btn-dark mt-5 border-custom-121212`);
    // button_container.appendChild(button_input);

    // With Modal
    const button_modal = document.createElement('div');
    button_modal.setAttribute(`class`, `btn btn-dark mt-5 border-custom-121212`);
    button_modal.setAttribute('data-bs-toggle', 'modal');
    button_modal.setAttribute('data-bs-target', '#finish_create_modal');
    button_modal.innerHTML = "Submit New Quiz"
    button_container.appendChild(button_modal);
  // Submit Button

  // Form

}


function fillOption(dokumen) {
  let opt_id = `${dokumen.id}-answer`;

  document.querySelector(`#${opt_id}`).value = dokumen.value;
  document.querySelector(`#${opt_id}`).innerHTML = dokumen.value;
}