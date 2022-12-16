
def predict_rub_salary(salary_from, salary_to):
    if salary_from and salary_to:
        return (salary_to + salary_from) // 2
    elif salary_from:
        return salary_from * 1.2
    elif salary_to:
        return salary_to * 0.8
