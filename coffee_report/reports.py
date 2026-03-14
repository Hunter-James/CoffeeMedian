import abc
import statistics
from typing import List, Dict, Any


class ReportStrategy(abc.ABC):
    #Абстрактный класс для всех будущих отчетов

    @property
    @abc.abstractmethod
    def headers(self) -> List[str]:
        #Возвращает заголовки для таблицы отчета
        pass

    @abc.abstractmethod
    def generate(self, data: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        #Принимает сырые данные из CSV и возвращает подготовленные для таблицы строки
        pass


class MedianCoffeeReport(ReportStrategy):
    #Отчет: медианная сумма трат на кофе по каждому студенту

    @property
    def headers(self) -> List[str]:
        return ["student", "median_coffee"]

    def generate(self, data: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        student_expenses: Dict[str, List[float]] = {}

        for row in data:
            student = row.get("student")
            if not student:
                continue

            raw_expense = row.get("coffee_spent")
            # Если ключа нет или значение пустое — пропускаем запись
            if raw_expense is None or raw_expense == "":
                continue

            try:
                expense = float(raw_expense)
            except ValueError:
                continue

            if student not in student_expenses:
                student_expenses[student] = []
            student_expenses[student].append(expense)

        results = []
        for student, expenses in student_expenses.items():
            # Считаем медиану.
            median_val = int(statistics.median(expenses)) #Приводим к int, чтобы соответствовать виду в примере (без .0)
            results.append({
                "student": student,
                "median_coffee": median_val
            })
        # Сортировка по убыванию трат
        results.sort(key=lambda x: x["median_coffee"], reverse=True)
        return results

# Реестр отчетов. При добавлении нового отчета, просто добавляем его сюда.
REPORT_REGISTRY: Dict[str, ReportStrategy] = {
    "median-coffee": MedianCoffeeReport()
}