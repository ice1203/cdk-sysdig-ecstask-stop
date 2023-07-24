import json
import boto3
import re
# AWS ECS clientを初期化
client = boto3.client('ecs')


def lambda_handler(event, context):
    # print(json.dumps(event))
    data = event['Records'][0]['Sns']['Message']

    # aws.fargate.task.arnが存在するか確認
    match = re.search(r'aws.fargate.task.arn:\s*(.*?)\n', data)
    if match:
        # 停止対象のFargateタスクARNを表示
        task_arn = match.group(1)
        print("Fargate-Task-ARN to be stopped: " + task_arn)
        try:
            # ECSタスクを停止
            response = client.stop_task(
                cluster=task_arn.split('/')[1],
                task=task_arn,
                reason='Stopped by Lambda function'
            )
            print(f'Stopped task: {task_arn}')
        except Exception as e:
            print(f'Error stopping task: {task_arn}. Error: {str(e)}')
            raise e
    else:
        # 'aws.fargate.task.arn'が見つからない場合、エラーを出力して終了
        print('Error: aws.fargate.task.arn not found in data')
        raise Exception(
            'Error: aws.fargate.task.arn not found in data')

    return {
        'statusCode': 200,
        'body': json.dumps(data)
    }
