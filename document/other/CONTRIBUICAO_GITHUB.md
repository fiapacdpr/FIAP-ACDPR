# Versionamento colaborativo no GitHub

# OBS.: Isso somente é uma simulação do que faríamos na vida real. As branches não foram criadas.

## Divisão

1. Patrick de Azevedo: aplicação Python e testes.
2. Clara Gava: estatística e API meteorológica em R.
3. Daniel Mioni, Álvaro Schumacker, Rodrigo Verçosa: resumo do artigo e referências.
4. Todos: testes integrados, revisão e vídeo.

## Fluxo recomendado

O responsável cria um repositório público ou privado e adiciona os colegas como colaboradores. Cada integrante trabalha em uma branch própria:

```bash
git clone https://github.com/fiapacdpr/FIAP-ACDPR
git switch -c feature/python-crud
git add farmtech.py tests/
git commit -m "feat: implementa CRUD e cálculos agrícolas"
git push -u origin feature/python-crud
```

Para os demais artefatos, podem ser usadas branches como `feature/analise-r`, `feature/api-clima` e `docs/resumo-embrapa`. Cada branch deve gerar um Pull Request revisado por outro integrante antes do merge em `main`.

## Evidências para avaliação

- histórico com commits pequenos e mensagens claras;
- branches de mais de um integrante;
- Pull Requests com revisão;
- `README.md` atualizado;
- link definitivo registrado em `link_repositorio_github.txt`.

Não incluam senhas, tokens ou chaves no repositório. A API escolhida não exige chave.
