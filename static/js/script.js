
document.addEventListener("DOMContentLoaded", function() {
  
  
  searchInputCity.value = '';
  searchInputAddress.value = '';
  
    
    
    
  
  searchResults.innerHTML = '';
  const hamb = document.querySelector(".hamb");
  const nav = document.querySelector(".nav-mobile");
  hamb.addEventListener("click", function() {
    hamb.classList.toggle("active");
    nav.classList.toggle("active");
  });
  
  
});
function showError() {
  alert("Please log in or register as a seller first.");
  window.location = "/"; 
}

function showError1() {
  alert("Please log in first");
  window.location = "/"; 
}



const searchInputAddress = document.getElementById('address-input');
const searchButton = document.getElementById('search-button');
const searchResults = document.getElementById('search-results');
const searchInputCity = document.getElementById('city-input');

searchInputAddress.disabled = true;

function updateCitySearchResults(cityQuery) {
  if (!cityQuery) {
    searchResults.innerHTML = '';
    searchResults.style.display = 'none';
    return;
  }
  
  const url = '/searchcity?city=' + cityQuery;
  fetch(url)
  .then(response => response.json())
  .then(data => {
    console.log(data)
    
        searchResults.innerHTML = '';
        
        const uniqueCity = [];
        
        data.forEach(result => {
          const city = result.city;
          const formattedCity = city.toLocaleUpperCase('en-US'); 
          if (!uniqueCity.includes(formattedCity)) {
            
            uniqueCity.push(formattedCity);
            
            const resultItem = document.createElement('div');
            resultItem.textContent = formattedCity;
            console.log(resultItem)
            resultItem.classList.add('result-item'); 
            
            searchResults.appendChild(resultItem);
            
            resultItem.addEventListener('click', () => {
              searchInputCity.value = city; 
              searchInputAddress.disabled = false;
              searchResults.style.display = 'none'; 
            });
            
            
            
          }
        });
        
        if (uniqueCity.length > 0) {
          searchResults.style.display = 'block';
        } else {
          searchResults.style.display = 'none';
        }
      })
      .catch(error => {
        console.error('Error fetching search results:', error);
      });
    }
    
    
    // Event listener for input keyup
    searchInputCity.addEventListener('keyup', () => {
      const query = searchInputCity.value;
      updateCitySearchResults(query);
    });
    
    
      
      
    
    
    function updateAddressSearchResults(addressQuery) {
      if (!addressQuery) {
        searchResults.innerHTML = '';
        searchResults.style.display = 'none';
        return;
      }
      
      const url = '/searchaddress?address=' + addressQuery;
      fetch(url)
      .then(response => response.json())
      .then(data => {
        console.log(data)
        
        searchResults.innerHTML = '';
        
        const uniqueAddress = [];
        
        data.forEach(result => {
          const address = result.address;
          const formattedAddress = address.toLocaleUpperCase('en-US'); 
          if (!uniqueAddress.includes(formattedAddress)) {
            
            uniqueAddress.push(formattedAddress);
            
            const resultItem = document.createElement('div');
            resultItem.textContent = formattedAddress;
            console.log(resultItem)
            resultItem.classList.add('result-item'); 
            
            searchResults.appendChild(resultItem);
            
            resultItem.addEventListener('click', () => {
              searchInputAddress.value = address; 
              searchResults.style.display = 'none'; 
            });
            
            
            
          }
        });
        
        if (uniqueAddress.length > 0) {
          searchResults.style.display = 'block';
        } else {
          searchResults.style.display = 'none';
        }
      })
      .catch(error => {
        console.error('Error fetching search results:', error);
      });
    }
    
    
    // Event listener for input keyup
    searchInputAddress.addEventListener('keyup', () => {
      const query = searchInputAddress.value;
      updateAddressSearchResults(query);
    });
    
    
    function performSearch() {
      const cityQuery = searchInputCity.value.trim();
      const addressQuery = searchInputAddress.value.trim();
      
      const url = '/properties?city=' + encodeURIComponent(cityQuery) + '&address=' + encodeURIComponent(addressQuery);
      
      
      window.location.href = url;
    }
    
    searchButton.addEventListener('click', () => {
      performSearch();
    });
    
    searchInputAddress.addEventListener('keydown', event => {
      if (event.key === 'Enter') {
        performSearch();
      }
    });
    
    
    
    
    
    
    var modal = document.getElementById('myModal');
    var modal1 = document.getElementById('myModal1');
    
    function openModal() {
      document.body.classList.add('modal-open');
      modal.style.display = 'flex';
      modal.addEventListener('focusout', handleFocusOut);
    }
    
    function openModal1() {
      document.body.classList.add('modal-open');
      modal1.style.display = 'flex';
      modal1.addEventListener('focusout', handleFocusOut1);
    }
    
    function closeModal() {
      document.body.classList.remove('modal-open');
      modal.style.display = 'none';
      modal.removeEventListener('focusout', handleFocusOut);
    }
    
    function handleFocusOut(event) {
      if (!modal.contains(event.relatedTarget)) {
        closeModal();
      }
    }
    
    function closeModal1() {
      document.body.classList.remove('modal-open');
      modal1.style.display = 'none';
      modal1.removeEventListener('focusout', handleFocusOut1);
    }
    
function handleFocusOut1(event) {
  if (!modal1.contains(event.relatedTarget)) {
    closeModal();
  }
}

