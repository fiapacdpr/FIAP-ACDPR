# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# Atividade em Grupo: Cap 1 - Play no seu Desenvolvimento como Dev

## Nome do grupo: FIAP-ACDPR

## 👨‍🎓 Integrantes: 
- <a href="https://www.linkedin.com/in/%C3%A1lvaro-luiz-schumacker-boeira-j%C3%BAnior-5010b01a4/">Álvaro Luiz Schumacker Boeira Junior</a>
- <a href="https://www.linkedin.com/in/clara-gava-6204633a1/">Clara Salles Gava</a>
- <a href="https://www.linkedin.com/in/daniel-mioni-6b7bb434/">Daniel Ferrucio Mioni</a> 
- <a href="mailto:rodrigo.vercosa2011@gmail.com">Rodrigo Verçosa</a> 
- <a href="https://www.linkedin.com/in/patrickazevedo/">Patrick de Azevedo Ferreira</a>

## 👩‍🏫 Professores:
### Tutor(a) 
- <a href="https://www.linkedin.com/in/sabrina-otoni-22525519b/">Sabrina Otoni</a>
### Coordenador(a)
- <a href="https://www.linkedin.com/in/andregodoichiovato/">André Godoi</a>


## 📜 Descrição

O projeto da **FarmTech Solutions** aplica programação e análise de dados à **Agricultura Digital**, desenvolvendo uma solução para apoiar o gerenciamento de duas culturas relevantes do Estado do Pará: : **açaí** e **mandioca**.

Em **Python**, a aplicação permite cadastrar culturas, calcular áreas de plantio e determinar a quantidade necessária de insumos. Os dados são armazenados em vetores e gerenciados por um menu que possibilita inserir, consultar, atualizar e excluir registros. O programa utiliza estruturas de decisão, repetição e funções.

Em **R**, os dados são utilizados para análises estatísticas, incluindo média e desvio-padrão. INDO ALÉM, há também uma aplicação que consulta uma **API meteorológica pública**, apresentando informações climáticas que podem auxiliar o planejamento agrícola.

O **GitHub** é utilizado para versionamento e desenvolvimento colaborativo. O projeto também inclui uma atividade de Formação Social baseada em material da **Embrapa**, relacionando tecnologia, agricultura e impactos sociais.

Por fim, o funcionamento das aplicações Python e R será demonstrado em vídeo. Os códigos, o resumo acadêmico e o link do vídeo serão reunidos em um arquivo ZIP, consolidando programação, estatística, colaboração e Agricultura Digital.


## Regras de cálculo

### Açaí - retângulo

- Área: `comprimento × largura`;
- número de ruas: `piso(largura / espaçamento entre ruas) + 1`;
- plantas por rua: `piso(comprimento / espaçamento entre plantas) + 1`;
- insumo: `número de plantas × dose em g / 1.000`.

O padrão didático é 5 m × 5 m, coerente com orientações técnicas da Embrapa para cultivo em terra firme.

### Mandioca - trapézio

- Área: `(base maior + base menor) × altura / 2`;
- comprimento médio das ruas: `(base maior + base menor) / 2`;
- estimativa de ruas e plantas conforme os espaçamentos informados;
- insumo: `número de plantas × dose em g / 1.000`.

O padrão didático é 1 m × 1 m, utilizado no Trio da Produtividade da Mandioca em experiências no Pará.

## Observação agronômica

As doses iniciais e os registros são exclusivamente demonstrativos. Recomendação de fertilizantes ou defensivos deve considerar cultura, fase, solo, clima, rótulo do produto e orientação de engenheiro agrônomo.


## 📁 Estrutura de pastas

Dentre os arquivos e pastas presentes na raiz do projeto, definem-se:

- <b>.github</b>: Nesta pasta ficarão os arquivos de configuração específicos do GitHub que ajudam a gerenciar e automatizar processos no repositório.

- <b>assets</b>: deste repositório, aqui estão os arquivos relacionados a elementos estruturados, como .csv; semiestruturados, como .json; não-estruturadoa, como imagens.

- <b>config</b>: estão posicionados aqui arquivos de configuração que são usados para definir parâmetros e ajustes do projeto.

- <b>document</b>: aqui estão todos os documentos do projeto que as atividades poderão pedir, como o resumo do artigo "Uso de veículos aéreos não tripulados 
(VANT) em Agricultura de Precisão". Na subpasta "other", adicione documentos complementares e menos importantes.

- <b>scripts</b>: Posiciona-se aqui scripts auxiliares para tarefas específicas do seu projeto. Exemplo: deploy, migrações de banco de dados, backups.

- <b>src</b>: Todo o código fonte criado para o desenvolvimento do projeto ao longo da Fase 1.

- <b>src/IR-ALEM</b>: usando o R, aqui está a conexão a uma API meteorológica pública para coletar dados climáticos, processar e exibir as informações meteorológicas via texto simples no terminal.

- <b>README.md</b>: arquivo que serve como guia e explicação geral sobre o projeto (o mesmo que você está lendo agora).

## Entregas incluídas

- `farmtech.py`: aplicação Python com menu, vetores, cálculos, decisões e loops;
- `dados_plantio.json`: persistência do vetor com quatro registros demonstrativos;
- `dados_plantio.csv`: integração entre Python e R;
- `analise_estatistica.R`: média, mediana, desvio-padrão, mínimo e máximo;
- `clima_api.R`: consulta à API pública Open-Meteo para cinco municípios paraenses (IR ALÉM);
- `resumo_artigo_vant.docx` e `resumo_artigo_vant.pdf`: resumo de uma página;
- `ROTEIRO_VIDEO.md`: roteiro para vídeo de até cinco minutos;
- `link_video_youtube.md` e `link_video_youtube.txt`: arquivos com informações do vídeo do YouTube;
- `link_repositorio_github.md`: arquivo com informação do link do repositório;
- `areas_por_talhao.png` e `estatisticas_por_cultura.csv`: arquivos as saídas dos scripts em R;
- `CONTRIBUICAO_GITHUB.md`: fluxo colaborativo sugerido (simulação);
- `CHECKLIST_ENTREGA.md`: conferência final.

## 🔧 Como executar o código

Requisito: Python 3.10 ou superior. Não há dependências externas.

Pasta: /src

```bash
python farmtech.py
```

O menu permite incluir, listar, atualizar ou excluir uma posição do vetor. Todas as alterações são gravadas em JSON e exportadas para CSV. Os dados iniciais são exemplos fictícios de municípios do Pará e podem ser alterados durante o vídeo.

#### Como executar a análise em R

Requisito: R 4.1 ou superior.

Pasta: /src

```bash
Rscript analise_estatistica.R
```

O script lê `dados_plantio.csv`, apresenta as estatísticas no terminal e gera, em `saida_R`, um CSV consolidado e um gráfico PNG.

#### IR ALÉM: Como executar a API meteorológica em R

Pasta: /scripts

Primeiro instale a única dependência:

```bash
Rscript instalar_pacotes.R
```

Depois execute:

Pasta: /src/IR-ALEM

```bash
Rscript clima_api.R
```

Escolha Belém, Santarém, Marabá, Castanhal ou Altamira. A consulta usa a Open-Meteo, não exige chave e mostra condição atual e previsão de sete dias em texto no terminal. É necessário acesso à internet.

## 🗃 Histórico de lançamentos

* 0.4.0 - 14/09/2026
    * 
* 0.3.0 - 13/09/2026
    * 
* 0.2.0 - 09/09/2026
    * 
* 0.1.0 - 03/09/2026
    *

## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>

