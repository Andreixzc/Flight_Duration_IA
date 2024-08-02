### 1ª Tarefa

Primeiro criei o banco de dados com armazenando os dois arquivos CSV, `airports` e `positions`. Depois fiz um script que puxou os dados ordenando eles pelo ID de cada aeronave, a fim de facilitar o pré-processamento. Como os registros eram naturalmente ordenados por tempo, ficou mais fácil.

Daí, chegou a parte de segmentar os voos, e como eu tinha separado os registros em arquivos separados por ID de aeronave, pude segmentá-los em memória porque limitei a quantidade de registros analisados, evitando assim o estouro de RAM e diminuindo a complexidade de ter que salvar a referência dos registros de ID diferente, por exemplo.

Percebi que havia um padrão no registro do tempo dos voos e logo cheguei à conclusão que para segmentar os voos em função do tempo. A maior dificuldade foi pensar em um limiar de tempo (intervalo) que separasse os voos. Diante disso, cheguei a 2 possíveis soluções:

1. **Percorrer o CSV de `airports` e tentar encontrar um limiar que gerasse o menor tempo de voo possível dada essa combinação de aeroportos.**  
   Problema: Complexidade alta, teríamos que pensar em ordenar os arquivos em chunks de distância baseadas em um ponto de origem, sendo assim teríamos que pensar em definir uma distância de threshold entre aeroportos para agrupá-los, pois se não fizermos isso, temos a chance de calcular distâncias de voos que não são possíveis de fazer. Daí, usaríamos esse limiar para segmentar os voos.

2. **Definir um limiar base e, por tentativa e erro, encontrar uma que minimiza os voos 'impossíveis', de duração duvidosa.**  
   Depois disso, bastaria remover os voos que por acaso tiveram a mesma origem e o mesmo destino. Depois talvez os outliers, que são casos incomuns, como por exemplo os casos de voos que têm duração muito pequena que são provenientes de destinos inóspitos, como ilhas.  
   Problema: Essa solução ainda pode gerar inconsistências, mas realisticamente falando é a mais viável. 

Optei pela segunda opção. Depois disso, bastou fazer a aproximação das coordenadas de origem e destino para encontrar os respectivos aeroportos.

### 2ª Tarefa

Problema clássico de sliding window, bastou ir 'deslizando' a janela até encontrar o maior valor possível que respeitava o intervalo de 2 dias. Primeiramente pensei que pudesse ser um problema de DP, mas lembrei que tinha que seguir analisando os registros sequencialmente.

### 3ª Tarefa

Bastou rodar um script para que pegava a tabela gerada na 1ª tarefa e calcular a duração do voo em minutos e pronto, minha base de dados estava pronta para o modelo.
