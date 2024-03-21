from behave import given, when, then
from app import app, index_documents

@given('I am on the home page')
def visit_home_page(context):
    context.client = app.test_client()

@when('I enter a valid keyword and URL and click search')
def search_with_valid_keyword_and_url(context):
    response = context.client.get('/search?url=https://www.example.com/&keyword=test')
    context.response = response

@when('I enter a missing keyword or URL and click search')
def search_with_missing_keyword_or_url(context):
    response = context.client.get('/search')
    context.response = response

@then('I should see the search results')
def see_search_results(context):
    assert b'Results' in context.response.data

@then('I should see an error message')
def see_error_message(context):
    assert b'Both keyword and URL parameters are required.' in context.response.data

@given('the web crawler has crawled the provided URL')
def web_crawler_has_crawled_url(context):
    pass  # Implement this step to simulate crawling

@when('I search for a keyword')
def search_for_keyword(context):
    results = index_documents('test')
    context.results = results

@then('the documents should be indexed')
def documents_should_be_indexed(context):
    assert context.results != 0
