'''
@desc    The message test classes.
@author  arthuchaut <arthuchaut@gmail.com>
@version 0.1.0
@date    2019-09-25
@note    0.1.0 Writing the first drafts.
'''

from typing import Any

import pytest

from symbios.utils import Props
from symbios.message import SendingMessage, IncomingMessage


class TestSendingMessage:
    '''The SendingMessage tests class.
    '''

    @pytest.mark.parametrize('body', ['Hello', {}, 42, 3.14])
    def test_sending_message(self, body: Any) -> None:
        '''Test the SendingMessage class atrributes integrity.
        '''

        message: SendingMessage = SendingMessage(body)

        assert message.body == body


class TestIncomingMessage:
    '''The IncomingMessage tests class.
    '''

    @pytest.mark.parametrize('delivery', [True])
    @pytest.mark.parametrize(
        'header',
        [
            Props(),
            Props(content_type='text/plain'),
            Props(content_type='application/json', correlation_id='1-2-3-4'),
        ],
    )
    @pytest.mark.parametrize('body', ['Hello', {}, 42, 3.14])
    def test_incoming_message(
        self, delivery: Any, header: object, body: Any, delivered_message_model
    ) -> None:
        '''Test the IncomingMessage class attributes integrity.
        '''

        message: IncomingMessage = IncomingMessage(
            delivered_message_model(delivery, header, body)
        )

        assert (
            message.delivery == delivery
            and message.props == header
            and message.body == body
        )

