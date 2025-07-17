

````markdown
# 0x03 - Unittests and Integration Tests

This directory contains Python test modules to validate the correctness and robustness of application utilities using **unit tests** and **integration tests**. The focus is on using the `unittest` framework along with mocking tools such as `patch`, `Mock`, and `parameterized`.

---

## Project Structure

```bash
.
├── utils.py                 # Utility module with JSON fetching and nested map access functions
├── test_utils.py           # Unit tests for utils.py
├── client.py               # Client module (used for integration testing)
├── test_client.py          # Integration tests for client.py
├── fixtures.py             # Fixtures used in integration tests
└── README.md               # This file
````

---

## Learning Objectives

* Understand and apply **unit testing** and **integration testing**
* Use `unittest.TestCase` for structuring test cases
* Utilize `parameterized` to test multiple inputs and expected outputs
* Patch external calls and dependencies using `unittest.mock.patch`
* Mock functions, return values, properties, and more
* Write clean, maintainable test code that covers edge cases

---
## Unit Testing Concepts Covered

### 1. Parameterized Testing

* Use `@parameterized.expand()` to test the same function with different input/output combinations.
* Example: `test_access_nested_map()` checks that nested dictionary values are accessible and raise appropriate exceptions when keys are missing.

### 2. Patching Functions and Methods

* Mock external or non-deterministic behaviors (e.g., HTTP requests or caching).
* Example: `test_get_json()` patches `requests.get` to return a mock response instead of making an actual HTTP call.

### 3. Patching with Decorators and Context Managers

* Decorators: `@patch("module.path")` for clean test signatures.
* Context Managers: `with patch("module.path"):` for inline control.

### 4. Mocking HTTP Calls

* Prevents external HTTP requests during tests.
* `test_get_json()` ensures that a mocked version of `requests.get()` returns the expected JSON payload without reaching the network.
### 5. Mocking a Property

* Using `@patch.object` to mock properties such as `.json` on a response object.
* Ensures testability of class attributes and computed properties without invoking actual logic.

---

## Integration Testing Concepts

### 6. Fixtures

* Load static data for integration tests from `fixtures.py`
* Enables consistent, repeatable testing with known data states.

### 7. Integration Tests

* Test real interactions between modules such as `Client` and external APIs.
* Uses `@patch` to isolate parts of the system while still validating end-to-end behavior.
* Confirms that the flow of logic across classes and methods works as intended.

---

## How to Run Tests

```bash
# Run all unit and integration tests
$ python3 -m unittest discover

# Run specific test file
$ python3 -m unittest test_utils.py
$ python3 -m unittest test_client.py
```

---

## Dependencies

Ensure you have the following installed in your virtual environment:

```bash
pip install parameterized
```

---

## Contributing

1. Fork this repo
2. Create your feature branch (`git checkout -b test-feature`)
3. Commit your changes (`git commit -m 'Add new test case'`)
4. Push to the branch (`git push origin test-feature`)
5. Open a Pull Request

---

## License

This project is for educational purposes under the ALX Software Engineering Program.

---


