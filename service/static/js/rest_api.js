$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#shopcart_id").val(res._id);
        $("#customer_id").val(res.name);
        $("#items_list").val(res.category);
        if (res.items_available == true) {
            $("#items_available").val("true");
        } else {
            $("#items_available").val("false");
        }
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#shopcart_id").val("");
        $("#customer_id").val("");
        $("#items_available").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    // ****************************************
    // Create a Shopcart
    // ****************************************

    $("#create-shopcart-btn").click(function () {

        var customer_id = $("#customer_id").val();
        var items_list = [];

        var data = {
            "cusomer_id": customer_id,
            "items_list": []
            
        };

        console.log(data)

        var ajax = $.ajax({
            type: "POST",
            url: "/shopcarts",
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });


    // ****************************************
    // Update a Pet
    // ****************************************

    $("#update-btn").click(function () {

        var pet_id = $("#pet_id").val();
        var name = $("#pet_name").val();
        var category = $("#pet_category").val();
        var available = $("#pet_available").val() == "true";

        var data = {
            "name": name,
            "category": category,
            "available": available
        };

        var ajax = $.ajax({
                type: "PUT",
                url: "/pets/" + pet_id,
                contentType: "application/json",
                data: JSON.stringify(data)
            })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Retrieve a Shopcart
    // ****************************************

    $("#retrieve-btn").click(function () {
        console.log("Function works")
        var shopcart_id = $("#shopcart_id").val();

        var ajax = $.ajax({
            type: "GET",
            url: "/shopcarts/" + shopcart_id,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            //update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            //clear_form_data()
            //flash_message(res.responseJSON.message)
            flash_message("Error in retrieve-btn")
        });

    });

    // ****************************************
    // Delete a Pet
    // ****************************************

    $("#delete-btn").click(function () {

        var pet_id = $("#pet_id").val();

        var ajax = $.ajax({
            type: "DELETE",
            url: "/pets/" + pet_id,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("Pet has been Deleted!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#pet_id").val("");
        clear_form_data()
    });

    // ****************************************
    // Search for a Pet
    // ****************************************

    $("#search-btn").click(function () {

        var name = $("#pet_name").val();
        var category = $("#pet_category").val();
        var available = $("#pet_available").val() == "true";

        var queryString = ""

        if (name) {
            queryString += 'name=' + name
        }
        if (category) {
            if (queryString.length > 0) {
                queryString += '&category=' + category
            } else {
                queryString += 'category=' + category
            }
        }
        if (available) {
            if (queryString.length > 0) {
                queryString += '&available=' + available
            } else {
                queryString += 'available=' + available
            }
        }

        var ajax = $.ajax({
            type: "GET",
            url: "/pets?" + queryString,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            $("#search_results").empty();
            $("#search_results").append('<table class="table-striped" cellpadding="10">');
            var header = '<tr>'
            header += '<th style="width:10%">ID</th>'
            header += '<th style="width:40%">Name</th>'
            header += '<th style="width:40%">Category</th>'
            header += '<th style="width:10%">Available</th></tr>'
            $("#search_results").append(header);
            var firstPet = "";
            for(var i = 0; i < res.length; i++) {
                var pet = res[i];
                var row = "<tr><td>"+pet._id+"</td><td>"+pet.name+"</td><td>"+pet.category+"</td><td>"+pet.available+"</td></tr>";
                $("#search_results").append(row);
                if (i == 0) {
                    firstPet = pet;
                }
            }

            $("#search_results").append('</table>');

            // copy the first result to the form
            if (firstPet != "") {
                update_form_data(firstPet)
            }

            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

})
