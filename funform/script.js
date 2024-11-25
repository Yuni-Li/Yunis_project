// Initialization
const street = document.getElementById('streetName');
const suburb = document.getElementById('suburb');
const postcode = document.getElementById('postcode');
const dob = document.getElementById('dob');
const buildingType = document.getElementById('buildingType');
var features = document.querySelectorAll('input[name=features]');
const selectBtn = document.getElementById('selectAllBtn');
const resetBtn = document.getElementById('reset');
var text = document.getElementById("text");

// Main
function checkValidInput() {
  const streetValue = street.value;
  const suburbValue = suburb.value;
  const postcodeValue = postcode.value;
  let age = getAge(dob.value);


  if (streetValue.length > 50 || streetValue.length < 3) {
    return text.value = 'Please input a valid street name';
  } else {
    text.value = '';
  }

  if (suburbValue.length > 50 || suburbValue.length < 3) {
    return text.value = 'Please input a valid suburb';
  } else {
    text.value = '';
  }

  if (postcodeValue.length != 4 || isNaN(postcodeValue)) {
    return text.value = 'Please input a valid postcode';
  } else {
    text.value = '';
  }

  if (age < 0) {
    return text.value = 'Please enter a valid date of birth';
  } else {
    text.value = '';
  }

  type = buildingType.value === `Apartment` ? `an Apartment` : 'a House';
  output = `You are ${age} years old, and your address is ${streetValue} St, ${suburbValue}, ${postcodeValue}, Australia. Your building is ${type}, and it has ${getFeatures()}`;
  text.value = output;
}

// User interaction
street.onblur = () => checkValidInput();
suburb.onblur = () => checkValidInput();
postcode.onblur = () => checkValidInput();
dob.onblur = () => checkValidInput();
buildingType.onchange = () => checkValidInput();
features.forEach(feature => feature.onchange = () => {
  updateSelectBtn();
  checkValidInput();
});

// Switch between select and deselect button
selectBtn.onclick = () => {
  if (selectBtn.value === 'Select All') {
    features.forEach(feature => {
      feature.checked = true;
      feature.onchange = () => {
        checkValidInput();
        updateSelectBtn();
      };
    });
    selectBtn.value = 'Deselect All';
  } else {
    features.forEach(feature => {
      feature.checked = false;
      feature.onchange = () => {
        checkValidInput();
        updateSelectBtn();
      };
    });
    selectBtn.value = 'Select All';
  }
  checkValidInput();
}


// Helper Functions
function getAge(date) {
  const [day, month, year] = date.split('/').map(str => parseInt(str, 10));
  const today = new Date();
  const cur_year = today.getFullYear();
  const cur_month = today.getMonth() + 1;
  const cur_day = today.getDate();
  let age = cur_year - year;

  // Basic check and set the year has to between 1900 and current year
  if (!/[0-9]{2}\/[0,1][0-9]\/[1,2][0,9][0-9]{2}$/.test(date)) return -1;
  if (day > 31 || month > 12 || year > cur_year) return -1;

  // Invalid date check, dob cannot later than today
  // Correct Age
  if ((month > cur_month || (month === cur_month && day > cur_day))) age--;

  return age;
}

// Get current selected features
function getFeatures() {
  const selected = document.querySelectorAll('input[name=features]:checked');
  let cur_features = [];
  selected.forEach(feature => cur_features.push(feature.value));

  if (cur_features.length === 0) {
    return 'no features';
  } else if (cur_features.length === 1) {
    return cur_features[0];
  } else {
    const last_feature = cur_features.pop();
    return cur_features.join(', ') + ', and ' + last_feature;
  }
}

// If all buttons are selected/deselected manually
// Change current button to select/deselect all
function updateSelectBtn() {
  var featuresArray = Array.from(features);
  const allChecked = featuresArray.every(feature => feature.checked);
  const allUnChecked = featuresArray.every(feature => !feature.checked);
  if (allChecked) selectBtn.value = 'Deselect All';
  else if (!allUnChecked) selectBtn.value = 'Select All';
}
