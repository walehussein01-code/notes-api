cat > lambda_function.py <<'EOF'
import json, os, time, uuid
import boto3
from boto3.dynamodb.conditions import Key

table = boto3.resource("dynamodb").Table(os.environ["TABLE_NAME"])

def respond(code, body):
    return {"statusCode": code,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(body, default=str)}

def lambda_handler(event, context):
    user_id = event["requestContext"]["authorizer"]["jwt"]["claims"]["sub"]
    route = event["routeKey"]

    if route == "POST /notes":
        data = json.loads(event.get("body") or "{}")
        text = str(data.get("text", "")).strip()
        if not text:
            return respond(400, {"error": "text is required"})
        item = {"userId": user_id, "noteId": str(uuid.uuid4()),
                "text": text[:500], "createdAt": int(time.time())}
        table.put_item(Item=item)
        return respond(201, item)

    if route == "GET /notes":
        result = table.query(KeyConditionExpression=Key("userId").eq(user_id))
        return respond(200, result["Items"])

    if route == "DELETE /notes/{noteId}":
        note_id = event["pathParameters"]["noteId"]
        try:
            table.delete_item(
                Key={"userId": user_id, "noteId": note_id},
                ConditionExpression="attribute_exists(noteId)",
            )
        except table.meta.client.exceptions.ConditionalCheckFailedException:
            return respond(404, {"error": "note not found"})
        return respond(204, {})

    return respond(404, {"error": "not found"})
EOF