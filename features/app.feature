Feature: Searching functionality in the web application

  Scenario: Searching with valid keyword and URL
    Given I am on the home page
    When I enter a valid keyword and URL and click search
    Then I should see the search results

  Scenario: Searching with missing keyword or URL
    Given I am on the home page
    When I enter a missing keyword or URL and click search
    Then I should see an error message

  Scenario: Indexing documents after crawling
    Given the web crawler has crawled the provided URL
    When I search for a keyword
    Then the documents should be indexed
