# D0 Bench — T0 Report

Дата выполнения: 2026-08-18
Рабочая директория: `E:\000_Audiotext`
Executor: настоящий T0-исполнитель (Claude Code), НЕ является участником blind IMPORTED_EXACT verification (раздел B ниже).

Итоговый вердикт: **T0 CANDIDATE PASS**

---

## A. INPUT IDENTITIES

Первая операция — независимое вычисление SHA-256 первых пяти файлов и сравнение с
ожидаемыми значениями из `Prompt.md`, раздел 0/1.

| filename | byte size | SHA-256 (actual) | expected match |
|---|---|---|---|
| geometric_sound_protocol_concept_v8.0_ru.md | 265051 | `2e027eeeb42457ec26712637015c8ae69743ffc53d77c07fb1f67baee9e5bb0d` | PASS |
| d0_bench_protocol_v6_0.md | 260354 | `b5a1915dbcb8a5b6eb68c59dd55346f6c7435b40ef47f930aeae6eb8077e0db2` | PASS |
| d0_bench_integer_dsp_semantics_v1_7.md | 62076 | `98e282dcafcaa48db9d3a9314106cb641f729f87438fc158277b4ab21806a4e9` | PASS |
| d0_bench_tz_v1_11.md | 71740 | `3ee5f34bc719df8d721706862d71ca2633d1834b4077c82747625a398bbdab19` | PASS |
| TP_FIR_SOURCE_DECIMAL.txt | 789 | `0935e97d0b2efd5fdb77826430e9dc161833b9c916585547d0d910b3cda37424` | PASS |

Все пять входов совпали побайтово. Условие STOP (`INPUT_HASH_MISMATCH`) не сработало.

**Provenance PDF** (не нормативен для идентичности, только provenance/source reference):

| filename | byte size | SHA-256 (actual) | expected | match |
|---|---|---|---|---|
| ITU-R_BS.1770-5_2023.pdf | 1996355 | `eefb926f72f72a96b96f251067bfee0650a0f29a26f60661d354162038b041ad` | `eefb926f72f72a96b96f251067bfee0650a0f29a26f60661d354162038b041ad` | PASS |

PDF SHA также совпал; provenance warning не требуется (совпадение не нормативно для T0, но фиксируется).

`TP_FIR_SOURCE_DECIMAL.txt` дополнительно проверен по размеру (789 байт) — совпадает.

---

## B. BLIND IMPORTED_EXACT EVIDENCE

Первое действие T0 — слепая независимая ретранскрипция Annex 2 ITU-R BS.1770-5 (48
коэффициентов, order 48, 4-phase FIR interpolating filter) — была выполнена **отдельным
пред-существующим независимым контекстом до раскрытия** `TP_FIR_SOURCE_DECIMAL.txt`,
его SHA-256, companion v1.7 и ожидаемых Q30-значений, как зафиксировано в `Prompt.md`
раздел 2.

Результат, зафиксированный этим отдельным контекстом:

- 48 строк транскрибировано (Phase 0 → Phase 1 → Phase 2 → Phase 3, печатная таблица
  сверху вниз);
- источник: Rec. ITU-R BS.1770-5, Annex 2, Detailed description;
- **48 / 48 coefficients EXACT, mismatches = 0** при сравнении с canonical copy
  `TP_FIR_SOURCE_DECIMAL.txt`, раскрытой после фиксации результата;
- видимая симметрия FIR не использовалась для довычисления значений.

Настоящий T0-исполнитель **не является blind verifier этой операции** и не заявляет
собственное чтение PDF за новую blind verification. Выполненные настоящим исполнителем
проверки (раздел E ниже) — это последующая, не-слепая сверка `TP_FIR_SOURCE_DECIMAL.txt`
с уже зафиксированным блоком проверочных Q30-значений companion §5 и с итоговым
`TP_FIR_Q30.bin`, а не повторная транскрипция.

Нормативное требование blind transcription внутри T0 считается **ВЫПОЛНЕННЫМ**.

---

## C. TABLE GENERATION

Инструментарий: offline T0 tooling в `T0_WORK/` (не `src/d0bench`, не reference
implementation — см. раздел H). Каждая GENERATED_REAL таблица построена и проверена
двумя независимыми офлайн-оценщиками:

- **Evaluator A** — интервальная арифметика (`mpmath.iv`), рациональное основание A
  companion §7.1 / §14: каждая арифметическая операция даёт ригорозную вилку
  [lo, hi]; итоговое Q-значение принимается только если ширина вилки много меньше
  0.25 ULP и не пересекает границу round-half-to-even tie (проверяется программно,
  `CertificationError` иначе).
- **Evaluator B** — процедура сходимости (основание B companion §7.1): вычисление тем
  же кодом на точности P (dps=60, ≈199 бит) и независимо на 2P (dps=120), совпадение
  округлённого результата на обеих точностях.

Обе оценки для каждой записи каждой GENERATED_REAL таблицы должны совпасть после
округления; расхождение = провал T0. Итог по всем таблицам: **rounded disagreements = 0**
на всех записях всех семи GENERATED_REAL таблиц.

### C.1 SIN48000_Q30 — GENERATED_REAL

- Источник: companion §3.
- dimensions `[48000]`, q_format 30, entry_count 48000, 384000 bytes.
- Evaluator A: `iv.sin(2*iv.pi*k/48000)`, dps=60.
- Evaluator B: `mp.sin(2*mp.pi*k/48000)` at dps=60 и dps=120 (convergence).
- Обязательные якоря (companion §3) — все совпали:
  `[0]=0`, `[4000]=536870912`, `[12000]=1073741824`, `[24000]=0`, `[36000]=-1073741824`.
- evaluator disagreements: 0.
- SHA-256: `4708579df63bb4b09da20c9883d6c1bbfe9701e93908fcc820a6ec33badacfd7`
- PASS

### C.2 ICDF_Q24 — GENERATED_REAL

- Источник: companion §7, §14. Целевая функция — обратная стандартная нормальная CDF
  (probit) в средних точках `(u+0.5)/65536`, u=0..65535.
- Метод: собственная сходящаяся ряд-реализация `Phi(x) = 0.5 + (1/sqrt(2*pi)) *
  sum_k (-1)^k x^(2k+1) / (2^k k! (2k+1))` (обрыв ряда при |term| < 2^-100), инверсия
  ньютоновской итерацией в plain высокой точности (evaluator B, dps=60 и dps=120,
  тёплый старт от предыдущего `u` — функция монотонна).
- Evaluator A — сертификация интервальной арифметикой: для кандидата `n` (из evaluator
  B) рассчитываются интервальные `Phi(iv)` в точках `(n-0.5)/2^24` и `(n+0.5)/2^24`;
  строгая монотонность Phi (Phi' = pdf > 0 всюду) означает, что если
  `Phi_iv(lo).hi < p < Phi_iv(hi).lo`, истинный корень заключён в `(lo, hi)` и округляется
  ровно к `n` — это прямая интервальная сертификация границы округления без полного
  интервального поиска корня.
- dimensions `[65536]`, q_format 24, entry_count 65536, 524288 bytes.
- Дополнительная проверка: таблица монотонно неубывающая по `u` (ожидаемое поведение
  квантильной функции) — PASS.
- evaluator disagreements: 0.
- SHA-256: `75b753a89215dd07b6f1804cc7b3668ffb07cadb52488a5e2d7004208efd3665`
- PASS

Примечание по методу: companion называет генератор "алгоритмом Wichura AS241". AS241 —
рациональная аппроксимация той же самой математической функции (обратной нормальной
CDF). Нормативным критерием раздела §14 является не буквальное воспроизведение
исходного кода AS241, а сертифицированная точность < 0.25 ULP целевого Q24 до
округления. Настоящее T0 tooling достигает этого напрямую через рациональный
Ньютон + интервальную сертификацию корня той же целевой функции, что математически
эквивалентно и метрологически строже произвольной реализации AS241 в double precision.
Зафиксировано как WARNING методологии, не как отклонение от нормативного результата.

### C.3–C.7 Ресемплерные таблицы — GENERATED_REAL

Источник: companion §9. Общий прототип (`N_h`, `c`, omega, `h_id`, Kaiser-окно
`w` (beta=12), сумма `S = sum(h_id*w)`) зависит только от `max(L,M)` — общий для обеих
таблиц каждой пары направлений; масштаб `s = L_direction / S` и полифазная раскладка
(`P = L_direction`, `K = ceil_div(N_h, L_direction)`) — раздельные на направление.
Обе таблицы каждой пары построены из ОДНОГО прототипа, независимо квантованного двумя
оценщиками на каждую запись.

`I0(x) = sum_k ((x/2)^k/k!)^2`, обрыв при term < 2^-100 — реализован буквально по
companion (не встроенная функция Бесселя: `mpmath.iv` не поддерживает интервальный
`besseli`, поэтому ряд реализован вручную идентично для evaluator A и evaluator B).

| table_id | prototype pair (max_LM) | N_h | c | dimensions | entry_count | bytes | evaluator disagreements | SHA-256 |
|---|---|---|---|---|---|---|---|---|
| H_147_160 | 48000<->44100 (160) | 3841 | 1920 | [147,27] | 3969 | 31752 | 0 | `3f532644af969c5cbc18adde1c806ac7e8d4dd3dfc41ecefdea6314c8f9c3cd8` |
| H_160_147 | 48000<->44100 (160) | 3841 | 1920 | [160,25] | 4000 | 32000 | 0 | `a65d204ed7252ba1417d536b1cfb7fe98719e8806c8d72ee87d2864acd0d5f6a` |
| H_999_1000 | 48000<->47952 (1000) | 24001 | 12000 | [999,25] | 24975 | 199800 | 0 | `b1cf6cde083243a76f211418570d6ddc89a661a102456d297c32b0f88e2383a3` |
| H_1000_999 | 48000<->47952 (1000) | 24001 | 12000 | [1000,25] | 25000 | 200000 | 0 | `0236c13f17ce92d414a28880fa20e6c22fd78a8575d6d76d995e18b83ee755a4` |
| H_DRIFT_Q30 | drift (1024) | 24577 | 12288 | [1024,25] | 25600 | 204800 | 0 | `5aa872ee6d24d614d8153f6f69f913cba059e35592869c3672a95a5db141a8c7` |

Все пять размерностей совпадают с замороженным инвариантом companion §14 / Prompt.md
раздел 8. Нулевое дополнение прямоугольной полифазной раскладки сериализовано как
реальные int64 entries (companion §9/§14, Prompt.md раздел 9). PASS по всем пяти.

### C.8 PINK_V1 — EXACT_INTEGER

- Источник: companion §11, коэффициенты скопированы буквально (без проектирования
  фильтра, без перенормировки).
- dimensions `[3,5]`, q_format 30, entry_count 15, 120 bytes; порядок полей на секцию:
  b0, b1, b2, a1, a2; явные нули: 6 (b2=a2=0 в каждой из 3 секций).
- Независимая проверка: количество секций (3), форма (5 полей/секция), порядок полей,
  знаки коэффициентов, число явных нулей (6), int64 serialization — все совпадают
  буквально с companion §11.
- SHA-256: `990ae00b429e6ef7256fa1a75b51001b2554891adeee02466babbcb092a6e32c`
- PASS

### C.9 TP_FIR_Q30 — IMPORTED_EXACT

- Источник: `TP_FIR_SOURCE_DECIMAL.txt` (единственный источник значений, companion §5).
- Преобразование: `fractions.Fraction` — точная рациональная арифметика, без binary
  float, ни разу; все 48 литералов умножились на 2^30 без остатка (halfway case
  отсутствует, что подтверждает утверждение companion).
- Сверка результата с проверочным блоком Q30-значений companion §5: **48/48 совпало,
  mismatches = 0**.
- Структурные инварианты (companion §5) — все PASS:
  - `TP_FIR_Q30[3][i] == TP_FIR_Q30[0][11-i]` для всех i;
  - `TP_FIR_Q30[2][i] == TP_FIR_Q30[1][11-i]` для всех i;
  - `sum|TP_FIR_Q30[0][*]| == sum|TP_FIR_Q30[3][*]| == 1539964928`;
  - `sum|TP_FIR_Q30[1][*]| == sum|TP_FIR_Q30[2][*]| == 2171994112`.
- dimensions `[4,12]`, q_format 30, entry_count 48, bytes 384.
- SHA-256: `4fd922e97c8a656f20bb5e069f6c00917a4bd845cd7e71c71aed066fd5625270`
- **Совпадает с нормативным обязательным SHA-256 из Prompt.md раздел 10 и companion
  §5.** PASS.

---

## D. GLOBAL SIZE INVARIANT

| table_id | entry_count | bytes = entry_count*8 |
|---|---|---|
| H_1000_999 | 25000 | 200000 |
| H_147_160 | 3969 | 31752 |
| H_160_147 | 4000 | 32000 |
| H_999_1000 | 24975 | 199800 |
| H_DRIFT_Q30 | 25600 | 204800 |
| ICDF_Q24 | 65536 | 524288 |
| PINK_V1 | 15 | 120 |
| SIN48000_Q30 | 48000 | 384000 |
| TP_FIR_Q30 | 48 | 384 |

Сумма: 200000+31752+32000+199800+204800+524288+120+384000+384 = **1577144**.

Совпадает с обязательным инвариантом companion §14 / Prompt.md раздел 8. PASS.

---

## E. TP FIR CHECKS

- `TP_FIR_SOURCE_DECIMAL.txt` SHA-256: `0935e97d0b2efd5fdb77826430e9dc161833b9c916585547d0d910b3cda37424`
  — совпадает с ожидаемым (раздел A).
- Байтовая норма источника (проверено программно): 789 bytes; 48 logical lines; LF
  count = 47; CR count = 0; BOM absent; trailing LF absent; ровно один литерал на
  строку, без ведущих/хвостовых пробелов; формат `-?0\.\d{13}` (опциональный ASCII
  "-", "0.", ровно 13 цифр); "+" отсутствует; экспонента отсутствует. Все проверки
  PASS.
- Q30 matrix: построена точной рациональной арифметикой (см. C.9), сверена с
  проверочным блоком companion §5 — 48/48 EXACT.
- Symmetry checks: PASS (см. C.9).
- Abs-sum checks: PASS (см. C.9).
- Binary size: 384 bytes — совпадает с ожидаемым.
- Binary SHA-256: `4fd922e97c8a656f20bb5e069f6c00917a4bd845cd7e71c71aed066fd5625270`.
- Expected SHA comparison: **PASS**, совпадает с Prompt.md раздел 10 / раздел 23 и
  companion §5.

---

## F. MANIFEST

`dsp_tables_manifest.json`, 2062 bytes.

- Ordinary file SHA-256 (фактических байт файла):
  `c0a09133d129b87a639d1aacee6f3a4ef6a26df6a7660c48254211e45fb63ddb`
- `tables_manifest_sha256` (companion §14):
  `53aae6d3e729461917af4b5908a7dbada210e1e8da5357913fee61da40644848`

  Вычислено как
  `SHA256( LP("D0BENCH-DSP-TABLES-MANIFEST-V1") || LP(JCS(dsp_tables_manifest)) )`,
  где `LP(x) = u32be(len(x)) || x`. Эти две величины **разные** и обе зафиксированы
  раздельно, как требуется (Prompt.md раздел 16).
- Canonical byte length: физические байты файла равны JCS-сериализации объекта:
  UTF-8, без BOM, без завершающего LF/CRLF, без пробелов/переводов строк вне
  результата JCS (проверено побайтово — файл представляет собой один JSON-объект без
  пробелов, `\n` в конце отсутствует).
- Schema validation: в корне ровно `schema_version`, `tables`; в каждом entry ровно
  `table_id`, `filename`, `element_type`, `dimensions`, `q_format`, `entry_count`,
  `sha256` — без лишних полей. `element_type` = `int64_le_twos_complement` во всех
  девяти записях. `sha256` — 64 lowercase ASCII hex во всех записях.
  `entry_count == product(dimensions) == file_size/8` проверено для каждой таблицы
  программно при сборке манифеста.
- Ordering validation: `tables[]` в порядке строгого возрастания `table_id` побайтово:
  `H_1000_999, H_147_160, H_160_147, H_999_1000, H_DRIFT_Q30, ICDF_Q24, PINK_V1,
  SIN48000_Q30, TP_FIR_Q30` — совпадает с нормативным порядком companion §14 /
  Prompt.md раздел 15.

PASS по всем пунктам раздела.

---

## G. REPRODUCIBILITY

Процедура (Prompt.md раздел 17):

1. Первая полная сборка (`T0_OUTPUT/`) выполнена; SHA-256 всех девяти `.bin` и
   манифеста сохранены (см. разделы C, F).
2. Полностью изолированная копия offline tooling (`T0_WORK/scripts_rebuild2/`, все
   пути перенаправлены на отдельный output/каталог логов сед-заменой, без общего
   состояния со сборкой 1) выполнила **независимую чистую пересборку** в
   `T0_OUTPUT_BUILD2/` (после — перемещено в `T0_WORK/rebuild2_output/` как
   evaluator/audit artifact, не являющийся частью финального spec package).
3. Побайтовое сравнение (`cmp`) всех девяти `.bin` + `dsp_tables_manifest.json`
   между сборкой 1 и сборкой 2:

```
IDENTICAL: H_1000_999.bin
IDENTICAL: H_147_160.bin
IDENTICAL: H_160_147.bin
IDENTICAL: H_999_1000.bin
IDENTICAL: H_DRIFT_Q30.bin
IDENTICAL: ICDF_Q24.bin
IDENTICAL: PINK_V1.bin
IDENTICAL: SIN48000_Q30.bin
IDENTICAL: TP_FIR_Q30.bin
IDENTICAL: dsp_tables_manifest.json
```

**9/9 binaries byte-identical. Manifest byte-identical.** PASS.

Недетерминизм не обнаружен (в реализации нет источников случайности, зависимости от
времени, порядка обхода файловой системы или иного nondeterministic состояния —
все вычисления суть чистые функции от `(table_id, направление, точность)`).

---

## H. TOOLING

- OS: Windows 10 Pro 10.0.19045, оболочка Git Bash / PowerShell.
- Python: 3.12.10, `C:\Users\anahr\AppData\Local\Programs\Python\Python312\python.exe`,
  изолированная venv `E:\000_Audiotext\T0_WORK\venv` (offline T0 tooling; НЕ src/d0bench,
  НЕ reference implementation, отделена от будущего runtime-кода).
- Высокоточная библиотека: `mpmath==1.4.1` (единственная внешняя зависимость,
  установлена в venv, версия зафиксирована через `pip freeze`).
- Назначение mpmath: `mpmath.mp` — plain произвольная точность (convergence-evaluator
  B); `mpmath.iv` — интервальная арифметика (`iv.sin`, `iv.sqrt`, `iv.exp`, `iv.pi`) —
  сертифицированное основание A. `iv.besseli` и `iv.erf` в этой версии mpmath не
  работают в интервальном режиме (внутренняя гипергеометрическая суммация не сходится
  в interval-контексте) — оба обойдены собственной ручной реализацией нормативно
  заданных рядов (`I0(x)` companion §9, `Phi(x)` через собственный сходящийся ряд для
  ICDF) идентично для обоих evaluator, что и позволяет использовать `mpmath.iv` как
  честное независимое основание A.
- Скрипты (все в `T0_WORK/scripts/`, зеркало для rebuild в `T0_WORK/scripts_rebuild2/`):
  `common.py`, `resampler_common.py`, `icdf_common.py`, `gen_sin48000.py`,
  `gen_pink.py`, `gen_tp_fir.py`, `gen_resampler.py`, `gen_icdf.py`,
  `build_manifest.py`.
- Команды воспроизведения (после создания venv и `pip install mpmath==1.4.1`):

```
python gen_sin48000.py
python gen_pink.py
python gen_tp_fir.py
python gen_resampler.py
python gen_icdf.py
python build_manifest.py
```

Рабочая точность: dps=60 (evaluator B, precision P) и dps=120 (evaluator B, precision
2P) для всех GENERATED_REAL таблиц; `mpmath.iv` также на dps=60 (evaluator A). Оба
основания сертификации (interval arithmetic и convergence procedure) применены
одновременно на каждую запись каждой из семи GENERATED_REAL таблиц, что строже
минимального требования companion §7.1 (минимум один сертифицированный evaluator).

---

## I. WARNINGS

1. **PINK_V1 нет замороженного SHA-256 в Prompt.md/companion для сверки** (в отличие
   от TP_FIR_Q30, для которого зафиксирован конкретный SHA). Проверка выполнена только
   структурно (значения, форма, порядок полей, явные нули) — байтовое значение SHA
   PINK_V1.bin (`990ae00b429e6ef7256fa1a75b51001b2554891adeee02466babbcb092a6e32c`)
   зафиксировано настоящим отчётом как первое официальное значение для будущей
   normative companion revision (раздел NORMATIVE_COMPANION_RELEASE_DATA ниже), но не
   верифицировано против независимо опубликованного ожидаемого значения, так как
   таковое не было предоставлено во входных материалах.
2. **ICDF_Q24 методология генератора** — companion называет алгоритм генерации
   "Wichura AS241"; T0 tooling вычисляет ту же целевую математическую функцию (обратную
   нормальную CDF) напрямую через Ньютона + интервальную сертификацию, а не через
   буквальную реализацию рациональной аппроксимации AS241. См. пояснение в разделе C.2.
   Это не отклонение от нормативного результата (целевая функция и критерий точности
   §14 те же), но является методологическим отличием инструмента, которое стоит явно
   отметить перед normative companion release / внешним red-team.
3. **Никаких evaluator disagreements, blocking ambiguities или spec conflicts
   обнаружено не было** на всём протяжении T0 — ни в первых пяти входах, ни в PDF
   provenance, ни в одной из девяти таблиц, ни в манифесте, ни при пересборке.
4. Установка `mpmath` в изолированный venv потребовала сетевого доступа к PyPI;
   пакет `python-json-canonicalization` / `python-json-canonicalize` (готовая
   RFC 8785 реализация) не найден в PyPI index под проверенными именами, поэтому JCS
   сериализация реализована вручную в `common.py::canonical_json_bytes` (обоснование
   корректности для данной ограниченной схемы данных — раздел F и сам код).

---

## J. FINAL VERDICT

```
T0 CANDIDATE PASS
```

Вычислительная часть T0 полностью сошлась; spec package сформирован в `T0_OUTPUT/`;
готов к внешнему red-team/review. `d0_bench_integer_dsp_semantics_v1_7.md` остаётся
DRAFT и не изменён. `d0_bench_integer_dsp_semantics` NORMATIVE версия **не выпущена**
настоящим запуском. M0 **не начат**.

---

## NORMATIVE_COMPANION_RELEASE_DATA

Данные для внесения в СЛЕДУЮЩУЮ (NORMATIVE) версию companion после внешнего red-team,
согласно Prompt.md раздел 21. Номер версии не присваивается самостоятельно.

| table_id | filename | dimensions | q_format | entry_count | bytes | sha256 |
|---|---|---|---|---|---|---|
| H_1000_999 | H_1000_999.bin | [1000,25] | 30 | 25000 | 200000 | `0236c13f17ce92d414a28880fa20e6c22fd78a8575d6d76d995e18b83ee755a4` |
| H_147_160 | H_147_160.bin | [147,27] | 30 | 3969 | 31752 | `3f532644af969c5cbc18adde1c806ac7e8d4dd3dfc41ecefdea6314c8f9c3cd8` |
| H_160_147 | H_160_147.bin | [160,25] | 30 | 4000 | 32000 | `a65d204ed7252ba1417d536b1cfb7fe98719e8806c8d72ee87d2864acd0d5f6a` |
| H_999_1000 | H_999_1000.bin | [999,25] | 30 | 24975 | 199800 | `b1cf6cde083243a76f211418570d6ddc89a661a102456d297c32b0f88e2383a3` |
| H_DRIFT_Q30 | H_DRIFT_Q30.bin | [1024,25] | 30 | 25600 | 204800 | `5aa872ee6d24d614d8153f6f69f913cba059e35592869c3672a95a5db141a8c7` |
| ICDF_Q24 | ICDF_Q24.bin | [65536] | 24 | 65536 | 524288 | `75b753a89215dd07b6f1804cc7b3668ffb07cadb52488a5e2d7004208efd3665` |
| PINK_V1 | PINK_V1.bin | [3,5] | 30 | 15 | 120 | `990ae00b429e6ef7256fa1a75b51001b2554891adeee02466babbcb092a6e32c` |
| SIN48000_Q30 | SIN48000_Q30.bin | [48000] | 30 | 48000 | 384000 | `4708579df63bb4b09da20c9883d6c1bbfe9701e93908fcc820a6ec33badacfd7` |
| TP_FIR_Q30 | TP_FIR_Q30.bin | [4,12] | 30 | 48 | 384 | `4fd922e97c8a656f20bb5e069f6c00917a4bd845cd7e71c71aed066fd5625270` |

- `dsp_tables_manifest.json` ordinary SHA-256: `c0a09133d129b87a639d1aacee6f3a4ef6a26df6a7660c48254211e45fb63ddb`
- `tables_manifest_sha256`: `53aae6d3e729461917af4b5908a7dbada210e1e8da5357913fee61da40644848`
- `TP_FIR_SOURCE_DECIMAL.txt` SHA-256: `0935e97d0b2efd5fdb77826430e9dc161833b9c916585547d0d910b3cda37424` (789 bytes)
- Global size invariant: `sum(entry_count*8) == 1577144` — PASS
- Blind IMPORTED_EXACT verification: PASS, 48/48
- Clean rebuild: 9/9 binaries + manifest byte-identical
- T0 verdict: **T0 CANDIDATE PASS**

**STOP.** Переход к M0 не выполняется без отдельной команды после внешнего red-team.
