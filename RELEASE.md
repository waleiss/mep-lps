# Processo de Release (main e develop)

Este guia descreve um fluxo simples e confiável para criar releases para o cliente mantendo duas branches principais: `main` e `develop`.

- `develop`: branch de integração contínua. Merge de features e fixes acontece aqui.
- `main`: branch estável. Tudo que é mergeado aqui está pronto para ir ao cliente.

Releases são marcadas por tags semânticas (ex.: `v1.2.0`). Ao criar uma tag em `main`, um Release no GitHub será aberto automaticamente (workflow incluso).

## Requisitos
- Git com acesso ao repositório `origin` (GitHub).
- Permissão para criar branches e tags.
- Commits preferencialmente em padrão de Conventional Commits (opcional, mas ajuda na geração de notas de release).

## Versão Semântica (semver)
Use `MAJOR.MINOR.PATCH`:
- MAJOR: mudanças incompatíveis (breaking changes)
- MINOR: novas funcionalidades compatíveis
- PATCH: correções de bugs sem mudança de API

Exemplos: `v1.0.0`, `v1.1.0`, `v1.1.1`.

## Fluxo de trabalho diário
1) Crie branches de feature a partir de `develop` (ex.: `feature/minha-feature`).
2) Abra PR para `develop` e faça o merge após review e testes.
3) Quando estiver pronto para liberar ao cliente, crie uma PR de `develop` para `main`.
4) Após o merge na `main`, crie uma tag de release em `main`.

## Como criar uma release da main
1) Garanta que você está na `main` e sincronizado:
   - `git checkout main`
   - `git pull --ff-only`
2) Defina a versão (ex.: `v1.0.0`) e crie a tag anotada:
   - `git tag -a v1.0.0 -m "release: v1.0.0"`
3) Envie a tag para o remoto:
   - `git push origin v1.0.0`

Isso aciona o workflow de Release no GitHub, que:
- Gera um Release com notas automaticamente.
- Compila o frontend (`frontend/app`) e anexa um pacote (`frontend-dist.zip`) como artefato no Release.

Observação: Caso o build do frontend precise de ajustes, edite o workflow em `.github/workflows/release.yml`.

## Hotfix (correção urgente na produção)
1) Crie uma branch a partir de `main` (ex.: `hotfix/corrige-bug`).
2) Corrija e abra PR para `main`.
3) Após merge em `main`, crie uma nova tag de patch (ex.: `v1.0.1`) e envie.
4) Faça back-merge de `main` para `develop` para manter tudo sincronizado.

## Boas práticas
- Proteja as branches `main` e `develop` no GitHub (PRs com review obrigatório, checks passando).
- Use Conventional Commits para notas de release melhores.
- Mantenha `docker-compose.prod.yml` atualizado para facilitar a entrega ao cliente.

## Entrega ao cliente
- Preferencial: entregue referência da tag (ex.: `v1.0.0`) + instruções de deploy.
- Alternativa: baixe o Release no GitHub e forneça o `frontend-dist.zip` para hospedagem estática.
- Para rodar containers, use `docker-compose.prod.yml` (ajuste variáveis de ambiente conforme necessário).

