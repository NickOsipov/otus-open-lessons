#!/bin/bash
# Блокирует любые shell-команды, которые создают .venv внутри репозитория.
# Причина: уроки хранят только pyproject.toml, окружение живёт вне репо.
# Запуск кода разрешён только с явным UV_PROJECT_ENVIRONMENT.

set -uo pipefail

input=$(cat)
command=$(printf '%s' "$input" | jq -r '.command // empty')

if [[ -z "$command" ]]; then
  echo '{ "permission": "allow" }'
  exit 0
fi

allow() {
  echo '{ "permission": "allow" }'
  exit 0
}

deny() {
  jq -n --arg user "$1" --arg agent "$2" \
    '{ permission: "deny", user_message: $user, agent_message: $agent }'
  exit 0
}

# 1. Явное создание виртуального окружения запрещено всегда.
if [[ "$command" =~ (^|[\;\&\|[:space:]])(uv[[:space:]]+venv|virtualenv([[:space:]]|$)|python[0-9.]*[[:space:]]+-m[[:space:]]+venv) ]]; then
  deny \
    "Заблокировано: команда создаёт виртуальное окружение в репозитории." \
    "Запрещено создавать .venv. В репозитории OTUS окружения не хранятся: правь pyproject.toml, а для запуска используй UV_PROJECT_ENVIRONMENT=\"\$HOME/.cache/otus-uv/{lesson-slug}\" uv run ..."
fi

# 2. Команды uv, которые молча создают .venv в папке проекта.
if [[ "$command" =~ (^|[\;\&\|[:space:]])uv[[:space:]]+(run|sync|add|remove|pip|export|tree|build)([[:space:]]|$) ]]; then
  if [[ "$command" != *"UV_PROJECT_ENVIRONMENT="* ]]; then
    deny \
      "Заблокировано: uv создаст .venv внутри урока. Нужен UV_PROJECT_ENVIRONMENT." \
      "Эта команда uv создаст .venv в папке урока. Повтори её с окружением вне репозитория, например: UV_PROJECT_ENVIRONMENT=\"\$HOME/.cache/otus-uv/{lesson-slug}\" uv add httpx. Если запускать код не обязательно, ограничься правкой pyproject.toml."
  fi
fi

allow
