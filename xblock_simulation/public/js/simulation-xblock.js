
window.SimulationXBlockStudentView = function(runtime, element, initArgs) {
  'use strict';

  var contentElement = element.querySelectorAll('.simulation-content')[0];

  if (initArgs['initFunction'].length > 0) {
    window[initArgs['initFunction']](runtime, contentElement, initArgs);
  }

};
