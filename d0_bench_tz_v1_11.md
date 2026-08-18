# Техническое задание: реализация лабораторного стенда D0

Версия ТЗ: 1.11  
Дата: 2026-08-18  
Язык документа: русский

Companion (текущий драфт): `d0_bench_integer_dsp_semantics_v1.7.md`, SHA-256 `98e282dcafcaa48db9d3a9314106cb641f729f87438fc158277b4ab21806a4e9`, статус DRAFT / T0 INPUT. Нормативная версия companion возникает только по завершении T0; нормативная редакция ТЗ пинует ее не именем файла, а объектом `dsp_semantics_reference.json` (поля: version, sha256, tables_manifest_sha256), что исключает устаревшие ссылки на имя при смене версии. Companion закрывает машинную математику: canonical WAV v1, округление и Q-форматы, фазовая решетка и синус без интерполяции, порядок операций синтеза, true peak FIR, решатель Gram по Барейсу, PRNG и DISCRETE_GAUSSIAN_U16, биквад, ресемплер, композиция звеньев и cell_id, NMS и планирование сканера, подписанные записи. При конфликте между ТЗ и companion по машинной математике действует companion.

**СТАТУС: NON-NORMATIVE DRAFT FOR REVIEW.** До публикации `bench_program_manifest.json` этот файл не является шагом 4 раздела 34 протокола и не имеет нормативной силы. После публикации манифеста выпускается нормативная редакция этого ТЗ, в чей заголовок входят ЧЕТЫРЕ нормативных источника — протокол, концепция, НОРМАТИВНАЯ версия companion (после T0) и `bench_program_manifest.json` — плюс `program_hash256`, что делает последовательность шагов 3 -> 4 криптографически доказуемой. До этого момента любые работы по данному тексту являются подготовкой ревью, а не реализацией.

Изменения 1.10 -> 1.11: в раздел 11.7 внесена граница между дефектом DRAFT-спецификации и технической ошибкой реализации, чтобы дефекты, найденные до нормативного использования редакции, не заносились в реестр как implementation failure, а дефекты, уже повлиявшие на порожденный артефакт или evidence, заносились обязательно. Companion не менялся, пин v1.7 сохранен. Изменения 1.9 -> 1.10: пин companion v1.7, исправившего достижимый максимум `true_peak_q` (16968703 вместо 16968704 при несимметричном S24) и убравшего ссылку на несуществующий на шаге T0 `checksums.sha256`. Изменения 1.8 -> 1.9: пин companion v1.6, закрывшего четыре дефекта пути true peak (диапазон выходных позиций, байтовая норма `TP_FIR_SOURCE_DECIMAL.txt`, носитель его SHA-256 при закрытой схеме манифеста таблиц, шаг ITU 12.04 dB); `TP_FIR_SOURCE_DECIMAL.txt` внесен в перечень объектов уровня ТЗ раздела 8.2, поскольку реестр не допускает wildcards и безымянная формулировка "нормативные таблицы данных" не покрывает текстовый артефакт. Изменения 1.7 -> 1.8: пин companion v1.5, устаревшее имя пробы в перечне разделов companion заменено на DISCRETE_GAUSSIAN_U16. Изменения 1.6 -> 1.7: пин companion v1.4, устранено дублирование статуса в шапке. Изменения 1.5 -> 1.6: пин companion v1.3, объект dsp_tables_manifest.json добавлен в реестр, заголовочная формула нормативной редакции исправлена на ЧЕТЫРЕ источника. Изменения 1.4 -> 1.5 закрывали два P0 и семь P1 red team v1.4 (GPT): версия companion при T0 не переписывается на месте, stateful-звенья получили исполнимые контракты, генератор ресемплерных таблиц полностью воспроизводим, ссылка на companion через reference-объект, имя манифеста кандидата унифицировано, A3 включает обязательные граничные метрики, dedup сканера стал отчетным, anti-rollback якорь определен, отчеты разделяют ячейки с насыщением. Изменения 1.3 -> 1.4 закрывали пять P0 и одиннадцать P1 red team v1.3 (GPT): companion и его таблицы включены в допуски crosscheck и G8, добавлен шаг T0, расширены G3-контракт и ключи БД, physical profile привязан явно, уточнены 308-семантика и anti-rollback. Изменения 1.2 -> 1.3 закрывали восемнадцать пунктов implementability red team (GPT): четыре P0 и четыре P1 вынесены в companion по DSP-семантике, остальные закрыты правками ниже. Изменения 1.1 -> 1.2 закрывали двенадцать пунктов внешнего red team (GPT): переименование acceptance в A0-A8 с запретом создавать gate evidence (P0), драфт-статус и третий нормативный хеш (P0), полный реестр манифестов без wildcards, разделение BCH и copy-валидатора, граница G0-crosscheck, исполняемый paired/standalone workflow, контракт commit-beacon-reveal, переквалификация при смене кодек-бинаря, dual-mono инвариант, привязка strata к манифесту, разделение JCS- и schema-тестов, объектная модель в CLI.

Нормативные источники, которым это ТЗ подчинено:

| Документ | SHA-256 |
| --- | --- |
| `d0_bench_protocol_v6.0.md` | `b5a1915dbcb8a5b6eb68c59dd55346f6c7435b40ef47f930aeae6eb8077e0db2` |
| `geometric_sound_protocol_concept_v8.0_ru.md` | `2e027eeeb42457ec26712637015c8ae69743ffc53d77c07fb1f67baee9e5bb0d` |

При любом расхождении между этим ТЗ и протоколом стенда действует протокол. ТЗ не может ослабить ни один gate, изменить ни одну формулу и заранее объявить победителя. Обнаруженное противоречие обрабатывается как `PROTOCOL_CONFLICT` по разделу 27 протокола: исправляется либо ТЗ, либо протокол новой major-версией, но не код втихую.

Зафиксированные продуктовые решения, на которых построено ТЗ:

1. Целевой канал: YouTube, цифровой тракт от загрузки до скачанного файла. Акустический перезахват (динамик-микрофон) вне модели угрозы и вне support claim.
2. Точка декодирования: скачанный файл. Клиентская обработка воспроизведения (loudness, эквалайзеры, Bluetooth) не входит в тракт декодера; loudness policy платформы учитывается только как canary-триггер по разделу 30 протокола.
3. Область ТЗ: только лабораторный стенд D0 (G0-G8). Русский адаптер, storyboard P1-P3, blind test, генератор сообщений, видеослой и GUI не входят и проектируются после freeze.

---

## 1. Назначение и границы

### 1.1. Что строится

Пакет программ, выполняющий программу экспериментов протокола v6.0: синтез четырех кандидатов D0, локальная канальная матрица, реальные YouTube-блоки, сканер, ранжирование, конечный автомат, манифесты и отчеты. Пакет предоставляет все механизмы для формирования freeze package раздела 29 протокола, но сам по себе его не производит: полный freeze package возникает только в результате выполнения эксперимента, включая selection и confirmation holdout, external challenge, независимое G8 другой стороной и transport observation. Готовность программного обеспечения и `FREEZE_READY` эксперимента — разные состояния, и первое никогда не подразумевает второе.

### 1.2. Что не строится

- Windows GUI и любой пользовательский интерфейс кроме CLI.
- Кодирование текста, преамбулы, adapter, suite payload сверх трех резервных физических профилей на кандидата.
- Автоматическое принятие решения о freeze: последний переход `FREEZE_READY -> FROZEN` выполняется человеком отдельной подписанной командой.
- Вторая (независимая) реализация. Она делается другой стороной по разделу 23 протокола; настоящее ТЗ определяет только границу между реализациями (раздел 12).

### 1.3. Два бинарных продукта одного репозитория

```text
d0bench        основной CLI стенда (reference implementation)
d0bench-xport  экспортер публичных векторов, схем и corpus-заданий
               для независимой реализации и внешних аудиторов
```

---

## 2. Среда разработки и инструменты

ТЗ инструментонезависимо: любой исполнитель, следующий разделам 3-11, произведет совместимую реализацию. Основной запланированный инструмент — Claude Code; при его использовании обязательны следующие правила, вытекающие из G8:

1. Reference-реализация и независимая реализация не могут делаться одним и тем же диалоговым контекстом, одной сессией или переносом кода между ними. Допустим общий доступ к протоколу, схемам и публичным векторам — и только к ним.
2. Каждая задача Claude Code формулируется ссылкой на раздел этого ТЗ и раздел протокола, а не пересказом. Пересказ порождает дрейф формул.
3. Сгенерированный код проходит те же acceptance tests раздела 13, что и написанный вручную; происхождение кода не ослабляет ни один тест.

Языки и закрепленные зависимости. Политика зависимостей раздельна для двух путей, чтобы требование чистоты нормативной математики не конфликтовало с криптографией оркестрации:

```text
язык ядра            Python >= 3.12 (нативные целые произвольной точности
                     покрывают требование 128-bit/arbitrary-precision
                     без внешних библиотек)

нормативный DSP/math путь (exactmath, synth, decode, ranking,
manifests-хеширование):
                     ТОЛЬКО стандартная библиотека Python;
                     никакого numpy/scipy/cryptography

нормативный orchestration/security путь (statemachine, commitments):
                     стандартная библиотека плюс pinned cryptography
                     ИСКЛЮЧИТЕЛЬНО для подписей Ed25519; ее версия и
                     sha256 колеса фиксируются в env_manifest.json;
                     ни один байт из нее не участвует в DSP-вычислениях

ускоряющий код       numpy разрешен ТОЛЬКО в ненормативных путях
                     (визуализация, черновой поиск фаз) и обязан
                     завершаться проверкой нормативным кодом

кодеки               нормативной единицей является не имя библиотеки,
                     а четверка из env_manifest.json:
                       sha256 конкретного статического бинаря ffmpeg,
                       точное имя кодека,
                       точная строка опций,
                       sha256 выходного файла на fixture-входе.
                     Текущий выбор env_manifest: libfdk_aac для AAC,
                     libopus для Opus. ЛЮБОЕ изменение sha256 кодек-бинаря
                     аннулирует все codec-dependent evidence и требует
                     новой канальной квалификации, потому что совпадение
                     на одном fixture не доказывает эквивалентность
                     encoder-сборок на транзиентах, multisine,
                     near-clipping входах, других битрейтах и MDCT-смещениях.
                     Fixture-хеш служит smoke-детектором подмены,
                     а не критерием эквивалентности

скачивание           yt-dlp, pinned версия, sha256 в env_manifest.json
загрузка             официальный YouTube Data API v3 resumable upload;
                     OAuth-токены только в локальном secret store вне
                     репозитория и вне артефактов; в манифесты попадают
                     только псевдоним аккаунта и версии инструментов
хранилище            SQLite (файл на experiment index) + файловое дерево
                     артефактов d0_bench_v6/ по разделу протокола
схемы                JSON Schema draft 2020-12; валидатор в CI
хеши                 SHA-256 из hashlib; JCS по RFC 8785 собственной
                     реализацией с golden vectors (внешняя JCS-библиотека
                     запрещена в нормативном пути); обязательные JCS-векторы:
                     UTF-16 сортировка ключей, escaping, минус-ноль,
                     числовые границы, дубликаты ключей на границе парсера
```

Запрещено в нормативном коде: float, `math.log/exp/sin/cos`, недетерминированные итерации по dict/set без сортировки, локале-зависимые операции, системное время в вычислениях (время только в логах).

---

## 3. Репозиторий

```text
d0bench/
  pyproject.toml            # pinned deps, единая точка версий
  env_manifest.json         # sha256 всех внешних бинарей
  README.md
  spec/                     # копии протокола и концепции + их sha256
  schemas/                  # все JSON Schema (раздел 8)
  src/d0bench/
    exactmath/              # раздел 4: integer semantics
    synth/                  # раздел 5: таблицы, кандидаты, оптимизатор, WAV
    decode/                 # раздел 6: оценщик, копии, агрегация, fla
    channel/                # раздел 7: локальные преобразования, сетка, strata
    youtube/                # раздел 9: upload/download/readiness/context
    scanner/                # раздел 10: потоковый сканер и бюджеты
    ranking/                # раздел 6.5: интервальная Pareto, метрики 1-10
    statemachine/           # раздел 11: состояния, lineage, commitments
    manifests/              # JCS, LP, хеши, генерация и валидация
    reports/                # отчеты и final_decision
    cli/                    # раздел 14
  vectors/                  # golden vectors, генерируются и замораживаются
  tests/
    unit/
    golden/                 # побитовые сравнения с vectors/
    harness/                # A0/ .. A8/ по разделу 13; экспериментальные
                            # G-свидетельства в CI-тестах не живут
  tools/xport/
```

Правило одного источника: каждая нормативная константа существует ровно в одном месте — в манифесте или в `spec/`. Дублирование числа в коде без ссылки на манифест — дефект ревью.

---

## 4. Модуль exactmath: исполнимая `integer_semantics.json`

Протокол требует `integer_semantics.json`; это ТЗ определяет его как пару из декларативного файла и исполняющего модуля, причем модуль генерирует часть файла, а не наоборот описывается им задним числом.

Обязательные функции, все на чистых целых:

```text
lp(bytes) -> bytes                # length-prefixed сериализация
jcs(obj) -> bytes                 # RFC 8785
sha256_domain(tag, payload)       # LP(tag) || LP(payload)
ratio_cmp(a_num,a_den,b_num,b_den)        # точное сравнение дробей
ratio_within_band(...)                    # cross multiplication, без деления
ten_log10_fixed_q(num, den) -> int        # нормативный fixed-point лог
ceil_div(a, b)                            # (a + b - 1) // b
nearest_rank(L, num, den)                 # max(1, ceil_div(num*L, den))
weighted_nearest_rank(pairs, q_num, q_den)  # накопительное правило 17
mirror_weighted_nearest_rank(...)
bch_encode_15_7(m) / bch_decode_bd2(rx15)    # чистый BCH, см. п.3 ниже
affine_mask(word)                            # XOR 0x000B
gf64_mul                                     # poly 0x43; RS см. обертки ниже
crc32c(bytes)
fixed_sin_q(index, table)                    # только табличный синус
```

RS реализуется одним generic-ядром с обязательными типизированными обертками, потому что концепция содержит два разных укороченных кода с одинаковыми parity-коэффициентами и разной длиной DATA, и подмена одного другим — тихая ошибка ровно того класса, который G0 обязан исключить:

```text
rs_encode_shortened(data, k, n, shortening)   # generic ядро, gen из 18.5,
rs_decode_shortened(...)                      # старшая степень -> свободный член

d0_rs_encode_16_8(data8)        # BOOT: 8 DATA + 8 PARITY, shortening 47
d0_rs_decode_16_8(...)          # именно этим кодом занимается стенд D0
suite_rs_encode_24_16(data16)   # suite transport: 16 DATA + 8 PARITY,
suite_rs_decode_24_16(...)      # shortening 39; в стенде только для
                                # cross-confusion фикстур G5
```

Прямой вызов generic-ядра вне оберток в нормативном коде запрещен и ловится тестом. Golden vectors обеих оберток раздельны: BOOT-вектор 18.6 обязан падать при подаче в suite-обертку и наоборот.

Требования:

1. `ten_log10_fixed_q` задается алгоритмом (целочисленное масштабирование + таблица/итерация с фиксированным rounding и tie rule), а не словом "логарифм"; алгоритм, шаг Q и граничные векторы входят в `integer_semantics.json`. Все DSP-примитивы (округление, синус, окно, true peak, Gram, AWGN, биквад, ресемплер, композиция, cell_id, NMS) определены НЕ здесь, а в нормативном companion; их повторное определение в коде или ТЗ запрещено.
2. Все аккумуляторы имеют объявленную ширину; переполнение objявленной ширины — исключение, не wrap. Python скрывает переполнение, поэтому проверка ширины явная: negative overflow vectors из G0 обязаны падать контролируемо.
3. BCH-декодер чистый и не знает о dual-rail, потому что dual-rail это независимое физическое свидетельство, а смешение слоев в одном API создает скрытую связность реализации и лишает независимую реализацию возможности проверять механизмы порознь. Слои разведены:

```text
bch_decode_bd2(rx15) -> BCH_EXACT | BCH_CORRECTED | BCH_UNCORRECTABLE
dual_rail_decode(observation) -> подпись из смысловых координат
marker_decode(observation)    -> роль маркера либо отсутствие

validate_d0_copy(bch_result, dual_rail_result,
                 marker_result, expected_role)
    -> VALID(value_or_role) | ERASURE | CONFLICT
       | MISCORRECTION_REJECTED
```

В `false_logical_acceptance` участвует ТОЛЬКО выход `validate_d0_copy`; статусы BCH-слоя в него не попадают напрямую. Копийная агрегация 2-из-2 и 2-из-3 работает поверх `validate_d0_copy` пер-копийно.
4. Векторы обязательны при сборке: BCH-таблица ложных исправлений по весам (180/455 при 3 и далее по протоколу), RS-векторы 18.5-18.6, CRC-пары, квантильные ранги для L ∈ {1,3,8,20,100}, взвешенный ранг с неравными весами, интервальное цензурирование, fla-сравнение на границе предела.

---

## 5. Модуль synth

### 5.1. Синтез форм

Вход: `candidate_manifest.json` кандидата (имя строго по реестру §8.2; вариант `d0_candidate_manifest.json` ЗАПРЕЩЕН как отдельный тип и ловится реестром) (частоты, амплитуды, фазы, окна, копийная структура). Выход: канонический WAV 48000 Гц, mono, 24 bit, ровно 48000 отсчетов на токен.

1. Синус только по нормативной fixed-point таблице (четвертьволновая, размер и Q фиксируются в манифесте кандидата; интерполяции нет — фазовая решетка companion §3).
2. Окно — fixed-point таблица из манифеста; fade и форма по разделу 8 протокола, sanity vectors `W1/W2` для N ∈ {48000, 24000, 16000} обязаны воспроизводиться.
3. Копийные структуры четырех кандидатов (`B1` одна полносекундная, `T2` две последовательные, `T3` три последовательные, `F3` три одновременные) реализуются одним параметризованным генератором, а не четырьмя копиями кода.
4. `energy_integer`, `sample_peak_q`, `true_peak_q` (true peak — по нормативной таблице `TP_FIR_Q30` companion §5), `crest_factor_q` вычисляются здесь и записываются в артефакт-БД.

### 5.2. Фазовый оптимизатор

Черновой поиск (минимизация пик-фактора) может использовать float/numpy. Результат — целочисленный вектор фаз — прогоняется нормативным синтезом, и приемка идет только по нормативным `sample_peak_q`/`true_peak_q`. Бюджет оптимизатора (число итераций, seed) — из `optimizer_method_manifest.json`; журнал попыток сохраняется для development attestation.

### 5.3. FEASIBILITY_PREPASS

Реализуется как отдельная команда: для каждого кандидата и каждой из 72 форм вычисляется `E_cap` под общими пиковыми пределами, затем `E_common_cap`, `E_target` и статусы `SYNTHESIS_INFEASIBLE` / `COMMON_ENERGY_INFEASIBLE` строго по разделу 6.1 протокола. Никакая последующая команда не запускается при невыполненном prepass.

### 5.4. Объем

Полный reference-набор описывается двумя разными типами объектов, и смешивать их нельзя:

```text
936 artifact references:
    288 assembled-form references   (72 формы x 4 кандидата)
    648 diagnostic-subform references

864 unique WAV objects после обязательной дедупликации B1,
    потому что assembled форма и diagnostic subform кандидата B1
    ссылаются на один и тот же WAV
```

Артефакт-БД хранит references и WAV-объекты раздельно: reference несет candidate ID, роль и указатель на WAV по его sha256; один WAV может иметь несколько references. Генерация обязана быть детерминированной и идемпотентной: повторный запуск дает побайтно те же 864 файла, что проверяется в CI хешем каталога и счетчиком references 936/864.

---

## 6. Модуль decode и ranking

### 6.1. Оценщик

Согласованные фильтры по оконным базисам кандидата; совместная оценка при неортогональности (Gram matrix из манифеста, решение целочисленно масштабированной системой с фиксированным правилом округления). Native score — только внутренняя диагностика; межкандидатное сравнение — исключительно через `common_failure_reserve_ratio`, реализуемое добавлением калиброванной целочисленной энергии шума к уже полученному наблюдению до порога отказа (двоичный поиск по замороженной сетке уровней, censoring по 9.3 протокола).

### 6.2. Копии и агрегация

Правила 5.2 протокола: у `T2` два обязательных совпадения без RECOVERED, у `T3`/`F3` кворум 2 из 3. Выход по каждой форме: `(aggregate_status, value_or_role)` с полным словарем статусов. Conditional copy-failure matrix накапливается здесь.

### 6.3. false_logical_acceptance

Единый учетчик по разделу 17 протокола: любое принятое неверное `value_or_role`, включая marker/object cross-class и ложную grammar, относится на family текущей ячейки; знаменатель — отказы этой family. Пороговые сравнения только `ratio_cmp`. Статусы `FLA_INSUFFICIENT_FAILURES` — здесь же.

### 6.4. Структурные координаты

Отдельный движок: ladder -> stratum (within_stratum_rule) -> взвешенный квантиль; интервальный статус по правилу "lower bound каждого censored строго больше значения агрегата"; рекурсивное цензурирование; worst-case рядом. Вход — только артефакт-БД и `structural_metric_manifest.json`; никакого доступа к результатам других кандидатов при вычислении одного (защита от связности реализации).

### 6.5. Ranking

Интервальная epsilon-Pareto по трем координатам, затем последовательные метрики 1-10 с `epsilon_j`, `NON_DISCRIMINATING_*`-ветвями и полным протоколированием пути (`development_decision_path.json` и его selection-аналог генерируются одним и тем же кодом с разными входами). `decision_basis`, `selection_policy`, tie-break по `candidate_id` — по разделу 26.

---

## 7. Модуль channel и таксономия strata

### 7.1. Локальные преобразования

Трансформ-движок реализует ПОЛНУЮ обязательную channel-матрицу протокола, а не подмножество; все примитивы — по companion §7-§11: DISCRETE_GAUSSIAN_U16, розовый и shaped шум, notch, low-pass, high-pass, limiter, AGC, sample clipping, burst-стирания, mute и additive burst, клики, crop, insertion, deletion, ресемплинг 44100 и 47952, дрейф частоты дискретизации, AAC/Opus через pinned ffmpeg с bitexact-флагами, повторный transcode, MDCT-смещения, gain, tilt, канальные операции стерео-контракта (dual-mono, downmix, swap, раздельные gain и полярность, межканальная задержка, противофазная примесь) и комбинированные цепочки. Ячейки с насыщением публикуют `saturation_count`, и отчеты всюду разделяют `noise_only_cells` и `noise_plus_saturation_cells`: ячейка с ненулевым счетчиком не попадает ни в одну агрегатную координату без этой метки, потому что ее граница отказа частично является границей клиппинга. Отсутствие любого класса матрицы — блокер A3. Каждая ячейка = (transform chain, параметры, seed) с каноническим cell ID.

Все перечисленные воздействия являются цифровыми пробами устойчивости представления и границ декодера, и только ими. Ни один тест этого стенда не может быть представлен в отчете как валидация тракта динамик-комната-микрофон или аналогового перезахвата; наличие шума, notch, drift или клиппинга в корпусе не является утверждением, что стенд моделирует акустическую среду. Формулировка входит в запрещенные по разделу 32 протокола.

### 7.2. Сетки

`REQUIRED_GRID`, `STRUCTURAL_COMPARISON_GRID`, `BOUNDARY_GRID`, `STRESS_GRID` — генерируются из одного `channel_grid.json`; планировщик умеет: полный прогон, только-стохастические-ячейки для replicate seed sets (u95_k), расширение лестниц по severity в development с журналом.

### 7.3. Таксономия strata — рабочий продукт этапа ТЗ

До development G3 составляется и замораживается массив `structural_metric_manifest.structural_strata[]` (отдельного файла не существует, §8.3): не менее 8 стратов на класс, деление по физической таксономии (для notch — диапазоны положения x ширины; для burst — тип x зона размещения; для combined — семейства сочетаний), веса по умолчанию равные. Состав выводится из channel contract и калибровочного корпуса, без результатов кандидатов. Этот файл — вход preregistration, поэтому его подготовка включена в настоящий этап, а не отложена.

### 7.4. Смета локальной матрицы (ориентир для бюджета, не норматив)

При 8-12 стратах на класс, 4-6 ladder на страту, 6-10 severity-шагов: порядка 1000-2000 структурных ячеек на кандидата, плюс REQUIRED/BOUNDARY/STRESS. Прогон одной ячейки — миллисекунды на декодирование плюс стоимость кодека; полный локальный проход четырех кандидатов — часы, не дни, на одной машине. Числа уточняются в M2 и переносятся в `max_local_channel_jobs`.

---

## 8. Схемы и манифесты

Каждый JSON-объект протокола получает JSON Schema в `schemas/` и генератор/валидатор в `manifests/`.

### 8.1. Машинный реестр

Источником истины является рукописный корневой файл `spec/required_artifacts.lock.json`, который НЕ генерируется ни из чего; `schemas/` и производный `required_artifact_registry.json` проверяются против него. Это устраняет bootstrap-зависимость: случайное удаление схемы не может переписать реестр, потому что lock-файл независим. Реестр, где для каждого объекта заданы: `name`, `schema`, `producer`, `phase`, `required_before_state`, `hash_domain`, `may_contain_secret`, `public_after`. CI сверяет реестр с полным перечнем §8.2: отсутствие любого имени или лишнее имя — падение сборки. State machine отказывает в переходе, если для целевого состояния не существуют все объекты с соответствующим `required_before_state`.

### 8.2. Полный перечень нормативных объектов протокола v6.0

Извлечен из текста протокола автоматически и проверен вручную; wildcards, "x2" и "и т.д." запрещены в этом перечне:

```text
bench_program_manifest.json          canary_manifest.json
candidate_manifest.json              channel_grid.json
common_metric_manifest.json          concept_reference.json
confirmation_holdout_commitment.json confirmation_run_order_resolved.json
context_dependency_resolution_plan.json
cross_family_compatibility_manifest.json
cumulative_exposed_corpus_manifest.json
current_support_manifest.json        d0_profile_manifest.json
d0_rs_test_vectors.json              d0_topology_experiment_manifest.json
declaration_of_independence.json     development_decision_path.json
energy_partition_bias_analysis.json  energy_threshold_derivation.json
equivalence_bands.json               experiment_budget.json
experiment_core_manifest.json        experiment_design_manifest.json
experiment_lineage.json              external_challenge_commitment.json
external_challenge_run_order_resolved.json
external_challenge_scope_schema.json
external_challenge_scope_validation_independent.json
external_challenge_scope_validation_reference.json
external_challenge_transform_grammar.json
final_decision.json                  full_winner_reel_plan.json
full_winner_reel_plan_manifest.json  full_winner_reel_plan_resolved.json
hidden_package_seed_protocol.json    independent_correction_record.json
independent_results_commitment.json  integer_semantics.json
new_program_justification.json       optimizer_method_manifest.json
platform_context_compatibility_manifest.json
platform_control_manifest.json       predecessor_reference.json
preregistration_bundle_manifest.json provisional_decision.json
randomness_beacon_manifest.json      run_order.json
scanner_resource_manifest.json       scanner_spam_manifest.json
selection_holdout_commitment.json    selection_run_order_resolved.json
state_transition_log.jsonl           state_transition_table.json
structural_metric_manifest.json      suite_reserve_manifest.json
survivor_set_manifest.json           tool_versions.json
transport_observer_report.json       youtube_block_count.json
youtube_output_readiness_manifest.json
youtube_qualification_manifest.json
```

Кратность экземпляров (по одному `candidate_manifest.json` на каждого из четырех кандидатов, по три `physical_profile` через `suite_reserve_manifest.json` на survivor) задается полем `cardinality` реестра, а не текстом.

Physical profile отдельным файлом не существует: он является каноническим подобъектом `suite_reserve_manifest.json`, и `physical_profile_hash256` вычисляется по JCS именно этого подобъекта с доменом `GSP4-PHYSICAL-PROFILE`; поле `realizes` реестра фиксирует это соответствие, и замена любого байта подобъекта меняет хеш. Opening-записи протокол называет как evidence без фиксированного имени файла; ТЗ фиксирует имена: `selection_holdout_opening.json`, `confirmation_holdout_opening.json`, `external_challenge_opening.json`. Эти три имени — реализация opening records протокола, что записывается в реестре полем `realizes`.

Объекты уровня ТЗ, отсутствующие в протоколе, помечаются в реестре `origin: TZ` и не могут подменять протокольные: `env_manifest.json`, `youtube_upload_profile.json`, `required_artifact_registry.json`, `spec/required_artifacts.lock.json`, `implementation_error_registry.json`, `dsp_semantics_reference.json` (пинует версию, sha256 и tables_manifest_sha256 нормативного companion), `dsp_tables_manifest.json` (нормативная идентичность набора таблиц по companion §14), `TP_FIR_SOURCE_DECIMAL.txt` (48 исходных десятичных литералов ITU-R BS.1770-5 Annex 2; байтовая норма и SHA-256 по companion §5; в `tables[]` не входит и в инвариант суммарного размера не включается) и девять нормативных бинарных таблиц данных spec package `<table_id>.bin` по companion §14.

### 8.3. structural_strata

`structural_strata` НЕ является отдельным файлом. Это массив `structural_metric_manifest.structural_strata[]` внутри `structural_metric_manifest.json`, как определено разделом 17 протокола, и потому входит в experiment core hash автоматически. Создание отдельного `structural_strata.json` запрещено и ловится реестром: изменение стратов обязано менять нормативный хеш, а вынос их в файл вне design hash открыл бы правку после commitment без следа.

### 8.4. Правила

Schema-валидация обязательна при каждой записи и каждом чтении; неизвестное поле — ошибка; все хеши считаются по JCS; поле с float в нормативном манифесте — ошибка схемы. Сортировка ключей JCS обязана выполняться по массивам беззнаковых UTF-16 code units; использование родного порядка строк Python (сравнение по code points) для ключей JCS ЗАПРЕЩЕНО, поскольку проходит ASCII-тесты и ломается на supplementary-символах; обязательный вектор с символом вне BMP; дубликаты ключей отвергаются НА ГРАНИЦЕ ПАРСЕРА, до преобразования в словарь Python, где информация о дубликате уже потеряна, — обязательный вектор с дубликатом. Тесты JCS-каноникализации и тесты схем разделены: raw-JCS векторы (UTF-16 сортировка, escaping, минус-ноль, числовые границы, дубликаты ключей) проверяют сериализатор на произвольном JSON до всякой схемы; schema-тесты отдельно проверяют, что нормативные манифесты отвергают float и посторонние поля. Минус-ноль обязан пройти raw-JCS тест и быть отвергнут schema-тестом — это два разных теста, и подмена одного другим является дефектом.

---

## 9. Модуль youtube

1. Upload: resumable, профиль полностью задан `youtube_upload_profile.json`: container, audio codec, audio sample rate, channel layout, video codec, pixel format, fps, GOP, metadata policy, moov placement, sha256 ffmpeg-бинаря и полный командный шаблон сборки. Hard invariant концепции: `channel_layout = stereo`, и перед мультиплексированием левый и правый PCM обязаны совпадать побитово (dual mono, L = R); несовпадение — `UPLOAD_PROFILE_INVALID`, загрузка не выполняется. Значение `mono` в профиле — ошибка схемы. После платформы L и R могут различаться, и это законный вход decoder hypotheses, но на входе тракта равенство обязательно. Видеослой из frozen generator (одна статичная картинка + тайм-код, побитово одинаковый elementary stream внутри блока); privacy `unlisted`; никакие секреты не сериализуются. Кодек загрузки НЕ является выходным кодеком YouTube и нигде не трактуется как таковой. Семантика resumable-сессии фиксирована: session URI сохраняется персистентно до первого PUT; 308 — не ошибка, а штатное состояние resumable-передачи: реализация читает заголовок Range и продолжает с первого неподтвержденного байта, атомарно сохраняя подтвержденный Range после каждого 308; retryable-ошибки — 5xx с уважением Retry-After, иначе экспоненциальный backoff из манифеста; исчерпание max_retries или истечение сессии закрывает ПОПЫТКУ, создание новой сессии — новая попытка с записью в лог, обе учитываются в upload_span_limit; после успешной загрузки до записи video_id восстановление идет поиском по уникальному title-токену попытки, а не повторной загрузкой; повторная загрузка при существующем video_id запрещена.
2. Readiness polling по `youtube_output_readiness_manifest.json`: расписание опросов, fingerprint выбранного itag, `STABLE_READY` по числу стабильных наблюдений; таймаут -> `PLATFORM_BLOCK_INVALID`.
3. Download: yt-dlp с фиксированными параметрами формата; извлечение канонического PCM pinned ffmpeg; все хеши цепочки (source video/audio, downloaded, extracted) — в БД.
4. Platform context: hard-поля и soft-совместимость по 19.5; смена — `PLATFORM_CONTEXT_CHANGED` с остановкой попытки.
5. Блоки: генератор расписания из `run_order.json` (ротация латинского порядка), контроль `upload_span_limit_hours`, `PLATFORM_CONTROL-1` pre/mid/post, EWMA-карта дрейфа, статусная логика 19.6.
6. Paired против standalone — исполняемый workflow, а не только схема. Отдельные команды собирают paired comparison reel и standalone qualification loads, вычисляют `paired_standalone_delta` точной арифметикой, выставляют `CONTEXT_DEPENDENT` при превышении преregистрированного предела и исполняют `context_dependency_resolution_plan.json` с исходом `CONTEXT_RESOLVED` либо `CONTEXT_UNRESOLVED`. Acceptance-фикстура A4 обязана содержать намеренный случай, где paired проходит, а standalone нет, доказывая достижимость `CONTEXT_DEPENDENT` и фактический запуск resolution plan; без этой фикстуры A4 не считается пройденным.
7. Ничего в этом модуле не принимает решений о кандидатах; он производит артефакты и статусы блока.

---

## 10. Модуль scanner

Потоковый двухстадийный сканер по разделу 21: тайловая NMS, round-robin гипотез, неперераспределяемые квоты, вывод evidence в нормативном порядке, `RESOURCE_LIMIT`-статусы, отменяемость с измеряемой латентностью. Все пределы — только из `scanner_resource_manifest.json`; ни одного захардкоженного лимита. Spam-corpus генератор — по `scanner_spam_manifest.json`, включая обязательные случаи из 21.5.

---

## 11. Модуль statemachine

1. Состояния и переходы — таблица из `state_transition_table.json`, движок не содержит имен состояний в коде.
2. Каждый переход — append-only запись в `state_transition_log.jsonl` с prev/next/event/hashes/UTC и записью lineage.
3. Commit-beacon-reveal — не утилита, а state-контракт, потому что весь смысл церемонии в невозможности выбрать удобный результат. Обязательные элементы по разделу 10.3 протокола: future target pulse, custodian secret nonce не короче 32 байт, commitment nonce ДО pulse, primary beacon и упорядоченные fallback beacons, каноническая сериализация pulse, три раздельных дедлайна (beacon, package, reveal), package-specific domain, one-shot генерация, верификация commitment и reveal, generated case-ID vectors. API обязан делать нарушения невозможными, а не задокументированными:

```text
ceremony.commit_nonce(role)          # отказывает, если target pulse
                                     # уже опубликован или прошел
ceremony.fetch_pulse(role)           # только по расписанию manifest;
                                     # fallback в зафиксированном порядке
ceremony.generate_package(role)      # отказывает без верифицированного
                                     # pre-pulse nonce commitment;
                                     # повторный вызов для той же пары
                                     # (experiment_design_hash, role) —
                                     # терминальная ошибка эксперимента,
                                     # не повтор
ceremony.reveal(role)                # только внутри reveal deadline
```

Однократность обеспечивается персистентной записью в `state_transition_log.jsonl` до начала генерации (write-ahead) с fsync до необратимого действия, поэтому падение процесса между записью и генерацией тоже не дает второй попытки. Против отката из резервной копии ('generate еще не вызывался') до открытия первого holdout обязателен внешний anti-rollback якорь: подписанный checkpoint хеша головы лога, размещенный минимум одним из способов, не контролируемых оператором единолично: независимый custodian, immutable версионируемый удаленный объект, метка времени RFC 3161, публичный append-only репозиторий либо артефакт preregistration на OSF или Zenodo; локальный файл или NAS того же оператора якорем не является; расхождение головы с якорем — терминальная ошибка эксперимента. Пропуск любого дедлайна — терминальный статус по протоколу. Acceptance-фикстуры A5-набора обязаны включать: попытку commit после pulse, попытку generate без commitment, повторный generate — все три обязаны отказывать.
4. Бюджеты: единый учетчик потребления против манифеста; исчерпание любого — событие автомата, не warning.
5. Опасные команды CLI (открытие holdout, freeze) требуют интерактивного подтверждения строкой-фразой и пишут подписанный маркер.

---

### 11.5. Логическая схема хранилища

Обязательные таблицы и ключи уникальности (физическая реализация свободна, логика нормативна): `artifact_object(sha256 PK)`, `artifact_reference(candidate, role, form_id, wav_sha256, UNIQUE(candidate, role, form_id))`, `channel_cell(cell_id PK)`, `observation(UNIQUE(candidate_hash, form_id, cell_id, replicate_id))`, `copy_decision(UNIQUE(candidate_hash, form_id, cell_id, replicate_id, copy_index, phase))`, `aggregate_decision(UNIQUE(candidate_hash, form_id, cell_id, replicate_id, phase))`, `manifest(name, hash, UNIQUE(name, hash))`, `state_event(seq PK монотонный)`, `youtube_block(block_id PK)`, `resource_consumption(budget_name, UNIQUE per event)`. Нарушение уникальности — `DB_CONFLICT`, а не тихое обновление: повторный запуск не имеет права задваивать статистику.

### 11.6. Идемпотентность команд

Покомандно: `synth`, `channel run`, `structural`, `rank`, `report` — идемпотентны по хешам зависимостей: совпадение всех входных хешей возвращает существующий артефакт без новой записи исполнения. `youtube upload` НЕ идемпотентен никогда: каждый вызов — новая попытка в логе, повтор при существующем video_id — отказ. `youtube download` идемпотентен по (video_id, itag, версия yt-dlp). `state advance`, `commit`, `open` — строго однократны по построению §11.3.

### 11.7. Реестр технических ошибок

Технические ошибки реализации отделены от научных статусов протокола и живут в `implementation_error_registry.json`: `INVALID_MANIFEST`, `DEPENDENCY_HASH_MISMATCH`, `CANONICALIZATION_ERROR`, `ARITHMETIC_OVERFLOW`, `EXTERNAL_TOOL_FAILED`, `CODEC_OUTPUT_INVALID`, `DB_CONFLICT`, `ARTIFACT_HASH_MISMATCH`, `UPLOAD_PROFILE_INVALID`, `REGISTRY_MISMATCH`. CLI exit codes отображаются из этого реестра; записывать технический код в поле научного статуса — ошибка схемы, симметрично правилу A*/G*.

Пространство состояний этого реестра ограничено исполнением, валидацией и проверкой реализации. Дефект DRAFT-редакции спецификации сюда не заносится, если ни один артефакт, evidence или решение не были порождены под этой редакцией; его история фиксируется неизменяемостью редакций, полем предыдущей версии с ее SHA-256 и changelog. Триггер перехода в реестр объективен и не зависит от оценки серьезности: дефект регистрируется как техническая ошибка, если существует хотя бы один порожденный объект, пинующий дефектную редакцию по SHA-256 — нормативная таблица spec package, `dsp_semantics_reference.json`, любой манифест, отчет, gate evidence или запись БД. В этом случае регистрируется фактический технический код, запись ссылается на пару SHA-256 дефектной и исправленной редакций, а затронутые результаты инвалидируются по общим правилам. Отсутствие подходящего кода в перечне выше не является основанием не регистрировать: перечень расширяется, а не обходится.

## 12. Граница независимой реализации

Разрешено передавать второй стороне: протокол, концепцию, нормативный DSP companion `d0_bench_integer_dsp_semantics_v*.md` СО ВСЕМИ его нормативными таблицами данных и их хешами (это общая спецификация, а не код), все `schemas/`, `integer_semantics.json`, публичные golden vectors, `env_manifest.json` (pinned ffmpeg/yt-dlp как общие внешние бинари — это разрешено разделом 23), corpus-задания от `d0bench-xport`, замороженные входные артефакты.

Запрещено: любой файл из `src/`; любые таблицы или векторы, сгенерированные reference-реализацией и НЕ опубликованные в spec package (различие нормативно: shared normative table разрешена, reference implementation output запрещен); тексты промптов/сессий, при которых генерировался reference-код, черновики оптимизатора, reference per-cell результаты до `independent_results_commitment.json`.

`d0bench-xport` собирает передаваемый пакет одним архивом с манифестом содержимого и хешем; попадание запрещенного пути в архив — тест CI.

---

## 13. Implementation acceptance A0-A8

Таблица ниже описывает приемку РЕАЛИЗАЦИИ, а не экспериментальные gate. Ни один статус A0-A8 не является экспериментальным статусом G0-G8, не создает gate evidence и не имеет права изменять состояние experiment state machine. Идентификаторы A* и G* живут в разных пространствах имен кода и БД; попытка записать A-статус в поле G-статуса — ошибка схемы. G0-G8 возникают только при выполнении соответствующей фазы протокола на соответствующих протокольных данных.

| Harness | Тест приемки реализации |
| --- | --- |
| A0-MATH-HARNESS | все golden vectors раздела 4 совпали побитово; overflow-negative падают; повторная сборка `vectors/` идемпотентна; crosscheck по §13.1 сошелся |
| A1-SYNTH-HARNESS | prepass на четырех кандидатах воспроизводит `E_cap`/`E_target` фикстур; `SYNTHESIS_INFEASIBLE`-фикстура отрабатывает |
| A2-CLEAN-HARNESS | encode->decode всех 936 references без канала, ноль ошибок; счетчики 936/864 сходятся; отрицательный корпус — ноль ложных записей |
| A3-CHANNEL-HARNESS | каждая transform-ячейка детерминирована (повторный прогон — тот же хеш); структурный движок проходит synthetic ranking corpus целиком, включая инвариантность к удвоению ячеек страты; A3 проваливается при отсутствии ЛЮБОЙ обязательной temporal-boundary метрики (pre_echo_energy_ratio_db, post_echo_energy_ratio_db, smear_duration_samples, boundary_copy_margin_before, boundary_copy_margin_after) либо любой требуемой семьи MDCT-смещений относительно внутренних границ копий |
| A4-YOUTUBE-HARNESS | dry-run блока на loopback-кодеке: расписание, readiness, control-логика, инвалидация блока, обязательная фикстура `CONTEXT_DEPENDENT` с исполнением resolution plan |
| A5-SUITE-HARNESS | cross-confusion прогон фикстурных профилей; условия `SUITE_PROFILE_PASS` достижимы тестами; фикстуры отказов церемонии §11.3 |
| A6-SCANNER-HARNESS | scanner проходит обязательный spam-набор в заданных лимитах; cancellation latency измерена |
| A7-CONFIRMATION-HARNESS | winner-plan исполнитель собирает reel по плану фикстуры и сверяет superset хешей |
| A8-INDEPENDENT-HANDOFF-READINESS | `d0bench-xport` собирает пакет; schema round-trip; внутрипроектный мини-декодер совпадает на 16 формах |

Соответствие "harness обеспечивает готовность к gate" (enables, не equals):

```text
A0 -> G0    A1 -> G1    A2 -> G2    A3 -> G3
A4 -> G4    A5 -> G5    A6 -> G6    A7 -> G7    A8 -> G8
```

Настоящий G4 — это реальные преregистрированные YouTube-блоки со `STABLE_READY` и platform controls; настоящий G5 — immutable suite-профили и sealed cross-confusion cases; настоящий G7 — winner-only confirmation на отдельном holdout с полным YouTube winner corpus; настоящий G8 — исполнение независимой реализацией другой стороны: другой автор, другой код, без общего design context. Loopback-прогон A4 не дает права ни на какую формулировку вида "G4 PASS".

### 13.1. Граница G0-crosscheck

Требование протокола о двух математических реализациях для G0 не закрывается вторым вызовом тех же функций. `tools/g0_crosscheck/` — отдельная мини-реализация со своей границей: не импортирует ничего из `src/d0bench`; не читает сгенерированные reference-таблицы; получает на вход только протокол, нормативный DSP companion с его таблицами данных, `integer_semantics.json` и публичные векторы; содержит собственные реализации BCH, GF(64), RS, JCS, LP, квантилей и граничной арифметики; ее code hash фиксируется в отчете A0 до первого сравнения. Это еще не внешний G8, но это настоящая implementation diversity для G0, а не тавтология. Нарушение границы (любой import из `src/`) — падающий тест CI.

CI: unit + golden на каждый коммит; A-harnesses — на тег. Ни один нормативный модуль не мержится без своего golden-теста.

---

## 14. CLI

```text
d0bench math verify                     # A0
d0bench synth all|--candidate X         # 936 references -> 864 WAV;
                                        # acceptance: оба счетчика
d0bench prepass                         # A1, E_target
d0bench channel run --grid ... --phase development|selection
d0bench structural aggregate|u95
d0bench rank --input ... --emit decision-path
d0bench youtube block plan|upload|poll|download|close
d0bench youtube paired --block ...
d0bench youtube standalone --block ...
d0bench youtube compare-context --block ...
d0bench youtube resolve-context --plan ...
d0bench scanner run|spam
d0bench state show|advance --event ...
d0bench commit design|holdout|challenge
d0bench open selection|confirmation     # с фразой подтверждения
d0bench report final|freeze-package
d0bench xport independent-kit
```

Каждая команда: exit code по статусу, машинный JSON в stdout при `--json`, полный лог в файле, никакой интерактивности кроме опасных подтверждений.

---

## 15. Вехи и смета

| Веха | Содержание | Оценка |
| --- | --- | --- |
| T0 | сборка и заморозка нормативных таблиц companion, вписывание их SHA-256, публикация spec package | дни, при нормативной публикации |
| M0 | exactmath + все golden vectors + схемы ядра (A0) | 1-2 недели |
| M1 | synth + prepass + clean decode (A1-A2) | 1-2 недели |
| M2 | channel + strata + структурный движок + ranking (A3) | 2-3 недели |
| M3 | scanner + spam corpus (A6) | 1-2 недели |
| M4 | youtube workflows + блоки + контроль дрейфа (A4) | 2 недели + календарное время pilot-загрузок |
| M5 | statemachine + commitments + все манифесты + отчеты (A5, A7, A8) | 2 недели |
| M6 | полный development-проход; фактическое потребление против опубликованных верхних бюджетов | по факту |

Правило stop-and-verify: после M0 работа останавливается до побитового совпадения golden-векторов с `tools/g0_crosscheck/` в границе §13.1. Если спецификация где-то неисполнима, это выяснится здесь, а не на YouTube.

Смета в единицах протокола (для будущего программного манифеста, уточняется на M2/M6): 936 reference-артефактов; 12 suite-профилей; локальная матрица порядка 10^4 ячеек-прогонов на полный development-проход; YouTube — `B_required(n)` блоков по 19.1 плюс pilot и winner-plan; календарное окно selection ≤ 28 дней.

### 15.1. Порядок относительно программного манифеста

Действует порядок раздела 34 протокола без изменений: `bench_program_manifest.json` публикуется до начала реализации (шага 5). Прежняя редакция этого параграфа, объявлявшая перестановку шагов "задокументированной интерпретацией", удалена как прямое нарушение собственных правил стека: ТЗ не имеет полномочий переставлять нормативные шаги протокола, и такой пункт создавал бы `PROTOCOL_CONFLICT` в момент публикации.

Проблема честной оценки бюджетов до реализации решается внутри правил, а не их обходом: манифест публикуется с ЖЕСТКИМИ ВЕРХНИМИ бюджетами, назначенными консервативно из сметы раздела 15 этого ТЗ (само ТЗ данных кандидатов не касается и data-influenced tuning не является). Верхний бюджет законно недорасходовать; его нельзя увеличить после публикации. Если M0-M2 покажут, что какой-либо верхний бюджет назначен ниже реальной потребности, это обрабатывается как исчерпание бюджета по правилам протокола, а не тихой правкой манифеста. Уточненные оценки M2/M6 публикуются как информативные приложения к отчетам, не изменяя манифест.

---

## 16. Определение готовности

Реализация не начинается до публикации `bench_program_manifest.json` с верхними бюджетами по §15.1. Стенд готов к development-фазе (шаг 7 раздела 34), когда: все harness A0-A3 и A6 зелёные; A4 зелёный; фактическое потребление укладывается в опубликованные верхние бюджеты; `structural_metric_manifest.structural_strata[]` заморожен; `d0bench-xport` собирает независимый пакет без запрещенных путей.
