from app.models import Task

TASKS = [

    # 🔴 HARD 1
    Task(
        id="hard_subtle_bug",
        diff="""
def max_value(arr):
    max = 0
    for num in arr:
        if num > max:
            max = num
    return max
""",
        issue_type="logic",
        description_keywords=["incorrect", "initialization", "negative"],
        fix_keywords=["-inf", "float", "min value"],
        difficulty="hard"
    ),

    # 🔴 HARD 2
    Task(
        id="hard_edge_case",
        diff="""
def average(nums):
    return sum(nums) / len(nums)
""",
        issue_type="logic",
        description_keywords=["empty", "division", "zero"],
        fix_keywords=["check", "len", "zero"],
        difficulty="hard"
    ),

    # 🟡 MEDIUM
    Task(
        id="medium_variable_typo",
        diff="""
def calculate_total(price, tax):
    total = price + tax
    return tota
""",
        issue_type="logic",
        description_keywords=["undefined", "variable", "typo"],
        fix_keywords=["total"],
        difficulty="medium"
    ),

    # 🔴 HARD 3
    Task(
        id="hard_nested_loop_performance",
        diff="""
def find_duplicates(arr):
    duplicates = []
    for i in range(len(arr)):
        for j in range(len(arr)):
            if i != j and arr[i] == arr[j]:
                duplicates.append(arr[i])
    return duplicates
""",
        issue_type="performance",
        description_keywords=["nested", "loop", "inefficient"],
        fix_keywords=["set", "optimize", "hash"],
        difficulty="hard"
    ),

    # 🔴 HARD 4
    Task(
        id="hard_memory_inefficiency",
        diff="""
def get_squares(n):
    result = []
    for i in range(n):
        result.append(i*i)
    return result
""",
        issue_type="performance",
        description_keywords=["memory", "inefficient", "list"],
        fix_keywords=["yield", "generator"],
        difficulty="hard"
    ),
]