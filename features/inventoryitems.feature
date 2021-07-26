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
