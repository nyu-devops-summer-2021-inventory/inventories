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

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Inventory RESTful Service" in the title
    And I should not see "404 Not Found"

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
    And I press the "Clear" button
    And I paste the "ID" field
    And I press the "Retrieve" button
    Then the "SKU" field should be empty
    And the "Condition" field should be empty
    And the "Restock_Level" field should be empty
    And the "Restock_Amount" field should be empty