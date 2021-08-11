$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#inventory_item_id").val(res.id);
        $("#inventory_item_sku").val(res.sku);
        $("#inventory_item_count").val(res.count);
        $("#inventory_item_condition").val(res.condition);
        $("#inventory_item_restock_level").val(res.restock_level);
        $("#inventory_item_restock_amount").val(res.restock_amount);
        if (res.in_stock == true) {
            $("#inventory_item_in_stock").val("true");
        } else {
            $("#inventory_item_in_stock").val("false");
        }
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#inventory_item_sku").val("");
        $("#inventory_item_count").val("");
        $("#inventory_item_condition").val("");
        $("#inventory_item_restock_level").val("");
        $("#inventory_item_restock_amount").val("");
        $("#inventory_item_in_stock").val("");

        $("#flash_message").empty();
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

        var sku = $("#inventory_item_sku").val();
        var count = $("#inventory_item_count").val();
        var item_condition = $("#inventory_item_condition").val();
        var restock_level = $("#inventory_item_restock_level").val();
        var restock_amount = $("#inventory_item_restock_amount").val();
        var in_stock = $("#inventory_item_in_stock").val() == "true";

        var data = {
            "sku": sku,
            "count": count,
            "condition": item_condition,
            "restock_level": restock_level,
            "restock_amount": restock_amount,
            "in_stock": in_stock
        };

        var ajax = $.ajax({
            type: "POST",
            url: "/api/inventories",
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

        var inventory_item_id = $("#inventory_item_id").val()
        var sku = $("#inventory_item_sku").val();
        var count = $("#inventory_item_count").val();
        var condition = $("#inventory_item_condition").val();
        var restock_level = $("#inventory_item_restock_level").val();
        var restock_amount = $("#inventory_item_restock_amount").val();
        var in_stock = $("#inventory_item_in_stock").val() == "true";

        var data = {
            "sku": sku,
            "count": count,
            "condition": condition,
            "restock_level": restock_level,
            "restock_amount": restock_amount,
            "in_stock": in_stock
        };

        var ajax = $.ajax({
                type: "PUT",
                url: "/api/inventories/" + inventory_item_id,
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
            url: "/api/inventories/" + inventory_item_id,
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

        var inventory_item_id = $("#inventory_item_id").val();

        var ajax = $.ajax({
            type: "DELETE",
            url: "/api/inventories/" + inventory_item_id,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Set an Inventory Item to In-Stock
    // ****************************************

    $("#in-stock-btn").click(function () {

        var inventory_item_id = $("#inventory_item_id").val();

        var ajax = $.ajax({
            type: "PUT",
            url: "/api/inventories/" + inventory_item_id + "/in-stock",
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("Success")
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

        var sku = $("#inventory_item_sku").val();
        var count = $("#inventory_item_count").val();
        var condition = $("#inventory_item_condition").val();
        var restock_level = $("#inventory_item_restock_level").val();
        var restock_amount = $("#inventory_item_restock_amount").val();
        var in_stock = $("#inventory_item_in_stock").val();

        var queryString = ""

        if (sku) {
            queryString += 'sku=' + sku
        }
        
        if (count) {
            if (queryString.length > 0) {
                queryString += '&count=' + count
            } else {
                queryString += 'count=' + count
            }
        }
        
        if (condition) {
            if (queryString.length > 0) {
                queryString += '&condition=' + condition
            } else {
                queryString += 'condition=' + condition
            }
        }

        if (restock_level) {
            if (queryString.length > 0) {
                queryString += '&restock_level=' + restock_level
            } else {
                queryString += 'restock_level=' + restock_level
            }
        }

        if (restock_amount) {
            if (queryString.length > 0) {
                queryString += '&restock_amount=' + restock_amount
            } else {
                queryString += 'restock_amount=' + restock_amount
            }
        }

        if (in_stock.length > 0) {
            if (queryString.length > 0) {
                queryString += '&in_stock=' + in_stock
            } else {
                queryString += 'in_stock=' + in_stock
            }
        }

        var ajax = $.ajax({
            type: "GET",
            url: "/api/inventories?" + queryString,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            $("#search_results").empty();
            $("#search_results").append('<table class="table-striped" cellpadding="10">');
            var header = '<tr>'
            header += '<th style="width:10%">ID</th>'
            header += '<th style="width:10%">SKU</th>'
            header += '<th style="width:10%">Count</th>'
            header += '<th style="width:10%">Condition</th>'
            header += '<th style="width:10%">Restock Level</th>'
            header += '<th style="width:10%">Restock Amount</th>'
            header += '<th style="width:10%">In Stock</th>'
            $("#search_results").append(header);
            var firstItem = "";
            for(var i = 0; i < res.length; i++) {
                var item = res[i];
                var row = "<tr><td>"+item.id+"</td><td>"+item.sku+"</td><td>"+item.count+"</td><td>"+item.condition+"</td><td>"+item.restock_level+"</td><td>"+item.restock_amount+"</td><td>"+item.in_stock+"</td></tr>";
                $("#search_results").append(row);
                if (i == 0) {
                    firstItem = item;
                }
            }

            $("#search_results").append('</table>');

            // copy the first result to the form
            if (firstItem != "") {
                update_form_data(firstItem)
            }

            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

})
