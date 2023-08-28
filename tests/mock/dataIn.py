
data1 = r"""class &&jfbfd849_523"*zxcfdsf-45hdghf5+/o"
! read
g64ndf423--||
k765w4hdf void+87465343; ==&&
"657hgffgh7{]"]!= ->"""

data2 = r"""void main() {
    int i = 0, j = 0
    int k = i + j
    print(k)
}"""

data3 = r"""public void connect() {
    try {
      printlnDebug(
        "Trying to connect to the MQTT broker " + this.serverURI + "..."
      );

      this.mqttClient =
        new MqttClient(
          this.serverURI,
          String.format("cliente_java_%d", System.currentTimeMillis()),
          new MqttDefaultFilePersistence(System.getProperty("java.io.tmpdir"))
        );

      this.mqttClient.setCallback(this);
      this.mqttClient.connect(mqttOptions);
    } catch (MqttException ex) {
      printlnDebug(
        "Error connecting to MQTT broker " + this.serverURI + " - " + ex
      );
    }
}"""

data4 = r"""const variable int class function main
if else else if for boolean while true false 
"&@#!$" """

data5 = r"""int main
int a = 3 const a_2=5
3 = 5 = a325;
b = "string" """

data6 = r"""abg-+if.variablesi { .1.0
;v. 1 a5_a JH1)("&&&"
||111 consta // comentário
/* 
 bloco
 de
 comentário
*/
! "isso e uma cadeia*&"
}}"""

data7 = r"""++++++++++
>++++++++++++++++++++++++++++++++++++++++++++++++
>++++++++++
[

  >++++++++++++++++++++++++++++++++++++++++++++++++
  >++++++++++
  [

	  >++++++++++++++++++++++++++++++++++++++++++++++++
	  >++++++++++
	  [
	    <<<<<
	    >>
	    >>+
	    <<<<<
	    >>>>>>-
	  ]
	  <----------------------------------------------------------

	  <<+
	  >-
  ]
  <----------------------------------------------------------

  <<+
  >
  -
]"""

data8 = r"""viariables const
class 
methods objects main return if
else then for read
print
void
int
real 
boolean string true false """

data9 = r"""int main(int argc, char argv)
{
    if (sodium_init() < 0) {
        cout << "Error on libsodium init!\n";
        return -1;
    }
    QApplication a(argc, argv);
    shoyu w;
    w.show();
    return a.exec();
}"""

data10 = r"""int a = 3;
int b = 6;

double result=a*b // resultado"""

data11 = r"""3....+1 156.+hji, 7!1
Aaa$eof56&_. const abc
A+1 "isso é uma cadeia errada"
& aeo_ just 15.3.2.1; //cheio de erro
" não vou fechar isso
/*
Isso não é um comentário de bloco
*
Jksjsjsksksjsksks"""

data12 = r"""for 3..variavel in 893..variables+  {
	int ab@ = 2 * 1.1.1.!
	float ab = 1. * 9.0.0
	string teste"teste" = "teste"

	int resultado = 3.+aa-ab //resultado
}"""

data13 = r"""8.1.2+9
test@test = 5
/* Este
não
é um
comentário de bloco
*
/"""

data14 = r"""6.a35&.99; numb /*teste
proc*/ |abc28
07084.!& 4025"origin*&/op"
y25"ib34@%!(H" 
sofjv*%ao
923.<-47"""

data15 = r"""9..abc
|&|id_789
3.4.5.
1.,2
][
1nt
/*"""

data16 = r"""2.2. 
variavel$
v@riavel_ 
8aaa
"cadeia de caracteres 
mal 
f
o
r
m
a
d
a """

data17 = r"""// erro numero:
2..2 2....... 2.@ 2.a 2.2.2 2.+asdas

// erro token
@as #$@$ @.2 @#

// erro identificador
as@ 

// erro cadeia mal formada
"asdasdas 212038yu890 ja0j)*)UY)* @J) 

// erro comentario mal formador
/* adsad"""

data18 = r"""3.3.3.3@1@a=5a@n=3

int a@a@a@a = "Árvore"

3..................2

/*

COMENTÁRIO DE BLOCO MAL FORMADO (?)"""

DataIn = [data1, data2, data3, data4, data5, data6, data7, data8, data9, data10, data11, data12, data13, data14, data15, data16, data17, data18]