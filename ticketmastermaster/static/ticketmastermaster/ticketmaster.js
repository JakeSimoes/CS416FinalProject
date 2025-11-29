$("#submit").on("submit", function (event) {
  const genreInput = $("#genre-input").val();
  const cityInput = $("#city-input").val();
  $("#alert").hide();
  if (!genreInput.trim()) {
    $("#alert").text("Search term cannot be empty. Please enter a search term.").show();
  } else if (!cityInput.trim()) {
    $("#alert").text("City cannot be empty. Please enter a city.").show();
  } else {
      const params = new URLSearchParams(window.location.search);
      params.set("genre", genreInput.trim());
      params.set("city", cityInput.trim());
      params.delete("toast");
      window.location.search = params.toString();
  }
  // Prevents refreshing
  event.preventDefault();
});

console.log("test");