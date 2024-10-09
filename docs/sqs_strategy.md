# Estrutura da mensagem

```json
{
  "task_name": "string",           // O nome da task a ser executada
  "args": [],                      // Argumentos da task a serem passados como lista
  "kwargs": {                      // Argumentos da task a serem passados como palavras-chave
    "param1": "value1",
    "param2": "value2"
  },
  "callback": {                    // Dados relacionados ao callback para quando a task for concluída
    "url": "http://example.com/callback",  // URL para o qual a resposta deve ser enviada
    "auth_token": "token_value",           // Token de autenticação para validar o callback
    "method": "POST",                      // Método HTTP a ser usado (opcional, padrão: POST)
    "headers": {                           // Headers HTTP adicionais para a requisição (opcional)
      "Content-Type": "application/json"
    }
  },
  "metadata": {                   // Metadados adicionais (opcional)
    "task_id": "uuid",            // ID único da task (para rastreamento)
    "priority": "high",           // Prioridade da mensagem (low, medium, high)
    "retries": 3,                 // Número de tentativas caso a task falhe
    "expires_at": "2023-12-31T23:59:59Z" // Data e hora de expiração da mensagem (ISO 8601)
  }
}
``` 