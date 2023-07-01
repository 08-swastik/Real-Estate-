// add sticky navigation bar

// activate the hamburger menu and mobile navigation
document.addEventListener("DOMContentLoaded", function() {
    searchInput.value = '';
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
    window.location = "/"; // Redirect to the home page
  }
  
  const searchInput = document.getElementById('search-input');
  const searchButton = document.getElementById('search-button');
  const searchResults = document.getElementById('search-results');
  

  function updateSearchResults(query) {
    if (!query) {
      searchResults.innerHTML = '';
      searchResults.style.display = 'none';
      return;
    }
  
    const url = '/search?query=' + query;
    fetch(url)
      .then(response => response.json())
      .then(data => {
        searchResults.innerHTML = '';
  
        const uniqueAddresses = [];
  
        data.forEach(result => {
          const address = result.address;
          const formattedAddress = address.toLocaleUpperCase('en-US'); // Convert address to uppercase English format
          if (!uniqueAddresses.includes(formattedAddress)) {
            uniqueAddresses.push(formattedAddress);
  
            const resultItem = document.createElement('div');
            resultItem.textContent = formattedAddress;
            resultItem.classList.add('result-item'); // Add a class to each result item

            resultItem.addEventListener('click', () => {
              const selectedCity = result.address;
              const fullUrl = searchButton.getAttribute('data-url') + '?city=' + encodeURIComponent(selectedCity);
              window.location.href = fullUrl;
            });

            searchResults.appendChild(resultItem);
          }
        });
  
        if (uniqueAddresses.length > 0) {
          searchResults.style.display = 'block';
        } else {
          searchResults.style.display = 'none';
        }
      })
      .catch(error => {
        console.error('Error fetching search results:', error);
      });
  }

  searchButton.addEventListener('click', () => {
    const query = searchInput.value;
    updateSearchResults(query);
  });
  
  // Event listener for input keyup
  searchInput.addEventListener('keyup', () => {
    const query = searchInput.value;
    updateSearchResults(query);
  });
  
  
  

  


function performSearch() {
  const city = searchInput.value.trim();
  const url = searchButton.getAttribute("data-url");

  if (city !== "") {
    const fullUrl = url + "?city=" + encodeURIComponent(city);
    window.location.href = fullUrl;
  }
}

searchButton.addEventListener('click', performSearch);

// Event listener for input keyup
searchInput.addEventListener('keyup', event => {
  if (event.key === 'Enter') {
    performSearch();
  }
});
  