window.IncrementSimulation = function(runtime, element, initArgs) {
  'use strict';

  console.log(initArgs);

  var div = document.createElement('div');
  element.appendChild(div);

  var render = function(value) {
    div.innerHTML = '<button class="increment-simulation-button">' + value + '</button>';
  }

  var value = initArgs['userState']['value'];
  if (Number.isInteger(value) === false) {
    value = 0;
  }

  render(value);

  element.addEventListener('click', function(event) {
    var payload = JSON.stringify({
      'value': value + 1,
    });

    $.ajax({
      type: 'POST',
      url: initArgs['updateUserStateUrl'],
      data: payload,
      success: function(data) {
        value = data['value']
        render(value);
      }
    });
  });
};
