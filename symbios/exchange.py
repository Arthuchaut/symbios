'''
@desc    The exchange class for manage exchanges.
@author  arthuchaut <arthuchaut@gmail.com>
@version 0.1.0
@date    2019-09-20
@note    0.1.0 (2019-09-20): Writed the first drafts.
'''


class Exchange:
    '''The Exchange class declaration.

    Attributes:
        DIRECT (str): The default exhange type. Sends the message
            to alls the queues that are bound to the same routing_key that
            the message routing_key.

            Example: 
                If Producer::routing_key == Consumer::queue::binding_key
                then deliver the message to this queue.
        FANOUT (str): Sends the message to all the queues 
            that are bound to it. The routing_key will be ignored.

            Example:
                If Consumer::binding_key is bound to this exchange_type
                then deliver the message to this queue.
        TOPIC (str): Sends the message to all the queues that
            are bound to the same routing_key that the message routing_key
            and that the routing_key pattern of the bound queue is matching 
            with the message routing_key.

            Example:
                Producer::routing_key = 'my.routing.key'
                Consumer::binding_key = 'my.*.key'

                is_matching(Producer::routing_key, Consumer::binding_key)
                >>> True

                Producer::routing_key = 'his.routing.key'
                Consumer::binding_key = 'my.*.key'

                is_matching(Producer::routing_key, Consumer::binding_key)
                >>> False
        HEADERS (str): Sends the message to all queues at which 
            their routing_key matches to specific header attributes. 
            The routing_key is ignored.

            Example:
                Header::attr['x-match'] = 'my_value'
                Consumer::binding_key = 'my_value'

                Header::attr['x-match'] == Consumer::binding_key
                >>> True

                Header::attr['x-match'] = 'my_other_value'
                Consumer::binding_key = 'my_value'

                Header::attr['x-match'] == Consumer::binding_key
                >>> False
        exchange (str): The exchange name.
        exchange_type (str): The exchange type. See upper.
        passive (bool): Not create exchange if it not exists.
        durable (bool): Not delete the exchange after a broker restart.
        exclusive (bool): Delete the exchange after closed the connection.
        auto_delete (bool): Delete exchange when it empty from producers.
        nowait (bool): Not send a reply callback.
        arguments (dict): Some arguments for the declaration.
    '''

    DIRECT: str = 'direct'
    FANOUT: str = 'fanout'
    TOPIC: str = 'topic'
    HEADERS: str = 'headers'

    def __init__(
        self,
        exchange: str = '',
        *,
        exchange_type: str = DIRECT,
        passive: bool = False,
        durable: bool = False,
        auto_delete: bool = False,
        nowait: bool = False,
        arguments: dict = {}
    ):
        '''The Exchange initializer.

        Args:
            exchange (str): The exchange name. Default to ''.
            exchange_type (str): The exchange type. See upper.
                Default to DIRECT.
            passive (bool): Not create exchange if it not exists.
                Default to False.
            durable (bool): Not delete the exchange after a broker restart.
                Default to False.
            exclusive (bool): Delete the exchange after closed the connection.
                Default to False.
            auto_delete (bool): Delete exchange when it empty from producers.
                Default to False.
            nowait (bool): Not send a reply callback.
                Default to False.
            arguments (dict): Some arguments for the declaration.
                Default to {}.
        '''

        self.exchange: str = exchange
        self.exchange_type: str = exchange_type
        self.passive: bool = passive
        self.durable: bool = durable
        self.auto_delete: bool = auto_delete
        self.nowait: bool = nowait
        self.arguments: dict = arguments
