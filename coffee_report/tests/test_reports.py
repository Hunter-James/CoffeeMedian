import pytest
from reports import MedianCoffeeReport


@pytest.fixture
def sample_data():
    return [
        {"student": "Иван Кузнецов", "coffee_spent": "600"},
        {"student": "Иван Кузнецов", "coffee_spent": "650"},
        {"student": "Иван Кузнецов", "coffee_spent": "700"},

        {"student": "Мария Соколова", "coffee_spent": "100"},
        {"student": "Мария Соколова", "coffee_spent": "120"},
        {"student": "Мария Соколова", "coffee_spent": "150"},

        # Проверка четного количества записей для медианы (среднее двух средних)
        {"student": "Петр Ильин", "coffee_spent": "200"},
        {"student": "Петр Ильин", "coffee_spent": "300"},
    ]


def test_median_coffee_report_logic(sample_data):
    report = MedianCoffeeReport()
    result = report.generate(sample_data)

    # Должно быть 3 студента
    assert len(result) == 3

    # Проверка сортировки: Иван (650) -> Петр (250) -> Мария (120)
    assert result[0]["student"] == "Иван Кузнецов"
    assert result[0]["median_coffee"] == 650

    assert result[1]["student"] == "Петр Ильин"
    assert result[1]["median_coffee"] == 250

    assert result[2]["student"] == "Мария Соколова"
    assert result[2]["median_coffee"] == 120



def test_median_coffee_report_empty_data():
    report = MedianCoffeeReport()
    result = report.generate([])
    assert result == []


def test_median_coffee_report_invalid_data():
    # Проверка устойчивости к битым данным (например, отсутствует колонка)
    bad_data = [
        {"student": "Алексей"},  # Нет coffee_spent
        {"student": "Борис", "coffee_spent": "invalid"},  # Не число
        {"student": "Виктор", "coffee_spent": "500"},
    ]
    report = MedianCoffeeReport()
    result = report.generate(bad_data)

    assert len(result) == 1
    assert result[0]["student"] == "Виктор"
    assert result[0]["median_coffee"] == 500