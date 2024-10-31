def get_data_from_sns_event(sns_event: dict):
    """Extract data from SNS event."""
    try:
        return sns_event['Records'][0]['Sns']['Message']
    except KeyError:
        return sns_event