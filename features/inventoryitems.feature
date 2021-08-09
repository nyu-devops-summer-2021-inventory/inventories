Feature: The inventory item service back-end
    As a warehouse manager
    I need a RESTful catalog service
    So that I can keep track of everything I have in my inventory

Background:
    Given the following inventory items
        | sku       | count   | condition | restock_level | restock_amount | in_stock |
        | ABCD      | 10      | New       | 2             | 10             | True     |
        | EFGH      | 20      | Used      | 5             | 15             | True     |
        | IJKL      | 30      | Used      | 10            | 20             | True     |
        | MNOP      | 0       | New       | 2             | 5              | False    |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Inventory RESTful Service" in the title
    And I should not see "404 Not Found"

Scenario: Read an Item by ID
    When I visit the "Home Page"
    And I set the "SKU" to "MNOP"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "MNOP" in the results
    When I copy the "ID" field
    And I press the "Clear" button
    And I paste the "ID" field
    And I press the "Retrieve" button
    Then I should see "MNOP" in the "SKU" field
    And I should see "0" in the "Count" field
    And I should see "New" in the "Condition" field
    And I should see "2" in the "Restock_Level" field
    And I should see "5" in the "Restock_Amount" field
    And I should see "False" in the "In_Stock" dropdown

Scenario: Create an Item
    When I visit the "Home Page"
    And I set the "SKU" to "NEWSKU"
    And I set the "Count" to "10"
    And I set the "Condition" to "New"
    And I set the "Restock_Level" to "2"
    And I set the "Restock_Amount" to "10"
    And I select "True" in the "In_Stock" dropdown
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "ID" field
    And I press the "Clear" button
    Then the "ID" field should be empty
    And the "SKU" field should be empty
    And the "Condition" field should be empty
    When I paste the "ID" field
    And I press the "Retrieve" button
    Then I should see "NEWSKU" in the "SKU" field
    And I should see "New" in the "Condition" field
    And I should see "True" in the "In_Stock" dropdown

Scenario: Delete an Item
    When I visit the "Home Page"
    And I set the "SKU" to "ABCD"
    And I press the "Search" button
    Then I should see "ABCD" in the "SKU" field
    And I should see "New" in the "Condition" field
    And I should see "2" in the "Restock_Level" field
    And I should see "10" in the "Restock_Amount" field
    And I should see "True" in the "In_Stock" dropdown
    When I copy the "ID" field
    And I press the "Delete" button
    Then I should see the message "Success"
    When I press the "Clear" button
    And I paste the "ID" field
    And I press the "Retrieve" button
    Then the "SKU" field should be empty
    And the "Condition" field should be empty
    And the "Restock_Level" field should be empty
    And the "Restock_Amount" field should be empty

Scenario: List all items
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see "ABCD" in the results
    And I should see "EFGH" in the results
    And I should see "IJKL" in the results
    And I should see "MNOP" in the results 

Scenario: Use In-Stock Action
    When I visit the "Home Page"
    And I set the "SKU" to "MNOP"
    And I press the "Search" button
    Then I should see "MNOP" in the "SKU" field
    And I should see "New" in the "Condition" field
    And I should see "0" in the "Count" field
    And I should see "2" in the "Restock_Level" field
    And I should see "5" in the "Restock_Amount" field
    And I should see "False" in the "In_Stock" dropdown
    
    When I copy the "ID" field
    And I press the "Clear" button
    And I paste the "ID" field
    And I press the "In-Stock" button
    Then I should see the message "Success"
    
    When I press the "Retrieve" button
    Then I should see "MNOP" in the "SKU" field
    And I should see "New" in the "Condition" field
    And I should see "0" in the "Count" field
    And I should see "2" in the "Restock_Level" field
    And I should see "5" in the "Restock_Amount" field
    And I should see "True" in the "In_Stock" dropdown


Scenario: Update an Item
    When I visit the "Home Page"
    And I set the "SKU" to "ABCD"
    And I press the "Search" button
    Then I should see "ABCD" in the "SKU" field
    And I should see "New" in the "Condition" field
    
    When I change "SKU" to "LMAO"
    And I copy the "ID" field
    And I press the "Update" button
    Then I should see the message "Success"
    
    When I press the "Clear" button
    And I paste the "ID" field
    And I press the "Retrieve" button
    Then I should see "LMAO" in the "SKU" field
    
    When I press the "Clear" button
    And I press the "Search" button
    Then I should see "LMAO" in the results
    Then I should not see "ABCD" in the results

Scenario: Query an Item by SKU
    When I visit the "Home Page"
    And I set the "SKU" to "ABCD"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "ABCD" in the results
    And I should not see "EFGH" in the results
    And I should not see "IJKL" in the results
    And I should not see "MNOP" in the results
    
    When I press the "Clear" button
    And I set the "SKU" to "EFGH"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "EFGH" in the results
    And I should not see "ABCD" in the results
    And I should not see "IJKL" in the results
    And I should not see "MNOP" in the results
    
    # query a non-existent item
    When I press the "Clear" button
    And I set the "SKU" to "FAKE"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should not see "EFGH" in the results
    And I should not see "ABCD" in the results
    And I should not see "IJKL" in the results
    And I should not see "MNOP" in the results


Scenario: Query an Item by Condition
    When I visit the "Home Page"
    # Query all new items
    And I set the "Condition" to "New"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "ABCD" in the results
    And I should see "MNOP" in the results
    And I should not see "EFGH" in the results
    And I should not see "IJKL" in the results
    
    # query all used items
    When I press the "Clear" button
    And I set the "Condition" to "Used"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "EFGH" in the results
    And I should see "IJKL" in the results
    And I should not see "ABCD" in the results
    And I should not see "MNOP" in the results

    When I press the "Clear" button
    And I set the "Condition" to "OpenBox"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should not see "EFGH" in the results
    And I should not see "IJKL" in the results
    And I should not see "ABCD" in the results
    And I should not see "MNOP" in the results

Scenario: Query an Item by In-Stock
    When I visit the "Home Page"
    # Query all in-stock items
    And I select "True" in the "In_Stock" dropdown
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "ABCD" in the results
    And I should see "EFGH" in the results
    And I should see "IJKL" in the results
    And I should not see "MNOP" in the results
    
    # query all out-of-stock items
    When I press the "Clear" button
    And I select "False" in the "In_Stock" dropdown
    And I press the "Search" button
    Then I should see the message "Success"
    And I should not see "ABCD" in the results
    And I should not see "EFGH" in the results
    And I should not see "IJKL" in the results
    And I should see "MNOP" in the results