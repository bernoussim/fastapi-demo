import abc

from abc import ABCMeta
import boto3


class TaxRateRetriever(metaclass=ABCMeta):
    @abc.abstractmethod
    def get_tax_rate(self, country) -> float:
        pass


class TaxRateRetrieverSSM(TaxRateRetriever):
    def __init__(self):
        self.client = boto3.client('ssm')

    def get_tax_rate(self, country) -> float:
        response = self.client.get_parameter(Name=f"/tax/{country}")
        return float(response['Parameter']['Value'])


class TaxRateRetrieverDDB(TaxRateRetriever):
    def __init__(self):
        self.client = boto3.client('dynamodb')

    def get_tax_rate(self, country) -> float:
        response = self.client.get_item(
            TableName='tax_rate', Key={'country': {'S': country}}
        )
        return float(response['Item']['tax_rate']['N'])
