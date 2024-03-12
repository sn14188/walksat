from walksat import is_clause_satisfied

TEST_CASE_1 = {"X1": False, "X2": False, "X3": False}
TEST_CASE_2 = {"X1": True, "X2": True, "X3": True}

def test_case_1():
    clause = ["X1", "X2", "X3"]
    assert is_clause_satisfied(clause, TEST_CASE_1) == False
    clause = ["X1", "X2", "¬X3"]
    assert is_clause_satisfied(clause, TEST_CASE_1) == True

def test_case_2():
    clause = ["X1", "X2", "X3"]
    assert is_clause_satisfied(clause, TEST_CASE_2) == True
    clause = ["X1", "X2", "¬X3"]
    assert is_clause_satisfied(clause, TEST_CASE_2) == True
    clause = ["¬X1", "¬X2", "¬X3"]
    assert is_clause_satisfied(clause, TEST_CASE_2) == False
