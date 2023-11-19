# Inception Parser

O projeto de parser de anotações de texto do software Inception é uma colaboração com a Universidade de Évora, visando aprimorar a formatação do arquivo de saída gerado pelo próprio software. 

A principal finalidade é otimizar a legibilidade do documento final, unificando e formatando de maneira coesa todas as entidades extraídas durante o processo de anotação de texto. 

Em outras palavras, o parser atua como uma ferramenta que organiza e estrutura as informações extraídas pelo Inception, tornando o resultado mais compreensível e acessível para os usuários.

Também dentro da pasta src/exploratory-data-analysis é fornecido um notebook para análise exploratória dos dados com algumas visualizações do comportamento dos dados e distribuição das entidades entre as freguesias.

## Instruções

Para executar o parser de um ou mais arquivos: 
1. Copie-os para a pasta DataToParse;
2. Os arquivos devem estar em formato .tsv como retornado pelo Inception;
   1. Texto anotado: 
      ['#Text=Beringel, 1758\\r'] \
      ['#Text=Memória Paroquial de Beringel, Comarca de Beja\\r'] \
      ['#Text=[ANTT, Memórias paroquiais, vol. 7, nº 8, p. 755 a 760]\\r'] \
      ['#Text=\\r'] \
      ['#Text=“p. 755/\\r'] \
      ['#Text=Vila de Beringel.\\r'] \
      ['#Text=1 A vila de Beringel fica na província de Alentejo, no arcebispado de Évora, comarca de Beja.'] 
   2. seguido de cada palavra como o exemplo abaixo: \
      ['1-1', '0-8', 'Beringel', '_', '_', 'Header[52]', '']
3. Navegue até a pasta src do projeto e chame o script Main.py passando o nome do arquivo que queremos fazer o parser. 
4. O arquivo resultado do parser será gerado dentro da pasta ParsedData com o nome do arquivo, a data e hora de execução mais um sufixo "_parsed".
5. É gerado um arquivo de log para cada execução de cada arquivo onde podemos analisar o que ocorreu em cada linha analisada;
6. Durante o processo é feita uma análise da estrutura frase a frase, caso não possua 6 ou mais colunas, a linha é ignorada e o processo avança para a próxima linha;
7. Cada função utilizada encontra-se dentro da classe Parser\Inception.py. E cada função encontra-se documentada.
8. Também gera-se um arquivo agregado, contendo todas as entidades de todos arquivos analisados (caso tenha sido passado mais de um arquivo como parâmetro)

### Pré-requisitos

- Python (version 3.9.13);
- Existe um arquivo requirements com todas as outras dependências;

### Instalação

1. Clone o repositório:
   ```shell
   git clone <repository_url>
   ```

2. Instale as dependências necessárias:
   ```shell
   pip install -r requirements.txt
   ```

### Usage

1. Navegue até o diretório do projeto:
   ```shell
   cd ../inception-entity-parser/src/
   ```

2. Run the code:
   
   ```shell
   python Main.py "Beja_Beringel.modernizada"
   ```
   Caso seja mais de um arquivo, deve ser passado os nomes dos arquivos separados por ";" sem espaços entre os nomes.
   ```shell
   python Main.py "Beja_Beringel.modernizada;VilaVicosa_SantaAnaDeBencatel.revista.normalizada;VilaVicosa_SaoBartolomeu.revista.normalizada;"
   ```
   
3. Visualizar os logs:
Os logs serão salvos no diretório de logs com o formato [nome do arquivo]_[timestamp].log. 

5. Saída\resultados:
- A saída será salva como arquivos CSV:
   - Arquivos individuais: [nome do arquivo].csv
   - Arquivo agregado: freguesias_agregado.csv