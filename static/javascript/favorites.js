function toggleFavorite(restaurantId) {
  let favorites = JSON.parse(localStorage.getItem('favorites')) || [];
  const index = favorites.indexOf(restaurantId);
  
  if (index === -1) {
    // Add to favorites
    favorites.push(restaurantId);
    document.querySelector(`[data-restaurant-id="${restaurantId}"]`).textContent = "Remove from Favorites";
  } else {
    // Remove from favorites
    favorites.splice(index, 1);
    document.querySelector(`[data-restaurant-id="${restaurantId}"]`).textContent = "Add to Favorites";
  }
  
  localStorage.setItem('favorites', JSON.stringify(favorites));
}