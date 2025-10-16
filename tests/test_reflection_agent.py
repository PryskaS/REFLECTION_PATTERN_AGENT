import pytest
from reflection_pattern_agent.reflection_agent import ReflectionAgent

# Create a fake response object that looks exactly like the real OpenAI response.
class MockChoice:
    def __init__(self, content):
        self.message = MockMessage(content)

class MockMessage:
    def __init__(self, content):
        self.content = content

class MockCompletion:
    def __init__(self, content):
        self.choices = [MockChoice(content)]

# Test the generate method
def test_generate_without_reflection(mocker):
    """
    Tests the generate method in its simplest form, without any reflection history.
    We will "mock" the OpenAI API call to avoid making a real, slow, and expensive call.
    """
    # Arrange: Set up the test conditions
    mock_api_response = "This is a mock response from OpenAI."
    
    # Tell pytest-mock to replace the 'create' method of the chat completions
    # with a function that returns our fake response object.
    mocker.patch(
        "openai.resources.chat.completions.Completions.create",
        return_value=MockCompletion(mock_api_response)
    )

    agent = ReflectionAgent()
    test_prompt = "Test prompt"

    # Act: Call the method we are testing
    result = agent.generate(prompt=test_prompt)

    # Assert: Check if the result is what we expected
    assert result == mock_api_response


# Test the reflect method
def test_reflect_parses_critique_correctly(mocker):
    """
    Tests if the reflect method correctly calls the API and parses
    the bulleted list response into a Python list of strings.
    """
    # Arrange: Set up the test conditions
    # This is our fake critique from the "mocked" OpenAI API.
    mock_api_critique = """
    - The tweet is a bit too long.
    - It could use a more engaging emoji.
    - The call to action is weak.
    """

    # Mock the API call to return our fake critique.
    mocker.patch(
        "openai.resources.chat.completions.Completions.create",
        return_value=MockCompletion(mock_api_critique) # The same Mock classes from before
    )

    agent = ReflectionAgent()
    test_prompt = "Original prompt"
    test_output = "Generated output to be critiqued"

    # Act: Call the method we are testing
    reflections = agent.reflect(prompt=test_prompt, generated_output=test_output)

    # Assert: Check if our parsing logic worked as expected
    expected_reflections = [
        "- The tweet is a bit too long.",
        "- It could use a more engaging emoji.",
        "- The call to action is weak."
    ]
    
    assert reflections == expected_reflections
    assert isinstance(reflections, list) # Ensure the type is correct
    assert len(reflections) == 3        # Be specific about the expected outcome