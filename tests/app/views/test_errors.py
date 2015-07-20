# coding=utf-8

import mock
from nose.tools import assert_equal, assert_true
from requests import ConnectionError
from ...helpers import BaseApplicationTest


@mock.patch('app.main.views.search_api_client')
class TestErrors(BaseApplicationTest):
    def test_404(self, search_api_mock):
        res = self.client.get('/g-cloud/service/1234')
        assert_equal(404, res.status_code)
        assert_true(
            "Check you've entered the correct web "
            "address or start again on the Digital Marketplace homepage."
            in res.get_data(as_text=True))
        assert_true(
            "If you can't find what you're looking for, contact us at "
            "<a href=\"mailto:enquiries@digitalmarketplace.service.gov.uk?"
            "subject=Digital%20Marketplace%20feedback\" title=\"Please "
            "send feedback to enquiries@digitalmarketplace.service.gov.uk\">"
            "enquiries@digitalmarketplace.service.gov.uk</a>"
            in res.get_data(as_text=True))

    def test_500(self, search_api_mock):
        self.app.config['DEBUG'] = False
        search_api_mock.search_services.side_effect = ConnectionError()

        res = self.client.get('/g-cloud/search?q=email')
        assert_equal(500, res.status_code)
        assert_true(
            "Sorry, we're experiencing technical difficulties"
            in res.get_data(as_text=True))
        assert_true(
            "Try again later."
            in res.get_data(as_text=True))
