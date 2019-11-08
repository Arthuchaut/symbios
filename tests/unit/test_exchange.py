'''
@desc    The Exchange test class.
@author  arthuchaut <arthuchaut@gmail.com>
@version 0.1.0
@date    2019-09-25
@note    0.1.0 Writing the first drafts.
'''

import pytest

from symbios.exchange import Exchange


class TestExchange:
    '''The Exchange tests class.
    '''

    @pytest.mark.parametrize('name', ['exchange_name'])
    @pytest.mark.parametrize(
        'exchange_type',
        [Exchange.DIRECT, Exchange.FANOUT, Exchange.TOPIC, Exchange.HEADERS],
    )
    @pytest.mark.parametrize('passive', [False, True])
    @pytest.mark.parametrize('durable', [False, True])
    @pytest.mark.parametrize('auto_delete', [False, True])
    @pytest.mark.parametrize('nowait', [False, True])
    @pytest.mark.parametrize('arguments', [{}])
    def test_exchange(
        self,
        name: str,
        exchange_type: str,
        passive: bool,
        durable: bool,
        auto_delete: bool,
        nowait: bool,
        arguments: dict,
    ) -> None:
        '''Test the Exchange class attributes integrity.
        '''

        exchange: Exchange = Exchange(
            name,
            exchange_type=exchange_type,
            passive=passive,
            durable=durable,
            auto_delete=auto_delete,
            nowait=nowait,
            arguments=arguments,
        )

        assert (
            exchange.exchange == name
            and exchange.exchange_type == exchange_type
            and exchange.passive == passive
            and exchange.durable == durable
            and exchange.auto_delete == auto_delete
            and exchange.nowait == nowait
            and exchange.arguments == arguments
        )
