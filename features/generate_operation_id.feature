Feature: generate operation ID

  As an administrator
  I want to have operation IDs
  So that I can distinguish closely-spaced in time events related to different
  operations

  As a developer
  I want to have a control over ID formation process
  So that it can be customized without changing code

  Scenario: ID default type
    Given   default generator with default parameters
    When    I ask for a single ID
    Then    ID type must be string

  Scenario: ID default length
    Given   default generator with default parameters
    When    I ask for a single ID
    Then    ID length must be equal to 6

  Scenario: ID custom length
    Given   default generator with length 10
    When    I ask for a single ID
    Then    ID length must be equal to 10

  Scenario: ID custom length greater than max length
    Given   default generator with length 1000
    When    I ask for a single ID
    Then    ID length must be equal to 32

  Scenario: unique values
    Given   there are 100 different default generators
    When    I ask each generator for an ID for 500 times
    Then    99% of all generated IDs must be unique
