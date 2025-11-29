let updateButton = $(".button-update")
let cancelButton = $(".button-cancel")
let editButton = $(".button-edit")
let deleteButton = $(".button-delete")

editButton.on('click', function () {
    const post = $(this).closest(".post");
    toggleAll(post);
})

cancelButton.on('click', function () {
    const post = $(this).closest(".post");
    post.find(".post-text-edit").text(post.find(".post-text").text());
    toggleAll(post);
})

updateButton.on('click', function () {
    const post = $(this).closest(".post");
    const newText =
    $.ajax({
    type: "POST",
    url: "/discuss/update",
    data: { "text":  post.find(".post-text-edit").text()},
    dataType: "json", // Expected data type of the response (e.g., "json", "html", "xml")
    success: function(response) {
        // Callback function executed on successful request
        console.log("Success:", response);
    },
    error: function(jqXHR, textStatus, errorThrown) {
        // Callback function executed on request failure
        console.error("Error:", textStatus, errorThrown);
    }
});
})


function toggleAll(div) {
    updateForm = div.find('.update-form');
    if (updateForm.css('display') === "flex") {
        updateForm.css('display', 'none');
    } else {
      updateForm.css('display', 'flex');
    }
    // div.find(".button-update").toggle()
    // div.find(".button-cancel").toggle()
    div.find(".button-edit").toggle()
    div.find(".button-delete").toggle()
    div.find(".post-text").toggle()
    // div.find(".post-text-edit").toggle()
}