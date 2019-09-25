import pamqp

from pamqp.specification import Basic
from pamqp.specification import Exchange
from pamqp.specification import Queue
from aiormq.types import ConfirmationFrameType


class EmitACK:
    '''The producer frame confirmation class.
    '''

    def __init__(self, confirmation: ConfirmationFrameType):
        self.confirmation: ConfirmationFrameType = confirmation


class ListenACK:
    '''The consumer frame confirmation class.
    '''

    def __init__(self, confirmation: Basic.ConsumeOk):
        self.confirmation: Basic.ConsumeOk = confirmation


class ExchangeACK:
    '''The exchange declaraiton frame confirmation.
    '''

    def __init__(self, confirmation: Exchange.DeclareOk):
        self.confirmation: Exchange.DeclareOk = confirmation


class QueueACK:
    '''The queue declaration frame confirmation.
    '''

    def __init__(self, confirmation: Queue.DeclareOk):
        self.confirmation: Queue.DeclareOk = confirmation
