FUNC_NAME="add-submission"
RUNTIME="python3.7"
ROLE="arn:aws:iam::357902200561:role/lambda_invoke_function_assume_apigw_role"
HANDLER="lambda_handler"
ZIP_FILE="fileb:///Users/chris/treddit/lambda/build/add_submission.zip"

aws lambda create-function \
    --function-name $FUNC_NAME \
    --runtime $RUNTIME \
    --role $ROLE \
    --handler $HANDLER \
    --zip-file $ZIP_FILE
