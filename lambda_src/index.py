import json
import boto3
# AWS ECS clientを初期化
client = boto3.client('ecs')


def lambda_handler(event, context):
    # TODO implement
    print(json.dumps(event))
    data = json.loads(event['Records'][0]['Sns']['Message'])
    print(json.dumps(data))

    # stateがACTIVEの場合にのみ処理を行う
    # if data['alert']['state'] == 'ACTIVE':
    #    # entitiesリストをループ
    #    for entity in data['alert']['entities']:
    #        # dataLabelsが存在し、'aws.fargate.task.arn'のキーがあるか確認
    #        if 'dataLabels' in entity and 'aws.fargate.task.arn' in entity['dataLabels']:
    #            task_arn = entity['dataLabels']['aws.fargate.task.arn']
    #            try:
    #                # ECSタスクを停止
    #                response = client.stop_task(
    #                    cluster=task_arn.split('/')[1],
    #                    task=task_arn,
    #                    reason='Stopped by Lambda function'
    #                )
    #                print(f'Stopped task: {task_arn}')
    #            except Exception as e:
    #                print(f'Error stopping task: {task_arn}. Error: {str(e)}')
    #                raise e
    #        else:
    #            # 'aws.fargate.task.arn'が見つからない場合、エラーを出力して終了
    #            print('Error: aws.fargate.task.arn not found in data')
    #            raise Exception(
    #                'Error: aws.fargate.task.arn not found in data')

    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }
