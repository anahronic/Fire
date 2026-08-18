ЗАДАЧА: выполнить этап T0 проекта D0 Bench.

Работай непосредственно с приложенными файлами и их фактическими байтами.  
Не пересказывай спецификацию своими словами там, где можно сослаться на ее  
конкретный раздел. Приоритет источников и правила конфликтов бери из самих  
документов.

\============================================================  
0\. ПРЕДОСТАВЛЕННЫЕ ФАЙЛЫ  
\============================================================

Рабочий вход T0:

1\. geometric\_sound\_protocol\_concept\_v8.0\_ru.md

   ожидаемый SHA-256:  
   2e027eeeb42457ec26712637015c8ae69743ffc53d77c07fb1f67baee9e5bb0d

2\. d0\_bench\_protocol\_v6\_0.md

   ожидаемый SHA-256:  
   b5a1915dbcb8a5b6eb68c59dd55346f6c7435b40ef47f930aeae6eb8077e0db2

3\. d0\_bench\_integer\_dsp\_semantics\_v1\_7.md

   ожидаемый SHA-256:  
   98e282dcafcaa48db9d3a9314106cb641f729f87438fc158277b4ab21806a4e9

4\. d0\_bench\_tz\_v1\_11.md

   ожидаемый SHA-256:  
   3ee5f34bc719df8d721706862d71ca2633d1834b4077c82747625a398bbdab19

5\. TP\_FIR\_SOURCE\_DECIMAL.txt

   ожидаемый SHA-256:  
   0935e97d0b2efd5fdb77826430e9dc161833b9c916585547d0d910b3cda37424

   ожидаемый размер:  
   789 bytes

Дополнительный provenance/source document:

6\. ITU-R\_BS.1770-5\_2023.pdf

   SHA-256 локально предоставленной копии:  
   eefb926f72f72a96b96f251067bfee0650a0f29a26f60661d354162038b041ad

   ВАЖНО:  
   SHA этого PDF не является нормативной идентичностью spec package.  
   PDF предоставлен как provenance/source reference.  
   Нормативным импортированным текстовым артефактом является  
   TP\_FIR\_SOURCE\_DECIMAL.txt согласно companion.

\============================================================  
1\. ПЕРВАЯ ОПЕРАЦИЯ: ВЕРИФИКАЦИЯ ВХОДОВ  
\============================================================

До любых вычислений:

1\. Самостоятельно вычисли SHA-256 первых пяти файлов.  
2\. Проверь размер TP\_FIR\_SOURCE\_DECIMAL.txt.  
3\. Сравни с ожидаемыми значениями выше.  
4\. Отдельно вычисли SHA-256 предоставленной PDF-копии и запиши его  
   в provenance section отчета.

Если SHA-256 ЛЮБОГО из первых пяти файлов не совпал:

STOP.  
T0 не начинать.  
Ничего не исправлять автоматически.  
Выдать INPUT\_HASH\_MISMATCH с:  
\- filename;  
\- expected SHA-256;  
\- actual SHA-256;  
\- actual file size.

Несовпадение SHA PDF само по себе T0 не блокирует, поскольку SHA PDF  
не нормативен. В таком случае только зафиксировать provenance warning  
и не использовать PDF для изменения уже замороженного source file.

\============================================================  
2\. BLIND IMPORTED\_EXACT VERIFICATION УЖЕ ВЫПОЛНЕНА  
\============================================================

Первое действие T0 \- слепая независимая ретранскрипция Annex 2 \-  
уже выполнено ДО раскрытия проверяющему:

\- TP\_FIR\_SOURCE\_DECIMAL.txt;  
\- его SHA-256;  
\- companion v1.7;  
\- ожидаемых Q30-значений.

Независимый проверяющий получил только Recommendation ITU-R  
BS.1770-5 и правило порядка:

\- phase-major;  
\- Phase 0 \-\> Phase 1 \-\> Phase 2 \-\> Phase 3;  
\- внутри каждой фазы строки печатной таблицы сверху вниз.

Он независимо транскрибировал 48 коэффициентов из Annex 2,  
order 48, 4-phase FIR interpolating filter.

Зафиксированный результат:

Phase 0:

0.0017089843750  
0.0109863281250  
\-0.0196533203125  
0.0332031250000  
\-0.0594482421875  
0.1373291015625  
0.9721679687500  
\-0.1022949218750  
0.0476074218750  
\-0.0266113281250  
0.0148925781250  
\-0.0083007812500

Phase 1:

\-0.0291748046875  
0.0292968750000  
\-0.0517578125000  
0.0891113281250  
\-0.1665039062500  
0.4650878906250  
0.7797851562500  
\-0.2003173828125  
0.1015625000000  
\-0.0582275390625  
0.0330810546875  
\-0.0189208984375

Phase 2:

\-0.0189208984375  
0.0330810546875  
\-0.0582275390625  
0.1015625000000  
\-0.2003173828125  
0.7797851562500  
0.4650878906250  
\-0.1665039062500  
0.0891113281250  
\-0.0517578125000  
0.0292968750000  
\-0.0291748046875

Phase 3:

\-0.0083007812500  
0.0148925781250  
\-0.0266113281250  
0.0476074218750  
\-0.1022949218750  
0.9721679687500  
0.1373291015625  
\-0.0594482421875  
0.0332031250000  
\-0.0196533203125  
0.0109863281250  
0.0017089843750

Blind report:

\- 48 строк;  
\- 4 фазы x 12 коэффициентов;  
\- источник: Rec. ITU-R BS.1770-5, Annex 2, Detailed description,  
  печатная таблица FIR coefficients;  
\- таблица разделена издательской версткой между двумя страницами;  
\- колонки второй половины были продолжены по их горизонтальной позиции;  
\- неоднозначностей, влияющих на цифры или знаки, не обнаружено;  
\- видимая симметрия FIR НЕ использовалась для довычисления значений;  
  все 48 значений были транскрибированы непосредственно.

После фиксации результата была раскрыта canonical copy:

TP\_FIR\_SOURCE\_DECIMAL.txt

Результат сравнения:

48 / 48 coefficients EXACT  
mismatches \= 0

Считать нормативное требование blind transcription внутри T0  
ВЫПОЛНЕННЫМ.

Ты НЕ являешься blind verifier этой операции и не должен выдавать  
собственное чтение PDF за новую blind verification.

Ты можешь:  
\- проверить, что приведенные 48 строк совпадают с  
  TP\_FIR\_SOURCE\_DECIMAL.txt;  
\- проверить байтовую норму source-файла;  
\- включить результат в T0 report.

Но в отчете должно быть явно написано:

"Blind verification was performed by a separate pre-existing  
independent context before canonical source disclosure."

\============================================================  
3\. ЖЕСТКАЯ ГРАНИЦА ЗАДАЧИ  
\============================================================

ВЫПОЛНИТЬ ТОЛЬКО T0.

НЕ НАЧИНАТЬ M0.

На этом этапе ЗАПРЕЩЕНО:

\- создавать production/reference implementation d0bench;  
\- создавать src/d0bench;  
\- реализовывать CLI d0bench;  
\- реализовывать synth;  
\- реализовывать decode;  
\- реализовывать channel;  
\- реализовывать scanner;  
\- реализовывать ranking;  
\- реализовывать statemachine;  
\- начинать A0-A8;  
\- создавать G0-G8 evidence;  
\- выполнять development experiment;  
\- выполнять selection;  
\- выполнять confirmation;  
\- выполнять YouTube experiment;  
\- публиковать bench\_program\_manifest.json;  
\- изменять concept v8.0;  
\- изменять protocol v6.0;  
\- изменять TZ v1.11;  
\- изменять companion v1.7 НА МЕСТЕ;  
\- изменять TP\_FIR\_SOURCE\_DECIMAL.txt;  
\- менять нормативные алгоритмы;  
\- выбирать новые engineering constants;  
\- "исправлять" спецификацию догадкой;  
\- ослаблять требования certification/convergence.

Разрешено создавать исключительно вспомогательный offline tooling,  
необходимый для выполнения T0.

Такой tooling:  
\- не является src/d0bench;  
\- не является M0;  
\- не является reference implementation;  
\- должен быть отделен от будущего runtime-кода;  
\- должен быть сохранен для аудита;  
\- должен иметь зафиксированные версии используемых инструментов/пакетов.

Если для высокоточных вычислений необходимы внешние библиотеки,  
их можно использовать только как offline T0 tooling.  
Запиши точные версии и назначение каждого инструмента.

\============================================================  
4\. STOP RULE  
\============================================================

Если обнаружена:

\- неоднозначность спецификации;  
\- противоречие между нормативными документами;  
\- невозможность выполнить алгоритм однозначно;  
\- невозможность доказать требуемую error bound;  
\- расхождение двух независимых evaluator после Q-rounding;  
\- нарушение frozen invariant;  
\- несовпадение нормативного known hash;

НЕ ВЫБИРАЙ "наиболее разумную" трактовку.

STOP.

Выдай:

T0 BLOCKED

и укажи:

\- документ;  
\- раздел;  
\- точную формулу/фразу;  
\- конфликтующие требования;  
\- почему они допускают разные байтовые результаты либо не позволяют  
  доказать требуемый результат.

Не продолжай генерацию downstream-артефактов после блокера.

\============================================================  
5\. НОРМАТИВНЫЙ ИСТОЧНИК МАТЕМАТИКИ  
\============================================================

Для машинной DSP-математики следуй:

d0\_bench\_integer\_dsp\_semantics\_v1\_7.md

Особенно:

\- §1 rounding/Q formats;  
\- §3 SIN48000\_Q30;  
\- §5 true peak;  
\- §7 ICDF\_Q24;  
\- §9 resampler tables и H\_DRIFT\_Q30;  
\- §11 PINK\_V1;  
\- §14 T0 registry, provenance classes, serialization,  
  dsp\_tables\_manifest.json и invariants.

Если TZ пересказывает машинную математику иначе, приоритет имеет  
companion согласно самому TZ.

Protocol и Concept являются более высокими источниками в своих  
областях согласно правилам стека.

\============================================================  
6\. ЦЕЛЬ T0  
\============================================================

Собрать, независимо проверить, сериализовать и заморозить РОВНО  
девять нормативных бинарных таблиц spec package:

H\_1000\_999.bin  
H\_147\_160.bin  
H\_160\_147.bin  
H\_999\_1000.bin  
H\_DRIFT\_Q30.bin  
ICDF\_Q24.bin  
PINK\_V1.bin  
SIN48000\_Q30.bin  
TP\_FIR\_Q30.bin

После этого сформировать:

dsp\_tables\_manifest.json

TP\_FIR\_SOURCE\_DECIMAL.txt:

\- является отдельным нормативным текстовым артефактом spec package;  
\- НЕ входит в tables\[\] dsp\_tables\_manifest.json;  
\- НЕ входит в sum(entry\_count\*8) для девяти бинарников;  
\- остается побайтно неизменным.

\============================================================  
7\. КЛАССЫ ПРОИСХОЖДЕНИЯ  
\============================================================

Использовать классификацию companion §14.

\--------------------------  
7.1 GENERATED\_REAL  
\--------------------------

Таблицы:

SIN48000\_Q30  
ICDF\_Q24  
H\_147\_160  
H\_160\_147  
H\_999\_1000  
H\_1000\_999  
H\_DRIFT\_Q30

Требование:

Для КАЖДОЙ generated-real таблицы нужны два независимых offline evaluator.

Они не должны быть просто двумя вызовами одной функции либо одним кодом  
с измененной precision.

Минимум один evaluator обязан иметь сертифицируемое основание:

A. interval arithmetic;

ИЛИ

B. convergence procedure:  
   \- вычисление на precision P;  
   \- вычисление независимо на precision 2P;  
   \- одинаковый результат после нормативного round-half-to-even;  
   \- явная численная граница ошибки до округления;  
   \- доказанная absolute error \< 0.25 ULP целевого Q-format.

Простое совпадение двух высокоточных float/decimal результатов  
без error certificate НЕ закрывает требование.

Если хотя бы одна запись двух evaluator после нормативного округления  
не совпала:

T0 FAIL.

Не выбирать один evaluator как "правильный" постфактум.

\--------------------------  
7.2 IMPORTED\_EXACT  
\--------------------------

Таблица:

TP\_FIR\_Q30

Единственный источник значений:

TP\_FIR\_SOURCE\_DECIMAL.txt

Преобразование:

\- exact decimal или exact rational;  
\- без binary float;  
\- round half to even согласно companion, хотя на этих 48 значениях  
  halfway case отсутствует;  
\- orientation точно по companion §5;  
\- serialization точно по companion §14.

Не проектировать FIR.  
Не пересчитывать коэффициенты фильтра из frequency-response design.  
Не заменять source literals другой таблицей из библиотеки.

Blind transcription requirement уже закрыт отдельной стороной  
с результатом 48/48 EXACT, как указано выше.

\--------------------------  
7.3 EXACT\_INTEGER  
\--------------------------

Таблица:

PINK\_V1

Коэффициенты брать ТОЧНО из companion §11.

Не проектировать pink-noise filter заново.  
Не оптимизировать коэффициенты.  
Не нормировать их повторно.

Выполнить независимую проверку:  
\- количества секций;  
\- формы;  
\- порядка полей;  
\- знаков;  
\- int64 serialization.

\============================================================  
8\. ОЖИДАЕМЫЙ СОСТАВ ДЕВЯТИ БИНАРНИКОВ  
\============================================================

Следующий состав является frozen invariant.

table\_id       dimensions   q\_format   entry\_count   bytes  
\----------------------------------------------------------------  
H\_1000\_999     \[1000,25\]       30         25000      200000  
H\_147\_160      \[147,27\]        30          3969       31752  
H\_160\_147      \[160,25\]        30          4000       32000  
H\_999\_1000     \[999,25\]        30         24975      199800  
H\_DRIFT\_Q30    \[1024,25\]       30         25600      204800  
ICDF\_Q24       \[65536\]         24         65536      524288  
PINK\_V1        \[3,5\]           30            15         120  
SIN48000\_Q30   \[48000\]         30         48000      384000  
TP\_FIR\_Q30     \[4,12\]          30            48         384

Обязательный invariant:

sum(entry\_count \* 8\) \= 1577144

Расхождение:  
T0 FAIL.

\============================================================  
9\. БИНАРНАЯ СЕРИАЛИЗАЦИЯ  
\============================================================

Для всех девяти таблиц:

element\_type:  
int64\_le\_twos\_complement

Каждая запись сериализуется как signed int64 little-endian  
two's complement.

Никаких заголовков.  
Никакой длины перед данными.  
Никаких magic bytes.  
Никакого BOM.  
Никакого text representation.

Многомерные таблицы сериализовать row-major по companion §14.

Для rectangular polyphase tables учитывать padding zeros как реальные  
сериализуемые int64 entries.

Поэтому, например:

H\_147\_160:  
dimensions \= \[147,27\]  
entry\_count \= 3969

а не 3841\.

\============================================================  
10\. TP\_FIR\_Q30 ОБЯЗАТЕЛЬНЫЕ ПРОВЕРКИ  
\============================================================

TP\_FIR\_Q30 dimensions:

\[4,12\]

Serialization order:

outer loop:  
p \= 0..3

inner loop:  
i \= 0..11

То есть phase-major.

Файл:

TP\_FIR\_Q30.bin

ожидаемый размер:

384 bytes

обязательный SHA-256:

4fd922e97c8a656f20bb5e069f6c00917a4bd845cd7e71c71aed066fd5625270

Если SHA отличается:

T0 FAIL.

Не исправлять файл вручную.  
Не менять endianness "до совпадения".  
Не переставлять фазы "до совпадения".

Диагностировать первопричину.

Также проверить структурные invariants companion:

TP\_FIR\_Q30\[3\]\[i\] \== TP\_FIR\_Q30\[0\]\[11-i\]

TP\_FIR\_Q30\[2\]\[i\] \== TP\_FIR\_Q30\[1\]\[11-i\]

sum(abs(TP\_FIR\_Q30\[0\]\[\*\])) \= 1539964928  
sum(abs(TP\_FIR\_Q30\[3\]\[\*\])) \= 1539964928

sum(abs(TP\_FIR\_Q30\[1\]\[\*\])) \= 2171994112  
sum(abs(TP\_FIR\_Q30\[2\]\[\*\])) \= 2171994112

Проверить байтовую норму TP\_FIR\_SOURCE\_DECIMAL.txt:

\- size \= 789;  
\- 48 logical lines;  
\- LF count \= 47;  
\- CR count \= 0;  
\- BOM absent;  
\- trailing LF absent;  
\- один literal на строку;  
\- optional ASCII "-";  
\- mandatory "0.";  
\- ровно 13 decimal digits;  
\- "+" запрещен;  
\- exponent запрещен.

\============================================================  
11\. SIN48000\_Q30  
\============================================================

Генерировать строго по companion.

Обязательно проверить exact anchors:

SIN48000\_Q30\[0\]     \= 0  
SIN48000\_Q30\[4000\]  \= 536870912  
SIN48000\_Q30\[12000\] \= 1073741824  
SIN48000\_Q30\[24000\] \= 0  
SIN48000\_Q30\[36000\] \= \-1073741824

И все остальные invariants §3/§14 companion.

Не использовать runtime interpolation.

\============================================================  
12\. ICDF\_Q24  
\============================================================

Генерировать строго по companion §7 и §14.

Размер:

65536 entries

Q-format:

Q24

Не заменять нормативную процедуру произвольной inverse-normal функцией  
без требуемого error certificate.

Нужны два независимых evaluator и certification \< 0.25 ULP  
до нормативного round-half-to-even.

\============================================================  
13\. RESAMPLER TABLES  
\============================================================

Генерировать строго по companion §9 и §14:

H\_147\_160  
H\_160\_147  
H\_999\_1000  
H\_1000\_999  
H\_DRIFT\_Q30

Следовать нормативно определенным:

\- N\_h;  
\- center c;  
\- ideal response;  
\- omega;  
\- Kaiser beta;  
\- I0 rule;  
\- normalization;  
\- Q30 quantization;  
\- rectangular polyphase layout;  
\- zero padding;  
\- dimensions;  
\- row-major serialization.

Не менять prototype design.

Проверить нормативные dimensions:

48000 \-\> 44100:  
\[147\]\[27\]

44100 \-\> 48000:  
\[160\]\[25\]

48000 \-\> 47952:  
\[999\]\[25\]

47952 \-\> 48000:  
\[1000\]\[25\]

drift:  
\[1024\]\[25\]

Два independent evaluator обязательны.

\============================================================  
14\. PINK\_V1  
\============================================================

PINK\_V1:

dimensions \= \[3,5\]  
entry\_count \= 15  
q\_format \= 30

Порядок на каждую из трех секций:

b0, b1, b2, a1, a2

Явные нули b2 и a2 ДОЛЖНЫ присутствовать в binary table.

Использовать ровно coefficients companion §11.

Не переупорядочивать поля.  
Не удалять нулевые entries.  
Не проектировать фильтр.

\============================================================  
15\. dsp\_tables\_manifest.json  
\============================================================

После успешной генерации всех девяти таблиц создать:

dsp\_tables\_manifest.json

Структура:

{  
  "schema\_version": 1,  
  "tables": \[  
    {  
      "table\_id": "...",  
      "filename": "...",  
      "element\_type": "int64\_le\_twos\_complement",  
      "dimensions": \[...\],  
      "q\_format": ...,  
      "entry\_count": ...,  
      "sha256": "..."  
    }  
  \]  
}

Схема закрытая.

В root разрешены РОВНО:

schema\_version  
tables

В каждой table entry разрешены РОВНО:

table\_id  
filename  
element\_type  
dimensions  
q\_format  
entry\_count  
sha256

Никаких дополнительных полей.

table\_id:  
ASCII only.

filename:  
\<table\_id\>.bin

sha256:  
ровно 64 lowercase ASCII hex characters.

entry\_count:  
product(dimensions)

и одновременно:

entry\_count \= file\_size / 8

Порядок tables\[\]:

строго по table\_id в побайтовом UTF-8 ascending order.  
Так как table\_id ASCII, это совпадает с требуемым порядком code units.

Ожидаемый порядок:

H\_1000\_999  
H\_147\_160  
H\_160\_147  
H\_999\_1000  
H\_DRIFT\_Q30  
ICDF\_Q24  
PINK\_V1  
SIN48000\_Q30  
TP\_FIR\_Q30

\============================================================  
16\. БАЙТЫ dsp\_tables\_manifest.json  
\============================================================

Физические bytes файла должны быть:

JCS(dsp\_tables\_manifest)

То есть:

\- UTF-8;  
\- no BOM;  
\- no trailing LF;  
\- no trailing CRLF;  
\- никаких formatting spaces/newlines сверх результата JCS.

После записи файла:

1\. вычислить обычный SHA-256 фактических bytes  
   dsp\_tables\_manifest.json;

2\. отдельно вычислить нормативный:

tables\_manifest\_sha256 \=  
SHA256(  
    LP("D0BENCH-DSP-TABLES-MANIFEST-V1") ||  
    LP(JCS(dsp\_tables\_manifest))  
)

Не путать эти две величины.

В итоговом отчете вывести ОБЕ.

\============================================================  
17\. ПРОВЕРКА ИДЕМПОТЕНТНОСТИ  
\============================================================

После первого успешного построения:

1\. сохранить SHA-256 всех девяти .bin;  
2\. сохранить SHA-256 dsp\_tables\_manifest.json;  
3\. удалить только GENERATED OUTPUT копию в отдельной clean build area  
   либо выполнить эквивалентную чистую повторную сборку;  
4\. повторно построить T0 package тем же нормативным процессом;  
5\. сравнить все output bytes.

Требование:

9/9 binaries byte-identical  
manifest byte-identical

Если нет:

T0 FAIL.

Диагностировать nondeterminism.

Не перезаписывать первый результат молча.

\============================================================  
18\. АУДИТНЫЙ СЛЕД ДВУХ EVALUATOR  
\============================================================

Для каждой GENERATED\_REAL таблицы сохранить в T0 report:

\- evaluator A description;  
\- evaluator B description;  
\- implementation/tool;  
\- package/library version;  
\- precision;  
\- rounding method;  
\- error-certification method;  
\- максимальную доказанную pre-rounding error;  
\- результат P;  
\- результат 2P, если используется convergence;  
\- число entries;  
\- число rounded disagreements между A и B.

Ожидается:

rounded disagreements \= 0

Для IMPORTED\_EXACT сохранить:

\- source filename;  
\- source SHA-256;  
\- blind verification status;  
\- exact decimal/rational conversion method;  
\- resulting binary SHA-256.

Для EXACT\_INTEGER сохранить:

\- section source;  
\- coefficient count;  
\- explicit-zero count;  
\- serialized binary SHA-256.

\============================================================  
19\. OUTPUT DIRECTORY  
\============================================================

Создай отдельный каталог результата T0, не смешанный с будущим  
src/d0bench.

Например:

T0\_OUTPUT/

В финальном каталоге spec package должны находиться как минимум:

T0\_OUTPUT/  
  H\_1000\_999.bin  
  H\_147\_160.bin  
  H\_160\_147.bin  
  H\_999\_1000.bin  
  H\_DRIFT\_Q30.bin  
  ICDF\_Q24.bin  
  PINK\_V1.bin  
  SIN48000\_Q30.bin  
  TP\_FIR\_Q30.bin  
  dsp\_tables\_manifest.json  
  TP\_FIR\_SOURCE\_DECIMAL.txt  
  T0\_REPORT.md

TP\_FIR\_SOURCE\_DECIMAL.txt в output package должен быть ПОБАЙТНОЙ копией  
входного canonical source.

Не генерировать его заново из Q30.

Offline tooling и временные evaluator outputs держать отдельно, например:

T0\_WORK/

Они не являются нормативными binary tables.

\============================================================  
20\. T0\_REPORT.md  
\============================================================

Создай подробный T0\_REPORT.md.

Он должен содержать:

A. INPUT IDENTITIES

\- filename;  
\- byte size;  
\- SHA-256;  
\- pass/fail.

B. BLIND IMPORTED\_EXACT EVIDENCE

Обязательно зафиксировать:

\- blind verification выполнена отдельным контекстом;  
\- выполнена до раскрытия canonical source;  
\- 48/48 exact;  
\- mismatch \= 0;  
\- основной T0 executor не заявляет себя blind verifier.

C. TABLE GENERATION

Для каждой из девяти таблиц:

\- table\_id;  
\- provenance class;  
\- source section;  
\- dimensions;  
\- q\_format;  
\- entry\_count;  
\- byte size;  
\- evaluator A;  
\- evaluator B, если требуется;  
\- certification method;  
\- invariant checks;  
\- SHA-256;  
\- PASS/FAIL.

D. GLOBAL SIZE INVARIANT

Явно вычислить:

sum nine binary sizes \= 1577144

и показать отдельные слагаемые.

E. TP FIR CHECKS

\- source SHA;  
\- 48-line format;  
\- Q30 matrix check;  
\- symmetry checks;  
\- abs-sum checks;  
\- binary size;  
\- binary SHA;  
\- expected SHA comparison.

F. MANIFEST

\- ordinary file SHA-256;  
\- tables\_manifest\_sha256;  
\- canonical byte length;  
\- schema validation;  
\- ordering validation.

G. REPRODUCIBILITY

\- clean rebuild;  
\- 9/9 binary equality;  
\- manifest equality.

H. TOOLING

\- OS/environment;  
\- Python/runtime;  
\- high-precision libraries;  
\- exact package versions;  
\- commands necessary to reproduce T0.

I. WARNINGS

Все warnings, даже если они не блокируют T0.

J. FINAL VERDICT

Разрешены только:

T0 CANDIDATE PASS

или

T0 FAIL

или

T0 BLOCKED

"T0 CANDIDATE PASS" означает:

\- вычислительная часть T0 полностью сошлась;  
\- spec package сформирован;  
\- он готов к внешнему red-team/review;  
\- normative companion еще НЕ опубликован;  
\- M0 еще НЕ разрешен.

\============================================================  
21\. ЧТО ДЕЛАТЬ ПРИ PASS  
\============================================================

Если все проверки успешны:

1\. НЕ изменяй d0\_bench\_integer\_dsp\_semantics\_v1\_7.md.

2\. НЕ называй v1.7 NORMATIVE.

3\. НЕ начинай M0.

4\. НЕ создавай bench\_program\_manifest.json.

5\. НЕ выпускай самовольно следующую companion revision.

6\. Сформируй отдельный блок:

NORMATIVE\_COMPANION\_RELEASE\_DATA

В нем перечисли данные, которые после внешнего red-team должны быть  
внесены в СЛЕДУЮЩУЮ версию companion:

\- все девять table\_id;  
\- filename;  
\- dimensions;  
\- q\_format;  
\- entry\_count;  
\- byte size;  
\- SHA-256;  
\- dsp\_tables\_manifest.json ordinary SHA-256;  
\- tables\_manifest\_sha256;  
\- TP\_FIR\_SOURCE\_DECIMAL.txt SHA-256;  
\- результаты invariants;  
\- T0 verdict.

Не присваивай номер новой companion revision самостоятельно, если  
это не требуется спецификацией однозначно.

После этого ОСТАНОВИСЬ.

\============================================================  
22\. ЧТО ДЕЛАТЬ ПРИ FAIL/BLOCKED  
\============================================================

При T0 FAIL или T0 BLOCKED:

\- ничего downstream не публиковать;  
\- M0 не начинать;  
\- существующие DRAFT specifications не менять автоматически;  
\- output, приведший к fail, сохранить отдельно для диагностики;  
\- привести минимальный воспроизводимый пример;  
\- указать первый момент расхождения;  
\- если проблема specification-level, классифицировать ее отдельно  
  от implementation bug;  
\- не "чинить" нормативный документ без отдельного решения автора.

\============================================================  
23\. КОНЕЧНАЯ ЦЕЛЬ ЭТОГО ЗАПУСКА  
\============================================================

На выходе этого запуска я хочу получить НЕ программу D0 Bench,  
а проверяемый T0 spec package и T0\_REPORT.md.

Критерий успеха:

BLIND IMPORTED\_EXACT:  
PASS, 48/48

TP\_FIR\_Q30.bin:  
384 bytes  
SHA-256 \=  
4fd922e97c8a656f20bb5e069f6c00917a4bd845cd7e71c71aed066fd5625270

nine binaries:  
ровно 9

sum sizes:  
1577144 bytes

GENERATED\_REAL:  
два independent evaluator  
и требуемая certification \< 0.25 ULP

dsp\_tables\_manifest.json:  
canonical JCS bytes  
closed schema  
correct order  
correct hashes

clean rebuild:  
byte-identical

final status:  
T0 CANDIDATE PASS

После этого STOP.  
Не переходить к M0 без отдельной команды после внешнего red-team.  
