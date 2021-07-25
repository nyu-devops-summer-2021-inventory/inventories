$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#inventory_item_id").val(res._id);
        $("#sku").val(res.sku);
        $("#count").val(res.count);
        $("#condition").val(res.condition);
        $("#restock_level").val(res.restock_level);
        $("#restock_amount").val(res.restock_amount);
        if (res.in_stock == true) {
            $("in_stock").val("true");
        } else {
            $("#in_stock").val("false");
        }
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#inventory_item_id").val("");
        $("sku").val("");
        $("count").val("");
        $("condition").val("");
        $("restock_level").val("");
        $("restock_amount").val("");
        $("in_stock").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    // ****************************************
    // Create an Inventory Item
    // ****************************************

    $("#create-btn").click(function () {

        var sku = $("#sku").val();
        var count = $("#count").val();
        var condition = $("condition").val();
        var restock_level = $("restock_level").val();
        var restocl_amount = $("restock_amount").val();
        var in_stock = $("#in_stock").val() == "true";

        var data = {
            "sku": sku,
            "count": count,
            "condition": condition,
            "restock_level": restock_level,
            "restock_amount": restocl_amount,
            "in_stock": in_stock
        };

        var ajax = $.ajax({
            type: "POST",
            url: "/inventories",
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
    // Update an Inventory Item
    // ****************************************

    $("#update-btn").click(function () {

        var sku = $("#sku").val();
        var count = $("#count").val();
        var condition = $("condition").val();
        var restock_level = $("restock_level").val();
        var restocl_amount = $("restock_amount").val();
        var in_stock = $("#in_stock").val() == "true";

        var data = {
            "sku": sku,
            "count": count,
            "condition": condition,
            "restock_level": restock_level,
            "restock_amount": restocl_amount,
            "in_stock": in_stock
        };

        var ajax = $.ajax({
                type: "PUT",
                url: "/inventories/" + inventory_item_id,
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
    // Retrieve an Inventory Item
    // ****************************************

    $("#retrieve-btn").click(function () {

        var inventory_item_id = $("#inventory_item_id").val();

        var ajax = $.ajax({
            type: "GET",
            url: "/inventories/" + inventory_item_id,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Delete an Inventory Item
    // ****************************************

    $("#delete-btn").click(function () {

        var inventory_item_id = $("#pinventory_item_id").val();

        var ajax = $.ajax({
            type: "DELETE",
            url: "/inventories/" + inventory_item_id,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("Inventory item has been Deleted!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#inventory_item_id").val("");
        clear_form_data()
    });

    // ****************************************
    // Search for an Inventory Item
    // ****************************************

    $("#search-btn").click(function () {

        var sku = $("#sku").val();
        var count = $("#count").val();
        var condition = $("condition").val();
        var restock_level = $("restock_level").val();
        var restocl_amount = $("restock_amount").val();
        var in_stock = $("#in_stock").val() == "true";

        var queryString = ""

        if (sku) {
            queryString += 'sku=' + sku
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
