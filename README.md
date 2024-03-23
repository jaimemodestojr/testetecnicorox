# Teste técnico para engenheiro de dados - Rox

O teste consiste em um projeto que tem como objetivo a realização de tarefas corriqueiras na rotina de um engenheiro de dados, especificamente: fazer a modelagem conceitual dos dados fornecidos para o teste, criar a infraestrutura necessária para a realização do teste, criar todos os artefatos necessários para carregar os arquivos fornecidos para o banco criado, desenvolvimento de script para análise de dados e também criar um relatório em qualquer ferramenta de visualização de dados.

Segue abaixo a imagem da modelagem conceitual dos dados recomendada para o teste:

<img src="images/modelagem recomendada.png">

Os dados fornecidos para o teste são dados de vendas, clientes e produtos de uma empresa fictícia e todos estão no formato CSV.

Portanto temos como objetivos, falando de maneira resumida, a criação de uma pipeline ETL (Extract, Transform, Load) e um relatório baseado nos dados e nas análises feitas dos mesmos. Os dados do projeto estão localizados localmente. Para esse projeto, utilizaremos o modelo medalhão para efetuarmos toda a esteira de engenharia de dados. O modelo medalhão consiste em dividir essa esteira em 3 camadas, sendo elas:
  - Camada bronze: camada onde os dados ingeridos são armazenados. São os dados brutos, que ainda serão trabalhados durante o projeto;
  - Camada prata: camada onde os dados são ingeridos da camada bronze e têm um tratamento e uma limpeza iniciais;
  - Camada ouro: camada onde os dados são ingeridos da camada prata, agora limpos e tratados podem ter 3 destinos: ou são armazenados para posterior uso (seja para análises, para treinaentos de modelos de machine learning ou qualquer outro tipo de uso e aplicação), ou são aplicadas regras de negócio do cliente ou qualquer outro tipo de recomendação ou análise complexa exigida pelo cliente para que se agregue valor aos dados, ou ainda, podem ser utilizados para a confecção de visualização a partir de, por exemplo, dashboards.

<img src="images/lakehouse - medalhão.png">

Para a realização do projeto, foi utilizada a plataforma de computação em nuvem Google Cloud Platform (GCP). As ferramentas e serviços da GCP que serão usados em cada camada serão: na camada bronze, o Cloud Storage da Google Cloud Platform (GCP), na camada prata será o BigQuery e na camada ouro será o Looker. As ferramentas e serviços foram escolhidos por se adequarem melhor aos objetivos e necessidades do projeto.

- Primeiro, foi criado um bucket no Cloud Storage, chamado "dados_teste_rox" e, dentro dele, foram criadas duas pastas, "dados_recebidos" e "dados_finais";
- Em seguida, foi feita a ingestão dos arquivos fornecidos para o teste no bucket criado, em específico, na pasta "dados_recebidos". Essa ingestão foi feita através de um script em Python e, através do serviço do GCP chamado Cron Jobs, foi feito um agendamento, cujo qual ativa, diariamente, o funcionamento desse script, ou seja, automatiza a tarefa de ingestão de dados, mantendo o nosso banco de dados sempre atualizado;
- Em sequência, foi criado um cluster no serviço Dataproc, onde faremos o processamento deses dados, isto é, transformação e posterior análise dos mesmos;

# Código Python:

from google.cloud import storage
from pathlib import Path

bucket_name = "dados_rox"
local_dir = Path("caminho/da/pasta/local/contendo/os/arquivos/fornecidos/pelo/teste")
client = storage.Client()
bucket = client.bucket(bucket_name)

def upload_csv(filename):
    blob = bucket.blob(filename)
    blob.upload_from_filename(local_dir / filename)

csv_files = list(local_dir.glob("*.csv"))

for filename in csv_files:
    upload_csv(filename.name)

- O cluster criado, em Hadoop, tem suporte para Jupyter Notebook, que usaremos para tratar os dados. Esse tratamento será feito com Pyspark;
- Após o passo anterior, carregamos os dados prontos, isto é, tratados e limpos, na outra pasta criada dentro do bucket, a "dados_finais";
- Acessando a pasta "dados_finais" por um Jupyter Notebook dentro do Dataproc e do ambiente Hadoop, realizamos as queries que o teste solicitou, sendo elas:

1) Escreva uma query que retorna a quantidade de linhas na tabela Sales.SalesOrderDetail pelo campo SalesOrderID, desde que tenham pelo menos três linhas de detalhes:

SELECT SalesOrderID as id, 
COUNT(*) AS qtd 
FROM Sales.SalesOrderDetail as sod
GROUP BY SalesOrderID
HAVING qtd >= 3

2) Escreva uma query que ligue as tabelas Sales.SalesOrderDetail, Sales.SpecialOfferProduct e Production.Product e retorne os 3 produtos (Name) mais vendidos (pela soma de OrderQty), agrupados pelo número de dias para manufatura (DaysToManufacture):

SELECT * FROM(
  SELECT p.DaysToManufacture AS dtm,
         ROW_NUMBER() OVER(PARTITION BY p.DaysToManufacture ORDER BY sum(sod.OrderQty) DESC) as pos,
         p.Name as name,
         sum(sod.OrderQty) AS qtd
  FROM Sales.SpecialOfferProduct AS sop 
  INNER JOIN Production.Products AS p ON sop.ProductID = p.ProductID
  INNER JOIN Sales.SalesOrderDetail AS sod ON sop.SpecialOfferID = sod.SalesOrderDetailID
  GROUP BY name
  ) as by_pos
WHERE pos <= 3

3 Escreva uma query ligando as tabelas Person.Person, Sales.Customer e Sales.SalesOrderHeader de forma a obter uma lista de nomes de clientes e uma contagem de pedidos efetuados:

SELECT c.CustomerID as id, 
       CONCAT(p.FirstName, ' ', p.LastName) as name, 
       COUNT(*) AS qtd 
FROM Sales.SalesOrderHeader as soh
INNER JOIN	Sales.Customer as c ON soh.CustomerID = c.CustomerID
INNER JOIN Person.Person as p ON c.PersonID = p.BusinessEntityID 
GROUP BY c.PersonID
ORDER BY qtd DESC

4) Escreva uma query usando as tabelas Sales.SalesOrderHeader, Sales.SalesOrderDetail e Production.Product, de forma a obter a soma total de produtos (OrderQty) por ProductID e OrderDate:

SELECT sod.ProductID as id, 
       p.Name as name,
       sum(OrderQty) OVER(PARTITION BY sod.ProductID) AS qtd_id,
       soh.OrderDate,  
       sum(OrderQty) OVER(PARTITION BY soh.OrderDate) AS qtd_OrderDate
FROM Sales.SalesOrderDetail AS sod
INNER JOIN Sales.SalesOrderHeader as soh ON sod.SalesOrderID  = soh.SalesOrderID 
INNER JOIN Production.Products AS p ON sod.ProductID = p.ProductID 
GROUP BY sod.ProductID, soh.OrderDate
ORDER BY soh.OrderDate
  
6) Escreva uma query mostrando os campos SalesOrderID, OrderDate e TotalDue da tabela Sales.SalesOrderHeader. Obtenha apenas as linhas onde a ordem tenha sido feita durante o mês de setembro/2011 e o total devido esteja acima de 1.000. Ordene pelo total devido decrescente:

SELECT SalesOrderID, DATE(OrderDate), TotalDue 
FROM SalesOrderHeader AS soh 
WHERE DATE(OrderDate) BETWEEN DATE('2011-09-01') AND DATE('2011-09-30') AND TotalDue > 1.000
ORDER BY TotalDue DESC
