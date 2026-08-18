# D0 Bench Protocol

## Протокол сравнительного стенда версии 6.0

Дата: 2026-08-04  
Статус: проект протокола программы экспериментов до preregistration  
Язык документа: русский  
Связанная концепция: `geometric_sound_protocol_concept_v8.0_ru.md`  
SHA-256 связанной концепции: `2e027eeeb42457ec26712637015c8ae69743ffc53d77c07fb1f67baee9e5bb0d`  
Предыдущая версия: `d0_bench_protocol_v5.0.md`  
SHA-256 предыдущей версии: `a919aab880d03f871d5e2a0692d7450134d6aee0cf988517ea465083b77663d1`

Версия 6.0 закрывает дефекты двух внешних аудитов версии 5.0 (GPT, Gemini) и внутреннего повторного аудита. Полный перечень изменений и обоснование каждого решения находятся в разделе 36. Главное: единицей структурного квантиля стала заранее сбалансированная физическая stratum, а не строка сетки; правило цензурирования исправлено на интервальное; false-acceptance gate стал ролево полным, пофамильным и условным по отказам.

---

## 1. Назначение

Этот документ задает воспроизводимую программу экспериментов для выбора физической топологии неизменяемого корневого слоя D0 Геометрического звукового протокола.

Стенд сравнивает четыре обязательных кандидата:

- `D0-B1`;
- `D0-T2`;
- `D0-T3`;
- `D0-F3`.

Эксперимент должен ответить не на вопрос "какая схема выглядит красивее", а на вопрос:

> Какая топология при одинаковом энергетическом и пиковом бюджете надежнее всего сохраняет все логические формы D0, не создает ложных записей, оставляет физическое пространство для будущих suite и воспроизводимо работает в чистом цифровом канале, после локальных искажений и после реального перекодирования YouTube?

Документ является протоколом исследования, а не техническим заданием на программу. Он определяет один эксперимент и накопительную последовательность возможных экспериментов, чтобы новая preregistration не скрывала прежнюю неудачу. После внешнего аудита создается отдельное ТЗ для Claude Code или другой среды разработки. ТЗ обязано реализовать этот протокол без изменения его научных решений.

В этот документ не входят:

- GUI пользовательской Windows-программы;
- русский текстовый адаптер, кроме необходимых общих тестовых связей;
- окончательный физический suite;
- P1-P3 storyboard;
- художественный видеоряд;
- публикационная стратегия YouTube-канала;
- результаты будущего эксперимента;
- журнал red team аудитов.

---

## 2. Главный принцип

`BOOTSTRAP-1` нельзя выбирать рассуждением, удобством реализации или одним успешным роликом.

До freeze обязательны:

1. корневая preregistration всей программы экспериментов;
2. открытая development-фаза только на training corpus;
3. неизменяемая preregistration отдельного эксперимента;
4. отдельные `SELECTION_HOLDOUT` и `CONFIRMATION_HOLDOUT`;
5. одинаковые ограничения для всех кандидатов;
6. чистый математический gate до lossy-кодеков;
7. локальная полная матрица цифрового канала;
8. сравнительное испытание через реальный YouTube с контролем готовности и дрейфа платформы;
9. проверка пространства для первого и двух резервных suite-профилей;
10. scanner conformance и adversarial resource tests;
11. общая физическая шкала сравнения, не задаваемая самим кандидатом;
12. независимая реализация;
13. структурная проверка diversity до ранжирования по равномерному шуму;
14. независимый внешний challenge после фиксации предварительного победителя;
15. накопительная публикация всех успешных, неудачных и аннулированных экспериментов.
16. ровно три общие структурные координаты решения независимо от размера подробной channel grid;
17. точная целочисленная арифметика без wrap и saturation в нормативных сравнениях;
18. закрытая типизированная grammar для решающих external challenge cases;
19. заранее ограниченная и проверяемая процедура создания скрытых seeds с явными сроками и отказами.

Если ни один кандидат не проходит все бинарные условия, победителя нет. Порог нельзя ослабить после просмотра holdout.

---

## 3. Нормативные слова

Слова `ОБЯЗАН`, `ЗАПРЕЩЕНО`, `ТОЛЬКО`, `НЕ МОЖЕТ` обозначают нормативное требование.

Слова `РЕКОМЕНДУЕТСЯ`, `МОЖЕТ` обозначают ненормативный выбор, если соответствующее значение заранее зафиксировано в manifest.

Термины:

| Термин | Значение |
| --- | --- |
| training corpus | открытая часть корпуса, на которой разрешена настройка |
| selection holdout | закрытая часть корпуса для допуска и выбора предварительного победителя |
| confirmation holdout | отдельная закрытая часть корпуса только для финальной проверки уже выбранного победителя |
| external challenge | независимо составленный и заранее committed набор неожиданных воздействий, открываемый только после прохождения core confirmation |
| cumulative exposed corpus | объединение всех ранее раскрытых holdout и external challenge cases с неизменяемыми scope labels; in-scope items используются как обязательный regression gate, exploratory items остаются диагностическими |
| channel cell | одна полностью определенная комбинация преобразований и severity |
| candidate | одна физическая топология D0 со всеми таблицами и декодером |
| copy | независимо оцениваемая физическая копия одной логической формы |
| assembled form | итоговый секундный D0-токен из одной или нескольких копий |
| diagnostic subform | отдельная копия, сохраненная самостоятельным WAV для диагностики |
| hard gate | условие, при нарушении которого кандидат исключается |
| native margin | внутренняя диагностическая шкала estimator, не сравниваемая между кандидатами |
| common failure reserve | физически откалиброванный запас до отказа в общей для всех кандидатов шкале |
| structural class aggregate | одна из трех общих ранговых физических координат решения, вычисляемая по замороженной иерархии structural strata раздела 17; worst-case по классу сохраняется отдельно как hard-gate evidence и не является этой координатой |
| structural stratum | заранее определенная физическая группа ladder одного класса повреждений с одним внутристратным правилом агрегации; единица квантиля между стратами |
| structural diagnostic | подробный результат отдельной ladder, placement, width, codec cell или impairment family; является hard-gate evidence, но не новой координатой Pareto-решения |
| epsilon-dominance | отношение, при котором кандидат не хуже другого по всем структурным координатам с учетом equivalence band и лучше хотя бы по одной |
| equivalence band | заранее заданный порог практической неразличимости двух результатов, а не точность печати |
| right censoring | наблюдение, для которого первый отказ лежит выше достигнутой границы измерительной сетки |
| failure-support overlap | доля общих отказов двух копий среди channel observations, где отказала хотя бы одна из них |
| structural-first policy | заранее объявленная исследовательская политика, по которой устойчивость к notch, burst и combined damage проверяется до равномерного AWGN reserve; она не является утверждением универсального превосходства |
| block | группа YouTube-испытаний, проведенная в одном ограниченном временном окне |
| development attempt | открытый запуск до design commitment; не является новым experiment index, но полностью записывается в development log |
| experiment | одна попытка, начинающаяся с timestamped design commitment и использующая два одноразовых holdout |
| program | заранее ограниченная последовательность экспериментов с общей lineage |
| freeze | необратимая публикация корневого D0-профиля данного protocol family |

### 3.1. Источники нормативной истины

Логические инварианты берет на себя концепция GSP v8.0. Этот документ специализирует только методику D0-эксперимента. Experiment manifests заполняют численные поля, которые этот protocol намеренно оставляет параметрами preregistration. Fixed-point tables и golden vectors фиксируют байтовое представление.

Если концепция, этот protocol, manifest и test vector противоречат друг другу, реализация не выбирает удобный источник молча. Эксперимент получает `PROTOCOL_CONFLICT` и останавливается до выпуска согласованных новых версий.

---

## 4. Неизменяемые логические инварианты

Стенд не оптимизирует следующие значения:

```text
sample_rate_hz        = 48000
channel_count         = 1
sample_format_source  = signed PCM 24-bit
token_samples         = 48000
token_duration        = 1 second
logical_form_count    = 72
object6_count         = 64
marker_count          = 7
boot_sync_count       = 1
```

Каждый кандидат использует одинаковые:

- 64 значения `D0_OBJECT6(v)`, где `v = 0..63`;
- семь D0-маркеров: `D0_NO_CALL`, `D0_CALL_START`, `D0_CALL_END`, `D0_ANSWER_START`, `D0_ANSWER_END`, `D0_SUITE_ANSWER_START`, `D0_SUITE_ANSWER_END`;
- `BOOT_SYNC`;
- `D0_BCH(15,7,5)` с generator `0x1D1`;
- аффинную маску `0x000B`;
- логический порядок codeword `bit 14, bit 13, ..., bit 0`, где `bit 14` является старшим битом 15-битного слова. Физическое расположение этих позиций определяется только candidate carrier map и не выводится из слов `первый` или `последний`;
- dual-rail подпись `value6`;
- `D0_GF(64)` с polynomial `0x43`, `alpha = 0x02` и битовым отображением GSP v8.0;
- `D0_RS(16,8)` с коэффициентами generator `[1,55,61,37,48,47,20,6,22]` от старшей степени к свободному члену, DATA перед PARITY и сокращением на 47 ведущих нулей;
- секундную внешнюю сетку;
- логическую grammar записей и beacon;
- классы правильного решения, конфликта и стирания.

Изменение любого пункта этого раздела означает новый bench protocol major, а после freeze D0 означает новый protocol family.

---

## 5. Обязательные кандидаты

| ID | Физическое размещение в 1 секунде | Число копий | Агрегация |
| --- | --- | ---: | --- |
| `D0-B1` | одна форма длиной 48 000 отсчетов | 1 | одна валидная форма |
| `D0-T2` | две последовательные области по 24 000 отсчетов | 2 | обе копии валидны и совпадают |
| `D0-T3` | три последовательные области по 16 000 отсчетов | 3 | уникальное большинство 2 из 3 |
| `D0-F3` | три одновременные полносекундные копии на разных физических поддержках | 3 | уникальное большинство 2 из 3 |

### 5.1. Решения копии

Каждая копия возвращает ровно одно состояние:

```text
COPY_VALID(value_or_role, soft_metrics)
COPY_CONFLICT(soft_metrics)
COPY_ERASURE(soft_metrics)
```

Soft metric не является дополнительным голосом.

### 5.2. Решения собранной формы

| Кандидат | `ALL_COPIES_VALID` | `RECOVERED` | `CONFLICT` | `ERASURE` |
| --- | --- | --- | --- | --- |
| `D0-B1` | одна валидная копия | не применяется | несколько несовместимых решений одного уровня | нет валидного решения |
| `D0-T2` | две одинаковые валидные копии | не применяется | две разные валидные копии | валидна только одна либо ни одной |
| `D0-T3` | три одинаковые валидные копии | ровно две копии дают одно значение, а третья стерта, конфликтна либо дает другое значение | валидны не менее двух копий, но уникального большинства нет | меньше двух валидных копий |
| `D0-F3` | три одинаковые валидные копии | ровно две копии дают одно значение, а третья стерта, конфликтна либо дает другое значение | валидны не менее двух копий, но уникального большинства нет | меньше двух валидных копий |

Для marker форм вместо значения сравнивается marker role.

`D0-T2` сохраняется как обязательный detection-redundancy control. Его правило "обе копии обязаны совпасть" не исправляет стирание и ожидаемо платит большую AWGN-цену при делении энергии. Его научная роль состоит в проверке того, снижает ли двойное согласование ложное принятие и дает ли temporal separation структурную пользу, достаточную для компенсации этой цены. Эта роль не дает ему льготы в ranking.

### 5.3. Дополнительные кандидаты

Дополнительный кандидат разрешен только до preregistration. Для него до открытия holdout должны существовать:

- точное описание размещения;
- fixed-point synthesis tables;
- estimator;
- правило принятия;
- энергетический расчет;
- ресурсный бюджет;
- полный training corpus;
- место в заранее объявленном ranking.

После preregistration добавлять кандидатов запрещено. Дополнительный кандидат не участвует в выводе общего `E_target`: он проверяется на feasibility при уже замороженном target и проходит те же G2-G8, hard gates, structural aggregates и sequential metrics, что и обязательные кандидаты. В manifests он всегда имеет `candidate_origin = ADDITIONAL_PREREGISTERED`; обязательный кандидат имеет `candidate_origin = MANDATORY`.

До design commitment разрешен только один явно обозначенный шаг добавления кандидатов. Он выполняется после полного development pass четырех обязательных кандидатов, но до финального пересчета всех кандидатов. После этого candidate set закрывается, все результаты development пересчитываются симметрично, а прежние результаты не переносятся выборочно.

### 5.4. Полнота физического описания

Каждый `candidate_manifest.json` обязан иметь отдельные записи для:

- `D0_OBJECT6(v)`;
- каждого из семи D0-маркеров;
- `BOOT_SYNC`;
- каждой independently decoded copy;
- assembled form;
- estimator и copy aggregator.

Для каждой формы перечисляются:

```text
logical_role
copy_role
sample_count
q_format
physical_support
carrier_or_basis_map
window_table_hash256
amplitude_table_hash256
phase_table_hash256
pilot_presence_and_definition
bch_layer_presence_and_mapping
dual_rail_presence_and_mapping
special_marker_layer
normalization_rule
estimator_table_hash256
decision_thresholds
timing_tolerance_samples
```

Поле может иметь значение `ABSENT`, но не может отсутствовать. D0 не наследует неуказанный `PILOT`, `SEMANTIC_LAYER` или иной слой обычного suite-токена. Для `D0_OBJECT6(v)` BCH и dual-rail обязательны. Для marker и `BOOT_SYNC` manifest явно задает special matched form и доказывает, что она не принимается как `D0_OBJECT6`.

Candidate manifest также содержит canonical sample hashes всех 72 assembled forms и всех diagnostic subforms. Формы, которые нельзя однозначно синтезировать только из manifest и опубликованных таблиц, получают `CANDIDATE_SCHEMA_INCOMPLETE`.

---

## 6. Равные энергетические и пиковые условия

### 6.1. Общий бюджет

Сначала, независимо от кандидатов, фиксируются ограничения реального тракта:

```text
sample_peak_limit_q
true_peak_limit_q
integrated_loudness_reporting_method
true_peak_reference_algorithm_id
true_peak_reference_table_hash256
energy_headroom_numerator
energy_headroom_denominator
minimum_operational_energy_integer
reference_noise_energy_integer
minimum_transport_snr_numerator
minimum_transport_snr_denominator
energy_quantization_floor_integer
copy_energy_balance_tolerance
copy_energy_remainder_rule_id
E_tolerance
```

Peak limits не подбираются по результатам кандидатов. Они выводятся из master format, звуковой безопасности и transport contract. Headroom является рациональным числом в интервале `(0,1]` и фиксируется до запуска phase optimization.

Энергия вычисляется на каноническом integer PCM до контейнерного кодирования:

```text
E_total = sum(s[n]^2), n = 0..47999
```

Сумма вычисляется целочисленно без переполнения и сериализуется десятичной строкой. Floating-point результат не является нормативным.

Для каждой assembled form сначала синтезируется ненулевая каноническая prototype form. `Structurally valid finite waveform` означает конечную целочисленную PCM-последовательность точной нормативной длины, которая не равна нулю целиком, соответствует замороженным basis, support, role, Q-format и layer schema, не содержит переполнения и имеет конечные sample peak, true peak и положительную энергию. All-zero waveform, неопределенная форма либо форма, для которой optimizer не создал ни одного такого результата, получает `FORM_SYNTHESIS_INFEASIBLE` до вычисления общего энергетического target.

После preregistered phase optimization вычисляется максимальная масштабируемая целочисленная энергия, при которой одновременно выполняются оба peak limit:

```text
E_cap(candidate, logical_form) =
    max E_total под ограничениями sample peak и true peak
```

`E_cap` является конечным неотрицательным целым числом. `null`, `NaN`, `Infinity`, отрицательное значение, пустая строка и незаполненный placeholder запрещены. Значение ноль означает infeasible form и не участвует в общем минимуме.

До сравнения кандидатов выполняется `FEASIBILITY_PREPASS`. Сначала определяется минимальный cap, который после применения headroom и нормативного округления еще дает рабочую энергию:

```text
E_cap_min_required = минимальное e на нормативной energy grid,
                     для которого

floor_q(
    e *
    energy_headroom_numerator /
    energy_headroom_denominator
) >= minimum_operational_energy_integer
```

Эта формула, energy grid, peak limits, headroom, optimizer budget и `minimum_operational_energy_integer` фиксируются до optimization run любого обязательного кандидата.

Energy grid обязана быть конечной, монотонной и иметь preregistered верхнюю границу поиска. Если на ней не существует ни одного `e`, удовлетворяющего формуле, весь experiment получает `COMMON_ENERGY_INFEASIBLE`. Уменьшать `minimum_operational_energy_integer`, расширять grid или менять headroom после первого mandatory optimization run запрещено.

Обязательный кандидат получает `SYNTHESIS_INFEASIBLE`, если хотя бы одна из его 72 форм:

- не имеет конечного положительного `E_cap`;
- не получила ни одного structurally valid finite optimizer output;
- имеет `E_cap < E_cap_min_required`;
- нарушает fixed-point, basis, support или schema gate G1.

Все измеренные caps, prototype hashes, optimizer evidence и точная причина исключения публикуются. Исключение по этому правилу является результатом feasibility, а не свободным решением экспериментатора. Исключенный кандидат получает `EXCLUDED_BY_FEASIBILITY_PREPASS`, не выполняет G2-G6 и не входит в ranking, но его полный G0-G1 пакет остается частью final publication.

Пусть `F_mandatory` является множеством обязательных кандидатов, прошедших prepass. Если оно пусто, experiment получает `COMMON_ENERGY_INFEASIBLE`, а `E_target` не выводится.

Для непустого `F_mandatory` общая энергия не назначается свободным числом. Она выводится только по формуле:

```text
E_common_cap = min E_cap(candidate, logical_form)
               по всем candidate из F_mandatory
               и всем 72 формам

E_target = floor_q(
    E_common_cap *
    energy_headroom_numerator /
    energy_headroom_denominator
)
```

`floor_q` округляет вниз к заранее заданной целочисленной квантовой сетке энергии. Полученное `E_target` публикуется как производный результат, а не как решение экспериментатора. По построению `E_target >= minimum_operational_energy_integer`. Нарушение этого неравенства означает `ENERGY_DERIVATION_CONFLICT`, а не право изменить rounding или удалить кандидата.

Обязательный кандидат, прошедший `FEASIBILITY_PREPASS`, не может быть удален для повышения `E_target`. Дополнительный кандидат из раздела 5.3 не понижает общий target. Он обязан синтезироваться при уже выведенном `E_target` либо получает `SYNTHESIS_INFEASIBLE`.

После G1 `survivor_set_manifest.json` фиксирует immutable `energy_eligible_set`. Более позднее development-исключение по G2-G6 не разрешает пересчитать `E_target`. Непосредственно перед preregistration тот же manifest фиксирует final survivor set и:

```text
comparison_mode = COMPARATIVE, если допустимы два и более кандидата
comparison_mode = SOLE_FEASIBLE, если уже energy_eligible_set содержал ровно одного кандидата
comparison_mode = SOLE_SURVIVOR, если energy_eligible_set содержал не менее двух,
                  но после G2-G6 остался ровно один
```

При `SOLE_FEASIBLE` или `SOLE_SURVIVOR` кандидат все равно обязан пройти все hard gates, confirmation, external challenge и независимое воспроизведение. Последовательное ranking не выполняется, а итоговый отчет не может утверждать сравнительное физическое превосходство.

После вывода `E_target` каждая assembled form обязана удовлетворять:

```text
abs(E_total - E_target) <= E_tolerance
sample_peak <= sample_peak_limit_q
true_peak <= true_peak_limit_q
```

Для кандидата с `m > 1` независимо декодируемыми копиями энергия распределяется поровну в пределах `copy_energy_balance_tolerance`. Остаток fixed-point scale распределяется по замороженному порядку `copy_role`, заданному `copy_energy_remainder_rule_id`. Кандидат не может повысить надежность кворума, скрыто усилив две копии и обесточив третью.

`minimum_operational_energy_integer` не является свободным числом и не выводится из candidate waveform. До candidate synthesis открытый candidate-neutral calibration corpus определяет `reference_noise_energy_integer`, а channel contract задает рациональный minimum transport SNR. Нормативный вывод равен:

```text
minimum_operational_energy_integer = ceil_q(
    max(
        energy_quantization_floor_integer,
        reference_noise_energy_integer *
        minimum_transport_snr_numerator /
        minimum_transport_snr_denominator
    )
)
```

`ceil_q` округляет вверх к той же заранее заданной energy grid, которую использует `E_cap_min_required`. Calibration source, scored interval, DC rule, noise estimator, SNR ratio, accumulator width, rounding и golden vector фиксируются до первого mandatory synthesis run. Звуковой safety limit задает верхний peak/energy envelope и не используется как скрытая степень свободы нижнего порога. Кандидат с положительным, но недостаточным cap исключается тем же заранее выведенным порогом, что и любой другой кандидат. Специальное исключение или дополнительная энергия для `D0-F3`, `D0-B1` либо иной топологии запрещены.

Алгоритм true peak, коэффициент oversampling, коэффициенты фильтра, округление и граничное дополнение фиксируются в manifest и контрольных векторах. Ссылка только на название стандарта без таблиц и test vectors недостаточна для нормативного совпадения.

### 6.2. Учет `D0-F3`

Для трех ортогональных копий при равном распределении энергии исходная цель равна:

```text
E_copy = E_target / 3
RMS_scale_relative_to_B1 = 1 / sqrt(3)
```

Это отношение не является разрешением использовать floating-point в нормативном синтезе. Реальный fixed-point scale и остаток энергии задаются целыми числами в candidate manifest.

Амплитуда каждой копии не назначается автоматически равной 1/3. Дополнительное уменьшение может потребоваться только из-за измеренного составного crest factor или true peak.

Повышенный crest factor одновременной суммы является реальной физической ценой `D0-F3`, а не основанием дать ему дополнительную энергию. Одновременно он не может быть наказан произвольно выбранным `E_target`, потому что target выводится из общего feasible envelope раздела 6.1.

Для `D0-F3` применяется та же preregistered функция бюджета phase optimization, что и для других кандидатов. Оптимизатор может уменьшать peak factor, но не может менять логические признаки, физические поддержки или правила решения после фиксации candidate manifest.

### 6.3. Учет временных кандидатов

`D0-T2` и `D0-T3` не получают повышенную полную энергию для компенсации более короткой экспозиции копии. Сумма энергий всех временных копий должна уложиться в общий `E_target`.

Для каждой копии отдельно публикуются:

- энергия;
- RMS;
- sample peak;
- true peak;
- crest factor;
- effective analysis duration;
- окно и его hash.

Те же `copy_energy_balance_tolerance` и residual rule, что у `D0-F3`, применяются к `D0-T2` и `D0-T3`.

### 6.4. Оптимизация фаз

Если используется minimax phase optimization, preregistration фиксирует:

- целевую функцию;
- ограничения;
- Q-format;
- порядок обхода переменных;
- seed;
- число phase variables `P`;
- число ограничений `C`;
- формулу максимального числа objective evaluations `B(P,C)`;
- число deterministic multistarts;
- правило остановки;
- критерий сходимости;
- tie-break;
- hardware-independent контрольные векторы.

До первого optimization run любого обязательного кандидата `optimizer_method_manifest.json` получает independent timestamp attestation. Если optimizer method меняется в development, все прежние optimization outputs аннулируются, все четыре обязательных кандидата пересчитываются с нуля, а изменение записывается в development log. Нельзя сохранить удачные outputs старого метода только для части кандидатов.

Простое умножение числа итераций на число переменных не считается доказанной нормировкой, поскольку сложность optimizer может быть нелинейной. Всем кандидатам предоставляются один optimizer family, одна формула `B(P,C)`, одинаковое число multistarts на одну размерность и одинаковый критерий сходимости. Коэффициенты формулы являются целыми числами и фиксируются до запуска любого обязательного кандидата.

Bench protocol не назначает коэффициенты `B(P,C)` задним числом. До первого mandatory run manifest обязан содержать полную вычислимую формулу, все коэффициенты, integer semantics, upper bound, test vectors как минимум для фактических пар `(P,C)` каждого обязательного кандидата и независимую timestamp attestation. Ссылка на название optimizer без численной budget function дает `OPTIMIZER_BUDGET_UNSPECIFIED`.

Для каждого результата публикуются число evaluations, причина остановки, достигнутый objective, convergence residual и лучший результат каждого multistart. Исчерпание budget при наличии хотя бы одного structurally valid finite waveform не делает форму infeasible: используется лучший результат в замороженном порядке, а низкий crest performance проявляется через `E_cap`. Если ни одного valid waveform нет, форма получает `FORM_SYNTHESIS_INFEASIBLE`. Увеличивать budget только одному кандидату запрещено.

`FORM_SYNTHESIS_INFEASIBLE` назначается до вычисления `E_common_cap`. Нельзя одновременно оставить такую форму в минимуме и считать ее кандидата исключенным.

### 6.5. Secondary sensitivity arm

В дополнение к основному equal-energy плюс equal-peak сравнению разрешен диагностический `EQUAL_PEAK_ONLY_ARM`. В нем каждый кандидат использует собственную максимальную энергию под общими peak limits.

Этот arm показывает цену общего `E_target`, но не участвует в hard gates, ranking или выборе победителя. Его параметры и решение не использовать его для выбора фиксируются до holdout.

Результаты arm публикуются как симметричная sensitivity analysis для всех допустимых кандидатов. В текущем experiment index они не могут использоваться для изменения кандидатов, optimizer budget, `E_target`, thresholds, equivalence bands, survivor set, channel support claim, ranking, causal interpretation или формулировки победителя. Допустимы только заранее зарегистрированные фактические таблицы per-candidate energy и metric delta без вывода, что arm подтверждает либо опровергает выбор основного эксперимента. После окончательной публикации arm может мотивировать только новую публично отличимую программу или protocol major с явной ссылкой на прежний результат.

Если arm waveform не удовлетворяет собственным общим peak limits, это означает `ARM_SYNTHESIS_CONFLICT` и блокирует только arm для этого кандидата. Такое наблюдение не переопределяет feasibility основного equal-energy эксперимента и не доказывает, что `E_target` был выбран неверно. Если же arm обнаруживает расхождение с уже опубликованным G1 peak calculation той же самой waveform, статус равен `PROTOCOL_CONFLICT`.

---

## 7. Физическое разнообразие

Перестановка BCH-позиций по одному набору частот не считается разнообразием.

Для каждой пары копий публикуются физические поддержки `S_i` и `S_j`. Поддержки считаются различными только при одновременном выполнении условий:

1. наборы физических несущих или базисных функций реально различны;
2. нормированная межкопийная корреляция ниже preregistered threshold;
3. static notch не создает тождественно одинаковый набор повреждений;
4. conditional failure matrix показывает неидеальную корреляцию отказов в обязательной сетке;
5. различимость ролей копий сохраняется при timing tolerance.

Наличие разных supports само по себе не дает права заявить diversity. `structural_metric_manifest.json` до holdout фиксирует единые для всех многокопийных кандидатов:

```text
diversity_overlap_limit_num
diversity_overlap_limit_den
diversity_min_informative_failures
diversity_required_impairment_families[]
diversity_claim_type = DETECTION_DIVERSITY или RECOVERY_DIVERSITY
```

Порог является одним рациональным числом для всех кандидатов и всех пар копий и обязан удовлетворять `0 <= numerator < denominator`. Значение 1 запрещено, потому что оно пропускает идеально совпадающие failure supports. Candidate-specific пороги запрещены. Его численное значение и физическое обоснование выводятся только на открытом candidate-neutral calibration corpus до первого mandatory candidate diversity run и затем не меняются. Calibration corpus содержит как минимум duplicate-support negative control, который обязан провалить gate, и preregistered decorrelated positive control, который обязан его пройти; иначе `DIVERSITY_THRESHOLD_UNCALIBRATED`, блокирующий design commitment как protocol error, а не исключающий удобного кандидата.

Для каждой пары копий `(i,j)` и каждой заявленной impairment family на общей конечной сетке вычисляются:

```text
U_ij = count(copy_i_failed OR copy_j_failed)
I_ij = count(copy_i_failed AND copy_j_failed)
failure_support_overlap_ij = I_ij / U_ij
```

Состояния `COPY_CONFLICT` и `COPY_ERASURE` считаются failure. Если `U_ij < diversity_min_informative_failures`, результат равен `DIVERSITY_UNRESOLVED`; нулевая доля из недостаточного числа отказов не считается доказательством независимости. Иначе gate пройден только при точном условии:

```text
I_ij * diversity_overlap_limit_den
    <= U_ij * diversity_overlap_limit_num
```

Сравнение выполняется без floating-point и без переполнения. Для `RECOVERY_DIVERSITY` gate должен быть пройден всеми парами и всеми заявленными семьями. Для `DETECTION_DIVERSITY` дополнительно доказывается снижение числа ложных принятых значений относительно каждой одиночной копии, но такое доказательство не переименовывается в recovery. `D0-T2` может заявлять только `DETECTION_DIVERSITY`; `D0-T3` и `D0-F3` могут заявлять recovery только после прохождения соответствующего gate.

Overlap не объединяется в один pooled count по разным impairment families. Gate применяется отдельно к каждой preregistered family и каждой паре. Observation ID равен hash canonical transform graph, source form, placement и seed; дубликаты одного ID считаются один раз. Число и состав observations каждого family фиксируются до selection, одинаковы для всех кандидатов и не могут расширяться после candidate result для разбавления неудобных отказов. Метрика описывает только эту конечную сетку и не объявляется вероятностью отказа на неизвестном распределении.

Для `D0-F3` отдельно проверяются:

- объединенная полоса;
- crest factor суммы;
- inter-copy leakage;
- joint estimator conditioning;
- static notch;
- low-pass;
- spectral tilt;
- одновременный burst плюс notch.

Для `D0-T2` и `D0-T3` отдельно проверяются:

- каждая внутренняя граница;
- все codec-frame offsets относительно границы;
- pre-echo;
- temporal smear;
- insertion и deletion;
- burst, пересекающий две соседние копии;
- role permutation.

Полная conditional failure matrix, значения `U_ij`, `I_ij`, точные дроби overlap и hard-gate outcome публикуются для каждой пары. Если многокопийный кандидат получает `DIVERSITY_UNRESOLVED` либо превышает общий overlap limit в заявленной семье, он не может участвовать в ranking под заявленной топологией и получает `HARD_DIVERSITY_FAILED`. Порог нельзя ослабить после результата.

---

## 8. Sanity calculations до звукового стенда

Для окна `w[n]` длиной `N` вычисляются:

```text
W1_N(delta) = abs(sum(w[n] * exp(i*2*pi*delta*n/fs))) / sum(w[n])
W2_N(delta) = abs(sum(w[n]^2 * exp(i*2*pi*delta*n/fs))) / sum(w[n]^2)
E_N         = sum(w[n]^2)
```

Контрольный half-cosine baseline определяется самодостаточно:

```text
d_N(n) = min(n, N - 1 - n)

w_N[n] = 0.5 * (1 - cos(pi * d_N(n) / 240)), если d_N(n) < 240
w_N[n] = 1,                                      иначе
```

Формула в этом разделе служит только для вычисления sanity table в вещественной математике. Нормативный synthesis использует опубликованную fixed-point window table, ее Q-format, rounding rule и hash.

Контрольные значения для half-cosine baseline с fade 240 отсчетов и `delta = 1 Hz`:

| N | Длительность | `W1_N`, dB | `W2_N`, dB | `10 log10(N/48000)`, dB | `10 log10(E_N/E_48000)`, dB |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 48 000 | 1,000 s | -45,94 | -44,00 | 0,00 | 0,00 |
| 24 000 | 0,500 s | -3,84 | -3,81 | -3,01 | -3,04 |
| 16 000 | 0,333 s | -1,60 | -1,59 | -4,77 | -4,83 |

Независимая реализация обязана воспроизвести таблицу до 0,01 dB.

Эта таблица не выбирает победителя. Она показывает, что укороченные временные области имеют другую частотную характеристику. Она также не разрешает исключить `D0-T3`, потому что временная топология может иметь отдельное преимущество при burst, которого таблица не измеряет.

Для каждого кандидата до канальных тестов дополнительно вычисляются:

- main-lobe width;
- first-null spacing;
- equivalent noise bandwidth;
- side-lobe envelope;
- Gram matrix;
- condition number;
- basis rank;
- максимальная нормированная взаимная корреляция;
- энергия и peak каждой копии;
- aggregate energy и peak;
- sample hashes всех fixed-point таблиц.

`W1_N` и `W2_N` являются per-copy sanity metrics. Они не заменяют анализ assembled form. Для `D0-T2` и `D0-T3` дополнительно публикуется спектр всей последовательности с ее внутренними переходами. Для `D0-F3` публикуются spectrum и Gram matrix одновременной суммы. Если используется joint estimator, manifest обязан показать, как assembled observation преобразуется в независимые copy decisions до кворума.

Half-cosine является только контрольным baseline. Кандидат может использовать другое окно, если его fixed-point таблица, hash, энергия, границы и estimator зафиксированы до holdout. Нельзя считать, что все временные кандидаты автоматически имеют fade 240 отсчетов.

---

## 9. Два независимых доказательства пригодности

Оптимизация под YouTube не может заменить математическую различимость в чистом сигнале.

Каждый кандидат проходит два отдельных gate:

### 9.1. `CLEAN_MATH_GATE`

Проверяет, что кандидат самодостаточно различим в каноническом PCM и не зависит от артефактов AAC, Opus или конкретной платформы.

### 9.2. `YOUTUBE_TRANSPORT_GATE`

Проверяет, что уже математически пригодный кандидат переживает конкретный земной транспорт YouTube в заявленных границах.

Кандидат, не прошедший `CLEAN_MATH_GATE`, не может быть спасен хорошим результатом YouTube.

Победа на YouTube не означает универсальности сигнала. Она означает только совместимость с опубликованным `D0_CHANNEL_SUPPORT_ENVELOPE`.

### 9.3. Общая калибровочная шкала

Candidate-native score используется для принятия решения внутри замороженного estimator, но не сравнивается между топологиями.

Для межкандидатного сравнения применяется `COMMON_AWGN_RESERVE-1`. Пакет содержит несколько fixed-point noise vectors `z_j[n]` с нулевым средним, unit-energy normalization, разными preregistered seeds и SHA-256. Для уже полученного observation `x[n]` шум добавляется в целочисленной шкале:

```text
x_a,j[n] = saturate(x[n] + scale_q(a) * z_j[n])
```

AWGN reserve не смешивается с clipping reserve. Для каждого scored observation учитывается только общий prefix grid points, на котором `saturation_count = 0` у всех сравниваемых candidates. Фактическая добавленная энергия вычисляется как `sum((x_a,j[n] - x[n])^2)`. Первый point с saturation завершает калибровочную сетку, но не считается акустическим отказом. Clipping проверяется отдельными channel cells G3.

По возрастающей дискретной сетке `a` определяется максимальный safe prefix: решение обязано быть правильным для каждого меньшего или равного grid point и каждого обязательного noise vector. Случайное повторное правильное решение после первого отказа не восстанавливает safe prefix.

Нормативной общей величиной является точное отношение целых энергий на первом отказе:

```text
common_failure_reserve_ratio =
    E_added_noise_at_first_failure / E_observed_signal

common_failure_reserve_db_q =
    ten_log10_fixed_q(common_failure_reserve_ratio)
```

`E_observed_signal` является целочисленной энергией выровненного scored interval после проверяемого channel, до добавления calibration noise и после удаления только preregistered DC component. В обычном случае числитель является неотрицательным, а знаменатель положительным целым числом. Отношения сравниваются точным cross multiplication. Нормативная реализация использует unsigned accumulator шириной не менее 128 бит либо целые произвольной точности. Wrap, saturation, signed overflow и предварительное деление запрещены. `ten_log10_fixed_q(r)` вычисляет нормативное fixed-point представление `10 * log10(r)` только для equivalence band и отчета. Его алгоритм, scale, rounding и golden vectors входят в `integer_semantics.json`. Системный floating-point `log10` не является нормативным.

Baseline edge cases обрабатываются до sweep:

```text
если decoder ошибся при a = 0 и E_observed_signal > 0:
    common_reserve_status = BASELINE_FAILURE
    ratio = 0 / E_observed_signal
    dB_q = DB_NEGATIVE_INFINITY

если E_observed_signal = 0:
    common_reserve_status = ZERO_SIGNAL_BASELINE_FAILURE
    canonical ratio = 0 / 1
    observed_signal_energy_integer = 0
    dB_q = DB_NEGATIVE_INFINITY
```

`DB_NEGATIVE_INFINITY` является строковым enum, а не IEEE floating-point value и не минимальным конечным dB. В `REQUIRED_GRID` оба статуса нарушают hard gate. В `BOUNDARY_GRID` и `STRESS_GRID` они остаются измеренными границами отказа. Это правило предотвращает деление на ноль и не позволяет baseline failure выглядеть как right-censored success.

JSON Schema задает `common_failure_reserve_db_q` как `oneOf(integer, "DB_NEGATIVE_INFINITY")` и требует согласованную пару с `common_reserve_status`. Любая другая строка либо сочетание `DB_NEGATIVE_INFINITY` с положительным reserve numerator дает `PROTOCOL_CONFLICT`.

Для секундного signed PCM 24-bit G0 фиксирует следующие граничные значения:

```text
max_signal_energy_48k = 3377699720527872000          # 62 bits
max_difference_energy_48k = 13510797271498800000     # 64 bits
signal_x_difference = 45635416168050232317636614553600000000
difference_x_difference = 182541642911539418798798401440000000000
```

Последнее значение требует 128 значащих бит. Обязательный negative vector выполняет то же сравнение в 64-bit arithmetic и должен быть отвергнут как `INTEGER_WIDTH_INSUFFICIENT`, а не дать ranking result.

Чем больше отношение, тем больше добавленной физической энергии помехи выдержал кандидат относительно фактически полученного сигнала.

Если отказ не достигнут до верхней границы сетки, результат помечается `RIGHT_CENSORED`. Он означает нижнюю границу запаса, а не точное значение и не бесконечность. В development сетка обязана расширяться до первого отказа либо до заранее зафиксированного общего `maximum_safe_calibration_noise_energy`, выведенного из первого возможного saturation, hearing-safety и integer-range limits. Доля right-censored observations публикуется по candidate, channel cell и noise vector.

Если на конкретном ranking step все оставшиеся кандидаты right-censored на одной общей верхней границе, метрика получает `NON_DISCRIMINATING_CENSORED` и никого не исключает. Если часть кандидатов censored, а часть имеет измеренный отказ ниже границы, censored lower bound может считаться лучше только когда разница с измеренным значением превышает equivalence band. Иначе кандидаты остаются эквивалентными на этом шаге.

Перед holdout все реализации проходят аналитическую calibration cell с заранее известными `E_signal`, `E_noise` и ожидаемым dB после quantization. Разница native score не влияет на общий результат.

Для каждого channel cell итоговым показателем является минимум `common_failure_reserve_ratio` по обязательным noise vectors и логическим формам. Соответствующий `common_failure_reserve_db_q` хранится для отчета. Дополнительные физические оси, включая notch depth, burst duration и gain reserve, сохраняются отдельно и не пересчитываются произвольной candidate-specific формулой.

---

## 10. Программа экспериментов, preregistration и holdout

### 10.1. Корневая регистрация программы

До первой попытки публикуется `bench_program_manifest.json`. Он фиксирует:

- protocol и concept hashes;
- `program_id`;
- `program_max_experiments`;
- `max_candidate_count` и `max_youtube_block_dates`;
- допустимые классы изменений между экспериментами;
- терминальные stop rules;
- правило накопления раскрытых holdout;
- schema `experiment_lineage.json`;
- ответственного хранителя sealed holdout;
- независимого составителя и хранителя external challenge;
- допустимые public randomness beacon providers и правила их проверки;
- maximum independent pre-reference corrections;
- правило независимой временной фиксации;
- обязательство публиковать каждую попытку, включая abandoned и invalidated.

Идентичность программы:

```text
program_hash256 = SHA256(
    LP("GSP-D0-BENCH-PROGRAM-6") ||
    LP(JCS(bench_program_manifest))
)
```

В проекте существуют два независимых major-номера, и их нельзя смешивать. `bench_protocol_major = 6` нумерует методику этого стенда; все bench-теги вида `GSP-D0-*-6` следуют только ему и меняются с каждой major-версией стенда. `wire_protocol_major = 4` нумерует физическое семейство концепции GSP; теги `GSP4-D0-CANDIDATE`, `GSP4-D0-PHYSICAL-PROFILE` и `GSP4-PHYSICAL-PROFILE` следуют только ему и НЕ меняются при смене версии стенда, потому что идентифицируют объекты wire family, а не эксперимента. Оба числа записываются в `bench_program_manifest.json` отдельными полями.

`experiment_lineage.json` является append-only hash chain. Для записи `i`:

```text
lineage_entry_hash_i = SHA256(
    LP("GSP-D0-LINEAGE-6") ||
    LP(program_hash256) ||
    LP(previous_lineage_entry_hash) ||
    LP(JCS(lineage_entry_i))
)
```

Для первой записи `previous_lineage_entry_hash` равен 32 нулевым байтам. Запись содержит experiment index, manifests, UTC-даты, исход, причину остановки, hashes раскрытых данных и budget consumption. Удаление, перенумерация или скрытие попытки дает `LINEAGE_BROKEN` и запрещает freeze.

Каждый раскрытый selection или confirmation holdout навсегда добавляется в `cumulative_exposed_corpus_manifest.json` как in-scope regression data. Раскрытые external cases добавляются с исходными scope labels. Следующий эксперимент обязан пройти все прежние in-scope items как regression gate. Прежние exploratory items остаются диагностическими, если новая preregistration до development явно не переводит соответствующий класс в собственный support claim. Выбор нового победителя производится только на новом sealed holdout.

### 10.2. Development до preregistration эксперимента

До финальной preregistration разрешена только работа с открытыми данными:

- training corpus;
- cumulative exposed corpus;
- pilot codec runs;
- pilot YouTube blocks;
- carryover и platform-control development;
- построение всех candidate manifests;
- построение первого и двух резервных suite-профилей каждого кандидата;
- выбор hard gates, common calibration, equivalence bands и budgets.
- определение schema и границ `IN_SCOPE_SURPRISE` и `OUT_OF_SCOPE_EXPLORATORY` без доступа к содержимому external challenge.

G0-G6 сначала выполняются как development pass. Все tuning decisions должны быть завершены до sealed holdout. Результаты development публикуются и не смешиваются с selection results.

В конце development фиксируются survivor set, derived `E_target`, candidate hashes, suite-profile hashes, channel grid, три structural class aggregates, full structural diagnostics, common metric, ranking, `development_decision_path.json`, YouTube output-readiness rules, block count, scanner limits и полный budget.

### 10.3. Публичная preregistration эксперимента

До открытия `SELECTION_HOLDOUT` публикуются:

- этот protocol;
- `bench_program_manifest.json` и актуальная lineage;
- `d0_topology_experiment_manifest.json`;
- `experiment_design_manifest.json` и его независимая timestamp attestation;
- `experiment_core_manifest.json`;
- `candidate_manifest_<id>.json` каждого исходного кандидата;
- `survivor_set_manifest.json` с development-причиной каждого исключения;
- `channel_grid.json`;
- `structural_metric_manifest.json`;
- `common_metric_manifest.json`;
- `energy_threshold_derivation.json`;
- `optimizer_method_manifest.json` и его timestamp attestation;
- `equivalence_bands.json`;
- `development_decision_path.json`;
- `energy_partition_bias_analysis.json`;
- `youtube_qualification_manifest.json`;
- `youtube_output_readiness_manifest.json`;
- `youtube_block_count.json`;
- `full_winner_reel_plan_manifest.json` с отдельным plan hash для каждого survivor;
- `experiment_budget.json`;
- `selection_holdout_commitment.json`;
- `confirmation_holdout_commitment.json`;
- `external_challenge_commitment.json`;
- `external_challenge_scope_schema.json`;
- `external_challenge_transform_grammar.json`;
- `hidden_package_seed_protocol.json`;
- `randomness_beacon_manifest.json`;
- `run_order.json`;
- `platform_control_manifest.json`;
- `platform_context_compatibility_manifest.json`;
- `context_dependency_resolution_plan.json` с отдельным plan hash для каждого survivor;
- `suite_reserve_manifest.json`;
- `cross_family_compatibility_manifest.json`;
- `scanner_resource_manifest.json`;
- `state_transition_table.json`;
- `preregistration_bundle_manifest.json`;
- hard gates, ranking, stop rules;
- hashes исходного кода и окружения.

`d0_topology_experiment_manifest.json` является канонической верхнеуровневой записью, требуемой концепцией GSP v8.0. Он содержит schema version, protocol hash, program hash, experiment index, `experiment_core_hash256`, hash preregistration bundle и относительные пути ко всем компонентным manifests.

`channel_grid.json` является машинным представлением `D0_REQUIRED_CHANNEL_GRID`, `BOUNDARY_GRID` и `STRESS_GRID`. `youtube_qualification_manifest.json` является машинным представлением `D0_YOUTUBE_QUALIFICATION_SET` и правил временных блоков.

До создания любого скрытого пакета публикуется и получает независимую timestamp attestation `experiment_design_manifest.json`. Он содержит все data-independent решения эксперимента: program hash, experiment index, parent lineage hash, candidate и survivor sets, suite profiles, channel grid, structural и common metrics, diversity gate, energy-threshold derivation, equivalence bands, ranking, development decision path, context-resolution plans, platform rules, external scope schema, transform grammar, hidden-package seed protocol, randomness-beacon plan, budgets, state table и hashes кода. Он не содержит holdout seeds, commitments, run order либо скрытый case content.

Идентичность дизайна:

```text
experiment_design_hash256 = SHA256(
    LP("GSP-D0-BENCH-DESIGN-6") ||
    LP(JCS(experiment_design_manifest))
)
```

Только после timestamp этого hash независимые хранители однократно создают `SELECTION_HOLDOUT`, `CONFIRMATION_HOLDOUT` и external challenge. Каждый commitment record включает `experiment_design_hash256`, generator или composition procedure ID, custodian ID, creation timestamp и package hash. Обе закрытые выборки получают независимые seeds. External challenge получает отдельный commitment и хранится у независимого составителя, который не участвовал в synthesis, estimator tuning или ranking design. Все три объекта хранятся раздельно.

Для mechanically generated selection и confirmation corpora применяется замороженная commit-beacon-reveal ceremony из `hidden_package_seed_protocol.json`. Она использует secret nonce независимого хранителя и заранее выбранный будущий pulse публичного randomness beacon. Проект не публикует nonce, который можно перебирать после commitment хранителя.

До design commitment `randomness_beacon_manifest.json` фиксирует:

```text
primary_beacon_id
primary_pulse_id_or_utc
ordered_fallback_beacons[]
signature_verification_material_hash256
canonical_pulse_serialization
secret_nonce_length_bytes
custodian_commit_deadline_utc
beacon_availability_deadline_utc
package_commit_deadline_utc
reveal_deadline_after_open_authorization_seconds
```

`secret_nonce_length_bytes` обязан быть не меньше 32. Target pulse обязан находиться в будущем относительно timestamp `experiment_design_hash256`. Для каждого package и отдельного domain tag хранитель до target pulse создает secret nonce из cryptographically secure random source, фиксирует source class в signed record, публикует commitment и больше nonce не меняет:

```text
custodian_secret_commitment = SHA256(
    LP("GSP-D0-CUSTODIAN-SECRET-6") ||
    LP(package_role) ||
    LP(experiment_design_hash256) ||
    LP(custodian_secret_nonce)
)
```

После появления первого допустимого pulse из заранее замороженного порядка hidden seed равен:

```text
hidden_seed = SHA256(
    LP("GSP-D0-HIDDEN-PACKAGE-SEED-6") ||
    LP(package_role) ||
    LP(experiment_design_hash256) ||
    LP(custodian_secret_nonce) ||
    LP(canonical_beacon_pulse_bytes)
)
```

Package generator является детерминированной функцией hidden seed, design hash и опубликованного generator hash. Custodian создает package ровно один раз, подписывает его commitment до `package_commit_deadline_utc` и сохраняет secret nonce закрытым до разрешенного открытия package. Golden vectors обязаны доказывать порядок LP-полей, byte order и как минимум первые 16 generated case IDs для каждой роли package. Beacon pulse, его подпись, verification outcome и hash canonical bytes публикуются вместе с package commitment; secret nonce раскрывается только вместе с package.

Fallback разрешен только при недоступности либо криптографической невалидности primary pulse и только в заранее заданном порядке. Если ни один source не дал валидный pulse до deadline, статус равен `RANDOMNESS_BEACON_TIMEOUT`. Если хранитель не committed secret вовремя, статус равен `CUSTODIAN_COMMIT_TIMEOUT`. Если package commitment не создан вовремя, статус равен `PACKAGE_COMMIT_TIMEOUT`. Если после разрешения открытия secret не раскрыт вовремя, статус равен `CUSTODIAN_REVEAL_TIMEOUT`. Несовпадение commitment, pulse или пересчитанного seed дает `HIDDEN_SEED_MISMATCH`. Каждый такой исход аннулирует текущий experiment index, публикуется как signed failure record и не разрешает новый package для того же design hash.

External challenge может включать содержательно составленные человеком cases и поэтому не объявляется случайной выборкой. Та же ceremony фиксирует только mechanically generated параметры, placements и order. Независимый составитель дополнительно подписывает provenance log, число отвергнутых drafts, причины отклонения и заявление о том, что не видел candidate results. Commitment обеспечивает неизменность, но не доказывает беспристрастность ручного содержания. Независимость составителя, отсутствие candidate-specific branching и полный provenance остаются явными организационными предпосылками.

Для одного `experiment_design_hash256` разрешен ровно один commitment каждого типа. Появление альтернативного commitment, повторная генерация скрытого package либо изменение design после передачи его hash хранителю дает `HOLDOUT_MULTIPLE_GENERATION` и `EXPERIMENT_INVALIDATED`. Если создание package технически завершилось ошибкой до получения commitment, хранитель публикует signed failure record; повтор требует нового experiment design hash, нового experiment index и новой timestamp attestation. Preregistration получает отдельную независимую timestamp attestation после сборки полного bundle. Ключи selection, confirmation и external challenge не могут находиться в одном автоматически открываемом пакете.

Все нормативные JSON используют RFC 8785 JCS и не содержат floating-point values. Рациональные значения записываются как пара целых чисел либо каноническая десятичная строка с явно заданным scale.

Для hash preimage применяются:

```text
LP(bytes) = U32BE(length(bytes)) || bytes
U32BE     = беззнаковое 32-битное целое, старший байт первым
||        = конкатенация без разделителя
SHA256    = SHA-256 над точной последовательностью bytes
```

Все текстовые доменные метки кодируются UTF-8 без BOM. `length(bytes)` измеряется в байтах, а не в Unicode code points. Эти правила относятся к земному лабораторному транспорту и не объявляются частью семантики ответа неизвестного наблюдателя.

### 10.4. Идентичность эксперимента

`experiment_core_manifest.json` содержит `experiment_design_hash256`, program hash, experiment index, parent lineage hash, оба holdout commitments и external challenge commitment. Data-independent решения не копируются в него с возможностью расхождения: они разрешаются только через immutable design hash. Core не содержит `experiment_core_hash256`, `run_order.json` или hash производного run order.

```text
experiment_core_hash256 = SHA256(
    LP("GSP-D0-BENCH-6") ||
    LP(JCS(experiment_core_manifest))
)
```

Три порядка опытов выводятся разными domain tags без циклической зависимости:

```text
selection_run_order_seed = first64(
    SHA256(
        LP("GSP-D0-SELECTION-RUN-ORDER-6") ||
        LP(experiment_core_hash256) ||
        LP(selection_holdout_commitment_hash256)
    )
)

confirmation_run_order_seed = first64(
    SHA256(
        LP("GSP-D0-CONFIRMATION-RUN-ORDER-6") ||
        LP(experiment_core_hash256) ||
        LP(confirmation_holdout_commitment_hash256)
    )
)

external_challenge_run_order_seed = first64(
    SHA256(
        LP("GSP-D0-EXTERNAL-CHALLENGE-RUN-ORDER-6") ||
        LP(experiment_core_hash256) ||
        LP(external_challenge_commitment_hash256)
    )
)
```

`first64` означает первые восемь байт SHA-256 в сетевом порядке. Алгоритм PRNG, unbiased bounded draw и Fisher-Yates фиксируются test vectors.

`run_order.json` содержит три seed, generator ID и правила разрешения порядка, но не раскрывает скрытые элементы. После открытия соответствующего объекта публикуется `selection_run_order_resolved.json`, `confirmation_run_order_resolved.json` или `external_challenge_run_order_resolved.json` с item hashes в фактическом порядке. Порядки confirmation и external challenge не вычисляются из selection outcomes.

После получения `run_order.json` создается `preregistration_bundle_manifest.json`. Он перечисляет `experiment_core_hash256`, hash run order и hashes всех компонентных preregistration-файлов, кроме верхнеуровневого `d0_topology_experiment_manifest.json`. Затем верхнеуровневый manifest ссылается на готовый bundle hash. Bundle manifest не участвует в выводе seed.

Каждый candidate manifest получает идентичность, совместимую с концепцией GSP v8.0:

```text
d0_candidate_hash256 = SHA256(
    LP("GSP4-D0-CANDIDATE") ||
    LP(JCS(candidate_manifest))
)
```

Candidate manifest перечисляет hashes всех synthesis tables, estimator tables и decision constants. Изменение любого из них меняет `d0_candidate_hash256`.

### 10.5. Два одноразовых holdout и внешний challenge

После preregistration первым открывается только `SELECTION_HOLDOUT`. На нем без настройки выполняются selection passes G2-G6. G0 и G1 не используют закрытые данные. Ranking получает `WINNER_PROVISIONAL` либо `NO_CANDIDATE`.

Selection и confirmation holdout являются независимыми реализациями замороженного in-distribution design, а не доказательством устойчивости к неизвестным классам искажений. Out-of-distribution probing выполняет внешний challenge, причем только cases внутри замкнутой опубликованной grammar могут влиять на support claim. Разница между этими задачами сохраняется в отчетности.

До открытия `CONFIRMATION_HOLDOUT` публикуется `provisional_decision.json` с hashes всех selection results и точным winner ID. Затем confirmation key открывается только для этого победителя, и выполняется core часть G7. Runner-up не проверяется на том же confirmation holdout.

External challenge содержит два заранее типизированных раздела:

- `IN_SCOPE_SURPRISE`: новые placements, compositions и impairment recipes внутри численных границ заявленного support envelope;
- `OUT_OF_SCOPE_EXPLORATORY`: новые классы либо severity за пределами заявленного support envelope.

Составитель фиксирует тип каждого case внутри sealed package до preregistration. Переклассификация после результата запрещена. Experiment team до открытия видит только commitment, schema, замкнутую опубликованную transform grammar, limits на число случаев и budget.

Числового попадания в support envelope недостаточно для статуса `IN_SCOPE_SURPRISE`. `external_challenge_transform_grammar.json` задает закрытый типизированный язык преобразований:

- конечный список допустимых primitive node types;
- разрешенные композиции и их порядок;
- maximum graph depth, node count и fan-out;
- физическую единицу и замкнутый диапазон каждого параметра;
- правила deterministic sample alignment и rounding;
- запрещенные циклы, decoder feedback, adaptive retry, undefined transforms и candidate-specific branches;
- maximum case count и minimum valid in-scope case count;
- canonical serialization и validator golden vectors.

Граф не является in-scope, если он нельзя построить только из разрешенных nodes либо если его topology отсутствует в grammar, даже когда отдельные числа лежат внутри известных диапазонов. Значение параметра может выбираться seeded rule из общей физической области, но case не может выбирать transform, frequency, placement или severity условием по `candidate_id`, candidate hash, development winner либо private candidate metric.

После открытия и до запуска любого decoder два независимо реализованных scope validator проверяют каждый case против grammar, `external_challenge_scope_schema.json` и preregistered support contract. Case, который не проходит оба validator либо получает разные canonical graphs, маркируется `INVALIDATED_SCHEMA`, публикуется полностью и может выполняться только как exploratory diagnostic. Он никогда не является candidate failure и навсегда добавляется в cumulative corpus с этим label.

Если после удаления invalid cases остаются все preregistered class quotas и не менее `minimum_valid_external_in_scope_cases`, experiment продолжается без замены cases. Иначе package получает `EXTERNAL_CHALLENGE_SCHEMA_INVALID`, текущий experiment index аннулируется, а ручное исправление либо догенерация cases запрещены.

External challenge открывается только после того, как неизменный preliminary winner прошел core confirmation. Провал любого валидного `IN_SCOPE_SURPRISE` hard gate дает `FULL_VALIDATION_FAILED`. `OUT_OF_SCOPE_EXPLORATORY` и `INVALIDATED_SCHEMA` не выбирают победителя и не расширяют support claim; их полный результат публикуется как граница внешней применимости. Ни один external result не разрешает tuning внутри текущего experiment index.

G8 выполняется после фиксации confirmation и external challenge и отдельно проверяет анализ, канонические результаты и ranking.

После открытия любой закрытой выборки запрещено менять:

- synthesis tables и carrier maps;
- окна, amplitudes и phases;
- estimator и thresholds;
- aggregation rules;
- candidate и survivor sets;
- channel cells и severity;
- common metric и noise vectors;
- equivalence bands;
- resource limits и ranking;
- YouTube block, readiness и platform control rules;
- suite profiles;
- scanner policy;
- external challenge scope labels, cases, thresholds и opening order.

Любое такое изменение дает `EXPERIMENT_INVALIDATED`. Внутри эксперимента holdout не перезапускается. Оба holdout и раскрытый external challenge публикуются, добавляются в lineage и cumulative exposed corpus и больше не используются для выбора в будущей попытке.

Новый эксперимент разрешен только если не исчерпан `program_max_experiments`. Он получает новый experiment index, два новых независимых holdout, новый external challenge, новую preregistration и отдельную lineage entry. Все предыдущие попытки остаются в freeze package.

---

## 11. Обязательный бюджет эксперимента

До preregistration публикуется `experiment_budget.json`.

### 11.1. Минимальный объем канонических D0-артефактов

Для кандидата с `m` копиями нужны:

```text
72 assembled-form references
72 * m diagnostic-subform references
```

| Кандидат | Assembled references | Diagnostic references | Всего references |
| --- | ---: | ---: | ---: |
| `D0-B1` | 72 | 72 | 144 |
| `D0-T2` | 72 | 144 | 216 |
| `D0-T3` | 72 | 216 | 288 |
| `D0-F3` | 72 | 216 | 288 |
| Итого | 288 | 648 | 936 |

У `D0-B1` assembled form и единственная diagnostic subform могут ссылаться на один WAV по hash. Поэтому базовый максимум уникальных WAV-объектов после обязательной дедупликации B1 равен 864. Дополнительное совпадение файлов заранее не предполагается.

К этому бюджету добавляются sequence artifacts:

- `BOOT_RECORD`;
- `CALL`;
- `ANSWER`;
- `SUITE_ANSWER`;
- Level 2 selector cases;
- поврежденные границы;
- false-aggregation cases;
- candidate-to-suite cross-confusion;
- platform controls;
- scanner spam и resource cases.

### 11.2. Обязательные численные поля бюджета

```text
max_unique_wav_objects
max_artifact_references
max_local_channel_jobs
max_youtube_uploads
max_youtube_pilot_uploads
max_youtube_selection_uploads
max_youtube_confirmation_uploads
max_external_challenge_cases
max_external_challenge_jobs
max_external_challenge_bytes
max_external_in_scope_cases
minimum_valid_external_in_scope_cases
max_external_in_scope_jobs
max_external_exploratory_cases
max_external_exploratory_jobs
max_youtube_download_bytes
max_platform_processing_wait_hours
max_platform_output_polls
max_cpu_core_hours
max_gpu_hours
max_peak_disk_bytes
max_wall_calendar_days
max_human_hours
max_external_cost_minor_units
max_repeated_invalid_platform_blocks
max_candidate_count
max_youtube_block_dates
max_independent_pre_reference_corrections
max_independent_material_correction_adjudications
max_restarts_within_experiment = 0
program_max_experiments
current_experiment_index
```

Для каждого значения задаются единица, предел, ответственное лицо и действие при превышении.

`program_max_experiments` совпадает с корневым program manifest и не может изменяться после первой попытки. Experiment index необратимо расходуется в момент публикации timestamped `experiment_design_hash256`, то есть до создания скрытых packages. Любая последующая aborted, invalidated либо незавершенная попытка расходует этот index независимо от того, был ли собран полный preregistration bundle или раскрыт holdout. До design commitment разрешенное открытое development не расходует новый index.

Budget исходит из того, что все четыре обязательных кандидата дойдут как минимум до полного development G3. Возможность formal dominance не используется для уменьшения обязательного бюджета заранее.

`max_youtube_uploads` равен сумме pilot, selection, confirmation, control и повторов invalid blocks. Confirmation budget не может быть меньше максимального upload count среди заранее зарегистрированных full-winner plans всех survivor. Число full-winner reels и число standalone qualification reels вычисляются до preregistration из точного artifact plan, а не оставляются устной оценкой. External challenge имеет отдельный неперераспределяемый budget и не может расходовать confirmation jobs до своего открытия. In-scope quota резервируется отдельно и не может быть вытеснена exploratory cases. Невыполненный in-scope case блокирует confirmation; exploratory case, не выполненный после исчерпания только своей quota, публикуется как `EXPLORATORY_NOT_RUN_RESOURCE_LIMIT` и не меняет winner.

Если `B_required(n)` из раздела 19.1 определяет минимальное число YouTube block dates для `n` кандидатов, корневой budget обязан удовлетворять:

```text
max_youtube_block_dates >= B_required(max_candidate_count)
```

Нарушение инварианта дает `PROGRAM_BUDGET_INCONSISTENT` до первого design commitment. Формулу нельзя обрезать произвольным `min(...)`, если это нарушает требования divisibility или balance.

Commit-beacon-reveal deadlines из раздела 10.3 также являются hard budgets. Они хранятся как абсолютные UTC timestamps либо как точные интервалы от подписанного opening authorization. Отсутствие ответа не создает бесконечное ожидание.

Placeholder, бесконечность и неограниченный автоматический retry запрещены.

Если `max_independent_pre_reference_corrections = 1`, budget обязан резервировать как минимум одну `max_independent_material_correction_adjudications`; иначе correction policy внутренне невыполнима и design получает `PROGRAM_BUDGET_INCONSISTENT`.

### 11.3. Stop rules

Эксперимент останавливается без победителя, если:

- исчерпан любой неперераспределяемый hard budget;
- не получено требуемое число валидных YouTube-блоков;
- holdout раскрыт до фиксации решения;
- commit-beacon-reveal ceremony не завершена в срок либо не воспроизводит seed;
- валидная часть external challenge не выполняет preregistered minimum и class quotas;
- обнаружена смена исходного кода или manifest;
- нарушена lineage либо превышен `program_max_experiments`;
- платформа не позволяет получить сопоставимые выходные дорожки;
- ни один кандидат не прошел hard gates;
- независимая реализация не воспроизводит нормативные результаты.

Ресурсный предел нельзя расширить после просмотра результата только для спасения конкретного кандидата. Расширение завершает текущую попытку и требует нового experiment index, двух новых holdout, нового external challenge и lineage entry. Корневой program limit при этом не меняется.

---

## 12. Артефактный пакет

Нормативная структура:

```text
d0_bench_v6/
  protocol/
    d0_bench_protocol_v6.0.md
    predecessor_reference.json
    concept_reference.json
  program/
    bench_program_manifest.json
    experiment_lineage.json
    cumulative_exposed_corpus_manifest.json
  preregistration/
    d0_topology_experiment_manifest.json
    experiment_design_manifest.json
    experiment_core_manifest.json
    experiment_budget.json
    survivor_set_manifest.json
    channel_grid.json
    structural_metric_manifest.json
    common_metric_manifest.json
    energy_threshold_derivation.json
    optimizer_method_manifest.json
    equivalence_bands.json
    development_decision_path.json
    energy_partition_bias_analysis.json
    youtube_qualification_manifest.json
    youtube_output_readiness_manifest.json
    youtube_block_count.json
    full_winner_reel_plan_manifest.json
    platform_control_manifest.json
    platform_context_compatibility_manifest.json
    context_dependency_resolution_plan.json
    selection_holdout_commitment.json
    confirmation_holdout_commitment.json
    external_challenge_commitment.json
    external_challenge_scope_schema.json
    external_challenge_transform_grammar.json
    hidden_package_seed_protocol.json
    randomness_beacon_manifest.json
    suite_reserve_manifest.json
    cross_family_compatibility_manifest.json
    scanner_resource_manifest.json
    state_transition_table.json
    integer_semantics.json
    run_order.json
    preregistration_bundle_manifest.json
  candidates/
    D0-B1/
      candidate_manifest.json
      tables/
      canonical_wav/
      diagnostic_wav/
    D0-T2/
    D0-T3/
    D0-F3/
  corpus/
    training/
    cumulative_exposed/
    selection_holdout_encrypted/
    confirmation_holdout_encrypted/
    external_challenge_encrypted/
    scanner_conformance/
    diversity_conformance/
    common_calibration/
  runs/
    local/
    youtube/
    controls/
  results/
    candidate_results/
    block_results/
    selection_results/
      selection_run_order_resolved.json
    confirmation_results/
      confirmation_run_order_resolved.json
      full_winner_reel_plan_resolved.json
    external_challenge_results/
      external_challenge_run_order_resolved.json
      external_challenge_scope_validation_reference.json
      external_challenge_scope_validation_independent.json
    confusion_matrices/
    support_envelopes/
    exclusion_envelopes/
    state_transition_log.jsonl
    final_decision.json
  implementations/
    reference/
    independent/
      declaration_of_independence.json
      independent_results_commitment.json
      independent_correction_record.json
  environment/
    tool_versions.json
    container_or_lockfiles/
  publication/
    provisional_decision.json
    transport_observer_report.json
    canary_manifest.json
    current_support_manifest.json
    README.md
    checksums.sha256
```

Каждый файл, влияющий на синтез, декодирование, выбор или интерпретацию результата, получает SHA-256. Относительные пути входят в JCS manifest. Дублирование содержимого определяется hash, а не именем файла.

---

## 13. Последовательность gate

| Gate | Development до preregistration | Selection holdout | Confirmation holdout | External challenge | Возможный результат |
| --- | --- | --- | --- | --- | --- |
| G0 | открытые math vectors | не используется | identity subset | не используется | pass или protocol error |
| G1 | feasibility prepass, derivation `E_target` | не используется | identity subset | не используется | pass или candidate reject |
| G2 | clean training и negatives | полный sealed clean subset | winner subset повторяется в G7 | in-scope и exploratory clean cases | pass или candidate reject |
| G3 | local channel training | sealed channel cells и seeds | winner boundary subset в G7 | unseen graphs внутри frozen grammar; новые classes только exploratory | pass или candidate reject |
| G4 | pilot YouTube blocks | preregistered comparison blocks | full winner YouTube set в G7 | только если case manifest явно требует platform run | pass или candidate reject |
| G5 | построение и tuning трех suite-профилей | sealed cross-confusion cases | winner profiles повторяются в G7 | sealed cross-family surprise cases | pass или candidate reject |
| G6 | scanner training и resource pilot | sealed adversarial cases | winner cases повторяются в G7 | sealed scanner surprise cases | pass или candidate reject |
| G7 | не выполняется | не выполняется | core winner-only validation | открывается только после core pass | pass или experiment failure |
| G8 | не выполняется | после фиксации всех результатов | те же зафиксированные данные | тот же раскрытый immutable package | `FREEZE_READY` или fail |

В development G0-G6 выполняются до experiment preregistration. После preregistration selection passes G2-G6 выполняются заново без tuning. Только после публикации provisional decision открывается confirmation holdout и выполняется core G7. External challenge открывается только после core pass. Поздний успех не отменяет ранний отказ.

---

## 14. G0: математика и сериализация

До генерации полного корпуса две реализации воспроизводят:

- BCH generator и все нормативные BCH vectors;
- аффинную маску;
- GF(64) multiplication;
- generic RS-вектор GSP v8.0 раздела 18.5;
- bootstrap `BOOT_DATA` и `BOOT_PARITY` GSP v8.0 раздела 18.6;
- `d0_rs_test_vectors.json` как минимум с zero, BOOT fixture и alternating/max-value DATA cases;
- JCS serialization;
- LP serialization;
- candidate hashes;
- run-order seed;
- window sanity vectors раздела 8;
- integer energy;
- sample peak;
- true peak reference calculation;
- PRNG shuffle vectors;
- `bch_miscorrection_fraction_by_exact_error_weight` полным перебором: 180/455 при весе 3, 540/1365 при 4, 1413/3003 при 5, 2355/5005 при 6, 3135/6435 при 7 и 8, симметрично при 9-12 и 105/105, 15/15, 1/1 при 13-15;
- квантильные rank и mirror-rank vectors для `L` из {1, 3, 8, 20, 100} при `q = 1/4`;
- взвешенный nearest-rank vector с неравными рациональными весами;
- interval censoring vectors: censored элемент ниже ранговой границы, дающий `LOWER_BOUND` при measured ранговой позиции;
- fla exact comparison vectors на границе предела;
- как минимум 16 generated case-ID vectors для каждой hidden package role;
- failure-support overlap и threshold cross multiplication;
- 128-bit boundary vectors раздела 9.3.

Для D0 RS явно проверяется, что generator coefficients `[1,55,61,37,48,47,20,6,22]` интерпретируются от старшей степени к свободному члену. Тесты обязаны падать при намеренно обратном порядке.

Минимальный самодостаточный набор `D0_RS(16,8)`:

| ID | DATA, 8 значений GF(64) | PARITY, 8 значений GF(64) |
| --- | --- | --- |
| `ZERO` | `[0,0,0,0,0,0,0,0]` | `[0,0,0,0,0,0,0,0]` |
| `BOOT` | `[19,45,4,1,1,1,2,4]` | `[37,1,55,37,52,23,57,62]` |
| `ALT_0_63` | `[0,63,0,63,0,63,0,63]` | `[25,61,17,29,30,44,34,2]` |
| `MAX` | `[63,63,63,63,63,63,63,63]` | `[6,49,6,45,7,51,53,13]` |

Каждая реализация обязана воспроизвести эти vectors до channel tests. Negative G0 cases намеренно меняют порядок коэффициентов, удаляют или добавляют коэффициент, меняют DATA/PARITY order и инвертируют один parity symbol. Каждый такой case обязан завершиться несовпадением, а не новым допустимым соглашением.

`integer_semantics.json` задает width каждого операнда и аккумулятора, signedness, порядок байтов, порядок операций и rounding ties. Для нормативных energy и ratio операций разрешены только exact arithmetic без wrap и saturation, unsigned accumulator не уже 128 бит либо integer arbitrary precision. Он также задает exact-ratio cross multiplication, `ten_log10_fixed_q`, ее scale, approximation bound и golden vectors. Неопределенное поведение языка, системный floating-point `log10` и зависимость от размера машинного `int` запрещены в нормативных расчетах.

G0 обязан доказать, что намеренно выбранная 64-bit реализация отвергается на 128-bit boundary vectors. Реализация не может считаться совместимой только потому, что малые примеры случайно не переполняются.

Любое несовпадение является ошибкой протокола или реализации. Настройка акустических параметров до устранения несовпадения запрещена.

---

## 15. G1: synthesis feasibility

Для всех 72 assembled forms и всех diagnostic subforms проверяются:

- точная длина 48 000 отсчетов assembled form;
- канонический PCM format;
- отсутствие integer overflow;
- `E_target` tolerance;
- sample peak limit;
- true peak limit;
- отсутствие NaN и floating-point зависимости в итоговом PCM;
- повторяемость sample hash на двух поддерживаемых компьютерах;
- соответствие physical support manifest;
- правильное расположение временных ролей;
- basis rank;
- Gram condition limit;
- inter-copy correlation limit;
- отсутствие непредусмотренных частот;
- decoder self-consistency.

G1 выполняется в неизменяемом порядке:

1. проверить schema и ненулевую prototype form;
2. выполнить optimizer строго внутри общего `B(P,C)`;
3. вычислить конечный целочисленный `E_cap` каждой формы;
4. применить `E_cap_min_required` и зафиксировать `F_mandatory`;
5. один раз вывести `E_target` по разделу 6.1;
6. синтезировать все feasible mandatory forms при общем target;
7. проверить дополнительные candidates при уже выведенном target;
8. зафиксировать immutable `energy_eligible_set`; final survivor set и `comparison_mode` фиксируются после development G2-G6 без пересчета target.

Candidate-specific target запрещен. Кандидат, исключенный на шагах 1-4, не входит в минимум `E_common_cap`. Кандидат, прошедший шаг 4, не может быть удален для повышения target.

Также проверяется полнота layer schema раздела 5.4. Отсутствующее поле не интерпретируется по аналогии с suite.

Кандидат с хотя бы одной невалидной формой получает `SYNTHESIS_INFEASIBLE`. Если не осталось ни одного mandatory feasible candidate, G1 возвращает `COMMON_ENERGY_INFEASIBLE`. Если остается ровно один общий survivor, фиксируется `SOLE_FEASIBLE`, но следующие gates не пропускаются.

---

## 16. G2: `CLEAN_MATH_GATE`

### 16.1. Положительный корпус

В canonical PCM без lossy преобразования проверяются:

- все 72 assembled forms;
- все diagnostic subforms;
- все допустимые timing offsets внутри preregistered tolerance;
- все marker roles;
- последовательности `BOOT_RECORD`, `CALL`, `ANSWER`, `SUITE_ANSWER`;
- Level 2 selector;
- граничные значения `D0_OBJECT6(0)` и `D0_OBJECT6(63)`;
- заранее выбранные минимальные и максимальные BCH weights;
- правильные и восстановленные кворумы.

Требуется ноль неверных логических решений и ноль пропущенных обязательных форм.

### 16.2. Отрицательный корпус

Проверяются:

- одиночная подформа многокопийного кандидата;
- неправильная роль копии;
- role permutation;
- несовместимые копии;
- склейки соседних токенов;
- первый и оба резервных suite-профиля каждого кандидата, как минимум во всех representative D0-cross-confusion forms;
- музыка;
- речь;
- белый и окрашенный шум;
- multisine вне D0 grammar;
- почти валидные BCH и dual-rail формы;
- смещенные маркеры;
- случайные PCM-последовательности с фиксированными seeds.

Требуется ноль ложных принятых D0 records и ноль ложных `EXACT`.

Провал обязательного отрицательного case одним кандидатом исключает этого кандидата. Он не делает весь сравнительный block невалидным, если platform control, source hashes и остальные block-validity условия сохранены. Отрицательный `PLATFORM_CONTROL-1`, предназначенный для проверки самого блока, имеет отдельную роль: его провал аннулирует block для всех кандидатов по разделу 19.

### 16.3. Метрики

Candidate-native score нормируется только для внутренней диагностики:

```text
score_norm = score_raw / template_energy
```

Внутренний запас:

```text
native_margin_db = 20 * log10(
    score_true /
    max(score_accept_threshold, score_best_wrong)
)
```

Все три score в этой формуле являются положительными величинами с направлением "больше лучше". Нулевая нижняя граница заменяется заранее фиксированным положительным floor. Если estimator использует cost, candidate manifest задает собственное отображение только для native diagnostics.

`native_margin_db` запрещено использовать для сравнения разных кандидатов, независимо от того, применены 10 или 20 log10. Межкандидатный ranking использует exact `common_failure_reserve_ratio` раздела 9.3 и другие прямо измеренные физические величины.

В G2 все feasible candidates проходят одну и ту же analytical AWGN calibration cell. Отчет содержит ожидаемое и фактическое отношение энергий, первый failure grid point по каждому seed, exact common reserve ratio, dB_q и censor status.

Порог native acceptance, false acceptance limit, condition number limit, correlation limit и minimum common reserve задаются численно до selection holdout.

---

## 17. G3: локальная цифровая матрица

`channel_grid.json` обязан содержать как минимум следующие классы:

- AAC-LC: 64, 96, 128, 192 и 320 kbit/s;
- Opus: 32, 48, 64, 96, 128 и 160 kbit/s;
- mono, dual-mono, downmix и channel imbalance;
- deterministic resampling между 44,1 kHz, 48 kHz и обратно;
- gain;
- limiter;
- AGC;
- sample clipping;
- true-peak overshoot cases;
- low-pass;
- high-pass;
- spectral tilt;
- static notch по положению, ширине и глубине;
- white, pink и shaped noise;
- codec-frame offset;
- repeated lossy transcodes;
- crop;
- insertion;
- deletion;
- mute burst;
- additive burst;
- sample-clock drift;
- combined burst plus notch;
- combined codec plus gain plus limiter;
- combined codec plus spectral damage.

Для каждой внутренней границы каждого временного кандидата и каждого обязательного AAC/Opus режима измеряются:

```text
pre_echo_energy_ratio_db
post_echo_energy_ratio_db
smear_duration_samples
boundary_copy_margin_before
boundary_copy_margin_after
```

`max_pre_echo_energy_ratio_db`, `max_post_echo_energy_ratio_db` и `max_smear_duration_samples` фиксируются до selection holdout. Эти tests применяются к фактическому candidate window, а не предполагают half-cosine.

Там же фиксируется gate ложных логических принятий. Прежняя метрика `false_value_rate` заменена на ролево полную `false_logical_acceptance`, потому что из 72 форм только 64 несут value: неверная marker role, принятие marker как object, object как marker, одного marker как другого либо неверная классификация `BOOT_SYNC` опаснее неверного `OBJECT6`, поскольку способны породить ложную grammar, boundary pair или beacon. Ложным логическим принятием считается ЛЮБОЕ принятое неверное `value_or_role`, включая ложный record или grammar более высокого уровня, независимо от того, как реализация классифицировала физическую причину или число битовых ошибок.

Знаменатель является условным по отказам, а не общим числом observations. Причина: pooled-знаменатель по всей сетке одновременно позволяет разбавить катастрофическую концентрацию ложных решений одной impairment family безопасными observations другой и штрафует живучего кандидата, который борется за сигнал глубже конкурентов и потому имеет больше возможностей ошибиться там, где рано отказавший кандидат тривиально показывает ноль. Условный знаменатель измеряет качество безопасного отказа независимо от того, где лежит граница кандидата:

```text
failure(cell)  = кандидат не вернул правильное value_or_role
                 (erasure, conflict, partial или ложное принятие)

fla_num(family) = число failures данной family,
                  завершившихся ложным принятием
fla_den(family) = число всех failures данной family
```

Правило раздела 7 о запрете pooling по impairment families применяется и здесь. Gate двухуровневый и раздельный по сеткам:

```text
boundary_family_fla_limit_num / boundary_family_fla_limit_den
boundary_global_fla_limit_num / boundary_global_fla_limit_den
stress_family_fla_limit_num  / stress_family_fla_limit_den
stress_global_fla_limit_num  / stress_global_fla_limit_den
fla_min_informative_failures
```

`BOUNDARY_GRID` и `STRESS_GRID` имеют раздельные пределы, потому что назначение сеток разное: предел, достаточно мягкий для намеренно запредельного stress, бесполезен около границы поддержки, а предел, достаточно строгий для границы, делает stress произвольно неисполнимым. Пределы для `BOUNDARY_GRID` являются hard gate; пределы для `STRESS_GRID` являются публикуемой характеристикой безопасной деградации с собственным мягким преregистрированным порогом. Кандидат проходит только если каждая family И глобальная доля соответствующей сетки внутри своих пределов. Если `fla_den(family) < fla_min_informative_failures`, family получает `FLA_INSUFFICIENT_FAILURES`: нулевая доля из недостаточного числа отказов не считается доказательством безопасности, но и не блокирует кандидата; статус публикуется. Сравнение долей выполняется точно, без предварительного деления:

```text
fla_num * limit_den <= fla_den * limit_num
```

с нормативной шириной аккумулятора из `integer_semantics.json`. На `REQUIRED_GRID` и `STRUCTURAL_COMPARISON_GRID` продолжает действовать нулевое требование раздела 25.

У `D0-F3` нет внутренних временных границ. Его `pre_echo`, `post_echo` и boundary smear fields получают явное значение `NOT_APPLICABLE`, а не ноль. Для него вместо этого обязательны inter-copy interference, assembled crest factor и simultaneous-basis leakage tests.

Для временных кандидатов перебираются все уникальные codec-frame offsets modulo hop относительно 0, 24 000, 16 000 и 32 000 отсчетов, когда соответствующая граница существует.

Для каждого burst перебираются все preregistered начальные позиции и длительности, включая повреждение двух соседних временных копий.

Сетка делится на:

- `REQUIRED_GRID`, определяющую бинарную поддержку;
- `BOUNDARY_GRID`, находящую первый измеренный отказ;
- `STRESS_GRID`, не входящую в обещание совместимости.

Результаты этих трех сеток не смешиваются.

`structural_metric_manifest.json` сохраняет все per-ladder результаты, но ranking использует ровно три общих structural class aggregates. Число координат решения заморожено:

```text
K_structural = 3

NOTCH_CLASS_RESERVE_DB_Q       # MAXIMIZE
BURST_CLASS_RESERVE_MS_Q       # MAXIMIZE
COMBINED_CLASS_FAILURE_RATE_Q  # MINIMIZE
```

Каждая координата является заранее зарегистрированной ранговой статистикой по своему классу, а не worst-case. Worst-case по классу остается обязательной публикуемой величиной и hard-gate evidence, но не используется как ранжирующая координата, потому что определяется одной экстремальной ячейкой и уже защищен бинарными условиями раздела 25. Обоснование выбора статистики: эффект топологии проявляется на промежуточных severity ladder, тогда как на экстремальной ячейке повреждение обычно подавляет все топологии по общей физической причине; в отличие от минимума, внутренний квантиль не определяется одной экстремальной ячейкой, а его фактическая повторяемость измеряется эмпирически через `u95_k`. Утверждение о снижении шума пропорционально `sqrt` числа элементов сознательно НЕ используется как обоснование: ячейки сетки не являются выборкой из одной распределительной модели, и асимптотика выборочного квантиля к ним неприменима.

Единицей квантиля является stratum, а не ячейка сетки. Причина нормативная: если квантиль берется по ячейкам, плотность сетки становится скрытой весовой функцией, и семейство повреждений, представленное большим числом placements, получает пропорционально больший голос; тогда победителя можно изменить, добавив формально недублирующие ячейки одной семьи, не изменив ни одного физического результата. Стратификация устраняет эту степень свободы: физический вес каждого семейства задается явно и замораживается, а уточнение сетки внутри stratum меняет только точность внутристратной оценки, но не вес семейства.

Агрегация трехуровневая:

```text
уровень 1: для каждой canonical ladder вычисляется
           first-unsafe reserve относительно общей reference point
уровень 2: внутри каждого stratum по ladder-значениям применяется
           within_stratum_rule; результатом является одно значение stratum
уровень 3: координата класса равна взвешенному nearest-rank квантилю
           по значениям strata этого класса
```

`structural_metric_manifest.json` фиксирует до первого mandatory candidate structural run:

```text
structural_strata[]:
    stratum_id
    stratum_class                  # NOTCH, BURST или COMBINED
    canonical_ladder_ids[]
    within_stratum_rule            # нормативная порядковая статистика,
                                   # по умолчанию медиана nearest-rank
    stratum_weight_num
    stratum_weight_den
minimum_strata_per_class           # не меньше 8
maximum_cells_per_stratum
structural_rank_quantile_num
structural_rank_quantile_den
```

Деление на strata, состав ladder каждого stratum и веса выводятся только из candidate-neutral источников: физической таксономии повреждений channel contract и открытого calibration corpus. Результаты кандидатов ЗАПРЕЩЕНО использовать при выборе состава strata и весов. Веса по умолчанию равны; неравные веса требуют опубликованного инженерного обоснования до development G3. Число severity points внутри ladder не дает ladder дополнительного веса, число ladder внутри stratum не дает stratum дополнительного веса, число ячеек сетки не влияет на веса вообще.

`L` каждого класса равно числу его strata, а не числу ячеек:

```text
L_notch    = число strata класса NOTCH
L_burst    = число strata класса BURST
L_combined = число strata класса COMBINED
```

`minimum_strata_per_class >= 8` обязателен, потому что при малом `L` nearest-rank квантиль вырождается обратно в минимум: `rank(4, 1, 4) = 1`. Значение 8 при `q = 1/4` дает rank 2, то есть координата уже не определяется единственным худшим stratum.

```text
structural_rank_quantile_num
structural_rank_quantile_den
```

`structural_rank_quantile` является одним общим рациональным числом в интервале `(0, 1/2]` для всех трех координат и всех кандидатов. Оно фиксируется вместе с инженерным обоснованием и golden vectors. Значение по умолчанию равно `1/4`. Candidate-specific квантили запрещены. Взвешенный nearest-rank вычисляется нормативным целочисленным правилом без интерполяции:

```text
strata сортируются по возрастанию значения;
при равных значениях порядок задается stratum_id;
W = сумма всех stratum weights (точные дроби через общий знаменатель);
для уровня q выбирается первое значение, на котором накопленный вес
достигает или превышает q * W (сравнение cross multiplication);
для зеркального уровня 1-q список сортируется по убыванию
и применяется то же правило.
```

При равных весах это правило совпадает с `rank(L, num, den) = max(1, ceil(num * L / den))`, где `ceil` вычисляется целочисленно как `(num * L + den - 1) div den`.

`NOTCH_CLASS_RESERVE_DB_Q` является взвешенным nearest-rank квантилем уровня `structural_rank_quantile` по strata класса NOTCH от per-stratum depth reserve. Ladder-значение уровня 1 равно физическому запасу глубины между общей нормативной точкой отсчета `NOTCH_REFERENCE_DEPTH_DB_Q` и первым unsafe attenuation depth данной ladder; все severity записываются в одной dB_q шкале. `BURST_CLASS_RESERVE_MS_Q` строится так же по strata класса BURST от запаса длительности между `BURST_REFERENCE_DURATION_MS_Q` и первым unsafe duration в миллисекундах. `COMBINED_CLASS_FAILURE_RATE_Q` является взвешенным nearest-rank квантилем зеркального уровня `1 - structural_rank_quantile` по strata класса COMBINED от per-stratum доли assembled `ERASURE` плюс `CONFLICT` на общей фиксированной `STRUCTURAL_COMPARISON_GRID`, являющейся candidate-neutral подмножеством `BOUNDARY_GRID`. Каждая из трех координат имеет одно определение для всех кандидатов, включая `D0-B1`.

Точки отсчета структурных запасов являются общими для всех кандидатов и фиксируются численно в `structural_metric_manifest.json` до holdout:

```text
NOTCH_REFERENCE_DEPTH_DB_Q
BURST_REFERENCE_DURATION_MS_Q
```

Обе выводятся только из candidate-neutral источников: channel contract, `STRUCTURAL_COMPARISON_GRID` и открытого calibration corpus. Candidate-declared support envelope, любой другой документ кандидата или его измеренный результат ЗАПРЕЩЕНО использовать как точку отсчета или ее компонент. Кандидат не может увеличить измеренный структурный запас изменением собственных заявлений. Reference points, quantile и правило nearest-rank входят в experiment core hash и после preregistration неизменяемы.

Рядом с каждым квантильным агрегатом обязательно публикуются worst-case значение класса, все stratum-значения и полные отсортированные per-ladder списки каждого stratum. Расхождение знака между квантильным и worst-case сравнением пары кандидатов не является ошибкой, но обязано быть явно показано в `development_decision_path.json` и итоговом отчете.

`STRUCTURAL_COMPARISON_GRID` фиксируется до holdout, имеет canonical cell IDs и не используется для расширения support claim. `REQUIRED_GRID` остается бинарным gate, а `STRESS_GRID` остается диагностикой. Одни и те же observations нельзя дублировать под несколькими IDs для изменения class failure rate или сдвига квантиля.

Все отдельные notch ladders, burst ladders, placements, widths, codec offsets и combined families остаются `structural_diagnostics[]`. Они входят в full publication, hard gates и regression corpus, но не создают дополнительные Pareto dimensions и не получают отдельного голоса в ranking. Candidate-specific `NOT_APPLICABLE`, искусственный ноль, единица или штраф в трех class aggregates запрещены. Добавление четвертой структурной координаты требует нового bench protocol major.

Equivalence band каждой aggregate coordinate задается в ее физической единице:

```text
epsilon_notch_db_q
epsilon_burst_ms_q
epsilon_combined_failure_rate_q
```

Ordinal ladder index, номер строки channel grid и candidate-native score не могут быть единицей `epsilon_k`.

Каждый `epsilon_k` строится по той же формуле, что `epsilon_j` раздела 26:

```text
epsilon_k = max(q_k, delta_k, 2 * u95_k)
```

`u95_k` измеряется повторами вычисления самого class aggregate, а не повторами отдельной ячейки, потому что повторяемость порядковой статистики отличается от повторяемости per-cell измерения. Механизм исполним и ограничен по бюджету, потому что локальная матрица G3 детерминирована при фиксированных seeds: единственным источником изменчивости являются стохастические компоненты ячеек, то есть noise, dither и рандомизированные placements. `structural_metric_manifest.json` фиксирует `structural_replicate_seed_sets` c числом наборов не меньше 5; для каждого набора пересчитываются только стохастические ячейки, детерминированные ячейки вычисляются один раз и дают нулевой вклад в разброс. Если все ячейки класса детерминированы, `u95_k = 0` легитимно. Полный повтор всей сетки десятки раз НЕ требуется; стоимость равна числу стохастических ячеек, умноженному на число replicate-наборов, и входит в `max_local_channel_jobs` отдельной строкой бюджета. `u95_k` является одним общим значением координаты и берется как наибольшая соответствующая граница среди всех обязательных кандидатов; выбор отдельного значения для фаворита запрещен. `delta_k` имеет физическое обоснование и единицу своей координаты. После открытия selection holdout менять `epsilon_k` запрещено.

Conditional copy-failure matrices обязательны для `D0-T2`, `D0-T3`, `D0-F3` и любого другого многокопийного кандидата, но являются diversity diagnostics и hard-gate evidence раздела 7. Они не входят напрямую в межкандидатный Pareto-vector, потому что у `D0-B1` нет пары копий. Их итоговое влияние измеряется общими assembled-form aggregates.

Если первый unsafe step отдельной ladder не достигнут, она получает lower-bound status `STRUCTURAL_RIGHT_CENSORED`. Development расширяет ее до preregistered physical или safety ceiling. Цензурирование распространяется по иерархии рекурсивно: если within_stratum_rule выбирает censored ladder-значение либо censored значение способно изменить внутристратный ранг, значение stratum является lower bound. Для координаты `COMBINED_CLASS_FAILURE_RATE_Q` цензурирование не возникает, потому что каждая ячейка ее сетки дает измеренное решение.

При вычислении межстратного квантиля каждое censored значение входит в отсортированный список своим lower bound. Позиционная проверка только выбранной ранговой позиции НЕДОСТАТОЧНА и запрещена: censored элемент, стоящий ниже ранговой границы, может в действительности превышать выбранное значение и сдвинуть истинный квантиль вверх, даже если сама ранговая позиция пришлась на measured элемент. Поэтому статус агрегата определяется значением, а не позицией:

```text
aggregate_value  = взвешенный nearest-rank по списку с подставленными
                   lower bounds; всегда является валидной нижней границей
                   истинного квантиля

aggregate_status = MEASURED, если lower bound каждого censored элемента
                   строго больше aggregate_value;
                   иначе LOWER_BOUND
```

Это правило не зависит от tie-break: при равенстве censored lower bound и aggregate_value статус равен `LOWER_BOUND`, поэтому `stratum_id` не может влиять на censor status и не становится скрытой координатой ранжирования.

Каждая структурная координата публикуется как идентифицированный интервал:

```text
aggregate_lower_bound
aggregate_upper_bound      # равен lower bound при MEASURED,
                           # UNBOUNDED_TO_CEILING при LOWER_BOUND
aggregate_status
```

Epsilon-dominance раздела 26 применяется к интервалам, а не к скалярам. Для координаты MAXIMIZE кандидат `a` доказанно лучше `b` только при `a_lower > b_upper + epsilon_k`; кандидат `a` считается не хуже `b`, если не доказано обратное, то есть если НЕ выполняется `b_lower > a_upper + epsilon_k`. При `upper = UNBOUNDED_TO_CEILING` превосходство над этим кандидатом по данной координате недоказуемо. Два lower bound не сравниваются как точные значения: `a >= 10` и `b >= 9` не доказывают превосходства `a`. Если из-за неидентифицированных интервалов ни одна пара не доказуема, координата никого не исключает; это менее мощно, но корректно.

Если на выбранном квантиле агрегаты всех сравниваемых кандидатов являются lower bounds на одной общей границе ceiling, координата non-discriminating по построению. Development обязан обнаружить это заранее: если на открытых development results хотя бы два кандидата имеют `LOWER_BOUND` aggregate на общей границе, сетка расширяется по severity до preregistration; если расширение упирается в preregistered physical или safety ceiling, координата объявляется `NON_DISCRIMINATING_BY_CEILING` в design manifest до holdout, а не обнаруживается такой постфактум. Доля censored ladder публикуется по кандидату, классу и stratum.

Если structural epsilon-Pareto step не исключает ни одного кандидата, результат структурного этапа равен `STRUCTURAL_NONDISCRIMINATING`. Это допустимый и публикуемый исход, после которого работает последовательный ranking. Он не дает права менять aggregates, epsilon или grid.

Development обязан построить `development_decision_path.json`: применить замороженный ranking к открытым development results, показать все три aggregates, pairwise differences, dominance matrix, set после structural group и каждого последующего шага. Это диагностирует фактически решающую метрику, но не разрешает выбирать порядок по желаемому победителю. Если ranking order меняется после этой проверки, все development results пересчитываются, а preregistration еще не может быть опубликована.

Structural aggregates G3 являются результатом синтетической и локальной channel matrix. Они не доказывают тот же порядок кандидатов после YouTube и не могут подменять G4.

Development G3 выполняется на training и cumulative exposed corpus. После preregistration selection G3 использует только sealed channel cells и seeds. Любой selection result запрещено использовать для настройки параметров.

---

## 18. Правила исключения кандидата

Все четыре обязательных кандидата должны быть полностью построены и пройти G0 и полный G1 feasibility prepass. Только G1 может исключить объективно несинтезируемого кандидата до G2. Все feasible candidates проходят development G2. Budget планируется так, как будто все четыре окажутся feasible и дойдут до G4.

Кандидат можно снять с дорогих G3-G7 только по одной из причин:

1. `SYNTHESIS_INFEASIBLE`;
2. нарушение hard gate на training corpus;
3. формальное доказательство доминирования, заранее разрешенное preregistration.

Формальное доминирование допустимо только если другой кандидат не хуже одновременно по:

- energy и peak feasibility;
- common clean failure reserve;
- каждому классу burst;
- каждому классу notch;
- combined damage;
- false acceptance;
- scanner resource;
- bandwidth reservation;
- suite exclusion;
- всем timing и role cases.

Одной таблицы `W1/W2`, одной оценки crest factor или эмпирического среднего недостаточно.

`D0-T3` нельзя исключить только потому, что `D0-F3` имеет полносекундное окно. `D0-F3` нельзя исключить только потому, что энергия делится между тремя копиями. `D0-B1` нельзя исключить только потому, что у него нет diversity. Все гипотезы проверяются по своим уникальным классам повреждений.

На практике formal dominance почти наверняка потребует значительной части G3. Это правило является консервативной возможностью, а не основанием уменьшать budget. Empirical dominance на training corpus без доказательства по всем обязательным классам не разрешает снять кандидата с selection holdout.

После preregistration правило исключения не меняется. Selection holdout может исключить кандидата только по заранее определенному hard gate.

---

## 19. G4: реальный YouTube и дрейф платформы

YouTube всегда перекодирует загруженные видео. Поэтому сравнение кандидатов, загруженных в разные месяцы без контроля, смешивает качество топологии с изменением платформы.

### 19.1. Сравнительный временной блок

Survivor set известен до experiment preregistration. Здесь `n` равно размеру именно этого preregistered set и не уменьшается после открытия selection holdout, даже если кандидат уже нарушил более ранний selection gate. Все preregistered candidates остаются в сравнительных blocks, их результаты публикуются, но нарушивший gate кандидат не возвращается в eligibility. Preregistration разрешена только при `n >= 1`. Если development G1-G6 оставляет `n = 0`, selection experiment не регистрируется и закрытый holdout не открывается: development продолжается только в заранее разрешенных границах либо программа получает `PROGRAM_STOPPED`. Для `n >= 1` число валидных selection blocks выводится формулой:

```text
B_required(n) = max(6, 2 * n)
```

| `n` | Обязательные blocks |
| ---: | ---: |
| 1 | 6 |
| 2 | 6 |
| 3 | 6 |
| 4 | 8 |

Для `n >= 3` формула дает две полные Latin-order cycles. Для `n = 1` и `n = 2` число шесть также кратно `n`. Поэтому каждый кандидат одинаковое число раз занимает каждую ordinal position, а исключение кандидата в development не увеличивает число обязательных blocks. Для дополнительных кандидатов применяется та же формула без верхнего исключения. `youtube_block_count.json` фиксирует точный результат до selection holdout.

До добавления optional candidate должны выполняться `n <= max_candidate_count` и `B_required(n) <= max_youtube_block_dates`. Оба предела фиксируются согласованно в program manifest и experiment budget и не увеличиваются после candidate results. Поскольку blocks выполняются на разных UTC-датах, `max_youtube_block_dates` не может превышать preregistered calendar window.

Из `selection_run_order_seed` сначала получается одна unbiased permutation `P` survivor IDs. Порядок кандидатов в block `b` равен `rotate_left(P, b mod n)`. Поэтому каждый кандидат занимает каждую ordinal position ровно `B_required(n) / n` раз. Порядок UTC-дат полных cycles может дополнительно переставляться тем же замороженным PRNG, но внутренняя cyclic balance не меняется. Golden run-order vectors обязательны для `n = 1..4` и для максимального разрешенного числа дополнительных кандидатов.

Каждый валидный block содержит:

1. один paired comparison reel со всеми кандидатами;
2. по одному standalone qualification reel каждого кандидата;
3. одинаковый qualification subset;
4. platform controls по разделу 19.4;
5. порядок uploads и сегментов из `run_order.json`.

Ranking использует standalone reels. Paired reel измеряет context и дает дополнительную внутриблочную диагностику.

Standalone source videos одного block имеют одинаковые duration, container policy и побитово одинаковый video elementary stream. Единственным candidate-dependent media payload является аудиодорожка. Paired reel использует тот же frozen video generator, frame content и encoder profile. Все video-layer hashes публикуются до upload.

Все uploads одного блока начинаются внутри `upload_span_limit_hours`, заданного до holdout. Блоки выполняются на разных UTC-датах. Вся selection YouTube program обязана завершиться внутри preregistered calendar window, которое не превышает 28 дней после первого upload.

Если block не содержит stable output каждого survivor, он недействителен целиком. Нельзя оставить удачный результат одного кандидата и повторить только неудачный результат другого.

### 19.2. Paired comparison reel

Paired reel содержит полный qualification segment каждого кандидата. Сегменты не смешиваются внутри логической записи. Между ними используется одинаковый fixed PCM guard.

До preregistration pilot corpus выполняет carryover matrix: каждый candidate segment проверяется после каждого возможного predecessor и в standalone encode. Guard увеличивается только в development. После preregistration он неизменяем.

`paired_standalone_delta_limit_db_q` фиксируется заранее. Для каждого block вычисляется:

```text
paired_standalone_delta_db_q =
    abs(ten_log10_fixed_q(paired_reserve_ratio / standalone_reserve_ratio))
```

Превышение получает `CONTEXT_DEPENDENT` и исключает paired result из любых ranking calculations. Если хотя бы один reserve right-censored и доступный interval не доказывает, что delta находится внутри limit, результат равен `CONTEXT_UNRESOLVED`. Standalone result остается авторитетным для selection, если его собственные controls валидны.

`CONTEXT_DEPENDENT` и `CONTEXT_UNRESOLVED` не являются пустыми диагностическими метками. До preregistration для каждого возможного winner публикуется immutable `context_dependency_resolution_plan.json`. Если provisional winner получил хотя бы один такой status, G7 дополнительно выполняет этот plan на full-message reels с фактическими predecessor, guard, preamble и boundary contexts. Кандидат не может получить `CONFIRMATION_PASSED`, пока каждый implicated context не пройдет common safety reserve и собственные controls. Любой обязательный отказ или повторно неразрешенный interval дает `FULL_VALIDATION_FAILED`.

Если standalone result отсутствует, не декодируется, имеет invalid controls либо не достигает `STABLE_READY`, весь block получает `PLATFORM_BLOCK_INVALID`. Context status применяется только к paired-to-standalone паре с валидными controls.

Порядок paired segments меняется между blocks по сбалансированной схеме. Это контролирует локальный codec history, но не объявляется доказательством отсутствия неизвестных file-level эвристик.

### 19.3. Готовность output вместо фиксированного ожидания

Первый доступный output не считается автоматически окончательным. `youtube_output_readiness_manifest.json` фиксирует:

```text
required_output_profile_set
poll_schedule_hours
output_stability_interval_hours
processing_timeout_hours
stable_observation_count
profile_equivalence_rule
```

Output становится `STABLE_READY`, только если требуемые codec, container, channel count и sample rate доступны и их media fingerprint не изменился в `stable_observation_count` последовательных проверках с интервалом не меньше `output_stability_interval_hours`.

Processing timeout является отдельным параметром и не смешивается с upload span. Он выбирается в development по pilot uploads с preregistered safety factor. Значение 72 часа не считается универсальным свойством YouTube.

Если required profile не достиг stable readiness до timeout, весь block получает `PLATFORM_BLOCK_INVALID`. Более позднее появление профиля после закрытия block регистрируется как platform observation, но не добавляется задним числом к selection data.

### 19.4. Platform control

`PLATFORM_CONTROL-1` фиксируется до experiment preregistration и содержит:

- калибровочный multisine;
- стационарный участок;
- переходный участок;
- фиксированный D0-like probe, не являющийся валидной D0 grammar;
- участки цифровой тишины для измерения добавленного шума;
- time reference для оценки сдвига и drift.

Контроль не участвует в выборе кандидата. Он обнаруживает изменение тракта.

До preregistration контроль обязан пройти clean negative test каждого survivor и не создавать D0 record, boundary pair или beacon.

В каждом selection и confirmation block все pre, mid и post control segments повторно проходят тот же negative test после YouTube. Физическая валидность platform control и candidate-specific false acceptance являются разными решениями. Если объективная calibration function либо общая platform metric контроля невалидна, весь block недействителен. Если transport control валиден, но decoder одного кандидата принимает probe как D0 artifact, только этот кандидат получает hard false-acceptance failure в данном block. Он не может аннулировать сопоставимые результаты остальных кандидатов.

Для каждой копии контроля измеряются:

- gain;
- time shift;
- sample-rate drift;
- spectral transfer vector;
- noise floor;
- transient smear;
- control margin;
- output codec, itag и sample rate;
- sample peak и true peak.

### 19.5. Регистрация и фиксация среды YouTube

Следующие hard conditions являются постоянными внутри одного эксперимента:

```text
account_id_pseudonym
account_class
privacy_state
client_upload_region
source_container_profile
video_resolution_and_frame_rate
video_layer_hash_rule
required_output_profile_set
profile_equivalence_rule
```

Изменение любого hard field между blocks дает `PLATFORM_CONTEXT_CHANGED`. Текущая попытка останавливается, если новый block нельзя повторить в исходном context внутри budget. Само логирование изменения не делает результаты сопоставимыми.

Следующие tool fields могут измениться внешне:

```text
uploader_name_and_version
downloader_name_and_version
extractor_name_and_version
```

До preregistration `platform_context_compatibility_manifest.json` задает binary compatibility tests. Обновление uploader допускается как `SOFT_CONTEXT_COMPATIBLE` только при передаче побитово того же preregistered source file. Обновление downloader или extractor допускается только если old и new tool на одном downloaded-file hash дают идентичный extracted canonical PCM либо заранее разрешенное побитовое преобразование с golden vectors. Непройденный или отсутствующий compatibility test превращает soft change в `PLATFORM_CONTEXT_CHANGED`.

Для каждого upload/download сохраняются:

```text
block_id
upload_started_utc
upload_completed_utc
required_profile_first_seen_utc
output_stable_utc
download_started_utc
download_completed_utc
account_class
privacy_state
client_upload_region
uploader_version
uploader_name
downloader_name
downloader_version
source_video_sha256
source_audio_sha256
youtube_video_id
public_watch_url
output_itag
output_container
output_audio_codec
output_sample_rate
output_channel_count
downloaded_file_sha256
extracted_pcm_sha256
extractor_name
extractor_version
```

`public_watch_url` содержит только обычный URL страницы ролика. Временный подписанный media URL не сохраняется. Cookies, access tokens и другие секреты не публикуются.

### 19.6. Контроль дрейфа

До selection holdout задаются control limits для каждой метрики `PLATFORM_CONTROL-1`.

Блок получает `PLATFORM_BLOCK_INVALID`, если:

- любой control segment не выполняет свою calibration function;
- control metric выходит за hard limit;
- pre, mid и post controls показывают внутриблочный drift выше limit;
- платформа выдает несопоставимый output profile;
- output не достигает `STABLE_READY`;
- изменился hard platform context либо soft change не прошел compatibility test;
- отсутствует хотя бы один candidate result;
- нарушен preregistered порядок.

Candidate-specific принятие валидного control probe как D0 artifact не является причиной `PLATFORM_BLOCK_INVALID`. Оно записывается как ложное решение данного кандидата и нарушает его hard gate. Это разделение запрещает неустойчивому кандидату использовать собственный decoder failure как право вето на весь сравнительный block.

Для постепенного дрейфа ведется preregistered EWMA или эквивалентная контрольная карта. Ее коэффициенты и границы фиксируются до holdout.

Недействительный блок не дает положительного или отрицательного результата ни одному кандидату. Он может быть повторен только в пределах общего budget.

Если невозможно получить preregistered число валидных блоков, итог равен `PLATFORM_UNSTABLE`, а D0 не замораживается.

### 19.7. Ranking внутри блоков

Сравниваются только standalone результаты кандидатов, присутствующих в одном валидном block. Внутриблочная величина равна минимуму `common_failure_reserve_ratio` по обязательным forms и cells. Итоговое YouTube-значение кандидата равно минимуму этих внутриблочных величин по всем валидным selection blocks, то есть worst-of-worst. Соответствующие dB_q публикуются для чтения. Paired results и native scores являются диагностическими.

Нельзя напрямую сравнивать абсолютный score кандидата января с абсолютным score другого кандидата марта.

Победа требует прохождения hard gates во всех валидных блоках. Средний высокий score не компенсирует один обязательный отказ.

### 19.8. Финальная проверка победителя

До experiment preregistration для каждого возможного survivor создается отдельный immutable full-winner plan. `full_winner_reel_plan_manifest.json` связывает candidate ID, candidate hash и plan hash. Каждый план перечисляет точный superset artifact hashes, deterministic focus-selection rules, порядок, guard, controls, maximum reel duration и worst-case expected upload count. Одна форма не означает один YouTube upload.

После selection и до открытия confirmation holdout публикуется `full_winner_reel_plan_resolved.json`, который только ссылается на заранее зарегистрированный plan hash предварительного победителя. Менять segmentation, guard, artifact subset или upload count после знания selection results запрещено.

План охватывает:

- все 72 assembled forms;
- все `72 * copy_count` diagnostic subforms;
- `BOOT_RECORD`;
- `CALL`;
- `ANSWER`;
- `SUITE_ANSWER`;
- Level 2 selector;
- поврежденные границы;
- relevant codec-frame offsets;
- повторный lossy transcode;
- minimum supported bitrate;
- boundary cells и первый отказ за ними.

Заранее фиксированное число lowest-reserve `D0_OBJECT6`, каждый marker и `BOOT_SYNC` дополнительно получают single-form standalone upload, чтобы длинный reel не был единственным эксплуатационным доказательством. Lowest-reserve формы выбираются только по preregistered metric, count и tie-break из selection results. Все возможные source hashes уже перечислены в plan superset.

Если победитель не проходит confirmation full validation или обязательную in-scope часть external challenge, runner-up не становится победителем автоматически. Текущий experiment получает `FULL_VALIDATION_FAILED`; уже открытые объекты раскрываются и добавляются в lineage, а неоткрытые обрабатываются по разделу 28. Следующая попытка возможна только как новый experiment index в пределах program limit.

---

## 20. G5: пространство будущих suite

Все suite-профили строятся, настраиваются и получают окончательные hashes в development до experiment preregistration. Selection holdout не может использоваться для поиска carrier map, изменения threshold или замены неудачного профиля.

Для каждого survivor фиксируются:

1. кандидат первого suite;
2. резервный suite profile A;
3. резервный suite profile B.

Все три должны быть физически различны между собой и находиться вне `D0_EXCLUSION_ENVELOPE` данного кандидата.

Проверяются:

- D0-to-suite cross-correlation;
- suite-to-D0 cross-correlation;
- false D0 grammar внутри suite streams;
- общий frequency reservation;
- guard intervals;
- объединенный basis rank;
- condition number;
- margin при channel transforms;
- возможность детерминированного carrier map;
- false peak rate scanner.

В selection G5 все три профиля каждого survivor проходят один и тот же sealed cross-confusion corpus. Проверять только первый suite, а два резервных считать существующими по расчету запрещено. В confirmation G7 те же три immutable-профиля победителя проходят независимый confirmation subset.

Профиль получает `SUITE_PROFILE_PASS` только если одновременно:

- suite stream создает ноль ложных D0 grammar и ноль ложных `EXACT`;
- D0 stream создает ноль ложных suite symbols;
- minimum cross-confusion `common_failure_reserve_ratio` не ниже preregistered safety reserve во всех REQUIRED cells;
- basis rank, condition number, resource и reservation limits соблюдены;
- на REQUIRED cells все отказы обозначены как erasure, conflict или partial, без единого ложного логического принятия; на cells тяжелее REQUIRED действуют те же family и global пределы `false_logical_acceptance`, что в разделах 17 и 25.

Два из трех прошедших профилей недостаточны. Все три обязательны.

Каждый профиль получает отдельный `physical_profile_hash256`. `suite_reserve_manifest.json` перечисляет все tables, окна, carrier maps, amplitudes, phases, estimator constants, thresholds и dependency hashes. Любая замена хотя бы одного байта после preregistration является сменой профиля и дает `EXPERIMENT_INVALIDATED`.

Если уже существует опубликованная D0 family, обязательны двунаправленные negative tests:

- новый D0 против всех прежних suite-профилей;
- прежний D0 против всех трех новых suite-профилей;
- новый scanner против прежних canonical и damaged artifacts;
- прежний reference scanner против нового corpus там, где формат входа совместим.

Совместимость не определяется после просмотра результата. `cross_family_compatibility_manifest.json` до preregistration сравнивает как минимум sample rate, channel count, token samples, logical form count, namespace mapping, canonical PCM normalization и scanner input schema. Только полное совпадение preregistered compatibility key разрешает двунаправленный executable test. Иначе case получает явное `FORMAT_INCOMPATIBLE_NOT_APPLICABLE` и текстовое объяснение, но не считается пройденным тестом.

До запуска cross-family decoder две schema implementations независимо воспроизводят compatibility key и case disposition. Если preregistered key либо label оказался вычислен неверно, статус равен `CROSS_FAMILY_SCHEMA_INVALID` и текущий experiment аннулируется. Такая ошибка package design не является физическим отказом кандидата и не может использоваться в ranking.

Отсутствие прежней family фиксируется явным значением `cross_family_scope = NONE`, а не пропуском поля.

Кандидат, который надежен сам по себе, но занимает пространство так, что нельзя построить три suite-профиля, не может стать корневым D0.

`D0_EXCLUSION_ENVELOPE` должен содержать численные границы и sample hashes, а не только рисунок полосы.

---

## 21. G6: scanner conformance и ресурсная честность

### 21.1. Полный первый проход

Matched filtering выполняется потоково по всей заявленной длительности файла. Глобальное правило "первые N peaks выигрывают" запрещено.

Non-maximum suppression применяется отдельно по фиксированным time tiles и marker roles. Размер tile и локальный peak cap фиксируются до holdout.

### 21.2. Справедливое распределение бюджета

Stage 2 hypotheses обрабатываются round-robin между time tiles. Каждый tile получает минимальный неперераспределяемый quota.

Отдельные неперераспределяемые бюджеты имеют:

- standalone beacon grammar;
- `BOOT_RECORD`;
- full-message boundaries;
- opaque pairing;
- cross-family hypotheses.

Opaque pairing и слабые marker peaks не могут расходовать beacon budget.

Более ранний по времени слабый peak не может навсегда вытеснить более поздний exact record.

`scanner_resource_manifest.json` обязан задавать целыми числами:

```text
max_input_duration_samples
time_tile_samples
stage1_peak_cap_per_tile_per_role
stage1_peak_cap_total
stage2_hypothesis_cap_per_tile
stage2_hypothesis_cap_total
standalone_beacon_quota
boot_record_quota
full_boundary_quota
opaque_pair_quota
cross_family_quota
max_supported_boundary_separation_samples
max_boundary_timing_tolerance_samples
max_pairing_distance_samples
max_wall_time_ns
max_cpu_time_ns
max_peak_memory_bytes
max_cancellation_latency_ns
```

Ни одно поле не может иметь значение `unlimited`, `auto` или зависеть от числа найденных peaks без отдельного hard cap. Сумма неперераспределяемых quota не может превышать общий stage budget.

`max_pairing_distance_samples` выводится, а не выбирается по удобству scanner:

```text
max_pairing_distance_samples >=
    max_supported_boundary_separation_samples +
    2 * max_boundary_timing_tolerance_samples

max_pairing_distance_samples <= max_input_duration_samples
```

Точное выбранное значение должно укладываться в hypothesis, memory и wall-time budgets. Conformance corpus содержит валидные boundary pairs на расстояниях `lower_bound - 1`, `lower_bound`, `max_pairing_distance_samples` и `max_pairing_distance_samples + 1`. Первые три обрабатываются по grammar, последний не образует pair. Если нижняя граница не помещается в resource budget, support duration уменьшается до preregistration либо кандидат scanner получает `RESOURCE_SCHEMA_INFEASIBLE`.

### 21.3. Evidence ordering

Нормативный порядок:

```text
MARKER_PEAK
PARTIAL_PATTERN
D0_RECORD_VALID
BOUNDARY_PAIR_VALID
FULL_GRAMMAR_VALID
FULL_EXACT
```

Повышение evidence rank монотонно. Кандидат более низкого rank не заменяет более высокий.

### 21.4. Ограничение гарантий

Если злоумышленник накладывает более сильный сигнал на тот же time-frequency cell, физически гарантировать обнаружение слабого легитимного сигнала невозможно.

В таком случае декодер обязан вернуть `RESOURCE_LIMIT`, `AMBIGUOUS` или `ERASURE` согласно измерению. Он не имеет права объявлять ложный `EXACT` или утверждать, что дорожка не содержит других артефактов.

### 21.5. Adversarial corpus

Размер spam-корпуса задается не словами "много" или "тысячи", а `scanner_spam_manifest.json` со следующими точными массивами и пределами:

```text
spam_peak_rates_per_minute[]
peak_amplitude_offsets_from_threshold_db_q[]
file_durations_samples[]
total_injected_peak_counts[]
marker_role_distributions[]
time_cluster_widths_samples[]
valid_artifact_positions_samples[]
random_seeds[]
expected_resource_status
```

Все элементы этих массивов являются конечными целыми или fixed-point значениями и фиксируются до holdout. Корпус обязан покрывать как минимум:

- rates 60, 600 и 6000 injected peaks на минуту в файле длительностью не меньше 60 секунд;
- amplitude offsets `-6`, `-1`, `-0.25`, `+0.25`, `+1`, `+6` dB относительно detection threshold, представленные нормативным fixed-point scale;
- один local-tile case с числом peaks не меньше `2 * stage1_peak_cap_per_tile_per_role`;
- один whole-file case с числом peaks не меньше `2 * stage1_peak_cap_total`;
- peaks ниже threshold на каждом зарегистрированном amplitude offset;
- peaks чуть выше detection threshold на каждом положительном offset;
- плотный D0-like multisine;
- валидный record в начале, середине и конце spam-файла;
- два и более сообщения;
- ложные BOOT pairs;
- unknown suite opaque pairs;
- поврежденный reply с целым внутренним ANSWER;
- marker-only overlap;
- cancellation на каждой стадии;
- исчерпание каждого отдельного budget;
- файл максимальной поддерживаемой длительности;
- одна область с физически неразделимым adversarial overlap.

Для каждого случая заранее фиксируются ожидаемые artifacts, statuses, неполнота отчета, предел memory, wall time и cancellation latency.

Selection corpus использует закрытые seeds и placements, но только значения из заранее опубликованных numeric grids. Добавлять более удобную плотность после просмотра результата запрещено. Отдельный clean-negative файл `PLATFORM_CONTROL-1` включается в каждый scanner batch и обязан оставаться отрицательным для всех survivor.

---

## 22. G7: полная проверка победителя

G7 начинается только после публикации `provisional_decision.json` и открытия отдельного `CONFIRMATION_HOLDOUT`. Проверяется только точный `d0_candidate_hash256` предварительного победителя. Runner-up и новый кандидат не получают доступа к этому holdout.

Предварительный победитель без изменения хотя бы одного параметра проходит:

- воспроизведение G0-G1 по опубликованным vectors как проверку идентичности реализации;
- confirmation subsets G2-G6;
- полный закрытый confirmation holdout;
- полный winner-only YouTube corpus из `full_winner_reel_plan.json`;
- все 72 формы;
- все diagnostic subforms;
- все обязательные combined damages;
- все reserve suite profiles;
- cross-family confusion, если существуют ранее опубликованные families;
- scanner conformance;
- boundary grid с первым измеренным отказом;
- `context_dependency_resolution_plan.json`, если selection зарегистрировал хотя бы один `CONTEXT_DEPENDENT` или `CONTEXT_UNRESOLVED`.

Все перечисленные core components являются обязательными. Значение `SKIPPED`, перенос результата selection, выборочная проверка только удобных forms или замена полного winner-only YouTube plan сокращенным reel запрещены. `NOT_APPLICABLE` разрешен только для component, чей scope был явно и обоснованно равен `NONE` уже в design manifest, например отсутствие прежней protocol family для cross-family gate. Пропуск любого применимого component означает `FULL_VALIDATION_FAILED`.

G7 использует новую run-order seed ветвь, выведенную из confirmation commitment, и не переиспользует selection placements. Повторная настройка estimator, common metric, equivalence bands, suite profiles, YouTube readiness rules или scanner limits запрещена.

Успех этой части фиксируется как `CONFIRMATION_CORE_PASSED`, но еще не дает `CONFIRMATION_PASSED`. Затем открывается committed external challenge и выполняется его замороженный run order.

Каждый валидный `IN_SCOPE_SURPRISE` case обязан выполнить те же logical, false-acceptance, common-reserve и resource gates, которые соответствуют его declared support coordinates. Любой обязательный отказ дает `FULL_VALIDATION_FAILED`. `OUT_OF_SCOPE_EXPLORATORY` и `INVALIDATED_SCHEMA` выполняются и публикуются полностью в пределах своего diagnostic budget, но их отказ не меняет winner и не расширяет support envelope.

Только успех core confirmation и всех валидных `IN_SCOPE_SURPRISE` cases при соблюдении minimum и class quotas дает `CONFIRMATION_PASSED`, но еще не `FREEZE_READY`. Любой core отказ также дает `FULL_VALIDATION_FAILED`. Runner-up не подставляется автоматически, потому что confirmation holdout уже раскрыт. Следующая попытка возможна только как новый experiment index по разделу 28.

---

## 23. G8: независимое воспроизведение

Независимая реализация может читать protocol, schemas, published constants и test vectors, но не может импортировать, вызывать, переводить построчно или генерироваться из DSP-кода reference implementation. Общие внешние codec binaries разрешены только если они перечислены как внешние зависимости обеих реализаций и не содержат project-specific DSP.

Перед запуском публикуется `declaration_of_independence.json` с авторами, repositories, dependency hashes, способом обмена test vectors и перечнем общего внешнего инструментария.

Независимая реализация получает frozen input artifacts, protocol, schemas и public constants, но до собственного commitment не получает reference per-cell outputs, equivalence sets либо полные reference metric tables. Она публикует `independent_results_commitment.json` с hashes своих canonical outputs, decisions, metric tables и ranking. Только затем открываются детальные reference result tables и выполняется сравнение.

До открытия reference result tables допускается не более `max_independent_pre_reference_corrections` исправлений, причем это число фиксируется до selection и не может превышать 1. Исправление разрешено только если independent team сама обнаружила дефект по protocol, public vectors или собственным consistency tests. Original commitment не удаляется. До раскрытия reference tables публикуются signed `independent_correction_record.json`, полный code diff hash, причина, затронутые outputs, corrected commitment и полная повторная генерация всех independent results. Частичное сохранение удобных старых outputs запрещено.

Если correction меняет independent winner, final equivalence set либо hard-gate outcome, устанавливается `INDEPENDENT_CORRECTION_MATERIAL`. G8 остается заблокированным до согласия третьей независимой реализации либо отдельного формального adjudication package, заранее предусмотренного budget. После открытия reference tables любые исправления independent implementation запрещены внутри текущего experiment index; несовпадение дает `INDEPENDENT_REPRODUCTION_FAILED`. Исчерпание correction budget дает тот же статус, а не право повысить предел.

Поскольку `provisional_decision.json` публикуется до confirmation, автор независимой реализации может знать ID предварительного победителя. G8 поэтому не называется winner-blind проверкой. Его защита состоит в независимом коде, предварительном commitment собственных детальных outputs и запрете доступа к reference per-cell evidence до этого commitment. Если требуется дополнительно скрыть winner ID, такая изоляция описывается отдельным operational manifest, но не считается гарантией этого protocol.

Она обязана воспроизвести:

- JCS и hashes;
- все canonical sample hashes;
- energy и peak values;
- window vectors;
- Gram matrices в заданной tolerance;
- все copy decisions;
- aggregate decisions;
- channel transformations с нормативными seeds;
- external challenge decisions на уже раскрытом immutable package;
- scanner JSON для conformance corpus;
- итоговый ranking;
- `D0_CHANNEL_SUPPORT_ENVELOPE`;
- `D0_EXCLUSION_ENVELOPE`.

`integer_semantics.json` нормативно задает ширину каждого аккумулятора, signedness, порядок операций, запрет wrap и saturation в exact operations, rounding, tie rule, exact-ratio comparison, `ten_log10_fixed_q` и serialization. При этих правилах canonical PCM, JCS, hashes, CRC, BCH, RS, fixed-point windows, целочисленные energy/peak values и dB_q golden vectors обязаны совпасть побитово. Это проверка спецификации, а не требование одинакового компилятора.

Только результаты внешнего codec или платформенного тракта, которые по определению не являются каноническими функциями project code, сравниваются по заранее фиксированным tolerances и по одинаковым сохраненным downloaded artifacts. Независимая реализация не обязана получить побитово тот же AAC или Opus bitstream от другого encoder build.

Независимый транспортный наблюдатель отдельно формирует `transport_observer_report.json`. Он проверяет соответствие source hashes, video IDs, UTC-времени, readiness observations, downloaded-file hashes, extraction commands и block validity. Наблюдатель не сообщает победителя анализатору до фиксации его результата.

Если две реализации дают разных победителей, статус равен `INDEPENDENT_REPRODUCTION_FAILED`.

Если development decision path и selection decision path впервые расходятся на разных metric classes, итоговая запись получает diagnostic `DECISION_PATH_DISTRIBUTION_SHIFT`. Это не аннулирует заранее замороженный алгоритм и не разрешает tuning, но обязательно раскрывается как evidence возможного distribution shift.

---

## 24. Метрики

Для каждой формы, копии, channel cell и реализации сохраняются:

```text
true_class
decoded_class
copy_status
aggregate_status
score_true
score_best_wrong
accept_threshold
native_margin_db
common_failure_reserve_num
common_failure_reserve_den
common_failure_reserve_db_q
common_reserve_censor_status
timing_error_samples
gain_error_q
sample_peak_q
true_peak_q
energy_integer
crest_factor_q
false_peak_count
pre_echo_energy_ratio_db_q
post_echo_energy_ratio_db_q
smear_duration_samples
paired_standalone_delta_db_q
output_readiness_status
platform_context_hash256
platform_context_compatibility_status
structural_class_aggregate_lower_bound[3]
structural_class_aggregate_upper_bound[3]
structural_class_aggregate_status[3]
structural_worst_case_values[3]
structural_stratum_values[]
structural_per_ladder_sorted_lists[]
structural_censored_ladder_fraction_by_stratum[]
fla_num_by_family_and_grid
fla_den_by_family_and_grid
fla_status_by_family_and_grid
structural_diagnostics[]
failure_support_overlap_num
failure_support_overlap_den
diversity_gate_status
external_challenge_scope
external_challenge_status
wall_time_ns
cpu_time_ns
peak_memory_bytes
```

Сводные метрики:

- confusion matrix;
- missed detection count;
- false acceptance count;
- false D0 record count;
- false `EXACT` count;
- copy erasure rate;
- joint erasure rate;
- conditional failure matrix;
- minimum common failure reserve;
- minimum native margin, только как внутренняя диагностика кандидата;
- lower percentile common reserve, только как дополнительная статистика;
- worst channel cell;
- first measured failure;
- maximum pre-echo ratio;
- maximum post-echo ratio;
- maximum transient smear;
- paired-to-standalone context delta;
- три structural class aggregates и structural epsilon-nondominated set;
- full per-ladder structural diagnostics;
- failure-support overlap и diversity gate outcome каждой пары копий;
- external in-scope pass count и exploratory failure map;
- platform invalid block count и причины;
- scanner peaks per minute;
- hypotheses per minute;
- cancellation latency;
- frequency reservation;
- suite reserve count.

`score_true`, `score_best_wrong`, `accept_threshold` и `native_margin_db` не сравниваются между кандидатами. Межкандидатными являются только явно общие физические метрики: exact `common_failure_reserve_ratio`, три structural class aggregates, error rates на общей сетке и resource values в одинаковой среде.

Среднее значение никогда не заменяет minimum common reserve или hard error count.

Confidence interval и статистическая модель задаются в preregistration. Для детерминированной конечной сетки главным результатом является полный подсчет, а не выборочная оценка.

---

## 25. Бинарные условия допуска

Кандидат допускается к ranking только если одновременно:

1. program manifest, experiment index и lineage chain валидны;
2. оба holdout commitments, external challenge commitment и их раздельное независимое хранение подтверждены до selection;
3. G0 пройден reference и independent math implementation;
4. все 72 формы и все обязательные diagnostic subforms допустимого кандидата синтезированы, а исключенные candidates имеют полный G1 evidence;
5. `FEASIBILITY_PREPASS`, derived `E_target`, common peak limits и optimizer budgets соблюдены;
6. common calibration cell и normative test vectors совпали;
7. `CLEAN_MATH_GATE` имеет ноль логических ошибок;
8. отрицательный clean corpus имеет ноль ложных records и `EXACT`;
9. каждый положительный case `REQUIRED_GRID` декодирован правильно, без `ERASURE`, `CONFLICT` либо неверной логической формы;
10. на `REQUIRED_GRID` и `STRUCTURAL_COMPARISON_GRID` любой отказ обозначен как erasure, conflict или partial, без единого ложного логического принятия; на `BOUNDARY_GRID` соблюдены family и global пределы `false_logical_acceptance` раздела 17 как hard gate; на `STRESS_GRID` те же доли опубликованы против собственного мягкого предела как характеристика безопасной деградации. Нулевое требование на тяжелых сетках неисполнимо по геометрии `D0_BCH(15,7,5)`: доля ложных исправлений bounded-distance декодера зависит от точного веса ошибки и по полному перебору составляет 39,56% при весах 3-4 и 11-12, 47,05% при 5-6 и 9-10, 48,72% при 7-8 и 100% при 13-15, поскольку слово из всех единиц является кодовым; dual-rail подпись перехватывает часть, но не все. Совокупная вероятность на данной сетке зависит от распределения весов ошибок канала и потому не является одной универсальной константой; нормативные векторы `bch_miscorrection_fraction_by_exact_error_weight` входят в G0;
11. minimum exact common failure reserve ratio не ниже preregistered safety reserve, а censoring обработан по разделу 9.3;
12. pre-echo, post-echo и smear не превышают preregistered limits;
13. получено требуемое число валидных standalone YouTube blocks, рассчитанное разделом 19.1;
14. каждый используемый output имеет `STABLE_READY`, а platform controls и context находятся внутри limits;
15. paired-to-standalone delta опубликован, а обязательный context-resolution plan зарегистрирован для любого `CONTEXT_DEPENDENT` или `CONTEXT_UNRESOLVED`;
16. selection YouTube qualification subset пройден без пропуска survivor;
17. все три immutable suite-профиля прошли sealed cross-confusion cases;
18. cross-family gate пройден либо явно имеет scope `NONE`;
19. scanner имеет ноль ложных `EXACT` и соблюдает все resource limits;
20. все три structural class aggregates полны для всех кандидатов, full diagnostics прошли conformance tests, а каждый многокопийный кандидат дополнительно имеет полную conditional failure matrix, достаточное число informative failures и прошел общий численный hard diversity gate раздела 7;
21. candidate не нарушил ни одного state transition, budget или stop rule.

Нарушение любого условия исключает кандидата.

`CONFIRMATION_PASSED`, прохождение всех `IN_SCOPE_SURPRISE` cases и согласие независимой реализации не являются условиями допуска к selection ranking, потому что происходят после выбора. Они являются отдельными обязательными условиями статуса `FREEZE_READY`.

---

## 26. Последовательный выбор с зонами практической эквивалентности

Точное равенство двух воспроизводимых вещественных измерений не используется как условие перехода к следующей метрике. Для каждой метрики `j` до holdout фиксируются независимо:

```text
q_j          = шаг канонической сериализации результата
delta_j      = минимально практически значимое различие
u95_j        = верхняя 95% граница repeatability uncertainty из development controls
epsilon_j    = max(q_j, delta_j, 2 * u95_j)
direction_j  = MAXIMIZE или MINIMIZE
```

`q_j` является точностью записи, а не зоной научной безразличности. `delta_j` имеет физическое обоснование и единицу измерения. `u95_j` является одним общим значением для метрики и берется как наибольшая соответствующая граница среди всех обязательных кандидатов и development repetitions, а не выбирается отдельно для фаворита. Для полностью детерминированной локальной метрики `u95_j` может быть нулем. После открытия selection holdout менять `epsilon_j` запрещено.

При `comparison_mode = SOLE_FEASIBLE` или `SOLE_SURVIVOR` последовательный выбор не выполняется. Единственный кандидат становится provisional winner только после прохождения всех selection hard gates. В отчете причина формулируется как "единственный допустимый кандидат", а не как измеренное превосходство.

При `comparison_mode = COMPARATIVE` первой применяется структурная epsilon-Pareto-группа.

Каждая structural coordinate представлена идентифицированным интервалом раздела 17. Для measured координаты интервал вырожден в точку. Правила сравнения:

```text
MAXIMIZE: a доказанно лучше b, если a_lower > b_upper + epsilon_k
MINIMIZE: a доказанно лучше b, если a_upper < b_lower - epsilon_k
a не хуже b, если НЕ доказано, что b лучше a
```

Кандидат `a` epsilon-dominates `b`, если `a` не хуже по каждой из трех structural class aggregate coordinates и доказанно лучше более чем на `epsilon_k` хотя бы по одной. При `upper = UNBOUNDED_TO_CEILING` соответствующее превосходство над кандидатом недоказуемо, и по этой координате его нельзя исключить. После structural step сохраняются все candidates, которые не epsilon-dominated ни одним другим кандидатом. Conditional copy-failure matrices и per-ladder diagnostics остаются обязательным hard evidence, но не подставляются в общий vector. Ни AWGN reserve, ни candidate-native score в structural group не входят.

Если set после structural step равен его input set, фиксируется `structural_step_status = STRUCTURAL_NONDISCRIMINATING`. Если он стал меньше, фиксируется `STRUCTURAL_FILTERED`. Structural-first order является заранее объявленной исследовательской политикой, а не выводом о том, что notch и burst универсально важнее фонового шума. Итоговый отчет любого сравнительного выбора содержит `selection_policy = SELECTED_UNDER_STRUCTURAL_FIRST_POLICY`.

После structural group применяется последовательная фильтрация:

```text
S_0 = structural epsilon-nondominated set

для j = 1..10:
    если |S_(j-1)| <= 1: остановиться
    если metric_j = NON_DISCRIMINATING_CENSORED:
        S_j = S_(j-1)
        продолжить
    b_j = лучшее значение metric_j среди S_(j-1)
    S_j = {c: within_best_equivalence_j(metric_j(c), b_j)}

если после metric_10 осталось несколько кандидатов:
    выбрать меньший UTF-8 byte string candidate_id
```

Для обычной fixed-point метрики `within_best_equivalence_j` означает разницу не больше `epsilon_j` в зарегистрированном направлении. Для exact reserve ratio `r_c` и лучшего ratio `r_b` сначала выбирается `r_b` точным cross multiplication, затем кандидат сохраняется при:

```text
ten_log10_fixed_q(r_c / r_b) >= -epsilon_j
```

Деление здесь является отношением двух рациональных чисел и реализуется exact cross products в unsigned 128-bit либо arbitrary-precision arithmetic. Floating-point, wrap и saturation не используются.

Если `r_b = 0`, все допущенные кандидаты на этом шаге имеют zero reserve и метрика получает `NON_DISCRIMINATING_BASELINE_FAILURE`. Если `r_b > 0`, кандидат с `r_c = 0` исключается без вызова logarithm. `ten_log10_fixed_q` вызывается только для двух положительных ratios.

Порядок последовательных общих метрик:

1. максимальный worst-of-worst standalone YouTube `common_failure_reserve_ratio` во всех валидных selection blocks;
2. максимальный худший `common_failure_reserve_ratio` в локальном `REQUIRED_GRID`;
3. максимальный minimum D0-to-suite cross-confusion reserve по всем трем профилям;
4. максимальное число дополнительных допустимых профилей сверх обязательных трех в фиксированном `SUITE_RESERVE_CANDIDATE_SET`;
5. минимальная ширина объединенного `D0_EXCLUSION_ENVELOPE`;
6. максимальный clean `common_failure_reserve_ratio`;
7. минимальный false-peak rate на общем scanner spam corpus;
8. минимальный scanner peak memory в одинаковой среде;
9. минимальный scanner wall time в одинаковой среде;
10. минимальная занятая размерность объединенного 48 000-sample basis.

Paired YouTube margin, candidate-native score и произвольная агрегированная utility в ranking не входят.

`equivalence_bands.json` содержит исходные pilot observations, расчет `u95_j`, инженерное обоснование `delta_j`, `q_j`, направление и test vectors.

`energy_partition_bias_analysis.json` до preregistration публикует аналитически ожидаемую разницу AWGN для одной копии, двух обязательных копий и quorum 2 из 3 при общем `E_target`. Здесь `Q(x)` является верхним хвостом стандартного нормального распределения, а `s` является полным single-copy-equivalent SNR до деления общей энергии между копиями.

Три альтернативные copy-error laws применяются одинаково к каждой физической копии:

```text
p_1(s) = Q(sqrt(s))
p_2(s) = Q(sqrt(2*s))
p_3(s) = min(1, 3*Q(sqrt(s)))
```

Для каждой law `p_m` aggregate failure при полном SNR `s` определяется без неоднозначной подстановки:

```text
F_B1,m(s) = p_m(s)

q_T2 = p_m(s / 2)
F_T2,m(s) = 1 - (1 - q_T2)^2

q_Q3 = p_m(s / 3)
F_Q3,m(s) = 3*q_Q3^2 - 2*q_Q3^3
```

`Q3` обозначает общую идеализированную aggregation law для `D0-T3` и `D0-F3`, а не утверждение об одинаковом реальном канале. Для target aggregate failure `10^-3` и `10^-6` анализ решает минимальный `s` для каждого кандидата и каждой law. Обязательные контрольные разности относительно `B1`, округленные до 0,01 dB:

| Copy-error law | Target | `T2 - B1`, dB | `Q3 - B1`, dB |
| --- | ---: | ---: | ---: |
| `p_1` | `10^-3` | 3,56 | 1,37 |
| `p_1` | `10^-6` | 3,26 | 1,47 |
| `p_2` | `10^-3` | 3,56 | 1,37 |
| `p_2` | `10^-6` | 3,26 | 1,47 |
| `p_3` | `10^-3` | 3,47 | 2,11 |
| `p_3` | `10^-6` | 3,24 | 1,85 |

Анализ обязан явно назвать предположения independent copy errors и идеализированного AWGN и рядом опубликовать empirical conditional failure matrix. Он не заменяет измерение и не входит в ranking, но показывает встроенную чувствительность sequential metrics 1, 2 и 6. Удалять неудобную модель после development запрещено.

Обязателен synthetic ranking corpus, который воспроизводит structural dominance, structural trade-off без dominance, `STRUCTURAL_NONDISCRIMINATING`, все шесть `decision_basis`, right-censored skip, censored элемент ниже ранговой границы при measured ранговой позиции, интервальную пару с недоказуемым превосходством из-за `UNBOUNDED_TO_CEILING`, пару кандидатов с противоположным знаком квантильного и worst-case сравнения, инвариантность агрегата к удвоению числа ячеек внутри одного stratum при неизменных ladder-результатах, family с `FLA_INSUFFICIENT_FAILURES` и достижение каждой sequential metric 1-10. "Достижение метрики" означает, что два кандидата входят в ее input set и после применения equivalence band хотя бы один из них исключается именно этой метрикой. Это доказывает, что поздние критерии реализованы и не являются мертвым кодом.

`development_decision_path.json` выполняет тот же алгоритм на фактических открытых development results, перечисляет set после каждого шага и явно показывает first deciding step. Он также публикует `predicted_energy_partition_gap_db_q` и проверяет, остановилась ли фильтрация на uniform-reserve metric 1, 2 или 6. Порядок, который на development обходит structural group из-за schema или missing coordinates, не может быть preregistered.

После selection `decision_basis` принимает ровно одно значение:

```text
SOLE_FEASIBLE
SOLE_SURVIVOR
STRUCTURAL_PRIORITY_SELECTION
DECIDED_BY_UNIFORM_RESERVE
SEQUENTIAL_OTHER_METRIC
FINAL_ID_TIEBREAK
```

`DECIDED_BY_UNIFORM_RESERVE` используется, если structural step никого не исключил и первый решающий sequential step равен 1, 2 либо 6. Если его наблюдаемый разрыв находится внутри заранее опубликованного диапазона idealized energy-partition analysis с учетом uncertainty, отчет дополнительно говорит `CONSISTENT_WITH_ENERGY_PARTITION_BIAS`; это не обесценивает измерение, но запрещает называть результат доказательством diversity. `STRUCTURAL_PRIORITY_SELECTION` используется, если structural step исключил хотя бы одного кандидата. Остальные значения следуют из названий и полного decision path.

Последний tie-break по `candidate_id` обеспечивает детерминизм, но не означает измеренного физического превосходства. Итоговый отчет обязан назвать всех кандидатов финального equivalence set.

---

## 27. Конечный автомат программы и эксперимента

Состояние не выводится из наличия отдельных файлов. Каждое изменение является append-only записью `state_transition_log.jsonl` с previous state, event, next state, artifact hashes, UTC timestamp и lineage entry. Пропуск обязательного состояния или возврат назад дает `PROTOCOL_CONFLICT`.

Имена вроде `RANDOMNESS_BEACON_TIMEOUT`, `DIVERSITY_THRESHOLD_UNCALIBRATED`, `INTEGER_WIDTH_INSUFFICIENT`, `CROSS_FAMILY_SCHEMA_INVALID` и `EXTERNAL_CHALLENGE_SCHEMA_INVALID` являются machine-readable reason codes, а не дополнительными состояниями. `state_transition_table.json` обязан для каждого reason code задать ровно один terminal transition либо development blocker. Неизвестный reason code дает `PROTOCOL_CONFLICT`.

### 27.1. Состояния

```text
PROGRAM_UNREGISTERED
PROGRAM_REGISTERED
DEVELOPMENT_ACTIVE
PROTOCOL_CONFLICT
DESIGN_COMMITTED
EXPERIMENT_PREREGISTERED
SELECTION_HOLDOUT_OPENED
WINNER_PROVISIONAL
CONFIRMATION_HOLDOUT_OPENED
CONFIRMATION_CORE_PASSED
EXTERNAL_CHALLENGE_OPENED
CONFIRMATION_PASSED
PLATFORM_UNSTABLE
NO_CANDIDATE
FULL_VALIDATION_FAILED
INDEPENDENT_REPRODUCTION_FAILED
EXPERIMENT_INVALIDATED
FREEZE_READY
FROZEN
PROGRAM_STOPPED
```

`PROTOCOL_CONFLICT`, `PLATFORM_UNSTABLE`, `NO_CANDIDATE`, `FULL_VALIDATION_FAILED`, `INDEPENDENT_REPRODUCTION_FAILED` и `EXPERIMENT_INVALIDATED` являются терминальными для текущего experiment index. Они не являются terminal для всей программы, пока остается разрешенный experiment index и исправление не нарушает root program rules. `FROZEN` не имеет исходящего перехода внутри этой protocol family.

### 27.2. Разрешенные переходы

| From | Event и обязательное доказательство | To |
| --- | --- | --- |
| `PROGRAM_UNREGISTERED` | опубликован program manifest и независимая timestamp attestation | `PROGRAM_REGISTERED` |
| `PROGRAM_REGISTERED` | открыт development log для experiment index | `DEVELOPMENT_ACTIVE` |
| `DEVELOPMENT_ACTIVE` | normative sources или контрольные vectors противоречат друг другу | `PROTOCOL_CONFLICT` |
| `DEVELOPMENT_ACTIVE` | опубликован design manifest с `n >= 1`, design hash и независимая timestamp attestation; experiment index необратимо зарезервирован | `DESIGN_COMMITTED` |
| `DEVELOPMENT_ACTIVE` | ни один кандидат не может войти в preregistered survivor set и дальнейшее разрешенное development прекращено | `PROGRAM_STOPPED` |
| `DESIGN_COMMITTED` | для exact design hash однократно созданы три commitments и опубликован полный preregistration bundle | `EXPERIMENT_PREREGISTERED` |
| `DESIGN_COMMITTED` | создан альтернативный commitment, package generation повторена, commit-beacon-reveal deadline нарушен, seed не воспроизводится либо bundle не завершен в hard budget | `EXPERIMENT_INVALIDATED` |
| `EXPERIMENT_PREREGISTERED` | открыт только selection key, commitment совпал | `SELECTION_HOLDOUT_OPENED` |
| `SELECTION_HOLDOUT_OPENED` | один survivor остался после ranking либо единственный кандидат в mode `SOLE_FEASIBLE`/`SOLE_SURVIVOR` прошел все selection gates; опубликован provisional decision | `WINNER_PROVISIONAL` |
| `SELECTION_HOLDOUT_OPENED` | никто не прошел hard gates | `NO_CANDIDATE` |
| `SELECTION_HOLDOUT_OPENED` | недополучены валидные platform blocks | `PLATFORM_UNSTABLE` |
| `WINNER_PROVISIONAL` | открыт confirmation key после фиксации winner | `CONFIRMATION_HOLDOUT_OPENED` |
| `CONFIRMATION_HOLDOUT_OPENED` | core confirmation G7 пройден полностью | `CONFIRMATION_CORE_PASSED` |
| `CONFIRMATION_HOLDOUT_OPENED` | любой обязательный core gate не пройден | `FULL_VALIDATION_FAILED` |
| `CONFIRMATION_CORE_PASSED` | external package открыт, commitment совпал, invalid-schema cases изолированы, а оставшаяся валидная часть прошла minimum и class quotas | `EXTERNAL_CHALLENGE_OPENED` |
| `CONFIRMATION_CORE_PASSED` | external package не проходит minimum либо class quotas после независимой schema validation | `EXPERIMENT_INVALIDATED` |
| `EXTERNAL_CHALLENGE_OPENED` | все валидные `IN_SCOPE_SURPRISE` gates пройдены, quotas соблюдены, exploratory и invalid-schema results зафиксированы | `CONFIRMATION_PASSED` |
| `EXTERNAL_CHALLENGE_OPENED` | любой валидный `IN_SCOPE_SURPRISE` gate не пройден | `FULL_VALIDATION_FAILED` |
| `CONFIRMATION_PASSED` | G8 согласован и freeze package complete | `FREEZE_READY` |
| `CONFIRMATION_PASSED` | независимая реализация расходится | `INDEPENDENT_REPRODUCTION_FAILED` |
| `FREEZE_READY` | отдельное подписанное решение о freeze | `FROZEN` |
| любой нетерминальный experiment state | нарушение manifest, holdout, budget или lineage | `EXPERIMENT_INVALIDATED` |
| `PROTOCOL_CONFLICT` | конфликт требует изменения protocol | `PROGRAM_STOPPED` |
| любой другой terminal experiment state | опубликована lineage entry, остался index, protocol неизменен, начата новая попытка | `DEVELOPMENT_ACTIVE` |
| любой terminal experiment state | experiment cap исчерпан либо сработал program stop rule | `PROGRAM_STOPPED` |

Переход от terminal experiment state к `DEVELOPMENT_ACTIVE` всегда создает новый experiment index. Он не возобновляет старый holdout и не меняет старую запись.

### 27.3. Итоговая запись

`final_decision.json` обязан содержать:

- status;
- program hash, experiment index и experiment hash;
- parent и final lineage hashes;
- hashes всех manifests;
- список кандидатов;
- причину исключения каждого проигравшего;
- все equivalence sets и полный ranking tuple каждого допущенного кандидата;
- structural step status, selection policy и `decision_basis`;
- winner ID, если он существует;
- число valid и invalid YouTube blocks;
- selection и confirmation commitment/opening evidence;
- randomness-beacon pulse, commit-beacon-reveal evidence и failure code, если он возник;
- external challenge commitment, opening evidence, valid, exploratory и invalid-schema counts и results hash;
- platform control summary;
- budget consumption;
- ссылки на envelopes;
- hashes reference и independent implementations;
- hash `transport_observer_report.json`;
- подписи либо provenance публикации;
- UTC timestamp.

---

## 28. Если ни один кандидат не прошел

Если текущий experiment получает `PROTOCOL_CONFLICT`, `NO_CANDIDATE`, `PLATFORM_UNSTABLE`, `FULL_VALIDATION_FAILED`, `INDEPENDENT_REPRODUCTION_FAILED` или `EXPERIMENT_INVALIDATED`:

- `BOOTSTRAP-1` не замораживается;
- результаты публикуются полностью;
- каждый уже открытый holdout публикуется, входит в cumulative exposed corpus и больше не используется для выбора;
- неоткрытый confirmation holdout либо публикуется как unused sealed object, либо криптографически уничтожается по preregistered rule, но не переносится в новую попытку;
- открытый external challenge публикуется полностью, а неоткрытый уничтожается или публикуется как unused sealed object по тому же заранее заданному rule;
- external cases с нарушенной grammar публикуются с неизменным label `INVALIDATED_SCHEMA`, входят в cumulative corpus только как exploratory diagnostics и никогда не превращаются задним числом в candidate failures;
- package, который еще не был создан при остановке `DESIGN_COMMITTED`, фиксируется как `NOT_CREATED` с signed custodian record и не подменяется пустым commitment;
- все timeout, beacon, commitment и reveal records публикуются даже если holdout не был создан;
- нельзя выбрать "наименее плохого";
- нельзя удалить неудобную channel cell задним числом;
- нельзя ослабить margin;
- нельзя автоматически добавить пятого кандидата в тот же эксперимент;
- нельзя автоматически назначить runner-up.

Следующий эксперимент получает:

- следующий monotonic experiment index;
- новую версию experiment manifest при неизменном protocol hash;
- документированную delta candidate set;
- training corpus, включающий все прежние раскрытые holdout как regression data;
- новый selection holdout и новый confirmation holdout с независимыми seeds;
- новый independently composed external challenge;
- новый resource budget;
- новую preregistration.

Внутри experiment index `max_restarts_within_experiment = 0`. Повтор недействительного YouTube block внутри заранее выделенного block-retry budget является повтором измерения, а не restart holdout. Любое изменение кандидата, metric, threshold, grid, budget или decision rule завершает experiment.

Каждая новая попытка обязана пройти все прежние раскрытые in-scope items как regression gate. Exploratory items сохраняют исходный diagnostic scope, если новая preregistration заранее не включает их класс в support claim. Раскрытые данные не участвуют в ranking, потому что стали development data. Новый выбор производится только на новых sealed selection и confirmation holdout.

Число попыток ограничено `program_max_experiments`, зафиксированным до первой. После его исчерпания статус равен `PROGRAM_STOPPED`. Все manifests, exposed data и lineage завершенной программы остаются публично доступными.

Продолжение требует новой публично отличимой программы с новым `program_id`, `new_program_justification.json` и ссылкой на полную прежнюю lineage. Justification перечисляет конкретные lessons learned, protocol delta, candidate delta, новые гипотезы и причины, по которым новая программа не повторяет прежний поиск без новой информации. Формулировки только "попробовать снова" недостаточно. Новая программа не может называться продолжением успешной preregistration старой программы.

Если требуется изменить метод этого protocol, текущая программа немедленно получает `PROGRAM_STOPPED`. Выпускается новый protocol major и новая root program registration. Один program manifest никогда не меняет закрепленный protocol hash между experiment indices.

---

## 29. Freeze package

Статус `FREEZE_READY` разрешен только после публикации:

- `bench_program_manifest.json`;
- полного `experiment_lineage.json`;
- `cumulative_exposed_corpus_manifest.json`;
- `experiment_design_manifest.json`, design hash и timestamp attestation;
- обоих holdout commitments, opening records и раскрытых corpora;
- external challenge commitment, opening record, scope labels и раскрытый corpus;
- `hidden_package_seed_protocol.json`, `randomness_beacon_manifest.json`, signed pulses, nonce commitments, reveals и проверку generated case IDs;
- `external_challenge_transform_grammar.json` и оба independent scope-validator reports;
- signed external challenge provenance log;
- `external_challenge_scope_validation_reference.json` и `external_challenge_scope_validation_independent.json`;
- `structural_metric_manifest.json`, три class aggregate results и full structural diagnostics;
- `common_metric_manifest.json`, calibration cells и `equivalence_bands.json`;
- `energy_threshold_derivation.json` с calibration evidence и golden vector;
- `development_decision_path.json` и `energy_partition_bias_analysis.json`;
- `optimizer_method_manifest.json` и development attestation;
- `state_transition_log.jsonl`;
- победившего topology ID;
- `d0_profile_manifest.json`;
- `d0_profile_hash256`;
- всех 72 canonical WAV;
- всех diagnostic subforms;
- fixed-point synthesis tables;
- estimator tables;
- thresholds;
- copy aggregation rule;
- energy и peak evidence;
- Gram matrices;
- `D0_CHANNEL_SUPPORT_ENVELOPE`;
- `D0_EXCLUSION_ENVELOPE`;
- первого suite candidate и двух reserve profiles;
- `cross_family_compatibility_manifest.json`;
- полного candidate comparison report;
- проигравших candidate manifests и results;
- YouTube source и download artifacts либо долговременных hashes и допустимых архивных копий;
- `d0_diversity_conformance_package`;
- `scanner_conformance_package`;
- reference implementation;
- independent implementation, `declaration_of_independence.json`, `independent_results_commitment.json` и report;
- `transport_observer_report.json`;
- platform readiness, paired-to-standalone и drift reports;
- context-dependency resolution report, если он был активирован;
- platform-context compatibility report;
- right-censoring summary;
- external challenge in-scope, exploratory и invalid-schema reports;
- experiment budget plan и фактическое consumption;
- checksums;
- DOI либо иной immutable identifier preregistration;
- отдельный DOI долговременного freeze archive.

Freeze является отдельным осознанным действием после `FREEZE_READY`. Сам успешный тест не изменяет protocol family автоматически.

Корневая идентичность победителя вычисляется по неизменяемому manifest без channel results:

```text
d0_profile_hash256 = SHA256(
    LP("GSP4-D0-PHYSICAL-PROFILE") ||
    LP(JCS(d0_profile_manifest))
)
```

Каждый из трех suite-профилей G5 получает:

```text
physical_profile_hash256 = SHA256(
    LP("GSP4-PHYSICAL-PROFILE") ||
    LP(JCS(physical_profile_manifest))
)
```

Channel results хешируются отдельно и не входят в физическую идентичность, чтобы не создавать цикл.

---

## 30. Мониторинг дрейфа после freeze

Результат YouTube является историческим доказательством на дату испытания, а не вечным свойством платформы.

### 30.1. Текущие статусы поддержки

```text
CURRENTLY_CONFIRMED
RETEST_DUE
RETEST_PENDING
REGRESSION_DETECTED
PLATFORM_UNAVAILABLE
HISTORICAL_ONLY
```

### 30.2. Canary

До `FROZEN` публикуется immutable `canary_manifest.json`. Он содержит точные source PCM hashes, video-layer hash, upload profile, expected output profile set, platform-control hash, extractor hash, thresholds, readiness rule и ordered artifact list. Формулировка "representative forms" без IDs и hashes запрещена.

Artifact list обязан включать:

- `PLATFORM_CONTROL-1`;
- exact minimum-margin `D0_OBJECT6` каждого победившего physical sub-estimator;
- каждый из семи marker IDs хотя бы один раз;
- `BOOT_SYNC`;
- валидный `BOOT_RECORD`;
- `CALL`, `ANSWER` и Level 2 selector;
- clean-negative D0-like probe;
- boundary form с наименьшим подтвержденным reserve.

Для `PLATFORM_CONTROL-1` и clean-negative probe поля положительного common reserve имеют значение `NOT_APPLICABLE`. Для них обязательны `decision = REJECT`, false-acceptance evidence и native negative score diagnostics. Нулевой reserve не подставляется, потому что он исказил бы positive minimum.

После freeze выполняется:

- один canary upload не реже одного раза в 30 календарных дней;
- один canary непосредственно перед публикацией нового suite;
- полная requalification не реже одного раза в 180 календарных дней;
- внеплановый canary после наблюдаемого изменения output codec, itag, sample rate или loudness behavior.

`current_support_manifest.json` хранит отдельно `due_reason = CANARY` или `due_reason = FULL_REQUALIFICATION`. Просрочка 30-дневного canary имеет семидневный grace period. Просрочка 180-дневной полной requalification имеет заранее фиксированный, не превышающий 14 дней grace period.

Если первый canary нарушает hard limit:

1. статус становится `RETEST_PENDING`;
2. новые пользовательские экспорты, обещающие YouTube support, блокируются;
3. в течение семи дней выполняется второй upload не ранее чем через 24 часа.

Если второй upload подтверждает отказ, статус становится `REGRESSION_DETECTED`.

Если повтор невозможен из-за недоступности платформы, статус становится `PLATFORM_UNAVAILABLE`.

### 30.3. Переходы current-support

| From | Событие | To |
| --- | --- | --- |
| `CURRENTLY_CONFIRMED` | истек срок canary или full requalification | `RETEST_DUE` с точным `due_reason` |
| `RETEST_DUE` | требуемая проверка не выполнена в своем grace period | `HISTORICAL_ONLY` с сохраненным `due_reason` |
| `CURRENTLY_CONFIRMED` или `RETEST_DUE` | первый hard failure | `RETEST_PENDING` |
| `RETEST_PENDING` | независимый повтор на другой UTC-дате подтверждает failure | `REGRESSION_DETECTED` |
| `RETEST_PENDING` | повтор физически недоступен | `PLATFORM_UNAVAILABLE` |
| `RETEST_DUE` с `CANARY` | canary полностью пройден до конца grace period | `CURRENTLY_CONFIRMED` |
| `RETEST_DUE` с `FULL_REQUALIFICATION` | полная requalification пройдена до конца grace period | `CURRENTLY_CONFIRMED` |
| `RETEST_PENDING`, `PLATFORM_UNAVAILABLE` или `HISTORICAL_ONLY` с причиной canary/availability | два полных успешных canary на разных UTC-датах, без failure между ними | `CURRENTLY_CONFIRMED` |
| `HISTORICAL_ONLY` с `FULL_REQUALIFICATION` | полная requalification успешно завершена | `CURRENTLY_CONFIRMED` |
| `REGRESSION_DETECTED` | полная requalification по frozen profile успешно завершена | `CURRENTLY_CONFIRMED` |

Один успешный canary после `RETEST_PENDING`, `PLATFORM_UNAVAILABLE` или `HISTORICAL_ONLY` не восстанавливает поддержку. Просроченную полную requalification и `REGRESSION_DETECTED` нельзя снять canary-парой.

### 30.4. Последствия регрессии

При `REGRESSION_DETECTED`:

- старый freeze package не переписывается;
- исторические результаты не удаляются;
- публичный current-support manifest обновляется;
- новые совместимые экспорты блокируются;
- D0 thresholds не ослабляются;
- D0 forms не переоптимизируются внутри family.

Frozen D0 thresholds выражаются в canonical decoder units после нормативного выравнивания, а не в LUFS конкретной версии платформы. Изменение loudness policy учитывается как измеренный channel gain и не меняет threshold. Если после допустимого выравнивания сигнал выходит из frozen support envelope, это regression.

Если сломан только suite за пределами корневого D0 envelope, создается новый suite. Если сломан сам D0 в ранее обещанной корневой области, восстановление совместимости требует нового protocol family.

### 30.5. Canary evidence

Каждый запуск публикует:

```text
canary_manifest_hash256
support_status_before
support_status_after
source_video_sha256
youtube_video_id
upload_started_utc
output_stable_utc
downloaded_file_sha256
extracted_pcm_sha256
platform_context_hash256
all artifact decisions
common reserve numerator, denominator, dB_q и censor status
для каждого canary artifact, channel cell и noise vector
control chart update
next_due_utc
```

Пропуск canary не переписывает историческую пригодность. Он только запрещает обозначать ее как current.

---

## 31. Явные предпосылки, ограничения и non-goals

Этот протокол опирается на проверяемые, но не гарантированные предпосылки:

1. YouTube и требуемые output profiles доступны во время platform blocks. Недоступность дает измеримый статус, а не право менять gate.
2. Hard platform context можно удерживать неизменным, а soft tool changes можно проверять замороженным compatibility test. Если нельзя, сравнение прекращается.
3. Sealed holdout действительно недоступен аналитикам до формального открытия. Commitment без организационного разделения доступа не считается достаточным.
4. Reference и independent implementers способны следовать одной точной fixed-point спецификации без обмена project DSP code.
5. Сохраненные source и downloaded artifacts доступны для независимой проверки. Одних таблиц результатов недостаточно.
6. Platform drift можно обнаруживать control artifacts, но нельзя предотвратить или полностью описать заранее.
7. Конечная channel grid доказывает только результат на перечисленных cells и не оценивается как универсальная модель всех будущих искажений.
8. Общий peak и energy budget является условием честного инженерного сравнения, а не утверждением об оптимальности для неизвестного физического канала.
9. YouTube является целевым цифровым транспортом первой family. Analog recapture, радиопередача и иные платформы не входят в support claim.
10. Земные hashes, JCS, BCH, RS и manifests обеспечивают воспроизводимость стенда. Они не объявляются универсальной семантикой для неизвестного наблюдателя.
11. External challenge расширяет проверку за пределы заранее видимых recipes, но не доказывает устойчивость к произвольному неизвестному воздействию.
12. Доступен хотя бы один заранее выбранный публичный randomness beacon с проверяемым pulse. Его недоступность является явным отказом процедуры, а не источником произвольного seed.
13. Commitment ручного external challenge доказывает неизменность content, но не устраняет возможный человеческий bias или сговор.
14. Три structural class aggregates измеряют выбранные synthetic/local classes. Они не доказывают тот же относительный порядок на YouTube, в аналоговом канале или при неописанном искажении.
15. Реализации имеют exact integer arithmetic не уже 128 бит либо arbitrary precision для нормативных cross products.

Non-goals:

- доказать, что неизвестный разум поймет D0;
- доказать внеземное происхождение reply;
- скрыть payload от специализированного человеческого декодирования;
- гарантировать поддержку YouTube после даты последней успешной квалификации;
- оптимизировать GUI, художественный визуал или пользовательский workflow;
- заменить будущие измерения рассуждением о предполагаемом поведении кодека.

---

## 32. Отчетность без преувеличений

Разрешенные формулировки:

- "кандидат прошел перечисленные channel cells";
- "ошибок не обнаружено в конечной обязательной сетке";
- "минимальный измеренный margin равен ...";
- "первая измеренная граница отказа равна ...";
- "поддержка YouTube подтверждена на даты ... для outputs ...";
- "кандидат является единственным допустимым, сравнительное превосходство не измерялось";
- "кандидат выбран в рамках заранее заданной structural-first policy";
- "структурный этап не различил кандидатов; решение принято uniform-reserve metric ...";
- "наблюдаемый uniform-reserve gap согласуется с заранее рассчитанной ценой разделения энергии";
- "external challenge пройден внутри scope ..., результаты за пределами scope перечислены отдельно";
- "неизвестно, переносится ли результат на другой кодек, платформу или будущую версию YouTube".

Запрещенные формулировки:

- "сигнал неразрушим";
- "сигнал универсален";
- "YouTube всегда сохранит код";
- "любой разум поймет D0";
- "отсутствие ошибки доказывает нулевую вероятность ошибки";
- "перспективный кандидат", "предварительный фаворит" или "ожидаемый победитель" до фиксации provisional decision;
- "external challenge доказывает устойчивость к любому неизвестному воздействию";
- "synthetic structural result доказывает тот же порядок кандидатов после YouTube";
- "structural-first policy доказывает универсальную важность notch и burst над AWGN";
- "reply доказывает внеземное происхождение".

---

## 33. Что должно войти в последующее ТЗ для Claude Code

После аудита этого протокола отдельное ТЗ обязано описать:

- структуру репозитория;
- язык и pinned dependencies;
- integer/fixed-point DSP;
- генераторы четырех кандидатов;
- phase optimizer;
- канонический WAV writer;
- soft decoder и copy aggregator;
- локальные AAC/Opus pipelines;
- планировщик channel grid;
- YouTube import/export workflow без хранения секретов;
- artifact database;
- scanner pipeline;
- resource scheduler;
- JCS manifests и JSON Schema;
- program lineage и append-only state machine;
- двухступенчатый design commitment, commit-beacon-reveal ceremony, deadlines и проверяемое однократное создание скрытых packages;
- раздельное sealing selection и confirmation holdout;
- независимое sealing, закрытая transform grammar, scope validation и delayed opening external challenge;
- run-order generation;
- common calibration noise и equivalence-band engine;
- engine трех structural class aggregates, epsilon-Pareto и development decision-path report;
- hard diversity overlap gate;
- exact reserve-ratio comparison и normative `ten_log10_fixed_q`;
- exact 128-bit или arbitrary-precision arithmetic и overflow-negative vectors;
- metrics engine;
- YouTube output-readiness polling и platform-context validation;
- paired и standalone qualification workflows;
- context-dependency resolution workflow;
- hard/soft platform-context compatibility tests;
- platform controls, drift chart и canary recovery;
- report generation;
- deterministic tests;
- independent implementation boundary;
- transport-observer export;
- CLI до создания GUI;
- acceptance tests, прямо соответствующие G0-G8.

ТЗ не может заранее объявить победителя и не может заменять hard gate ручным выбором.

---

## 34. Минимальный порядок выполнения

1. Провести внешний аудит этого protocol.
2. Исправить найденные методические дефекты только выпуском новой major версии protocol.
3. Опубликовать корневой `bench_program_manifest.json` до data-influenced tuning.
4. Написать ТЗ на bench implementation.
5. Реализовать G0, canonical vectors и integer semantics.
6. Реализовать четыре candidate synthesizer, decoder, scanner и common calibration.
7. Выполнить открытую development-фазу G0-G6, включая pilot YouTube blocks и carryover matrix.
8. Построить и заморозить все три suite-профиля каждого survivor.
9. Вывести общий `E_target`, equivalence bands, exact budgets, block plan и platform-readiness rules.
10. Опубликовать `experiment_design_manifest.json` с будущими randomness-beacon pulses, design hash и независимую timestamp attestation.
11. До target pulses получить signed custodian commitments, затем проверить public pulses и однократно сформировать два независимых sealed holdout и committed external challenge, привязав все три к design hash.
12. Опубликовать полный experiment preregistration bundle и независимую timestamp attestation.
13. Открыть только selection holdout и без tuning выполнить selection G2-G6.
14. Опубликовать `provisional_decision.json` с точным winner ID либо `NO_CANDIDATE`.
15. Открыть только для зафиксированного победителя confirmation holdout и выполнить все core components G7.
16. После `CONFIRMATION_CORE_PASSED` открыть external challenge, независимо валидировать grammar и выполнить valid in-scope, exploratory и invalid-schema diagnostics.
17. Провести независимое G8 и отдельную transport observation.
18. Опубликовать оба holdout, external challenge, результаты, lineage и полный freeze package.
19. Только затем принять отдельное подписанное решение о freeze.

---

## 35. Научно-технические источники

1. RFC 8999, version-independent protocol invariants: <https://www.rfc-editor.org/rfc/rfc8999.html>
2. RFC 8785, JSON Canonicalization Scheme: <https://www.rfc-editor.org/rfc/rfc8785.html>
3. RFC 6716, Opus and MDCT behavior: <https://www.rfc-editor.org/info/rfc6716/>
4. Fraunhofer IIS, MP3 and AAC Explained, switched MDCT and transient behavior: <https://www.iis.fraunhofer.de/content/dam/iis/de/doc/ame/conference/AES-17-Conference_mp3-and-AAC-explained_AES17.pdf>
5. NASA, multisine peak factor minimization: <https://ntrs.nasa.gov/api/citations/20240009677/downloads/NASA-TM-20240009677.pdf>
6. NIST, windows and spectral leakage: <https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=150008>
7. ITU-R BS.1770-5, loudness and true peak: <https://www.itu.int/rec/R-REC-BS.1770-5-202311-I>
8. NIST, blocking a process experiment: <https://www.itl.nist.gov/div898/handbook/pri/section3/pri332.htm>
9. NIST, randomization in experimental design: <https://www.itl.nist.gov/div898/handbook/pri/section3/pri3332.htm>
10. NIST, run-order plots for drift: <https://www.itl.nist.gov/div898/handbook/pmd/section4/pmd443.htm>
11. NIST, EWMA control charts for gradual drift: <https://www.itl.nist.gov/div898/handbook/toolaids/pff/mpc.pdf>
12. YouTube, recommended upload encoding settings: <https://support.google.com/youtube/answer/1722171>
13. YouTube, video and audio formatting specifications, including platform re-encoding: <https://support.google.com/youtube/answer/4603579>
14. YouTube, delayed availability of higher-quality processing: <https://support.google.com/youtube/answer/71674>
15. Open Science Framework, immutable registrations and preregistrations: <https://help.osf.io/article/330-welcome-to-registrations>
16. RFC 3161, Internet X.509 Time-Stamp Protocol: <https://www.rfc-editor.org/rfc/rfc3161.html>
17. NIST, numerical reproducibility in high-performance computing: <https://www.nist.gov/document-18636>
18. NIST PQC conference paper, reproducible testing and test vectors across implementations: <https://csrc.nist.gov/CSRC/media/Events/Second-PQC-Standardization-Conference/documents/accepted-papers/kannwischer-pqm4.pdf>
19. MITRE CWE-770, allocation of resources without limits or throttling: <https://cwe.mitre.org/data/definitions/770.html>
20. ITU-R F.1093-2, frequency diversity and correlation of degradation: <https://www.itu.int/dms_pubrec/itu-r/rec/f/R-REC-F.1093-2-200604-I%21%21PDF-E.pdf>
21. ITU-R P.530-19, diversity techniques and limits of frequency diversity: <https://www.itu.int/dms_pubrec/itu-r/rec/p/R-REC-P.530-19-202509-I%21%21PDF-E.pdf>
22. Zenodo, DOI and preservation-oriented records: <https://help.zenodo.org/docs/deposit/about-records/>
23. NASA, matched-filter detection in additive white Gaussian noise: <https://ntrs.nasa.gov/api/citations/19710025832/downloads/19710025832.pdf>
24. WILDS, separate evaluation of in-distribution performance and real-world distribution shifts: <https://proceedings.mlr.press/v139/koh21a.html>
25. NIST, Interoperable Randomness Beacons, signed and hash-chained public randomness for auditability: <https://csrc.nist.gov/projects/interoperable-randomness-beacons>
26. NIST IR 8213, a reference for public, time-stamped, signed and hash-chained randomness pulses: <https://csrc.nist.gov/pubs/ir/8213/ipd>
27. Scientific Reports, loss of Pareto selection pressure as the number of objectives grows: <https://www.nature.com/articles/s41598-024-70145-8>

---

## 36. Обоснование изменений версии 6.0

Версия 6.0 отвечает на два внешних аудита версии 5.0 (обозначены GPT и Gemini) и на внутренний повторный аудит (обозначен self). Для каждого пункта записано, что принято, что отклонено и почему. Раздел информативный; нормативны разделы 1-35.

### 36.1. Принято полностью

**GPT P1: единица квантиля и вес плотности сетки.** Подтверждено контрпримером: при квантиле по ячейкам уточнение сетки одной family меняло победителя без изменения физики. Введена трехуровневая иерархия ladder -> stratum -> координата с явными замороженными рациональными весами, `L` каждого класса равно числу strata, `minimum_strata_per_class >= 8` предотвращает вырождение квантиля в минимум при малом `L`. Разделены `L_notch`, `L_burst`, `L_combined`; несоответствие "cells против ladders против families" версии 5.0 устранено. Инвариантность агрегата к удвоению ячеек внутри stratum стала обязательным вектором synthetic corpus, то есть контрпример GPT превращен в постоянный регрессионный тест.

**GPT P1: правило цензурирования.** Подтверждено контрпримером `[1c, 2, ..., 100]`: censored элемент ниже ранговой границы меняет истинный квантиль, даже когда сама ранговая позиция measured. Позиционная проверка заменена значением: статус `MEASURED` только если lower bound каждого censored элемента строго больше значения агрегата; при равенстве статус `LOWER_BOUND`, поэтому tie-break по ID не может влиять на censor status. Каждая координата стала идентифицированным интервалом, epsilon-dominance переведена на интервальные сравнения; два lower bound не сравниваются как точные значения. Принят и консервативный принцип GPT: недоказуемое превосходство не исключает никого, это менее мощно, но корректно.

**GPT P1: pooled false-value rate.** Приняты все четыре составляющие: пофамильные пределы по образцу раздела 7, ролевая полнота (marker roles, `BOOT_SYNC`, cross-class, ложная grammar), раздельные пределы `BOUNDARY_GRID` и `STRESS_GRID`, точное сравнение cross multiplication без деления. Удалена зависимость от классификации "за пределом исправимости": считается любое принятое неверное `value_or_role`.

**GPT P2: namespace.** Bench-теги переведены на `-6`, каталог на `d0_bench_v6/`. Wire-теги `GSP4-*` сознательно сохранены, и в раздел 10.1 добавлено нормативное объявление двух независимых major: `bench_protocol_major = 6` нумерует методику, `wire_protocol_major = 4` нумерует физическое семейство концепции. Это ровно та развязка, которую предложил GPT, и она предотвращает будущую механическую замену всех четверок.

**GPT P2: устаревшее определение в разделе 3.** Подтверждено как прямой внутренний `PROTOCOL_CONFLICT` по собственным правилам документа. Определение заменено, добавлен термин stratum.

**GPT P2: переоценка `sqrt(L)`.** Принято. Ячейки сетки не являются выборкой из одной распределительной модели, асимптотика выборочного квантиля к ним неприменима, а рост `L` может означать уточнение одной family, то есть смену самого функционала. Формулировка заменена узкой: внутренний квантиль не определяется одной экстремальной ячейкой, фактическая повторяемость измеряется через `u95_k`. Это исправление текста, который пришел из аудита 4.0, то есть из моего собственного обоснования.

**GPT P2: интерпретация 47,3%.** Принято и проверено независимым полным перебором: доля ложных исправлений зависит от точного веса ошибки и составляет 39,56% при весах 3-4 и 11-12, 47,05% при 5-6 и 9-10, 48,72% при 7-8, 100% при 13-15. Значение 100% следует из того, что слово из всех единиц является кодовым, поскольку `g(1) = 1`. Sphere coverage 47,27% остается верной арифметикой, но не вероятностью для произвольного канала; нормативная формулировка пункта 10 переписана, векторы `bch_miscorrection_fraction_by_exact_error_weight` добавлены в G0.

**Gemini: штраф за живучесть.** Принято как реальный дефект знаменателя и закрыто сильнее, чем предложено: знаменатель стал условным по отказам. Кандидат, рано и чисто отказывающий, больше не получает тривиальный ноль, а кандидат, борющийся глубже конкурентов, не наказывается за дополнительные возможности ошибиться; измеряется именно качество безопасного отказа. При этом кандидат, выдающий ложные значения вместо стираний, по-прежнему ловится, потому что его доля ложных принятий среди его же отказов высока. Введен `fla_min_informative_failures` по образцу diversity gate: нулевая доля из двух отказов не является доказательством безопасности.

### 36.2. Принято частично

**Gemini: слепота квантиля при массовом цензурировании.** Сценарий в исходной формулировке (30% против 95% censored) при правиле версии 5.0 фактически различался: у кандидата с 30% цензурирования квантиль measured и низкий, у кандидата с 95% квантиль censored на ceiling, и правило "lower bound лучше measured более чем на epsilon" давало победу второму. Реальный краевой случай уже: оба кандидата censored на общей границе ceiling, тогда разрыв в доле цензурирования действительно невидим. Закрыто предупреждающим правилом: если на development хотя бы два кандидата имеют `LOWER_BOUND` aggregate на общей границе, сетка расширяется по severity до preregistration; если расширение упирается в физический или safety ceiling, координата объявляется `NON_DISCRIMINATING_BY_CEILING` в design manifest заранее, а не обнаруживается постфактум. Доля censored ladder публикуется по stratum и остается диагностикой, но не становится ranking-координатой, потому что это создало бы четвертую структурную координату в обход правила major.

**Gemini: невыполнимость `u95_k`.** Семантическая претензия принята: формулировка "на development controls" была неопределенной и позволяла прочтение через статический контрольный сигнал, на котором структурный агрегат не вычислим. Претензия о взрыве бюджета отклонена: локальная матрица G3 детерминирована при фиксированных seeds, поэтому изменчивость создают только стохастические ячейки, и повторять нужно только их. Введен явный механизм `structural_replicate_seed_sets` с числом наборов не меньше 5, нулевым вкладом детерминированных ячеек и отдельной строкой в `max_local_channel_jobs`. Полный повтор всей сетки не требуется.

### 36.3. Внутренний повторный аудит

**self: вырождение квантиля при малом числе strata.** Иерархия сама создает новый край: `rank(4, 1, 4) = 1`, то есть при четырех strata квантиль снова является минимумом. Закрыто требованием `minimum_strata_per_class >= 8` с показанной арифметикой.

**self: определение взвешенного nearest-rank.** Равновесная формула версии 5.0 не определяла поведение при неравных весах. Задано накопительное правило через cross multiplication с доказанным совпадением с равновесной формулой при равных весах; добавлен golden vector с неравными весами.

**self: рекурсия цензурирования.** Правило GPT сформулировано для одного уровня списка; в иерархии censored ladder должен корректно распространяться через within_stratum_rule на значение stratum и далее на координату. Записано явно, включая освобождение координаты `COMBINED` от цензурирования, поскольку каждая ее ячейка дает измеренное решение.

**self: судьба `FLA_INSUFFICIENT_FAILURES` на hard gate.** Без явного правила недостаток информативных отказов на `BOUNDARY_GRID` либо блокировал бы почти безотказного кандидата, либо тихо пропускался. Зафиксировано: статус публикуется и не блокирует, потому что отсутствие отказов не является свидетельством небезопасного отказа.

**self: candidate-specific probe acceptance в canary.** Проверено, что разделение "невалидный контроль тракта против ложного принятия кандидата", введенное в 19.4 и 19.6, не противоречит новой метрике: принятие валидного probe входит в `false_logical_acceptance` кандидата. Правок не потребовалось, зафиксировано здесь как проверенное.

### 36.4. Отклонено

**Gemini: формулировка "оба аудита закрыты, документ почти монолитен" применительно к 5.0.** Отклонена самим фактом этого раздела: три P1 версии 5.0 были реальными, два из них подтверждены контрпримерами.

**GPT: вариант полного отказа структурной координаты от исключения при любом неидентифицированном интервале.** Принят только как fallback внутри интервального правила. Полный отказ выбрасывал бы доказуемые случаи, где `a_lower > b_upper + epsilon` выполняется несмотря на цензурирование одной из сторон.

---

## 37. Итог

Стенд не должен подтвердить заранее выбранную идею. Он должен иметь право выбрать простейший `D0-B1`, временной `D0-T2`, кворумный `D0-T3`, частотно разнесенный `D0-F3` или не выбрать никого.

Главный результат эксперимента состоит не только в имени победителя. Он включает:

- доказательство чистой математической различимости;
- измеренную устойчивость в конечной цифровой матрице;
- три сопоставимых ранговых structural class aggregates с общими нормативными reference points, worst-case evidence и full diagnostics до AWGN ranking;
- численный hard diversity gate без candidate-specific порога;
- сопоставимое реальное испытание YouTube с контролем дрейфа;
- commit-beacon-reveal происхождение скрытых packages;
- независимый external challenge с typed grammar и раздельным in-scope, exploratory и invalid-schema отчетом;
- честную границу отказа;
- цену физической резервации;
- воспроизводимый scanner;
- полный ресурсный бюджет;
- независимое повторение;
- механизм обнаружения будущей регрессии платформы.

Только такой пакет позволяет необратимо заморозить `BOOTSTRAP-1` без подмены измерения предпочтением автора.
