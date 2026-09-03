# FarmTech Solutions - Agricultura Digital no Pará

Projeto acadêmico desenvolvido para a FIAP com duas culturas relevantes para o Pará: **açaí** e **mandioca**. O sistema calcula área, estima ruas e plantas, dimensiona insumo, mantém os dados em vetor, realiza CRUD e exporta os registros para análise em R.

## Entregas incluídas

- `farmtech.py`: aplicação Python com menu, vetores, cálculos, decisões e loops;
- `dados_plantio.json`: persistência do vetor com quatro registros demonstrativos;
- `dados_plantio.csv`: integração entre Python e R;
- `analise_estatistica.R`: média, mediana, desvio-padrão, mínimo e máximo;
- `clima_api.R`: consulta à API pública Open-Meteo para cinco municípios paraenses;
- `resumo_artigo_vant.docx` e `resumo_artigo_vant.pdf`: resumo de uma página;
- `ROTEIRO_VIDEO.md`: roteiro para vídeo de até cinco minutos;
- `link_video_youtube.txt` e `link_repositorio_github.txt`: arquivos a preencher;
- `CONTRIBUICAO_GITHUB.md`: fluxo colaborativo sugerido;
- `CHECKLIST_ENTREGA.md`: conferência final.

## Como executar a aplicação Python

Requisito: Python 3.10 ou superior. Não há dependências externas.

```bash
python farmtech.py
```

O menu permite incluir, listar, atualizar ou excluir uma posição do vetor. Todas as alterações são gravadas em JSON e exportadas para CSV. Os dados iniciais são exemplos fictícios de municípios do Pará e podem ser alterados durante o vídeo.

### Testes automatizados

Na pasta do projeto, execute:

```bash
python -m unittest discover -s tests -v
```

## Como executar a análise em R

Requisito: R 4.1 ou superior.

```bash
Rscript analise_estatistica.R
```

O script lê `dados_plantio.csv`, apresenta as estatísticas no terminal e gera, em `saida_R`, um CSV consolidado e um gráfico PNG.

## Como executar a API meteorológica em R

Primeiro instale a única dependência:

```bash
Rscript instalar_pacotes.R
```

Depois execute:

```bash
Rscript clima_api.R
```

Escolha Belém, Santarém, Marabá, Castanhal ou Altamira. A consulta usa a Open-Meteo, não exige chave e mostra condição atual e previsão de sete dias em texto no terminal. É necessário acesso à internet.

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

## Antes de entregar

Preencha os nomes/RMs do grupo, o endereço do repositório e o link do vídeo. Depois confira `CHECKLIST_ENTREGA.md` e gere novamente o ZIP sem a pasta `.git`.
