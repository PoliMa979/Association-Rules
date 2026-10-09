# HW4 Association Rules - памятка перед сдачей

## Готовые материалы

- `week4/` - актуальный starter и реализация семи `TODO(hw4)` в `script.js`.
- `output/pdf/polina_maltseva_a04_report.pdf` - отчёт A04 на английском языке.
- `build_report.py` - воспроизводимая сборка отчёта; в сдаваемую папку `week4/` не входит.

## Проверенные результаты

- Встроенные проверки: 11 passed, 0 failed, 0 pending.
- Дополнительная сверка: 66 itemset-count сравнений с прямым сканированием корзин.
- Порог 1% support / 30% confidence: 1 219 frequent itemsets, 950 rules.
- Порог 3% support / 60% confidence: 115 frequent itemsets, 5 rules.
- Выбранное полезное правило:
  - `22697 GREEN REGENCY TEACUP AND SAUCER -> 22699 ROSES REGENCY TEACUP AND SAUCER`;
  - `count(A U B) = 541`, `count(A) = 691`, `count(B) = 780`;
  - support `3.1674%`, confidence `78.2923%`, lift `17.1440`.
- Обратное направление: confidence `69.3590%`, lift `17.1440`.

## Что нужно сделать лично перед сдачей

1. Открыть `week4/index.html` в обычном браузере.
2. Нажать **Run tests** и убедиться, что показано `pass 11, fail 0, pending 0`.
3. Поставить support `3%`, confidence `60%`, нажать **Run rules** и проверить, что отображается 5 правил.
4. Открыть выбранное правило и сравнить числа с отчётом.
5. После личной проверки при желании убрать из раздела AI Usage Disclosure фразу о том, что browser check ещё не выполнен, и пересобрать PDF.
6. Приложить отдельно экспортированную сессию `polina_maltseva_a04_session.json`. Не публиковать её в открытом GitHub-репозитории: файл содержит полный журнал работы и локальные пути.

Не включать в сдаваемую `week4/` папку Python-файлы, временные изображения, логи или сгенерированные результаты.
