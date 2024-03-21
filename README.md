# Teste técnico para engenheiro de dados - Rox

O teste consiste em um projeto que tem como objetivo a realização de uma pipeline ETL (Extract, Transform, Load) e um relatório feito através do Looker, antigo Data Studio. Os dados do projeto estão em arquivos CSV e localizados localmente e são, em suma, dados de vendas e clientes da empresa X. Para esse projeto, utilizaremos o modelo medalhão para efetuarmos toda a esteira de engenharia de dados. O modelo medalhão consiste em dividir essa esteira em 3 camadas, sendo elas:
  - Camada bronze: camada onde os dados ingeridos são armazenados. São os dados brutos, que ainda serão trabalhados durante o projeto;
  - Camada prata: camada onde os dados são ingeridos da camada bronze e têm um tratamento e uma limpeza iniciais;
  - Camada ouro: camada onde os dados são ingeridos da camada prata, agora limpos e tratados podem ter 3 destinos: ou são armazenados para posterior uso (seja para análises, para treinaentos de modelos de machine learning ou qualquer outro tipo de uso e aplicação), ou são aplicadas regras de negócio do cliente ou qualquer outro tipo de recomendação ou análise complexa exigida pelo cliente para que se agregue valor aos dados, ou ainda, podem ser utilizados para a confecção de visualização a partir de, por exemplo, dashboards.

As ferramentas e serviços da Google Cloud Platform que usaremos em cada camada serão: na camada bronze, o Cloud Storage da Google Cloud Platform (GCP), na camada prata será o BigQuery e na camada ouro será o Looker.

Extração (Extract):

Sendo esse o representante da letra "E" da sigla ETL e significando extração, será a fase da pipeline responsável por fazer a ingestão dos dados, quaisquer que sejam as fontes. Nesse caso, temos apenas uma fonte e ela é o computador em que os arquivos se localizam. Usaremos, para isso, um conjunto de ferramentas e serviços da GCP, sendo esses: Cloud Storage, onde os arquivos serão armazenados e Cloud Composer, rodando uma DAG do Airflow, que será responsável por ativar a ingestão desses dados e será programada, em Python, para executar essa ingestão diariamente, no período da manhã.


sendo que os mesmos serão ingeridos para o Cloud Storage do GCP (Google Cloud Platform). Essa ingestão será feita através de uma DAG do Airflow, que nada mais é do que uma coleção de tarefas organizadas que você quer programar e executar, coleção essa feita utilizando a linguagem de programação Python. 

Para a ingestão dos arquivos em formato CSV, que estão localizados localmente no computador, temos três opções de serviços, quando falamos de uma ingestão feita utilizando a plataforma de computação em nuvem Google Cloud Platform (GCP): o Cloud Storage, o BigQuery e o Cloud Dataproc. Os 3 serviços tem a capacidade de realizar a tarefa, porém, cada um tem características diferentes que podem ser aplicadas a diversas necessidades, como a capacidade de trabalhar com grandes volumes de dados com escalabilidade e segurança do Cloud Storage, a possibilidade de efetuar análises complexas e com suporte a SQL e ferrametas de BI do BigQuery e a capacidade de processar e transformar dados em escala utilizando Spark ou Hadoop do Cloud Dataproc. Como, ao final do projeto, será feito um dashboard de BI, escolhi o BigQuery para trabalhar, visto seu suporte a ferramentas de BI que no caso do GCP, será o Looker, sendo essa a principal ferramenta de BI do GCP.

Da ingestão ou extração, passamos para a fase da transformação - e limpeza - dos dados. Para isso, utilizaremos o BigQuery, uma ferramenta da GCP que 
