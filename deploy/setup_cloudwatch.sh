#!/bin/bash

REGION="eu-central-1"
ACCOUNT_ID="ACCOUNT_ID"
CLUSTER_NAME="CLUSTER_NAME"
TASK_DEFINITION="TASK_DEFINITION"
SUBNET_ID="subnet-SUBNET_ID"
SECURITY_GROUP_ID="sg-SECURITY_GROUP_ID"
RULE_NAME="run-every-hour"
ROLE_NAME="CloudWatchEventsRole"
RULE_SCHEDULE="rate(1 hour)"

TRUST_POLICY_FILE="trust-policy.json"
cat > "$TRUST_POLICY_FILE" <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "events.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
EOF

aws iam create-role \
    --role-name "$ROLE_NAME" \
    --assume-role-policy-document file://"$TRUST_POLICY_FILE" || echo "Role already exists"

PERMISSION_POLICY_FILE="permission-policy.json"
cat > "$PERMISSION_POLICY_FILE" <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ecs:RunTask",
                "iam:PassRole"
            ],
            "Resource": "*"
        }
    ]
}
EOF

aws iam put-role-policy \
    --role-name "$ROLE_NAME" \
    --policy-name "${ROLE_NAME}Policy" \
    --policy-document file://"$PERMISSION_POLICY_FILE"

aws events put-rule \
    --name "$RULE_NAME" \
    --schedule-expression "$RULE_SCHEDULE" \
    --region "$REGION"

TARGETS_JSON="[
    {
        \"Id\": \"1\",
        \"Arn\": \"arn:aws:ecs:$REGION:$ACCOUNT_ID:cluster/$CLUSTER_NAME\",
        \"RoleArn\": \"arn:aws:iam::$ACCOUNT_ID:role/$ROLE_NAME\",
        \"EcsParameters\": {
            \"TaskDefinitionArn\": \"arn:aws:ecs:$REGION:$ACCOUNT_ID:task-definition/$TASK_DEFINITION\",
            \"LaunchType\": \"FARGATE\",
            \"NetworkConfiguration\": {
                \"awsvpcConfiguration\": {
                    \"Subnets\": [\"$SUBNET_ID\"],
                    \"SecurityGroups\": [\"$SECURITY_GROUP_ID\"],
                    \"AssignPublicIp\": \"ENABLED\"
                }
            }
        }
    }
]"

aws events put-targets \
    --rule "$RULE_NAME" \
    --targets "$TARGETS_JSON" \
    --region "$REGION"

rm -f "$TRUST_POLICY_FILE" "$PERMISSION_POLICY_FILE"

echo "CloudWatch Event '$RULE_NAME' has been configured to start the ECS task every hour."