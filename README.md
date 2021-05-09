# Kivy-Computer-Vision-Photevoc
Uma aplicação de visão computacional com filtros utilizando Kivy que permite fazer aplicativos para Android e IOS.
Aqui foi criado um app inspirado nas aulas de Visão computacional da Sigmoidal, o app funciona no windows e linux normalmente, entretanto, devido à bugs com relação ao OpenCV que ainda existem na plataforma Kivy não foi possível por hora disponibilizar na PlayStore, mas como é Open Source fica aqui o projeto. Abaixo mostro algumas das telas que o app possui.

A seguir é a tela de entrada, ela possui um fundo diferente, e apenas um botão já direto ao assunto, buscar a imagem que se deseja manipular.

![image](https://user-images.githubusercontent.com/23502680/117558839-e6282a00-b056-11eb-9a29-215f0e56c977.png)

Ao pressionar o único botão irá abrir uma nova tela que permitirá o usuário buscar uma imagem de sua escolha

![image](https://user-images.githubusercontent.com/23502680/117558862-0952d980-b057-11eb-96d5-be4e901b88ff.png)

Em seguida o usuário será posto em outra tela que mostrará a imagem selecionada com a presença de dois novos botões, o de cancelar e outro com o sinal de mais.

![image](https://user-images.githubusercontent.com/23502680/117558891-3b643b80-b057-11eb-9e5d-bc455dfd82fc.png)

Caso o usuário pressione cancelar, ele então será levado de volta a primeira tela - a de entrada. Do contrário, caso ele pressione o botão mais será mostrado as opções de filtros, como a seguir.

![image](https://user-images.githubusercontent.com/23502680/117558928-88e0a880-b057-11eb-80f7-14ceeed40368.png)

Para efeitos de demonstração irei pressionar o botão de brilho e contraste. Em seguida serão mostrados dois botões de deslize para ajuste conforme o gosto do usuário.

![image](https://user-images.githubusercontent.com/23502680/117558976-cc3b1700-b057-11eb-9732-6ccd68705e1d.png)

Outro exemplo é o grayscale que quando pressionado muda os tons da imagem imediatamente, sem levar em consideração as alterações feitas pelo botão de brilho e contraste.

![image](https://user-images.githubusercontent.com/23502680/117558997-f391e400-b057-11eb-9b3b-77d216bebe23.png)
