# Mapa de Rotas
Aqui você consegue conferir as Rotas da aplicação e seus parametros importantes para cada rota de API Rest nesse sistema.

As rotas dessa aplicação sem encontra no pacote: [Source/Routes](../src/routes).

[Voltar](https://github.com/bcarsoftware/acelera_concurso_api).

## Tabela de Conteúdo
1. [Rotas de Usuário](#rotas-de-usuário)
   * [Objetos JSON de Usuário](#objetos-json-de-usuário)
2. [Rotas de Concurso](#rotas-de-concurso)
   * [Objetos JSON de Concurso](#objetos-json-de-concurso)
3. [Rotas de Disciplina](#rotas-de-disciplina)
   * [Objetos JSON de Disciplina](#objetos-json-de-disciplina)
4. [Rotas de Assunto](#rotas-de-assunto)
   * [Objetos JSON de Assunto](#objetos-json-de-assunto)
5. [Rotas de Notas de Disciplina](#rotas-de-notas-de-disciplina)
   * [Objetos JSON de Notas de Disciplina](#objetos-json-de-notas-de-disciplina)
6. [Rotas de Notas de Assunto](#rotas-de-notas-de-assunto)
   * [Objetos JSON de Notas de Assunto](#objetos-json-de-notas-de-assunto)
7. [Rotas de Verificação por Email](#rotas-de-verificação-por-email)
   * [Objetos JSON de Verificação por Email](#objetos-json-de-verificação)

## Rotas de Usuário
Módulo: [User Routes](../src/routes/user_routes.py)

| Method | Rota                   | DTO                                         | Auth | Header Param                                                                                                  |
|--------|------------------------|---------------------------------------------|------|---------------------------------------------------------------------------------------------------------------|
| POST   | `/user`                | [UserDTO](../src/models_dtos/user_dto.py)   | OFF  | <details><code>{ "Content-Type": "application/json" }</code></details>                                        |
| PATCH  | `/user/recovery`       | [LoginDTO](../src/models_dtos/login_dto.py) | OFF  | <details><code>{ "Content-Type": "application/json" }</code></details>                                        |
| PATCH  | `/user/<user_id: int>` | [UserDTO](../src/models_dtos/user_dto.py)   | ON   | <details><code>{ "Content-Type": "application/json", "Authentication": "Bearer token_value"}</code></details> |                                                                        |
| POST   | `/user/login`          | [LoginDTO](../src/models_dtos/login_dto.py) | OFF  | <details><code>{ "Content-Type": "application/json" }</code></details>                                        |
| POST   | `/user/logout`         | -                                           | ON   | <details><code>{ "Content-Type": "application/json", "Authentication": "Bearer token_value"}</code></details> |                                                                      |
| DELETE | `/user/<user_id: int>` | -                                           | ON   | <details><code>{ "Content-Type": "application/json", "Authentication": "Bearer token_value"}</code></details> |

### Objetos JSON de Usuário
> UserDTO
> ```
> {
>    "first_name": "first name",
>    "last_name": "last name",
>    "date_born": "2000-12-10",
>    "gender": "FEMALE" | "MALE" | "NOT_BINARY" | "NOT_SAY",
>    "username": "username",
>    "email": "email@service.com",
>    "password": "password123",
>    "points": 10,
>    "deleted": bool = False
> }
> ```

> LoginDTO
> ```
> {
>   "username": "username",
>   "password": "password123"
> }
> ```

## Rotas de Concurso
Módulo: [PublicTender Routes](../src/routes/public_tender_routes.py)

| Method | Rota                                              | DTO                                                        | Auth | Header Param                                                                                                                   |
|--------|---------------------------------------------------|------------------------------------------------------------|------|--------------------------------------------------------------------------------------------------------------------------------|
| POST   | `/public-tender`                                  | [PublicTenderDTO](../src/models_dtos/public_tender_dto.py) | ON   | <details><code>{ "Content-Type": "application/json", "Authentication": "Bearer token_value"}</code></details>                  |
| PATCH  | `/public-tender/<public_tender_id:int>`           | [PublicTenderDTO](../src/models_dtos/public_tender_dto.py) | ON   | <details><code>{ "Content-Type": "application/json", "Authentication": "Bearer token_value"}</code></details>                  |
| GET    | `/public-tender`                                  | -                                                          | ON   | <details><code>{ "UserID": {int}, Content-Type": "application/json", "Authentication": "Bearer token_value"}</code></details>  |
| GET    | `/public-tender/<institute: str>/institute`       | -                                                          | ON   | <details><code>{ "UserID": {int}, "Content-Type": "application/json", "Authentication": "Bearer token_value"}</code></details> |
| GET    | `/public-tender/<tender_board: str>/tender-board` | -                                                          | ON   | <details><code>{ "UserID": {int}, "Content-Type": "application/json", "Authentication": "Bearer token_value"}</code></details> |
| DELETE | `/public-tender/<public_tender_id: int>`          | -                                                          | ON   | <details><code>{ "Content-Type": "application/json", "Authentication": "Bearer token_value"}</code></details>                  |

### Objetos JSON de Concurso
> [PublicTenderDTO](../src/models_dtos/public_tender_dto.py)
> ```
> {
>   "user_id": 0,
>   "tender_name": "nome do concurso"
>   "tender_board": "banca do concurso"
>   "work_tile": "cargo desejado"
>   "institute": "contratante"
>   "notice_link": "https://link_do_edital.com.br/pdf" | null
>   "tender_date": "2017-09-25" | null
>   "deleted": false
> }
> ```

## Rotas de Disciplina
Módulo: [Subject Routes](../src/routes/subject_routes.py)

| Method | Rota                                | DTO                                             | Auth | Header Param                                                                                                                     |
|--------|-------------------------------------|-------------------------------------------------|------|----------------------------------------------------------------------------------------------------------------------------------|
| POST   | `/subject`                          | [SubjectDTO](../src/models_dtos/subject_dto.py) | ON   | <details><code>{ "Content-Type": "application/json", "Authentication": "Bearer token_value"}</code></details>                    |
| PATCH  | `/subject/<subject_id: int>`        | [SubjectDTO](../src/models_dtos/subject_dto.py) | ON   | <details><code>{ "Content-Type": "application/json", "Authentication": "Bearer token_value"}</code></details>                    |
| GET    | `/subject`                          | -                                               | ON   | <details><code>{ "TenderID": {int}, "Content-Type": "application/json", "Authentication": "Bearer token_value"}</code></details> |
| GET    | `/subject/<name: str>`              | -                                               | ON   | <details><code>{ "TenderID": {int}, "Content-Type": "application/json", "Authentication": "Bearer token_value"}</code></details> |
| PATCH  | `/subject/<subject_id: int>/finish` | -                                               | ON   | <details><code>{ "Content-Type": "application/json", "Authentication": "Bearer token_value"}</code></details>                    |              
| DELETE | `/subject/<subject_id: int>`        | -                                               | ON   | <details><code>{ "Content-Type": "application/json", "Authentication": "Bearer token_value"}</code></details>                    |

### Objetos JSON de Disciplina
> [SubjectDTO](../src/models_dtos/subject_dto.py)
> ```
> {
>   "public_tender_id": 0
>   name: "subject name"
>   category: "GENERAL" | "SPECIFIC"
>   status: "COMPLETE" | "INCOMPLETE",
>   deleted: false
> }
> ```

## Rotas de Assunto
Módulo: [Topic Routes](../src/routes/topic_routes.py)

| Method | Rota                            | DTO                                         | Auth | Header Param                                                                                                                      |
|--------|---------------------------------|---------------------------------------------|------|-----------------------------------------------------------------------------------------------------------------------------------|
| POST   | `/topic`                        | [TopicDTO](../src/models_dtos/topic_dto.py) | ON   | <details><code>{ "Content-Type": "application/json", "Authentication": "Bearer token_value"}</code></details>                     |
| PATCH  | `/topic/<topic_id: int>`        | [TopicDTO](../src/models_dtos/topic_dto.py) | ON   | <details><code>{ "Content-Type": "application/json", "Authentication": "Bearer token_value"}</code></details>                     |
| GET    | `/topic`                        | -                                           | ON   | <details><code>{ "SubjectID": {int}, "Content-Type": "application/json", "Authentication": "Bearer token_value"}</code></details> |
| GET    | `/topic/<name: str>/name`       | -                                           | ON   | <details><code>{ "SubjectID": {int}, "Content-Type": "application/json", "Authentication": "Bearer token_value"}</code></details> |
| GET    | `/topic/<status: str>/status`   | -                                           | ON   | <details><code>{ "SubjectID": {int}, "Content-Type": "application/json", "Authentication": "Bearer token_value"}</code></details> |
| PATCH  | `/topic/<topic_id: int>/finish` | -                                           | ON   | <details><code>{ "Content-Type": "application/json", "Authentication": "Bearer token_value"}</code></details>                     |
| DELETE | `/topic/<topic_id: int>`        | -                                           | ON   | <details><code>{ "Content-Type": "application/json", "Authentication": "Bearer token_value"}</code></details>                     |

> status: COMPLETE | INCOMPLETE

### Objetos JSON de Assunto
> [TopicDTO](../src/models_dtos/topic_dto.py)
> ```
> {
>   subject_id: 0,
>   name: "topic name,
>   fulfillment: 50.0,
>   status: "COMPLETE" | "INCOMPLETE",
>   deleted: false
> }
> ```

## Rotas de Notas de Disciplina
Módulo: [NoteSubject Routes](../src/routes/note_subject_routes.py)

| Method | Rota                                      | DTO                                                      | Auth | Header Param                                                                                                  |
|--------|-------------------------------------------|----------------------------------------------------------|------|---------------------------------------------------------------------------------------------------------------|
| POST   | `/note-subject`                           | [NoteSubjectDTO](../src/models_dtos/note_subject_dto.py) | ON   | <details><code>{ "Content-Type": "application/json", "Authentication": "Bearer token_value"}</code></details> |
| PATCH  | `/note-subject/<note_subject_id: int>`    | [NoteSubjectDTO](../src/models_dtos/note_subject_dto.py) | ON   | <details><code>{ "Content-Type": "application/json", "Authentication": "Bearer token_value"}</code></details> |
| GET    | `/note-subject/<subject_id: int>/subject` | -                                                        | ON   | <details><code>{ "Content-Type": "application/json", "Authentication": "Bearer token_value"}</code></details> |
| PATCH  | `/note-subject/<note_subject_id: int>`    | [NoteSubjectDTO](../src/models_dtos/note_subject_dto.py) | ON   | <details><code>{ "Content-Type": "application/json", "Authentication": "Bearer token_value"}</code></details> |
| DELETE | `/note-subject/<note_subject_id: int>`    | -                                                        | ON   | <details><code>{ "Content-Type": "application/json", "Authentication": "Bearer token_value"}</code></details> |

### Objetos JSON de Notas de Disciplina
> [NoteSubjectDTO](../src/models_dtos/note_subject_dto.py)
> ```
> {
>   "subject_id": 0,
>   "description": "note subject dscription",
>   "finish": false,
>   "rate_success": 41.5 | null
>   "deleted": false
> }
> ```

## Rotas de Notas de Assunto
Módulo: [NoteTopic Routes](../src/routes/note_topic_routes.py)

| Method | Rota                                      | DTO                                                  | Auth | Header Param                                                                                                  |
|--------|-------------------------------------------|------------------------------------------------------|------|---------------------------------------------------------------------------------------------------------------|
| POST   | `/note-topic`                             | [NoteTopicDTO](../src/models_dtos/note_topic_dto.py) | ON   | <details><code>{ "Content-Type": "application/json", "Authentication": "Bearer token_value"}</code></details> |
| PATCH  | `/note-topic/<note_topic_id: int>`        | [NoteTopicDTO](../src/models_dtos/note_topic_dto.py) | ON   | <details><code>{ "Content-Type": "application/json", "Authentication": "Bearer token_value"}</code></details> |
| GET    | `/note-topic/<topic_id: int>/topic`       |                                                      | ON   | <details><code>{ "Content-Type": "application/json", "Authentication": "Bearer token_value"}</code></details> |
| PATCH  | `/note-topic/<note_topic_id: int>/finish` | [NoteTopicDTO](../src/models_dtos/note_topic_dto.py) | ON   | <details><code>{ "Content-Type": "application/json", "Authentication": "Bearer token_value"}</code></details> |
| DELETE | `/note-topic/<note_topic_id: int>`        |                                                      | ON   | <details><code>{ "Content-Type": "application/json", "Authentication": "Bearer token_value"}</code></details> |

### Objetos JSON de Notas de Assunto
> [NoteTopicDTO](../src/models_dtos/note_topic_dto.py)
> ```
> {
>   "topic_id": 0,
>   "description": "note topic dscription",
>   "finish": false,
>   "rate_success": 41.5 | null
>   "deleted": false
> }
> ```

## Rotas de Verificação por Email
Módulo: [EmailCode Routes](../src/routes/email_code_routes.py)

| Method | Rota                 | DTO                                                    | Auth | Header Param                                                           |
|--------|----------------------|--------------------------------------------------------|------|------------------------------------------------------------------------|
| POST   | `/email-code`        | [EmailDTO](../src/models_dtos/email_dto.py)            | OFF  | <details><code>{ "Content-Type": "application/json" }</code></details> |
| POST   | `/email-code/verify` | [ActiveCodeDTO](../src/models_dtos/active_code_dto.py) | OFF  | <details><code>{ "Content-Type": "application/json" }</code></details> |

### Objetos JSON de Verificação
> EmailDTO
> ```
> {
>   "email": "username@service.com"
> }
> ```

> ActiveCodeDTO
> ```
> {
>   "code": "code_not_encrypted" | null
>   "secure_code": "secure_encrypted_code",
>   "token": "jwt_token" | null
> }
> ```

*That's All Folks!*
[Voltar](https://github.com/bcarsoftware/acelera_concurso_api).
