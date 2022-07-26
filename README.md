# Hello strawberry project

## Installing dependencies

Project uses poetry to manage dependencies.
```
# activate venv
pip install poetry
python -m poetry install
```

## Running the project

Copy the `.env_example` file to `.env` - this is a file used as a config.
```
cp .env_example .env
```

Run PostgreSQL and the app:
```
docker compose up -d
alembic upgrade head
python main.py
```

## Infra

Install aws-cdk globally
```bash
npm install -g aws-cdk
cdk --version
```

Run
```bash
cdk bootstrap
# for ng accounts:
aws-vault exec cloudsandbox08 -- aws cloudformation create-stack --region eu-central-1 --capabilities CAPABILITY_NAMED_IAM --template-body file://my-bootstrap.yml --parameters ParameterKey=PermissionsBoundaryPolicy,ParameterValue=arn:aws:iam::690296641723:policy/netguru-boundary ParameterKey=CloudFormationExecutionPolicies,ParameterValue=arn:aws:iam::690296641723:policy/netguru-boundary --stack-name CDKToolkit
```
