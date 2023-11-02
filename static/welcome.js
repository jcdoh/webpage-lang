function populate_three(){
    $.each(most, function(index, value){
        let name = "<div class=\"list_one\"> " +
            (index+1) +
            ". <a href=\"view\/" +
            value.id +
            "\" class=\"list_two\">" +
            value.language +
            "<img class='icon' alt='Flag of Europe' src='https://www.mapsnworld.com/europe/europe-flag.jpg'> <\/a> <br> " +
            "<\/div> <div class=\"list_three\"> " +
            value.review +
            " <br> <span class=\"grey\">Worldwide Speakers<\/span>: " +
            value.speakers +
            " <\/div>"
        $("#top_three").append(name)
    })
    $.each(least, function(index, value){
        let name = "<div class=\"list_one\"> " +
            (index+1) +
            ". <a href=\"view\/" +
            value.id +
            "\" class=\"list_two\">" +
            value.language +
            "<img class='icon' alt='Flag of Europe' src='https://www.mapsnworld.com/europe/europe-flag.jpg'> <\/a><br> " +
            "<\/div> <div class=\"list_three\"> " +
            value.review +
            " <br> <span class=\"grey\">Worldwide Speakers<\/span>: " +
            value.speakers +
            " <\/div>"
        $("#bottom_three").append(name)
    })
}

$(document).ready(function(){
      populate_three()
})