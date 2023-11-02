function get_new_entry() {
      $("#add_form_button").on('click', function () {
            clear_error()
            $("#successful_entry").empty()
            let new_entry = validate_all()
            if (new_entry["language"] && new_entry["speakers"] && new_entry["family"] && new_entry["review"]
                && new_entry["video"] && new_entry["countries"] && new_entry["difficulty"]) {
                  save_new_entry(new_entry)
            }
      })
}

function get_edit_entry() {
      $("#edit_form_button").on('click', function(){
            clear_error()
            let new_entry = validate_all()
            new_entry["id"] = $('#ID').val()
            if (new_entry["language"] && new_entry["speakers"] && new_entry["family"] && new_entry["review"]
            && new_entry["video"] && new_entry["countries"] && new_entry["difficulty"]){
                edit_entry(new_entry)
            }
      })
}

function validate_all(){
      let new_entry = {}
      new_entry["difficulty"] = validate_empty("difficulty")
      new_entry["countries"] = parse_list(validate_empty("countries"));
      new_entry["video"] = validate_empty("video");
      new_entry["review"] = validate_empty("review");
      new_entry["family"] = validate_empty("family");
      new_entry["speakers"] = validate_int("speakers");
      new_entry["language"] = validate_empty("language");
      return new_entry
}

function parse_list(list){
      if (list !== false)
            return list.split(',')
}

function validate_int(id){
      let value = $('#'+id).val();
      if (value.length === 0 || value.trim().length === 0){
            let error = "<span class='error'>Please fill this out</span>"
            $("#"+id).focus()
            $("#"+id+'_error').append(error)
            return false
      }
      else if ($.isNumeric(value) === false){
            let error = "<span class='error'>Please enter only digits</span>"
            $("#"+id).focus()
            $("#"+id+'_error').append(error)
      }
      else{
            return value
      }
}

function validate_empty(id){
      let value = $('#'+id).val();
      let error = "<span class='error'>Please fill this out</span>"
      if (value.length === 0 || value.trim().length === 0){
            $("#"+id).focus()
            $("#"+id+'_error').append(error)
            return false
      }
      else{
            return value
      }
}

function save_new_entry(new_entry) {
      $.ajax({
            type: "POST",
            url: "save_new_entry",
            dataType: "json",
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify(new_entry),
            success: function (id) {
                  clear_entry()
                  $("#language").focus()
                  window.scrollTo(0, 0)
                  let text = "<span class='success'>Successful Entry</span> - <a href='/view/" +
                      id +
                      "' class='list_two'> view here </a>"
                  $("#successful_entry").append(text)

            },
            error: function (request, status, error) {
                  console.log("Error");
                  console.log(request)
                  console.log(status)
                  console.log(error)
            }
      });
}

function edit_entry(new_entry) {
      $.ajax({
            type: "POST",
            url: "http://127.0.0.1:5000/edit_entry",
            dataType: "json",
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify(new_entry),
            success: function (id) {
                  let url = "/view/"+id
                  window.location.replace(url)
            },
            error: function (request, status, error) {
                  console.log("Error");
                  console.log(request)
                  console.log(status)
                  console.log(error)
            }
      });
}

function dialog_pop_up(){
      $("#discard_form_button").button().on( "click", function() {
            $("#dialog").dialog("open");
      });
      $("#dialog").dialog({
            autoOpen: false,
            modal: true,
            width: 500,
            buttons: {
                  "Yes, discard": function() {
                        $( this ).dialog( "close" );
                        let id_here = $('#ID').val()
                        let url = "/view/"+id_here
                        window.location.replace(url)
                  },
                  "No, continue": function() {
                        $( this ).dialog( "close" );
                  }
            }
      })
}

function clear_error(){
      $("#language_error").empty()
      $("#speakers_error").empty()
      $("#family_error").empty()
      $("#review_error").empty()
      $("#video_error").empty()
      $("#countries_error").empty()
      $("#difficulty_error").empty()
}

function clear_entry(){
      $("#language").val("")
      $("#speakers").val("")
      $("#family").val("")
      $("#review").val("")
      $("#video").val("")
      $("#countries").val("")
      $("#difficulty").val("")
}

$(document).ready(function(){
      get_new_entry();
      get_edit_entry();
      dialog_pop_up();
})