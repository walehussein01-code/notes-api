*# Serverless Notes API*



*A small API where each logged-in user can create, list and delete their own notes. Built on AWS.*



*!\[Architecture](docs/architecture.png)*



*## What I used*

*- \*\*API Gateway:\*\* the front door. It receives requests and checks the login token.*

*- \*\*Cognito:\*\* checks who the user is.*

*- \*\*Lambda (Python):\*\* runs my code.*

*- \*\*DynamoDB:\*\* stores the notes.*

*- \*\*IAM:\*\* a permission that lets the Lambda touch only the notes table.*



*## What it can do*

*| Request | What happens |*

*|---------|--------------|*

*| POST /notes | Saves a new note |*

*| GET /notes | Shows my notes |*

*| DELETE /notes/{noteId} | Deletes one of my notes |*



*## How to try it*

*```bash*

*curl -X POST "$INVOKE\_URL/notes" -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d '{"text":"my first note"}'*

*curl "$INVOKE\_URL/notes" -H "Authorization: Bearer $TOKEN"*

*curl -X DELETE "$INVOKE\_URL/notes/NOTE\_ID\_HERE" -H "Authorization: Bearer $TOKEN"*

*```*



*## Problems I fixed*

*- API Gateway said "Not Found" because the DELETE route did not exist yet. I added it.*

*- The Lambda crashed with an indentation error. I found it in the CloudWatch logs.*

*- DynamoDB said AccessDenied. I fixed it by giving the Lambda role a small policy.*



*## What I want to add next*

*- An update route*

*- Infrastructure as code*

*- A small website that uses the API*



*## About me*

*Fuad Oseni,  AWS learner. GitHub: \[@walehussein01-code](https://github.com/walehussein01-code)*

