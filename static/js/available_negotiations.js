
function handleSelectChange(select) {
  const selectedValue = select.value;
  console.log(selectedValue);

    select.style.backgroundColor = getOptionColor(selectedValue);

    if (selectedValue === 'accepted') {
      
      const allSelectElements = document.querySelectorAll('.initialaction-select, .action-select');
      
      allSelectElements.forEach((element) => {
        if (element !== select) {
          element.value = 'rejected';
          element.style.backgroundColor = getOptionColor('rejected');
        }
      });
    }
  }
  

  function getOptionColor(value) {
    if (value === 'pending') {
      return '#999999';
    } else if (value === 'rejected') {
      return '#f04141';
    } else if (value === 'accepted') {
      return '#3f9783';
    }
  }

  document.addEventListener("DOMContentLoaded", function() {
    const selectElements = document.querySelectorAll('.initialaction-select');
    selectElements.forEach((selectElement) => {
      
      handleSelectChange(selectElement); 
    });
    const actionSelectElements = document.querySelectorAll('.action-select');
    actionSelectElements.forEach((selectElement) => {
      
      selectElement.addEventListener('change', function() {
        handleSelectChange(this); // Call the function on change event
      });
    });
    const actionSelectElements1 = document.querySelectorAll('.initialaction-select');
    actionSelectElements1.forEach((selectElement) => {
      
      selectElement.addEventListener('change', function() {
        handleSelectChange(this); // Call the function on change event
      });
  });
})


