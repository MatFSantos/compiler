
token1 = """1 <PRE, class>
1 <LOG, &&>
1 <IDE, jfbfd849_523>
1 <CAC, "*zxcfdsf-45hdghf5+/o">
2 <LOG, !>
2 <PRE, read>
3 <IDE, g64ndf423>
3 <ART, -->
3 <LOG, ||>
4 <IDE, k765w4hdf>
4 <PRE, void>
4 <ART, +>
4 <NRO, 87465343>
4 <DEL, ;>
4 <REL, ==>
4 <LOG, &&>
5 <CAC, "657hgffgh7{]">
5 <DEL, ]>
5 <REL, !=>
5 <DEL, ->>"""

token2 = """1 <PRE, void>
1 <PRE, main>
1 <DEL, (>
1 <DEL, )>
1 <DEL, {>
2 <PRE, int>
2 <IDE, i>
2 <REL, =>
2 <NRO, 0>
2 <DEL, ,>
2 <IDE, j>
2 <REL, =>
2 <NRO, 0>
3 <PRE, int>
3 <IDE, k>
3 <REL, =>
3 <IDE, i>
3 <ART, +>
3 <IDE, j>
4 <PRE, print>
4 <DEL, (>
4 <IDE, k>
4 <DEL, )>
5 <DEL, }>"""

token3 = """1 <IDE, public>
1 <PRE, void>
1 <IDE, connect>
1 <DEL, (>
1 <DEL, )>
1 <DEL, {>
2 <IDE, try>
2 <DEL, {>
3 <IDE, printlnDebug>
3 <DEL, (>
4 <CAC, "Trying to connect to the MQTT broker ">
4 <ART, +>
4 <IDE, this>
4 <DEL, .>
4 <IDE, serverURI>
4 <ART, +>
4 <CAC, "...">
5 <DEL, )>
5 <DEL, ;>
7 <IDE, this>
7 <DEL, .>
7 <IDE, mqttClient>
7 <REL, =>
8 <IDE, new>
8 <IDE, MqttClient>
8 <DEL, (>
9 <IDE, this>
9 <DEL, .>
9 <IDE, serverURI>
9 <DEL, ,>
10 <IDE, String>
10 <DEL, .>
10 <IDE, format>
10 <DEL, (>
10 <CAC, "cliente_java_%d">
10 <DEL, ,>
10 <IDE, System>
10 <DEL, .>
10 <IDE, currentTimeMillis>
10 <DEL, (>
10 <DEL, )>
10 <DEL, )>
10 <DEL, ,>
11 <IDE, new>
11 <IDE, MqttDefaultFilePersistence>
11 <DEL, (>
11 <IDE, System>
11 <DEL, .>
11 <IDE, getProperty>
11 <DEL, (>
11 <CAC, "java.io.tmpdir">
11 <DEL, )>
11 <DEL, )>
12 <DEL, )>
12 <DEL, ;>
14 <IDE, this>
14 <DEL, .>
14 <IDE, mqttClient>
14 <DEL, .>
14 <IDE, setCallback>
14 <DEL, (>
14 <IDE, this>
14 <DEL, )>
14 <DEL, ;>
15 <IDE, this>
15 <DEL, .>
15 <IDE, mqttClient>
15 <DEL, .>
15 <IDE, connect>
15 <DEL, (>
15 <IDE, mqttOptions>
15 <DEL, )>
15 <DEL, ;>
16 <DEL, }>
16 <IDE, catch>
16 <DEL, (>
16 <IDE, MqttException>
16 <IDE, ex>
16 <DEL, )>
16 <DEL, {>
17 <IDE, printlnDebug>
17 <DEL, (>
18 <CAC, "Error connecting to MQTT broker ">
18 <ART, +>
18 <IDE, this>
18 <DEL, .>
18 <IDE, serverURI>
18 <ART, +>
18 <CAC, " - ">
18 <ART, +>
18 <IDE, ex>
19 <DEL, )>
19 <DEL, ;>
20 <DEL, }>
21 <DEL, }>"""

token4 = """1 <PRE, const>
1 <IDE, variable>
1 <PRE, int>
1 <PRE, class>
1 <IDE, function>
1 <PRE, main>
2 <PRE, if>
2 <PRE, else>
2 <PRE, else>
2 <PRE, if>
2 <PRE, for>
2 <PRE, boolean>
2 <IDE, while>
2 <PRE, true>
2 <PRE, false>
3 <CAC, "&@#!$">"""

token5 = """1 <PRE, int>
1 <PRE, main>
2 <PRE, int>
2 <IDE, a>
2 <REL, =>
2 <NRO, 3>
2 <PRE, const>
2 <IDE, a_2>
2 <REL, =>
2 <NRO, 5>
3 <NRO, 3>
3 <REL, =>
3 <NRO, 5>
3 <REL, =>
3 <IDE, a325>
3 <DEL, ;>
4 <IDE, b>
4 <REL, =>
4 <CAC, "string">"""

token6 = """1 <IDE, abg>
1 <ART, ->
1 <ART, +>
1 <PRE, if>
1 <DEL, .>
1 <IDE, variablesi>
1 <DEL, {>
1 <DEL, .>
1 <NRO, 1.0>
2 <DEL, ;>
2 <IDE, v>
2 <DEL, .>
2 <NRO, 1>
2 <IDE, a5_a>
2 <IDE, JH1>
2 <DEL, )>
2 <DEL, (>
2 <CAC, "&&&">
3 <LOG, ||>
3 <NRO, 111>
3 <IDE, consta>
9 <LOG, !>
9 <CAC, "isso e uma cadeia*&">
10 <DEL, }>
10 <DEL, }>"""

token7 = """1 <ART, ++>
1 <ART, ++>
1 <ART, ++>
1 <ART, ++>
1 <ART, ++>
2 <REL, >>
2 <ART, ++>
2 <ART, ++>
2 <ART, ++>
2 <ART, ++>
2 <ART, ++>
2 <ART, ++>
2 <ART, ++>
2 <ART, ++>
2 <ART, ++>
2 <ART, ++>
2 <ART, ++>
2 <ART, ++>
2 <ART, ++>
2 <ART, ++>
2 <ART, ++>
2 <ART, ++>
2 <ART, ++>
2 <ART, ++>
2 <ART, ++>
2 <ART, ++>
2 <ART, ++>
2 <ART, ++>
2 <ART, ++>
2 <ART, ++>
3 <REL, >>
3 <ART, ++>
3 <ART, ++>
3 <ART, ++>
3 <ART, ++>
3 <ART, ++>
4 <DEL, [>
6 <REL, >>
6 <ART, ++>
6 <ART, ++>
6 <ART, ++>
6 <ART, ++>
6 <ART, ++>
6 <ART, ++>
6 <ART, ++>
6 <ART, ++>
6 <ART, ++>
6 <ART, ++>
6 <ART, ++>
6 <ART, ++>
6 <ART, ++>
6 <ART, ++>
6 <ART, ++>
6 <ART, ++>
6 <ART, ++>
6 <ART, ++>
6 <ART, ++>
6 <ART, ++>
6 <ART, ++>
6 <ART, ++>
6 <ART, ++>
6 <ART, ++>
7 <REL, >>
7 <ART, ++>
7 <ART, ++>
7 <ART, ++>
7 <ART, ++>
7 <ART, ++>
8 <DEL, [>
10 <REL, >>
10 <ART, ++>
10 <ART, ++>
10 <ART, ++>
10 <ART, ++>
10 <ART, ++>
10 <ART, ++>
10 <ART, ++>
10 <ART, ++>
10 <ART, ++>
10 <ART, ++>
10 <ART, ++>
10 <ART, ++>
10 <ART, ++>
10 <ART, ++>
10 <ART, ++>
10 <ART, ++>
10 <ART, ++>
10 <ART, ++>
10 <ART, ++>
10 <ART, ++>
10 <ART, ++>
10 <ART, ++>
10 <ART, ++>
10 <ART, ++>
11 <REL, >>
11 <ART, ++>
11 <ART, ++>
11 <ART, ++>
11 <ART, ++>
11 <ART, ++>
12 <DEL, [>
13 <REL, <>
13 <REL, <>
13 <REL, <>
13 <REL, <>
13 <REL, <>
14 <REL, >>
14 <REL, >>
15 <REL, >>
15 <REL, >>
15 <ART, +>
16 <REL, <>
16 <REL, <>
16 <REL, <>
16 <REL, <>
16 <REL, <>
17 <REL, >>
17 <REL, >>
17 <REL, >>
17 <REL, >>
17 <REL, >>
17 <REL, >>
17 <ART, ->
18 <DEL, ]>
19 <REL, <>
19 <ART, -->
19 <ART, -->
19 <ART, -->
19 <ART, -->
19 <ART, -->
19 <ART, -->
19 <ART, -->
19 <ART, -->
19 <ART, -->
19 <ART, -->
19 <ART, -->
19 <ART, -->
19 <ART, -->
19 <ART, -->
19 <ART, -->
19 <ART, -->
19 <ART, -->
19 <ART, -->
19 <ART, -->
19 <ART, -->
19 <ART, -->
19 <ART, -->
19 <ART, -->
19 <ART, -->
19 <ART, -->
19 <ART, -->
19 <ART, -->
19 <ART, -->
19 <ART, -->
21 <REL, <>
21 <REL, <>
21 <ART, +>
22 <REL, >>
22 <ART, ->
23 <DEL, ]>
24 <REL, <>
24 <ART, -->
24 <ART, -->
24 <ART, -->
24 <ART, -->
24 <ART, -->
24 <ART, -->
24 <ART, -->
24 <ART, -->
24 <ART, -->
24 <ART, -->
24 <ART, -->
24 <ART, -->
24 <ART, -->
24 <ART, -->
24 <ART, -->
24 <ART, -->
24 <ART, -->
24 <ART, -->
24 <ART, -->
24 <ART, -->
24 <ART, -->
24 <ART, -->
24 <ART, -->
24 <ART, -->
24 <ART, -->
24 <ART, -->
24 <ART, -->
24 <ART, -->
24 <ART, -->
26 <REL, <>
26 <REL, <>
26 <ART, +>
27 <REL, >>
28 <ART, ->
29 <DEL, ]>"""

token8 = """1 <IDE, viariables>
1 <PRE, const>
2 <PRE, class>
3 <PRE, methods>
3 <PRE, objects>
3 <PRE, main>
3 <PRE, return>
3 <PRE, if>
4 <PRE, else>
4 <PRE, then>
4 <PRE, for>
4 <PRE, read>
5 <PRE, print>
6 <PRE, void>
7 <PRE, int>
8 <PRE, real>
9 <PRE, boolean>
9 <PRE, string>
9 <PRE, true>
9 <PRE, false>"""
token9 = r"""1 <PRE, int>
1 <PRE, main>
1 <DEL, (>
1 <PRE, int>
1 <IDE, argc>
1 <DEL, ,>
1 <IDE, char>
1 <IDE, argv>
1 <DEL, )>
2 <DEL, {>
3 <PRE, if>
3 <DEL, (>
3 <IDE, sodium_init>
3 <DEL, (>
3 <DEL, )>
3 <REL, <>
3 <NRO, 0>
3 <DEL, )>
3 <DEL, {>
4 <IDE, cout>
4 <REL, <>
4 <REL, <>
4 <CAC, "Error on libsodium init!\n">
4 <DEL, ;>
5 <PRE, return>
5 <ART, ->
5 <NRO, 1>
5 <DEL, ;>
6 <DEL, }>
7 <IDE, QApplication>
7 <IDE, a>
7 <DEL, (>
7 <IDE, argc>
7 <DEL, ,>
7 <IDE, argv>
7 <DEL, )>
7 <DEL, ;>
8 <IDE, shoyu>
8 <IDE, w>
8 <DEL, ;>
9 <IDE, w>
9 <DEL, .>
9 <IDE, show>
9 <DEL, (>
9 <DEL, )>
9 <DEL, ;>
10 <PRE, return>
10 <IDE, a>
10 <DEL, .>
10 <IDE, exec>
10 <DEL, (>
10 <DEL, )>
10 <DEL, ;>
11 <DEL, }>"""

token10 = """1 <PRE, int>
1 <IDE, a>
1 <REL, =>
1 <NRO, 3>
1 <DEL, ;>
2 <PRE, int>
2 <IDE, b>
2 <REL, =>
2 <NRO, 6>
2 <DEL, ;>
4 <IDE, double>
4 <IDE, result>
4 <REL, =>
4 <IDE, a>
4 <ART, *>
4 <IDE, b>"""

token11 = """1 <ART, +>
1 <NRO, 1>
1 <DEL, ,>
1 <NRO, 7>
1 <LOG, !>
1 <NRO, 1>
2 <DEL, .>
2 <PRE, const>
2 <IDE, abc>
3 <IDE, A>
3 <ART, +>
3 <NRO, 1>
4 <IDE, aeo_>
4 <IDE, just>
4 <DEL, ;>"""

token12 = r"""1 <PRE, for>
1 <IDE, in>
1 <ART, +>
1 <DEL, {>
2 <PRE, int>
2 <REL, =>
2 <NRO, 2>
2 <ART, *>
2 <LOG, !>
3 <IDE, float>
3 <IDE, ab>
3 <REL, =>
3 <ART, *>
4 <PRE, string>
4 <IDE, teste>
4 <CAC, "teste">
4 <REL, =>
4 <CAC, "teste">
6 <PRE, int>
6 <IDE, resultado>
6 <REL, =>
6 <ART, ->
6 <IDE, ab>
7 <DEL, }>"""

token13 = r"""1 <ART, +>
1 <NRO, 9>
2 <REL, =>
2 <NRO, 5>"""

token14 = r"""1 <DEL, ;>
1 <IDE, numb>
3 <NRO, 4025>
3 <CAC, "origin*&/op">
4 <IDE, y25>
4 <CAC, "ib34@%!(H">
5 <IDE, sofjv>
5 <ART, *>
6 <ART, ->
6 <NRO, 47>"""

token15 = r"""5 <DEL, ]>
5 <DEL, [>"""

token16 = r"""6 <IDE, mal>
7 <IDE, f>
8 <IDE, o>
9 <IDE, r>
10 <IDE, m>
11 <IDE, a>
12 <IDE, d>
13 <IDE, a>"""

token17 = r"""5 <DEL, .>
5 <NRO, 2>"""

token18 = r"""1 <REL, =>
1 <REL, =>
1 <NRO, 3>
3 <PRE, int>
3 <REL, =>"""

token_out = [
    token1.split('\n') if token1 is not None else [],
    token2.split('\n') if token2 is not None else [],
    token3.split('\n') if token3 is not None else [],
    token4.split('\n') if token4 is not None else [],
    token5.split('\n') if token5 is not None else [],
    token6.split('\n') if token6 is not None else [],
    token7.split('\n') if token7 is not None else [],
    token8.split('\n') if token8 is not None else [],
    token9.split('\n') if token9 is not None else [],
    token10.split('\n') if token10 is not None else [],
    token11.split('\n') if token11 is not None else [],
    token12.split('\n') if token12 is not None else [],
    token13.split('\n') if token13 is not None else [],
    token14.split('\n') if token14 is not None else [],
    token15.split('\n') if token15 is not None else [],
    token16.split('\n') if token16 is not None else [],
    token17.split('\n') if token17 is not None else [],
    token18.split('\n') if token18 is not None else [],
]

errors1 = None
errors2 = None
errors3 = None
errors4 = None
errors5 = None
errors6 = None
errors7 = None
errors8 = None
errors9 = None
errors10 = None
errors11 = r"""1 <NMF, 3....>
1 <NMF, 156.+hji>
2 <IMF, Aaa$eof56&_>
3 <CMF, "isso é uma cadeia errada">
4 <TMF, &>
4 <NMF, 15.3.2.1>
5 <CMF, " não vou fechar isso>
6 <CoMF, >"""
errors12 = r"""1 <NMF, 3..variavel>
1 <NMF, 893..variables>
2 <IMF, ab@>
2 <NMF, 1.1.1.>
3 <NMF, 1. >
3 <NMF, 9.0.0>
6 <NMF, 3.+aa>"""
errors13 = r"""1 <NMF, 8.1.2>
2 <IMF, test@test>
3 <CoMF, >"""
errors14 = r"""1 <NMF, 6.a35&.99>
2 <TMF, |abc28>
3 <NMF, 07084.!&>
5 <TMF, %ao>
6 <NMF, 923.<>"""
errors15 = r"""1 <NMF, 9..abc>
2 <TMF, |&|id_789>
3 <NMF, 3.4.5.>
4 <NMF, 1.,2>
6 <NMF, 1nt>
7 <CoMF, >"""
errors16 = r"""1 <NMF, 2.2.>
2 <IMF, variavel$>
3 <IMF, v@riavel_>
4 <NMF, 8aaa>
5 <CMF, "cadeia de caracteres >"""
errors17 = r"""2 <NMF, 2..2>
2 <NMF, 2.......>
2 <NMF, 2.@>
2 <NMF, 2.a>
2 <NMF, 2.2.2>
2 <NMF, 2.+asdas>
5 <TMF, @as>
5 <TMF, #$@$>
5 <TMF, @>
5 <TMF, @#>
8 <IMF, as@>
11 <CMF, "asdasdas 212038yu890 ja0j)*)UY)* @J) >
14 <CoMF, >"""
errors18 = r"""1 <NMF, 3.3.3.3@1@a>
1 <NMF, 5a@n>
3 <IMF, a@a@a@a>
3 <CMF, "Árvore">
5 <NMF, 3..................2>
7 <CoMF, >"""

errors_out = [
    errors1.split('\n') if errors1 is not None else [],
    errors2.split('\n') if errors2 is not None else [],
    errors3.split('\n') if errors3 is not None else [],
    errors4.split('\n') if errors4 is not None else [],
    errors5.split('\n') if errors5 is not None else [],
    errors6.split('\n') if errors6 is not None else [],
    errors7.split('\n') if errors7 is not None else [],
    errors8.split('\n') if errors8 is not None else [],
    errors9.split('\n') if errors9 is not None else [],
    errors10.split('\n') if errors10 is not None else [],
    errors11.split('\n') if errors11 is not None else [],
    errors12.split('\n') if errors12 is not None else [],
    errors13.split('\n') if errors13 is not None else [],
    errors14.split('\n') if errors14 is not None else [],
    errors15.split('\n') if errors15 is not None else [],
    errors16.split('\n') if errors16 is not None else [],
    errors17.split('\n') if errors17 is not None else [],
    errors18.split('\n') if errors18 is not None else [],
]