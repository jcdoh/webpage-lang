function get_query(){
      $("#search_button").on('click', function(){
            let text = $("#search_text").val()
            if (text.length === 0 || text.trim().length === 0){
                  clear()
            }
            else {
                  url = "/search_results/" + text
                  window.location.replace(url)
            }
      })
      $("#search_text").keypress(function(e) {
            if (e.which === 13) {
                  $("#search_button").click()
            }
      })
}

function redirect_edit(){
      $("#edit_button").on('click', function(){
            url = "/edit/" + info.id
            window.location.replace(url)
      })
}

function add_entry(){
      $("#add_button").on('click', function(){
            $("#successful_entry").empty()
            window.location.replace("/add")
      })
}

function replace_text(name_of_class){
      let inputText = document.getElementsByClassName(name_of_class);
      for (let i = 0; i < inputText.length; i++) {
            let text = inputText[i]
            let innerHTML = text.innerHTML;
            let index = innerHTML.toLowerCase().indexOf(search.toLowerCase());
            if (index >= 0) {
                  innerHTML = innerHTML.substring(0, index) + "<span class='bolded'>" +
                      innerHTML.substring(index, index + search.length) + "</span>" + innerHTML.substring(index + search.length);
                  console.log(innerHTML)
                  text.innerHTML = innerHTML;
            }
      }
}

function clear(){
      $("#search_text").val("")
      $("#search_text").focus()
}

$(document).ready(function(){
      get_query()
      add_entry()
      redirect_edit()
      replace_text("replace_family")
      replace_text("replace_language")
      replace_text("replace_country")
})