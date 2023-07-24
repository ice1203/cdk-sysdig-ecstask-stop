import * as cdk from "aws-cdk-lib";
import { Construct } from "constructs";
import * as lambda from "aws-cdk-lib/aws-lambda";
import { SnsEventSource } from "aws-cdk-lib/aws-lambda-event-sources";
import * as sns from "aws-cdk-lib/aws-sns";
import * as iam from "aws-cdk-lib/aws-iam";

export class CdkSysdigLambdaStack extends cdk.Stack {
    constructor(scope: Construct, id: string, props?: cdk.StackProps) {
        super(scope, id, props);

        const sysdigAwsAccountID: string = "263844535661";
        // ecsタスク停止するためのポリシー
        const ecsTaskStopPolicyStatement = new iam.PolicyStatement({
            sid: "allowECSTaskStop",
            resources: ["arn:aws:ecs:*:*:task/*/*"],
            actions: ["ecs:StopTask"],
        });
        // lambdaのIAMロール
        const lambdaRole = new iam.Role(this, "MyLambdaRole", {
            assumedBy: new iam.ServicePrincipal("lambda.amazonaws.com"),
        });
        lambdaRole.addManagedPolicy(
            iam.ManagedPolicy.fromAwsManagedPolicyName(
                "service-role/AWSLambdaBasicExecutionRole"
            )
        );
        // lambdaのIAMロールにECSのタスク停止権限を付与
        lambdaRole.addToPolicy(ecsTaskStopPolicyStatement);
        // Lambda function
        const myLambda = new lambda.Function(this, "MyLambda", {
            runtime: lambda.Runtime.PYTHON_3_9,
            handler: "index.lambda_handler",
            code: lambda.Code.fromAsset("lambda_src"),
            role: lambdaRole,
        });
        // sns topic
        const topic = new sns.Topic(this, "MyTopic");
        // sns topicに対するlambdaのサブスクリプション
        myLambda.addEventSource(
            new SnsEventSource(topic, {
                filterPolicy: {},
            })
        );
        // sysdigAwsAccountIDのアカウントに対して、sns topicに対するpublish権限を付与
        topic.grantPublish(new iam.AccountPrincipal(sysdigAwsAccountID));
    }
}
