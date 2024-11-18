import boto3
from util.config import Config
from util.singleton import Singleton


class DatabaseConnection(metaclass=Singleton):
    def __init__(self):
        self.__database = boto3.client('dynamodb', region=Config.AWS_REGION.value)

    def insert_one(self, table: str, obj: dict):
        """
        Inserts a single object into the database
        table: str -- The name of the table to insert into
        obj: dict -- The object to insert
        """
        self.__database.put_item(
            TableName=table,
            Item=obj
        )

    def insert_many(self, table: str, objs: [dict]):
        """
        Inserts multiple objects into the database
        table: str -- The name of the table to insert into
        objs: [dict] -- The objects to insert
        """
        # update_many also inserts data if it doesn't exist
        return self.update_many(table, objs)

    def select_one(self, table: str, ftr: dict)-> [dict, None]:
        """
        Returns a single object from the database
        table: str -- The name of the table to query upon
        ftr: dict -- The filter to apply to the query
        """
        response = self.__database.get_item(
            TableName=table,
            Key=ftr
        )

        response.get('Item', default=None)

    def select_many(self, table: str, ftr: dict)-> [dict]:
        """
        Returns a list of objects from the database
        table: str -- The name of the table to query upon
        ftr: dict -- The filter to apply to the query
        """
        expression_values = {f":val{i}": value for i, value in enumerate(ftr.values())}
        expression_names = {f"#attr{i}": key for i, key in enumerate(ftr.keys())}
        filter_expression = " AND ".join([f"#attr{i} = :val{i}" for i in range(len(ftr))])

        response = self.__database.scan(
            TableName=table,
            FilterExpression=filter_expression,
            ExpressionAttributeValues=expression_values,
            ExpressionAttributeNames=expression_names
        )

        if response.get('Items', default=None):
            return response['Items']
        else:
            return []

    def update_one(self, table: str, ftr: dict):
        """
        Updates a single object in the database
        table: str -- The name of the table to query upon
        ftr: str -- The filter to apply to the query
        """
        key = {k: ftr[k] for k in ['timestamp']}
        update_attrs = {k: v for k, v in ftr.items() if k != 'timestamp'}

        expression_values = {f":val{i}": value for i, value in enumerate(update_attrs.values())}
        expression_names = {f"#attr{i}": key for i, key in enumerate(update_attrs.keys())}
        update_expression = "SET " + ", ".join([f"#attr{i} = :val{i}" for i in range(len(update_attrs))])

        response = self.__database.update_item(
            TableName=table,
            Key=key,
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_values,
            ExpressionAttributeNames=expression_names
        )

        return response

    def update_many(self, table: str, ftr: dict):
        """
        Updates multiple objects in the database
        table: str -- The name of the table to query upon
        ftr: str -- The filter to apply to the query
        """
        key = list(ftr.keys())[0]
        update_attrs = {k: v for k, v in ftr.items() if k != key}

        # First get all matching items
        items = self.select_many(table, key)

        # Prepare batch write requests
        batch_items = {
            table: [
                {
                    'PutRequest': {
                        'Item': {**item, **update_attrs}
                    }
                }
                for item in items
            ]
        }

        # DynamoDB has a limit of 25 items per batch write
        batch_size = 25
        responses = []

        for i in range(0, len(batch_items[table]), batch_size):
            batch_chunk = {
                table: batch_items[table][i:i + batch_size]
            }
            response = self.__database.batch_write_item(
                RequestItems=batch_chunk
            )
            responses.append(response)

        return responses

    def delete_one(self, table: str, ftr: dict):
        """
        Deletes a single object from the database
        table: str -- The name of the table to query upon
        ftr: dict -- The filter to apply to the query
        """
        response = self.__database.delete_item(
            TableName=table,
            Key=ftr
        )
        return response

    def delete_many(self, table, ftr):
        """
        Deletes multiple objects from the database
        table: str -- The name of the table to query upon
        ftr: dict -- The filter to apply to the query
        """
        # First get all matching items
        items = self.select_many(table, ftr)

        # Prepare batch write requests
        batch_items = {
            table: [
                {
                    'DeleteRequest': {
                        'Key': item
                    }
                }
                for item in items
            ]
        }

        # DynamoDB has a limit of 25 items per batch write
        batch_size = 25
        responses = []

        for i in range(0, len(batch_items[table]), batch_size):
            batch_chunk = {
                table: batch_items[table][i:i + batch_size]
            }
            response = self.__database.batch_write_item(
                RequestItems=batch_chunk
            )
            responses.append(response)

        return responses
