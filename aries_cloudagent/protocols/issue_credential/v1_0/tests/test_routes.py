from asynctest import TestCase as AsyncTestCase
from asynctest import mock as async_mock

from aiohttp import web as aio_web

from .....config.injection_context import InjectionContext
from .....storage.error import StorageNotFoundError
from .....holder.base import BaseHolder
from .....messaging.request_context import RequestContext
from .....wallet.base import DIDInfo

from .. import routes as test_module


class TestCredentialRoutes(AsyncTestCase):
    async def test_credential_exchange_list(self):
        mock = async_mock.MagicMock()
        mock.query = {
            "thread_id": "dummy",
            "connection_id": "dummy",
            "role": "dummy",
            "state": "dummy",
        }
        context = RequestContext(base_context=InjectionContext(enforce_typing=False))
        mock.app = {
            "request_context": context,
        }
        mock.app["request_context"].settings = {}

        with async_mock.patch.object(
            test_module, "V10CredentialExchange", autospec=True
        ) as mock_cred_ex:
            mock_cred_ex.query = async_mock.CoroutineMock()
            mock_cred_ex.query.return_value = [mock_cred_ex]
            mock_cred_ex.serialize = async_mock.MagicMock()
            mock_cred_ex.serialize.return_value = {"hello": "world"}

            with async_mock.patch.object(
                test_module.web, "json_response"
            ) as mock_response:
                await test_module.credential_exchange_list(mock)
                mock_response.assert_called_once_with(
                    {"results": [mock_cred_ex.serialize.return_value]}
                )

    async def test_credential_exchange_list_x(self):
        mock = async_mock.MagicMock()
        mock.query = {
            "thread_id": "dummy",
            "connection_id": "dummy",
            "role": "dummy",
            "state": "dummy",
        }
        context = RequestContext(base_context=InjectionContext(enforce_typing=False))
        mock.app = {
            "request_context": context,
        }
        mock.app["request_context"].settings = {}

        with async_mock.patch.object(
            test_module, "V10CredentialExchange", autospec=True
        ) as mock_cred_ex:
            mock_cred_ex.query = async_mock.CoroutineMock(
                side_effect=test_module.StorageError()
            )
            with self.assertRaises(test_module.web.HTTPBadRequest):
                await test_module.credential_exchange_list(mock)

    async def test_credential_exchange_retrieve(self):
        mock = async_mock.MagicMock()
        mock.match_info = {"cred_ex_id": "dummy"}
        context = RequestContext(base_context=InjectionContext(enforce_typing=False))
        mock.app = {
            "request_context": context,
        }
        mock.app["request_context"].settings = {}

        with async_mock.patch.object(
            test_module, "V10CredentialExchange", autospec=True
        ) as mock_cred_ex:
            mock_cred_ex.retrieve_by_id = async_mock.CoroutineMock()
            mock_cred_ex.retrieve_by_id.return_value = mock_cred_ex
            mock_cred_ex.serialize = async_mock.MagicMock()
            mock_cred_ex.serialize.return_value = {"hello": "world"}

            with async_mock.patch.object(
                test_module.web, "json_response"
            ) as mock_response:
                await test_module.credential_exchange_retrieve(mock)
                mock_response.assert_called_once_with(
                    mock_cred_ex.serialize.return_value
                )

    async def test_credential_exchange_retrieve_not_found(self):
        mock = async_mock.MagicMock()
        mock.match_info = {"cred_ex_id": "dummy"}
        context = RequestContext(base_context=InjectionContext(enforce_typing=False))
        mock.app = {
            "request_context": context,
        }
        mock.app["request_context"].settings = {}

        with async_mock.patch.object(
            test_module, "V10CredentialExchange", autospec=True
        ) as mock_cred_ex:
            mock_cred_ex.retrieve_by_id = async_mock.CoroutineMock(
                side_effect=test_module.StorageNotFoundError()
            )
            with self.assertRaises(test_module.web.HTTPBadRequest):
                await test_module.credential_exchange_retrieve(mock)

    async def test_credential_exchange_retrieve_x(self):
        mock = async_mock.MagicMock()
        mock.match_info = {"cred_ex_id": "dummy"}
        context = RequestContext(base_context=InjectionContext(enforce_typing=False))
        mock.app = {
            "request_context": context,
        }
        mock.app["request_context"].settings = {}

        with async_mock.patch.object(
            test_module, "V10CredentialExchange", autospec=True
        ) as mock_cred_ex:
            mock_cred_ex.retrieve_by_id = async_mock.CoroutineMock()
            mock_cred_ex.retrieve_by_id.return_value = mock_cred_ex
            mock_cred_ex.serialize = async_mock.MagicMock(
                side_effect=test_module.BaseModelError()
            )
            with self.assertRaises(test_module.web.HTTPBadRequest):
                await test_module.credential_exchange_retrieve(mock)

    async def test_credential_exchange_retrieve_not_found(self):
        mock = async_mock.MagicMock()
        mock.match_info = {"cred_ex_id": "dummy"}
        context = RequestContext(base_context=InjectionContext(enforce_typing=False))
        mock.app = {
            "request_context": context,
        }
        mock.app["request_context"].settings = {}

        with async_mock.patch.object(
            test_module, "V10CredentialExchange", autospec=True
        ) as mock_cred_ex:
            mock_cred_ex.retrieve_by_id = async_mock.CoroutineMock()

            # Emulate storage not found (bad credential exchange id)
            mock_cred_ex.retrieve_by_id.side_effect = StorageNotFoundError()

            with self.assertRaises(test_module.web.HTTPNotFound):
                await test_module.credential_exchange_retrieve(mock)

    async def test_credential_exchange_send(self):
        mock = async_mock.MagicMock()
        mock.json = async_mock.CoroutineMock()
        context = RequestContext(base_context=InjectionContext(enforce_typing=False))
        mock.app = {
            "outbound_message_router": async_mock.CoroutineMock(),
            "request_context": context,
        }
        mock.app["request_context"].settings = {}

        with async_mock.patch.object(
            test_module, "ConnectionRecord", autospec=True
        ) as mock_connection_record, async_mock.patch.object(
            test_module, "CredentialManager", autospec=True
        ) as mock_credential_manager, async_mock.patch.object(
            test_module.CredentialPreview, "deserialize", autospec=True
        ), async_mock.patch.object(
            test_module.web, "json_response"
        ) as mock_response:
            mock_credential_manager.return_value.create_offer = (
                async_mock.CoroutineMock()
            )

            mock_credential_manager.return_value.create_offer.return_value = (
                async_mock.CoroutineMock(),
                async_mock.CoroutineMock(),
            )

            mock_cred_ex_record = async_mock.MagicMock()
            mock_cred_offer = async_mock.MagicMock()

            mock_credential_manager.return_value.prepare_send.return_value = (
                mock_cred_ex_record,
                mock_cred_offer,
            )

            await test_module.credential_exchange_send(mock)

            mock_response.assert_called_once_with(
                mock_cred_ex_record.serialize.return_value
            )

    async def test_credential_exchange_send_no_proposal(self):
        conn_id = "connection-id"

        mock = async_mock.MagicMock()
        mock.json = async_mock.CoroutineMock(return_value={"connection_id": conn_id})
        context = RequestContext(base_context=InjectionContext(enforce_typing=False))
        mock.app = {
            "outbound_message_router": async_mock.CoroutineMock(),
            "request_context": context,
        }
        mock.app["request_context"].settings = {}

        with self.assertRaises(test_module.web.HTTPBadRequest) as context:
            await test_module.credential_exchange_send(mock)
        assert "credential_proposal" in str(context.exception)

    async def test_credential_exchange_send_no_conn_record(self):
        conn_id = "connection-id"
        preview_spec = {"attributes": [{"name": "attr", "value": "value"}]}

        mock = async_mock.MagicMock()
        mock.json = async_mock.CoroutineMock(
            return_value={"connection_id": conn_id, "credential_proposal": preview_spec}
        )
        context = RequestContext(base_context=InjectionContext(enforce_typing=False))
        mock.app = {
            "outbound_message_router": async_mock.CoroutineMock(),
            "request_context": context,
        }
        mock.app["request_context"].settings = {}

        with async_mock.patch.object(
            test_module, "ConnectionRecord", autospec=True
        ) as mock_connection_record, async_mock.patch.object(
            test_module, "CredentialManager", autospec=True
        ) as mock_credential_manager:

            # Emulate storage not found (bad connection id)
            mock_connection_record.retrieve_by_id.side_effect = StorageNotFoundError()

            mock_credential_manager.return_value.create_offer.return_value = (
                async_mock.MagicMock(),
                async_mock.MagicMock(),
            )

            with self.assertRaises(test_module.web.HTTPBadRequest):
                await test_module.credential_exchange_send(mock)

    async def test_credential_exchange_send_not_ready(self):
        conn_id = "connection-id"
        preview_spec = {"attributes": [{"name": "attr", "value": "value"}]}

        mock = async_mock.MagicMock()
        mock.json = async_mock.CoroutineMock(
            return_value={"connection_id": conn_id, "credential_proposal": preview_spec}
        )
        context = RequestContext(base_context=InjectionContext(enforce_typing=False))
        mock.app = {
            "outbound_message_router": async_mock.CoroutineMock(),
            "request_context": context,
        }
        mock.app["request_context"].settings = {}

        with async_mock.patch.object(
            test_module, "ConnectionRecord", autospec=True
        ) as mock_connection_record, async_mock.patch.object(
            test_module, "CredentialManager", autospec=True
        ) as mock_credential_manager:

            # Emulate connection not ready
            mock_connection_record.retrieve_by_id.return_value.is_ready = False

            mock_credential_manager.return_value.create_offer.return_value = (
                async_mock.MagicMock(),
                async_mock.MagicMock(),
            )

            with self.assertRaises(test_module.web.HTTPForbidden):
                await test_module.credential_exchange_send(mock)

    async def test_credential_exchange_send_proposal(self):
        conn_id = "connection-id"
        preview_spec = {"attributes": [{"name": "attr", "value": "value"}]}

        mock = async_mock.MagicMock()
        mock.json = async_mock.CoroutineMock(
            return_value={"connection_id": conn_id, "credential_proposal": preview_spec}
        )
        context = RequestContext(base_context=InjectionContext(enforce_typing=False))
        mock.app = {
            "outbound_message_router": async_mock.CoroutineMock(),
            "request_context": context,
        }
        mock.app["request_context"].settings = {}

        with async_mock.patch.object(
            test_module, "ConnectionRecord", autospec=True
        ) as mock_connection_record, async_mock.patch.object(
            test_module, "CredentialManager", autospec=True
        ) as mock_credential_manager, async_mock.patch.object(
            test_module.CredentialProposal, "deserialize", autospec=True
        ) as mock_proposal_deserialize, async_mock.patch.object(
            test_module.web, "json_response"
        ) as mock_response:

            mock_cred_ex_record = async_mock.MagicMock()

            mock_credential_manager.return_value.create_proposal.return_value = (
                mock_cred_ex_record
            )

            await test_module.credential_exchange_send_proposal(mock)

            mock_response.assert_called_once_with(
                mock_cred_ex_record.serialize.return_value
            )

            mock.app["outbound_message_router"].assert_called_once_with(
                mock_proposal_deserialize.return_value, connection_id=conn_id
            )

    async def test_credential_exchange_send_proposal_no_conn_record(self):
        mock = async_mock.MagicMock()
        mock.json = async_mock.CoroutineMock()
        context = RequestContext(base_context=InjectionContext(enforce_typing=False))
        mock.app = {
            "outbound_message_router": async_mock.CoroutineMock(),
            "request_context": context,
        }
        mock.app["request_context"].settings = {}

        with async_mock.patch.object(
            test_module, "ConnectionRecord", autospec=True
        ) as mock_connection_record, async_mock.patch.object(
            test_module, "CredentialManager", autospec=True
        ) as mock_credential_manager, async_mock.patch.object(
            test_module.CredentialPreview, "deserialize", autospec=True
        ) as mock_preview_deserialize:

            # Emulate storage not found (bad connection id)
            mock_connection_record.retrieve_by_id = async_mock.CoroutineMock(
                side_effect=StorageNotFoundError()
            )

            mock_credential_manager.return_value.create_proposal.return_value = (
                async_mock.MagicMock()
            )

            with self.assertRaises(test_module.web.HTTPBadRequest):
                await test_module.credential_exchange_send_proposal(mock)

    async def test_credential_exchange_send_proposal_deser_x(self):
        conn_id = "connection-id"
        preview_spec = {"attributes": [{"name": "attr", "value": "value"}]}

        mock = async_mock.MagicMock()
        mock.json = async_mock.CoroutineMock(
            return_value={"connection_id": conn_id, "credential_proposal": preview_spec}
        )
        context = RequestContext(base_context=InjectionContext(enforce_typing=False))
        mock.app = {
            "outbound_message_router": async_mock.CoroutineMock(),
            "request_context": context,
        }
        mock.app["request_context"].settings = {}

        with async_mock.patch.object(
            test_module, "ConnectionRecord", autospec=True
        ) as mock_connection_record, async_mock.patch.object(
            test_module, "CredentialManager", autospec=True
        ) as mock_credential_manager, async_mock.patch.object(
            test_module.CredentialProposal, "deserialize", autospec=True
        ) as mock_proposal_deserialize:
            mock_cred_ex_record = async_mock.MagicMock()
            mock_credential_manager.return_value.create_proposal.return_value = (
                mock_cred_ex_record
            )
            mock_proposal_deserialize.side_effect = test_module.BaseModelError()
            with self.assertRaises(test_module.web.HTTPBadRequest):
                await test_module.credential_exchange_send_proposal(mock)

    async def test_credential_exchange_send_proposal_not_ready(self):
        mock = async_mock.MagicMock()
        mock.json = async_mock.CoroutineMock()
        context = RequestContext(base_context=InjectionContext(enforce_typing=False))
        mock.app = {
            "outbound_message_router": async_mock.CoroutineMock(),
            "request_context": context,
        }
        mock.app["request_context"].settings = {}

        with async_mock.patch.object(
            test_module, "ConnectionRecord", autospec=True
        ) as mock_connection_record, async_mock.patch.object(
            test_module, "CredentialManager", autospec=True
        ) as mock_credential_manager, async_mock.patch.object(
            test_module.CredentialPreview, "deserialize", autospec=True
        ) as mock_preview_deserialize:

            # Emulate connection not ready
            mock_connection_record.retrieve_by_id = async_mock.CoroutineMock()
            mock_connection_record.retrieve_by_id.return_value.is_ready = False

            mock_credential_manager.return_value.create_proposal.return_value = (
                async_mock.MagicMock()
            )

            with self.assertRaises(test_module.web.HTTPForbidden):
                await test_module.credential_exchange_send_proposal(mock)

    async def test_credential_exchange_create_free_offer(self):
        mock = async_mock.MagicMock()
        mock.json = async_mock.CoroutineMock(
            return_value={
                "auto_issue": False,
                "cred_def_id": "cred-def-id",
                "connection_id": "dummy",
                "credential_preview": {
                    "attributes": [{"name": "hello", "value": "world"}]
                },
            }
        )

        mock.app = {
            "outbound_message_router": async_mock.CoroutineMock(),
            "request_context": async_mock.patch.object(
                aio_web, "BaseRequest", autospec=True
            ),
        }
        mock.app["request_context"].settings = {
            "default_endpoint": "http://1.2.3.4:8081"
        }
        mock.app["request_context"].inject = async_mock.CoroutineMock(
            return_value=async_mock.MagicMock(
                retrieve_by_id=async_mock.CoroutineMock(
                    return_value=async_mock.MagicMock(my_did="did")
                ),
                get_local_did=async_mock.CoroutineMock(
                    return_value=DIDInfo("did", "verkey", {"meta": "data"})
                ),
            )
        )

        with async_mock.patch.object(
            test_module, "ConnectionRecord", autospec=True
        ) as mock_connection_record, async_mock.patch.object(
            test_module, "CredentialManager", autospec=True
        ) as mock_credential_manager, async_mock.patch.object(
            test_module, "serialize_outofband"
        ) as mock_seroob, async_mock.patch.object(
            test_module.web, "json_response"
        ) as mock_response:
            mock_credential_manager.return_value.create_offer = (
                async_mock.CoroutineMock()
            )
            mock_cred_ex_record = async_mock.MagicMock()
            mock_credential_manager.return_value.create_offer.return_value = (
                mock_cred_ex_record,
                async_mock.MagicMock(),
            )
            mock_seroob.return_value = "abc123"

            await test_module.credential_exchange_create_free_offer(mock)

            mock_response.assert_called_once_with(
                {
                    "record": mock_cred_ex_record.serialize.return_value,
                    "oob_url": "abc123",
                }
            )

    async def test_credential_exchange_create_free_offer_no_cred_def_id(self):
        mock = async_mock.MagicMock()
        mock.json = async_mock.CoroutineMock(
            return_value={
                "auto_issue": False,
                "connection_id": "dummy",
                "credential_preview": {
                    "attributes": [{"name": "hello", "value": "world"}]
                },
            }
        )

        with self.assertRaises(test_module.web.HTTPBadRequest):
            await test_module.credential_exchange_create_free_offer(mock)

    async def test_credential_exchange_create_free_offer_no_preview(self):
        mock = async_mock.MagicMock()
        mock.json = async_mock.CoroutineMock()
        mock.json.return_value = {"comment": "comment", "cred_def_id": "dummy"}

        mock.app = {
            "outbound_message_router": async_mock.CoroutineMock(),
            "request_context": async_mock.patch.object(
                aio_web, "BaseRequest", autospec=True
            ),
        }
        mock.app["request_context"].settings = {}

        with self.assertRaises(test_module.web.HTTPBadRequest):
            await test_module.credential_exchange_create_free_offer(mock)

    async def test_credential_exchange_create_free_offer_retrieve_conn_rec_x(self):
        mock = async_mock.MagicMock()
        mock.json = async_mock.CoroutineMock(
            return_value={
                "auto_issue": False,
                "cred_def_id": "cred-def-id",
                "connection_id": "dummy",
                "credential_preview": {
                    "attributes": [{"name": "hello", "value": "world"}]
                },
            }
        )

        mock.app = {
            "outbound_message_router": async_mock.CoroutineMock(),
            "request_context": async_mock.patch.object(
                aio_web, "BaseRequest", autospec=True
            ),
        }
        mock.app["request_context"].settings = {}
        mock.app["request_context"].inject = async_mock.CoroutineMock(
            return_value=async_mock.MagicMock(
                get_local_did=async_mock.CoroutineMock(
                    side_effect=test_module.WalletError()
                )
            )
        )

        with async_mock.patch.object(
            test_module, "ConnectionRecord", autospec=True
        ) as mock_connection_record:
            with self.assertRaises(test_module.web.HTTPBadRequest):
                await test_module.credential_exchange_create_free_offer(mock)

    async def test_credential_exchange_create_free_offer_no_conn_id(self):
        mock = async_mock.MagicMock()
        mock.json = async_mock.CoroutineMock(
            return_value={
                "auto_issue": False,
                "cred_def_id": "cred-def-id",
                "credential_preview": {
                    "attributes": [{"name": "hello", "value": "world"}]
                },
            }
        )

        mock.app = {
            "outbound_message_router": async_mock.CoroutineMock(),
            "request_context": async_mock.patch.object(
                aio_web, "BaseRequest", autospec=True
            ),
        }
        mock.app["request_context"].settings = {
            "default_endpoint": "http://1.2.3.4:8081"
        }
        mock.app["request_context"].inject = async_mock.CoroutineMock(
            return_value=async_mock.MagicMock(
                get_public_did=async_mock.CoroutineMock(
                    return_value=DIDInfo("did", "verkey", {"meta": "data"})
                )
            )
        )

        with async_mock.patch.object(
            test_module, "ConnectionRecord", autospec=True
        ) as mock_connection_record, async_mock.patch.object(
            test_module, "CredentialManager", autospec=True
        ) as mock_credential_manager, async_mock.patch.object(
            test_module, "serialize_outofband"
        ) as mock_seroob, async_mock.patch.object(
            test_module.web, "json_response"
        ) as mock_response:

            mock_credential_manager.return_value.create_offer = (
                async_mock.CoroutineMock()
            )

            mock_cred_ex_record = async_mock.MagicMock()

            mock_credential_manager.return_value.create_offer.return_value = (
                mock_cred_ex_record,
                async_mock.MagicMock(),
            )

            mock_seroob.return_value = "abc123"

            await test_module.credential_exchange_create_free_offer(mock)

            mock_response.assert_called_once_with(
                {
                    "record": mock_cred_ex_record.serialize.return_value,
                    "oob_url": "abc123",
                }
            )

    async def test_credential_exchange_create_free_offer_no_conn_id_no_public_did(self):
        mock = async_mock.MagicMock()
        mock.json = async_mock.CoroutineMock(
            return_value={
                "auto_issue": False,
                "cred_def_id": "cred-def-id",
                "credential_preview": {
                    "attributes": [{"name": "hello", "value": "world"}]
                },
            }
        )

        mock.app = {
            "outbound_message_router": async_mock.CoroutineMock(),
            "request_context": async_mock.patch.object(
                aio_web, "BaseRequest", autospec=True
            ),
        }
        mock.app["request_context"].settings = {
            "default_endpoint": "http://1.2.3.4:8081"
        }
        mock.app["request_context"].inject = async_mock.CoroutineMock(
            return_value=async_mock.MagicMock(
                get_public_did=async_mock.CoroutineMock(return_value=None)
            )
        )

        with self.assertRaises(test_module.web.HTTPBadRequest):
            await test_module.credential_exchange_create_free_offer(mock)

    async def test_credential_exchange_create_free_offer_no_endpoint(self):
        mock = async_mock.MagicMock()
        mock.json = async_mock.CoroutineMock(
            return_value={
                "auto_issue": False,
                "cred_def_id": "cred-def-id",
                "credential_preview": {
                    "attributes": [{"name": "hello", "value": "world"}]
                },
            }
        )

        mock.app = {
            "outbound_message_router": async_mock.CoroutineMock(),
            "request_context": async_mock.patch.object(
                aio_web, "BaseRequest", autospec=True
            ),
        }
        mock.app["request_context"].settings = {}
        mock.app["request_context"].inject = async_mock.CoroutineMock(
            return_value=async_mock.MagicMock(
                get_public_did=async_mock.CoroutineMock(
                    return_value=DIDInfo("did", "verkey", {"meta": "data"})
                )
            )
        )

        with self.assertRaises(test_module.web.HTTPBadRequest):
            await test_module.credential_exchange_create_free_offer(mock)

    async def test_credential_exchange_create_free_offer_deser_x(self):
        mock = async_mock.MagicMock()
        mock.json = async_mock.CoroutineMock(
            return_value={
                "auto_issue": False,
                "cred_def_id": "cred-def-id",
                "connection_id": "dummy",
                "credential_preview": {
                    "attributes": [{"name": "hello", "value": "world"}]
                },
            }
        )

        mock.app = {
            "outbound_message_router": async_mock.CoroutineMock(),
            "request_context": async_mock.patch.object(
                aio_web, "BaseRequest", autospec=True
            ),
        }
        mock.app["request_context"].settings = {
            "default_endpoint": "http://1.2.3.4:8081"
        }
        mock.app["request_context"].inject = async_mock.CoroutineMock(
            return_value=async_mock.MagicMock(
                retrieve_by_id=async_mock.CoroutineMock(
                    return_value=async_mock.MagicMock(my_did="did")
                ),
                get_local_did=async_mock.CoroutineMock(
                    return_value=DIDInfo("did", "verkey", {"meta": "data"})
                ),
            )
        )

        with async_mock.patch.object(
            test_module, "ConnectionRecord", autospec=True
        ) as mock_connection_record, async_mock.patch.object(
            test_module, "CredentialManager", autospec=True
        ) as mock_credential_manager:
            mock_credential_manager.return_value.create_offer = (
                async_mock.CoroutineMock()
            )
            mock_cred_ex_record = async_mock.MagicMock()
            mock_credential_manager.return_value.create_offer.side_effect = (
                test_module.BaseModelError()
            )

            with self.assertRaises(test_module.web.HTTPBadRequest):
                await test_module.credential_exchange_create_free_offer(mock)

    async def test_credential_exchange_send_free_offer(self):
        mock = async_mock.MagicMock()
        mock.json = async_mock.CoroutineMock(
            return_value={
                "auto_issue": False,
                "cred_def_id": "cred-def-id",
                "credential_preview": {
                    "attributes": [{"name": "hello", "value": "world"}]
                },
            }
        )

        mock.app = {
            "outbound_message_router": async_mock.CoroutineMock(),
            "request_context": async_mock.patch.object(
                aio_web, "BaseRequest", autospec=True
            ),
        }
        mock.app["request_context"].settings = {}

        with async_mock.patch.object(
            test_module, "ConnectionRecord", autospec=True
        ) as mock_connection_record, async_mock.patch.object(
            test_module, "CredentialManager", autospec=True
        ) as mock_credential_manager, async_mock.patch.object(
            test_module.web, "json_response"
        ) as mock_response:

            mock_credential_manager.return_value.create_offer = (
                async_mock.CoroutineMock()
            )

            mock_cred_ex_record = async_mock.MagicMock()

            mock_credential_manager.return_value.create_offer.return_value = (
                mock_cred_ex_record,
                async_mock.MagicMock(),
            )

            await test_module.credential_exchange_send_free_offer(mock)

            mock_response.assert_called_once_with(
                mock_cred_ex_record.serialize.return_value
            )

    async def test_credential_exchange_send_free_offer_no_cred_def_id(self):
        mock = async_mock.MagicMock()
        mock.json = async_mock.CoroutineMock()
        mock.json.return_value = {
            "comment": "comment",
            "credential_preview": "dummy",
        }

        mock.app = {
            "outbound_message_router": async_mock.CoroutineMock(),
            "request_context": async_mock.patch.object(
                aio_web, "BaseRequest", autospec=True
            ),
        }
        mock.app["request_context"].settings = {}

        with self.assertRaises(test_module.web.HTTPBadRequest):
            await test_module.credential_exchange_send_free_offer(mock)

    async def test_credential_exchange_send_free_offer_no_preview(self):
        mock = async_mock.MagicMock()
        mock.json = async_mock.CoroutineMock()
        mock.json.return_value = {"comment": "comment", "cred_def_id": "dummy"}

        mock.app = {
            "outbound_message_router": async_mock.CoroutineMock(),
            "request_context": async_mock.patch.object(
                aio_web, "BaseRequest", autospec=True
            ),
        }
        mock.app["request_context"].settings = {}

        with self.assertRaises(test_module.web.HTTPBadRequest):
            await test_module.credential_exchange_send_free_offer(mock)

    async def test_credential_exchange_send_free_offer_no_conn_record(self):
        mock = async_mock.MagicMock()
        mock.json = async_mock.CoroutineMock(
            return_value={
                "auto_issue": False,
                "cred_def_id": "cred-def-id",
                "credential_preview": "dummy",
            }
        )

        mock.app = {
            "outbound_message_router": async_mock.CoroutineMock(),
            "request_context": async_mock.patch.object(
                aio_web, "BaseRequest", autospec=True
            ),
        }
        mock.app["request_context"].settings = {}

        with async_mock.patch.object(
            test_module, "ConnectionRecord", autospec=True
        ) as mock_connection_record, async_mock.patch.object(
            test_module, "CredentialManager", autospec=True
        ) as mock_credential_manager:

            # Emulate storage not found (bad connection id)
            mock_connection_record.retrieve_by_id = async_mock.CoroutineMock(
                side_effect=StorageNotFoundError()
            )

            mock_credential_manager.return_value.create_offer = (
                async_mock.CoroutineMock()
            )
            mock_credential_manager.return_value.create_offer.return_value = (
                async_mock.MagicMock(),
                async_mock.MagicMock(),
            )

            with self.assertRaises(test_module.web.HTTPBadRequest):
                await test_module.credential_exchange_send_free_offer(mock)

    async def test_credential_exchange_send_free_offer_not_ready(self):
        mock = async_mock.MagicMock()
        mock.json = async_mock.CoroutineMock()
        mock.json.return_value["auto_issue"] = True

        mock.app = {
            "outbound_message_router": async_mock.CoroutineMock(),
            "request_context": async_mock.patch.object(
                aio_web, "BaseRequest", autospec=True
            ),
        }
        mock.app["request_context"].settings = {}

        with async_mock.patch.object(
            test_module, "ConnectionRecord", autospec=True
        ) as mock_connection_record, async_mock.patch.object(
            test_module, "CredentialManager", autospec=True
        ) as mock_credential_manager:

            # Emulate connection not ready
            mock_connection_record.retrieve_by_id = async_mock.CoroutineMock()
            mock_connection_record.retrieve_by_id.return_value.is_ready = False

            mock_credential_manager.return_value.create_offer = (
                async_mock.CoroutineMock()
            )
            mock_credential_manager.return_value.create_offer.return_value = (
                async_mock.MagicMock(),
                async_mock.MagicMock(),
            )

            with self.assertRaises(test_module.web.HTTPForbidden):
                await test_module.credential_exchange_send_free_offer(mock)

    async def test_credential_exchange_send_bound_offer(self):
        mock = async_mock.MagicMock()
        mock.json = async_mock.CoroutineMock()

        mock.app = {
            "outbound_message_router": async_mock.CoroutineMock(),
            "request_context": async_mock.patch.object(
                aio_web, "BaseRequest", autospec=True
            ),
        }
        mock.app["request_context"].settings = {}

        with async_mock.patch.object(
            test_module, "ConnectionRecord", autospec=True
        ) as mock_connection_record, async_mock.patch.object(
            test_module, "CredentialManager", autospec=True
        ) as mock_credential_manager, async_mock.patch.object(
            test_module, "V10CredentialExchange", autospec=True
        ) as mock_cred_ex, async_mock.patch.object(
            test_module.web, "json_response"
        ) as mock_response:

            mock_cred_ex.retrieve_by_id = async_mock.CoroutineMock()
            mock_cred_ex.retrieve_by_id.return_value.state = (
                mock_cred_ex.STATE_PROPOSAL_RECEIVED
            )

            mock_credential_manager.return_value.create_offer = (
                async_mock.CoroutineMock()
            )

            mock_cred_ex_record = async_mock.MagicMock()

            mock_credential_manager.return_value.create_offer.return_value = (
                mock_cred_ex_record,
                async_mock.MagicMock(),
            )

            await test_module.credential_exchange_send_bound_offer(mock)

            mock_response.assert_called_once_with(
                mock_cred_ex_record.serialize.return_value
            )

    async def test_credential_exchange_send_bound_offer_bad_cred_ex_id(self):
        mock = async_mock.MagicMock()
        mock.json = async_mock.CoroutineMock()

        mock.app = {
            "outbound_message_router": async_mock.CoroutineMock(),
            "request_context": async_mock.patch.object(
                aio_web, "BaseRequest", autospec=True
            ),
        }
        mock.app["request_context"].settings = {}

        with async_mock.patch.object(
            test_module, "V10CredentialExchange", autospec=True
        ) as mock_cred_ex:
            mock_cred_ex.retrieve_by_id = async_mock.CoroutineMock()
            mock_cred_ex.retrieve_by_id.side_effect = test_module.StorageNotFoundError()

            with self.assertRaises(test_module.web.HTTPNotFound):
                await test_module.credential_exchange_send_bound_offer(mock)

    async def test_credential_exchange_send_bound_offer_no_conn_record(self):
        mock = async_mock.MagicMock()
        mock.json = async_mock.CoroutineMock()

        mock.app = {
            "outbound_message_router": async_mock.CoroutineMock(),
            "request_context": async_mock.patch.object(
                aio_web, "BaseRequest", autospec=True
            ),
        }
        mock.app["request_context"].settings = {}

        with async_mock.patch.object(
            test_module, "ConnectionRecord", autospec=True
        ) as mock_connection_record, async_mock.patch.object(
            test_module, "CredentialManager", autospec=True
        ) as mock_credential_manager, async_mock.patch.object(
            test_module, "V10CredentialExchange", autospec=True
        ) as mock_cred_ex:

            mock_cred_ex.retrieve_by_id = async_mock.CoroutineMock()
            mock_cred_ex.retrieve_by_id.return_value.state = (
                mock_cred_ex.STATE_PROPOSAL_RECEIVED
            )

            # Emulate storage not found (bad connection id)
            mock_connection_record.retrieve_by_id = async_mock.CoroutineMock(
                side_effect=StorageNotFoundError()
            )

            mock_credential_manager.return_value.create_offer = (
                async_mock.CoroutineMock()
            )
            mock_credential_manager.return_value.create_offer.return_value = (
                async_mock.MagicMock(),
                async_mock.MagicMock(),
            )

            with self.assertRaises(test_module.web.HTTPBadRequest):
                await test_module.credential_exchange_send_bound_offer(mock)

    async def test_credential_exchange_send_bound_offer_bad_state(self):
        mock = async_mock.MagicMock()
        mock.json = async_mock.CoroutineMock()

        mock.app = {
            "outbound_message_router": async_mock.CoroutineMock(),
            "request_context": async_mock.patch.object(
                aio_web, "BaseRequest", autospec=True
            ),
        }
        mock.app["request_context"].settings = {}

        with async_mock.patch.object(
            test_module, "V10CredentialExchange", autospec=True
        ) as mock_cred_ex:

            mock_cred_ex.retrieve_by_id = async_mock.CoroutineMock()
            mock_cred_ex.retrieve_by_id.return_value.state = mock_cred_ex.STATE_ACKED

            with self.assertRaises(test_module.web.HTTPBadRequest):
                await test_module.credential_exchange_send_bound_offer(mock)

    async def test_credential_exchange_send_bound_offer_not_ready(self):
        mock = async_mock.MagicMock()
        mock.json = async_mock.CoroutineMock()

        mock.app = {
            "outbound_message_router": async_mock.CoroutineMock(),
            "request_context": async_mock.patch.object(
                aio_web, "BaseRequest", autospec=True
            ),
        }
        mock.app["request_context"].settings = {}

        with async_mock.patch.object(
            test_module, "ConnectionRecord", autospec=True
        ) as mock_connection_record, async_mock.patch.object(
            test_module, "CredentialManager", autospec=True
        ) as mock_credential_manager, async_mock.patch.object(
            test_module, "V10CredentialExchange", autospec=True
        ) as mock_cred_ex:

            mock_cred_ex.retrieve_by_id = async_mock.CoroutineMock()
            mock_cred_ex.retrieve_by_id.return_value.state = (
                mock_cred_ex.STATE_PROPOSAL_RECEIVED
            )

            # Emulate connection not ready
            mock_connection_record.retrieve_by_id = async_mock.CoroutineMock()
            mock_connection_record.retrieve_by_id.return_value.is_ready = False

            mock_credential_manager.return_value.create_offer = (
                async_mock.CoroutineMock()
            )
            mock_credential_manager.return_value.create_offer.return_value = (
                async_mock.MagicMock(),
                async_mock.MagicMock(),
            )

            with self.assertRaises(test_module.web.HTTPForbidden):
                await test_module.credential_exchange_send_bound_offer(mock)

    async def test_credential_exchange_send_request(self):
        mock = async_mock.MagicMock()
        mock.json = async_mock.CoroutineMock()

        mock.app = {
            "outbound_message_router": async_mock.CoroutineMock(),
            "request_context": async_mock.patch.object(
                aio_web, "BaseRequest", autospec=True
            ),
        }
        mock.app["request_context"].settings = {}

        with async_mock.patch.object(
            test_module, "ConnectionRecord", autospec=True
        ) as mock_connection_record, async_mock.patch.object(
            test_module, "CredentialManager", autospec=True
        ) as mock_credential_manager, async_mock.patch.object(
            test_module, "V10CredentialExchange", autospec=True
        ) as mock_cred_ex, async_mock.patch.object(
            test_module.web, "json_response"
        ) as mock_response:

            mock_cred_ex.retrieve_by_id = async_mock.CoroutineMock()
            mock_cred_ex.retrieve_by_id.return_value.state = (
                mock_cred_ex.STATE_OFFER_RECEIVED
            )

            mock_cred_ex_record = async_mock.MagicMock()

            mock_credential_manager.return_value.create_request.return_value = (
                mock_cred_ex_record,
                async_mock.MagicMock(),
            )

            await test_module.credential_exchange_send_request(mock)

            mock_response.assert_called_once_with(
                mock_cred_ex_record.serialize.return_value
            )

    async def test_credential_exchange_send_request_bad_cred_ex_id(self):
        mock = async_mock.MagicMock()
        mock.json = async_mock.CoroutineMock()

        mock.app = {
            "outbound_message_router": async_mock.CoroutineMock(),
            "request_context": async_mock.patch.object(
                aio_web, "BaseRequest", autospec=True
            ),
        }
        mock.app["request_context"].settings = {}

        with async_mock.patch.object(
            test_module, "V10CredentialExchange", autospec=True
        ) as mock_cred_ex:
            mock_cred_ex.retrieve_by_id = async_mock.CoroutineMock()
            mock_cred_ex.retrieve_by_id.side_effect = test_module.StorageNotFoundError()

            with self.assertRaises(test_module.web.HTTPNotFound):
                await test_module.credential_exchange_send_request(mock)

    async def test_credential_exchange_send_request_bad_state(self):
        mock = async_mock.MagicMock()
        mock.json = async_mock.CoroutineMock()

        mock.app = {
            "outbound_message_router": async_mock.CoroutineMock(),
            "request_context": async_mock.patch.object(
                aio_web, "BaseRequest", autospec=True
            ),
        }
        mock.app["request_context"].settings = {}

        with async_mock.patch.object(
            test_module, "V10CredentialExchange", autospec=True
        ) as mock_cred_ex:

            mock_cred_ex.retrieve_by_id = async_mock.CoroutineMock()
            mock_cred_ex.retrieve_by_id.return_value.state = mock_cred_ex.STATE_ACKED

            with self.assertRaises(test_module.web.HTTPBadRequest):
                await test_module.credential_exchange_send_request(mock)

    async def test_credential_exchange_send_request_no_conn_record(self):
        mock = async_mock.MagicMock()
        mock.json = async_mock.CoroutineMock()

        mock.app = {
            "outbound_message_router": async_mock.CoroutineMock(),
            "request_context": async_mock.patch.object(
                aio_web, "BaseRequest", autospec=True
            ),
        }
        mock.app["request_context"].settings = {}

        with async_mock.patch.object(
            test_module, "ConnectionRecord", autospec=True
        ) as mock_connection_record, async_mock.patch.object(
            test_module, "CredentialManager", autospec=True
        ) as mock_credential_manager, async_mock.patch.object(
            test_module, "V10CredentialExchange", autospec=True
        ) as mock_cred_ex:

            mock_cred_ex.retrieve_by_id = async_mock.CoroutineMock()
            mock_cred_ex.retrieve_by_id.return_value.state = (
                mock_cred_ex.STATE_OFFER_RECEIVED
            )

            # Emulate storage not found (bad connection id)
            mock_connection_record.retrieve_by_id = async_mock.CoroutineMock(
                side_effect=StorageNotFoundError()
            )

            mock_credential_manager.return_value.create_offer = (
                async_mock.CoroutineMock()
            )
            mock_credential_manager.return_value.create_offer.return_value = (
                async_mock.MagicMock(),
                async_mock.MagicMock(),
            )

            with self.assertRaises(test_module.web.HTTPBadRequest):
                await test_module.credential_exchange_send_request(mock)

    async def test_credential_exchange_send_request_not_ready(self):
        mock = async_mock.MagicMock()
        mock.json = async_mock.CoroutineMock()

        mock.app = {
            "outbound_message_router": async_mock.CoroutineMock(),
            "request_context": async_mock.patch.object(
                aio_web, "BaseRequest", autospec=True
            ),
        }
        mock.app["request_context"].settings = {}

        with async_mock.patch.object(
            test_module, "ConnectionRecord", autospec=True
        ) as mock_connection_record, async_mock.patch.object(
            test_module, "CredentialManager", autospec=True
        ) as mock_credential_manager, async_mock.patch.object(
            test_module, "V10CredentialExchange", autospec=True
        ) as mock_cred_ex:

            mock_cred_ex.retrieve_by_id = async_mock.CoroutineMock()
            mock_cred_ex.retrieve_by_id.return_value.state = (
                mock_cred_ex.STATE_OFFER_RECEIVED
            )

            # Emulate connection not ready
            mock_connection_record.retrieve_by_id = async_mock.CoroutineMock()
            mock_connection_record.retrieve_by_id.return_value.is_ready = False

            mock_credential_manager.return_value.create_offer = (
                async_mock.CoroutineMock()
            )
            mock_credential_manager.return_value.create_offer.return_value = (
                async_mock.MagicMock(),
                async_mock.MagicMock(),
            )

            with self.assertRaises(test_module.web.HTTPForbidden):
                await test_module.credential_exchange_send_request(mock)

    async def test_credential_exchange_issue(self):
        mock = async_mock.MagicMock()
        mock.json = async_mock.CoroutineMock()

        mock.app = {
            "outbound_message_router": async_mock.CoroutineMock(),
            "request_context": async_mock.patch.object(
                aio_web, "BaseRequest", autospec=True
            ),
        }
        mock.app["request_context"].settings = {}

        with async_mock.patch.object(
            test_module, "ConnectionRecord", autospec=True
        ) as mock_connection_record, async_mock.patch.object(
            test_module, "CredentialManager", autospec=True
        ) as mock_credential_manager, async_mock.patch.object(
            test_module, "V10CredentialExchange", autospec=True
        ) as mock_cred_ex, async_mock.patch.object(
            test_module, "CredentialPreview", autospec=True
        ) as mock_cred_preview, async_mock.patch.object(
            test_module.web, "json_response"
        ) as mock_response:

            mock_cred_ex.retrieve_by_id = async_mock.CoroutineMock()
            mock_cred_ex.retrieve_by_id.return_value.state = (
                mock_cred_ex.STATE_REQUEST_RECEIVED
            )

            mock_cred_ex_record = async_mock.MagicMock()

            mock_credential_manager.return_value.issue_credential.return_value = (
                mock_cred_ex_record,
                async_mock.MagicMock(),
            )

            mock_cred_preview.return_value.deserialize.return_value = (
                async_mock.MagicMock()
            )
            mock_cred_preview.return_value.attr_dict.return_value = (
                async_mock.MagicMock()
            )

            await test_module.credential_exchange_issue(mock)

            mock_response.assert_called_once_with(
                mock_cred_ex_record.serialize.return_value
            )

    async def test_credential_exchange_issue_no_preview(self):
        mock = async_mock.MagicMock()
        mock.json = async_mock.CoroutineMock()
        mock.json.return_value = {
            "comment": "comment",
        }

        mock.app = {
            "outbound_message_router": async_mock.CoroutineMock(),
            "request_context": async_mock.patch.object(
                aio_web, "BaseRequest", autospec=True
            ),
        }
        mock.app["request_context"].settings = {}

        with self.assertRaises(test_module.web.HTTPBadRequest):
            await test_module.credential_exchange_issue(mock)

    async def test_credential_exchange_issue_bad_cred_ex_id(self):
        mock = async_mock.MagicMock()
        mock.json = async_mock.CoroutineMock()

        mock.app = {
            "outbound_message_router": async_mock.CoroutineMock(),
            "request_context": async_mock.patch.object(
                aio_web, "BaseRequest", autospec=True
            ),
        }
        mock.app["request_context"].settings = {}

        with async_mock.patch.object(
            test_module, "V10CredentialExchange", autospec=True
        ) as mock_cred_ex:
            mock_cred_ex.retrieve_by_id = async_mock.CoroutineMock()
            mock_cred_ex.retrieve_by_id.side_effect = test_module.StorageNotFoundError()

            with self.assertRaises(test_module.web.HTTPNotFound):
                await test_module.credential_exchange_issue(mock)

    async def test_credential_exchange_issue_bad_state(self):
        mock = async_mock.MagicMock()
        mock.json = async_mock.CoroutineMock()

        mock.app = {
            "outbound_message_router": async_mock.CoroutineMock(),
            "request_context": async_mock.patch.object(
                aio_web, "BaseRequest", autospec=True
            ),
        }
        mock.app["request_context"].settings = {}

        with async_mock.patch.object(
            test_module, "V10CredentialExchange", autospec=True
        ) as mock_cred_ex:

            mock_cred_ex.retrieve_by_id = async_mock.CoroutineMock()
            mock_cred_ex.retrieve_by_id.return_value.state = mock_cred_ex.STATE_ACKED

            with self.assertRaises(test_module.web.HTTPBadRequest):
                await test_module.credential_exchange_issue(mock)

    async def test_credential_exchange_issue_no_conn_record(self):
        mock = async_mock.MagicMock()
        mock.json = async_mock.CoroutineMock()

        mock.app = {
            "outbound_message_router": async_mock.CoroutineMock(),
            "request_context": async_mock.patch.object(
                aio_web, "BaseRequest", autospec=True
            ),
        }
        mock.app["request_context"].settings = {}

        with async_mock.patch.object(
            test_module, "ConnectionRecord", autospec=True
        ) as mock_connection_record, async_mock.patch.object(
            test_module, "CredentialManager", autospec=True
        ) as mock_credential_manager, async_mock.patch.object(
            test_module, "V10CredentialExchange", autospec=True
        ) as mock_cred_ex, async_mock.patch.object(
            test_module, "CredentialPreview", autospec=True
        ) as mock_cred_preview:

            mock_cred_ex.retrieve_by_id = async_mock.CoroutineMock()
            mock_cred_ex.retrieve_by_id.return_value.state = (
                mock_cred_ex.STATE_REQUEST_RECEIVED
            )

            # Emulate storage not found (bad connection id)
            mock_connection_record.retrieve_by_id = async_mock.CoroutineMock(
                side_effect=StorageNotFoundError()
            )

            mock_credential_manager.return_value.issue_credential = (
                async_mock.CoroutineMock()
            )
            mock_credential_manager.return_value.issue_credential.return_value = (
                async_mock.MagicMock(),
                async_mock.MagicMock(),
            )

            mock_cred_preview.return_value.deserialize.return_value = (
                async_mock.MagicMock()
            )
            mock_cred_preview.return_value.attr_dict.return_value = (
                async_mock.MagicMock()
            )

            with self.assertRaises(test_module.web.HTTPBadRequest):
                await test_module.credential_exchange_issue(mock)

    async def test_credential_exchange_issue_not_ready(self):
        mock = async_mock.MagicMock()
        mock.json = async_mock.CoroutineMock()

        mock.app = {
            "outbound_message_router": async_mock.CoroutineMock(),
            "request_context": async_mock.patch.object(
                aio_web, "BaseRequest", autospec=True
            ),
        }
        mock.app["request_context"].settings = {}

        with async_mock.patch.object(
            test_module, "ConnectionRecord", autospec=True
        ) as mock_connection_record, async_mock.patch.object(
            test_module, "CredentialManager", autospec=True
        ) as mock_credential_manager, async_mock.patch.object(
            test_module, "V10CredentialExchange", autospec=True
        ) as mock_cred_ex, async_mock.patch.object(
            test_module, "CredentialPreview", autospec=True
        ) as mock_cred_preview:

            mock_cred_ex.retrieve_by_id = async_mock.CoroutineMock()
            mock_cred_ex.retrieve_by_id.return_value.state = (
                mock_cred_ex.STATE_REQUEST_RECEIVED
            )

            # Emulate connection not ready
            mock_connection_record.retrieve_by_id = async_mock.CoroutineMock()
            mock_connection_record.retrieve_by_id.return_value.is_ready = False

            mock_credential_manager.return_value.issue_credential = (
                async_mock.CoroutineMock()
            )
            mock_credential_manager.return_value.issue_credential.return_value = (
                async_mock.MagicMock(),
                async_mock.MagicMock(),
            )

            mock_cred_preview.return_value.deserialize.return_value = (
                async_mock.MagicMock()
            )
            mock_cred_preview.return_value.attr_dict.return_value = (
                async_mock.MagicMock()
            )

            with self.assertRaises(test_module.web.HTTPForbidden):
                await test_module.credential_exchange_issue(mock)

    async def test_credential_exchange_issue_rev_reg_full(self):
        mock = async_mock.MagicMock()
        mock.json = async_mock.CoroutineMock()

        mock.app = {
            "outbound_message_router": async_mock.CoroutineMock(),
            "request_context": async_mock.patch.object(
                aio_web, "BaseRequest", autospec=True
            ),
        }
        mock.app["request_context"].settings = {}

        with async_mock.patch.object(
            test_module, "ConnectionRecord", autospec=True
        ) as mock_connection_record, async_mock.patch.object(
            test_module, "CredentialManager", autospec=True
        ) as mock_credential_manager, async_mock.patch.object(
            test_module, "V10CredentialExchange", autospec=True
        ) as mock_cred_ex, async_mock.patch.object(
            test_module, "CredentialPreview", autospec=True
        ) as mock_cred_preview:

            mock_cred_ex.retrieve_by_id = async_mock.CoroutineMock()
            mock_cred_ex.retrieve_by_id.return_value.state = (
                mock_cred_ex.STATE_REQUEST_RECEIVED
            )

            mock_connection_record.retrieve_by_id = async_mock.CoroutineMock()
            mock_connection_record.retrieve_by_id.return_value.is_ready = True

            mock_credential_manager.return_value.issue_credential = async_mock.CoroutineMock(
                side_effect=test_module.IssuerRevocationRegistryFullError()
            )
            mock_credential_manager.return_value.issue_credential.return_value = (
                async_mock.MagicMock(),
                async_mock.MagicMock(),
            )

            mock_cred_preview.return_value.deserialize.return_value = (
                async_mock.MagicMock()
            )
            mock_cred_preview.return_value.attr_dict.return_value = (
                async_mock.MagicMock()
            )

            with self.assertRaises(test_module.web.HTTPBadRequest) as context:
                await test_module.credential_exchange_issue(mock)

    async def test_credential_exchange_issue_deser_x(self):
        mock = async_mock.MagicMock()
        mock.json = async_mock.CoroutineMock()

        mock.app = {
            "outbound_message_router": async_mock.CoroutineMock(),
            "request_context": async_mock.patch.object(
                aio_web, "BaseRequest", autospec=True
            ),
        }
        mock.app["request_context"].settings = {}

        with async_mock.patch.object(
            test_module, "ConnectionRecord", autospec=True
        ) as mock_connection_record, async_mock.patch.object(
            test_module, "CredentialManager", autospec=True
        ) as mock_credential_manager, async_mock.patch.object(
            test_module, "V10CredentialExchange", autospec=True
        ) as mock_cred_ex, async_mock.patch.object(
            test_module, "CredentialPreview", autospec=True
        ) as mock_cred_preview:
            mock_cred_ex.retrieve_by_id = async_mock.CoroutineMock()
            mock_cred_ex.retrieve_by_id.return_value.state = (
                mock_cred_ex.STATE_REQUEST_RECEIVED
            )
            mock_cred_ex_record = async_mock.MagicMock()
            mock_credential_manager.return_value.issue_credential.return_value = (
                mock_cred_ex_record,
                async_mock.MagicMock(),
            )
            mock_cred_preview.deserialize = async_mock.MagicMock(
                side_effect=test_module.BaseModelError()
            )
            with self.assertRaises(test_module.web.HTTPBadRequest):
                await test_module.credential_exchange_issue(mock)

    async def test_credential_exchange_store(self):
        mock = async_mock.MagicMock()
        mock.json = async_mock.CoroutineMock()

        mock.app = {
            "outbound_message_router": async_mock.CoroutineMock(),
            "request_context": async_mock.patch.object(
                aio_web, "BaseRequest", autospec=True
            ),
        }
        mock.app["request_context"].settings = {}

        with async_mock.patch.object(
            test_module, "ConnectionRecord", autospec=True
        ) as mock_connection_record, async_mock.patch.object(
            test_module, "CredentialManager", autospec=True
        ) as mock_credential_manager, async_mock.patch.object(
            test_module, "V10CredentialExchange", autospec=True
        ) as mock_cred_ex, async_mock.patch.object(
            test_module.web, "json_response"
        ) as mock_response:

            mock_cred_ex.retrieve_by_id = async_mock.CoroutineMock()
            mock_cred_ex.retrieve_by_id.return_value.state = (
                mock_cred_ex.STATE_CREDENTIAL_RECEIVED
            )

            mock_cred_ex_record = async_mock.MagicMock()

            mock_credential_manager.return_value.store_credential.return_value = (
                mock_cred_ex_record,
                async_mock.MagicMock(),
            )

            await test_module.credential_exchange_store(mock)

            mock_response.assert_called_once_with(
                mock_cred_ex_record.serialize.return_value
            )

    async def test_credential_exchange_store_bad_cred_id_json(self):
        mock = async_mock.MagicMock()
        mock.json = async_mock.CoroutineMock(
            side_effect=test_module.JSONDecodeError("Nope", "Nope", 0)
        )

        mock.app = {
            "outbound_message_router": async_mock.CoroutineMock(),
            "request_context": async_mock.patch.object(
                aio_web, "BaseRequest", autospec=True
            ),
        }
        mock.app["request_context"].settings = {}

        with async_mock.patch.object(
            test_module, "ConnectionRecord", autospec=True
        ) as mock_connection_record, async_mock.patch.object(
            test_module, "CredentialManager", autospec=True
        ) as mock_credential_manager, async_mock.patch.object(
            test_module, "V10CredentialExchange", autospec=True
        ) as mock_cred_ex, async_mock.patch.object(
            test_module.web, "json_response"
        ) as mock_response:

            mock_cred_ex.retrieve_by_id = async_mock.CoroutineMock()
            mock_cred_ex.retrieve_by_id.return_value.state = (
                mock_cred_ex.STATE_CREDENTIAL_RECEIVED
            )

            mock_cred_ex_record = async_mock.MagicMock()

            mock_credential_manager.return_value.store_credential.return_value = (
                mock_cred_ex_record,
                async_mock.MagicMock(),
            )

            await test_module.credential_exchange_store(mock)

            mock_response.assert_called_once_with(
                mock_cred_ex_record.serialize.return_value
            )

    async def test_credential_exchange_store_bad_cred_ex_id(self):
        mock = async_mock.MagicMock()
        mock.json = async_mock.CoroutineMock()

        mock.app = {
            "outbound_message_router": async_mock.CoroutineMock(),
            "request_context": async_mock.patch.object(
                aio_web, "BaseRequest", autospec=True
            ),
        }
        mock.app["request_context"].settings = {}

        with async_mock.patch.object(
            test_module, "V10CredentialExchange", autospec=True
        ) as mock_cred_ex:
            mock_cred_ex.retrieve_by_id = async_mock.CoroutineMock()
            mock_cred_ex.retrieve_by_id.side_effect = test_module.StorageNotFoundError()

            with self.assertRaises(test_module.web.HTTPNotFound):
                await test_module.credential_exchange_store(mock)

    async def test_credential_exchange_store_bad_state(self):
        mock = async_mock.MagicMock()
        mock.json = async_mock.CoroutineMock()

        mock.app = {
            "outbound_message_router": async_mock.CoroutineMock(),
            "request_context": async_mock.patch.object(
                aio_web, "BaseRequest", autospec=True
            ),
        }
        mock.app["request_context"].settings = {}

        with async_mock.patch.object(
            test_module, "V10CredentialExchange", autospec=True
        ) as mock_cred_ex:

            mock_cred_ex.retrieve_by_id = async_mock.CoroutineMock()
            mock_cred_ex.retrieve_by_id.return_value.state = mock_cred_ex.STATE_ACKED

            with self.assertRaises(test_module.web.HTTPBadRequest):
                await test_module.credential_exchange_store(mock)

    async def test_credential_exchange_store_no_conn_record(self):
        mock = async_mock.MagicMock()
        mock.json = async_mock.CoroutineMock()

        mock.app = {
            "outbound_message_router": async_mock.CoroutineMock(),
            "request_context": async_mock.patch.object(
                aio_web, "BaseRequest", autospec=True
            ),
        }
        mock.app["request_context"].settings = {}

        with async_mock.patch.object(
            test_module, "ConnectionRecord", autospec=True
        ) as mock_connection_record, async_mock.patch.object(
            test_module, "CredentialManager", autospec=True
        ) as mock_credential_manager, async_mock.patch.object(
            test_module, "V10CredentialExchange", autospec=True
        ) as mock_cred_ex:

            mock_cred_ex.retrieve_by_id = async_mock.CoroutineMock()
            mock_cred_ex.retrieve_by_id.return_value.state = (
                mock_cred_ex.STATE_CREDENTIAL_RECEIVED
            )

            # Emulate storage not found (bad connection id)
            mock_connection_record.retrieve_by_id = async_mock.CoroutineMock(
                side_effect=StorageNotFoundError()
            )

            mock_credential_manager.return_value.store_credential.return_value = (
                mock_cred_ex,
                async_mock.MagicMock(),
            )

            with self.assertRaises(test_module.web.HTTPBadRequest):
                await test_module.credential_exchange_store(mock)

    async def test_credential_exchange_store_not_ready(self):
        mock = async_mock.MagicMock()
        mock.json = async_mock.CoroutineMock()

        mock.app = {
            "outbound_message_router": async_mock.CoroutineMock(),
            "request_context": async_mock.patch.object(
                aio_web, "BaseRequest", autospec=True
            ),
        }
        mock.app["request_context"].settings = {}

        with async_mock.patch.object(
            test_module, "ConnectionRecord", autospec=True
        ) as mock_connection_record, async_mock.patch.object(
            test_module, "CredentialManager", autospec=True
        ) as mock_credential_manager, async_mock.patch.object(
            test_module, "V10CredentialExchange", autospec=True
        ) as mock_cred_ex:

            mock_cred_ex.retrieve_by_id = async_mock.CoroutineMock()
            mock_cred_ex.retrieve_by_id.return_value.state = (
                mock_cred_ex.STATE_CREDENTIAL_RECEIVED
            )

            # Emulate connection not ready
            mock_connection_record.retrieve_by_id = async_mock.CoroutineMock()
            mock_connection_record.retrieve_by_id.return_value.is_ready = False

            mock_credential_manager.return_value.store_credential.return_value = (
                mock_cred_ex,
                async_mock.MagicMock(),
            )

            with self.assertRaises(test_module.web.HTTPForbidden):
                await test_module.credential_exchange_store(mock)

    async def test_credential_exchange_remove(self):
        mock = async_mock.MagicMock()
        mock.match_info = {"cred_ex_id": "dummy"}

        mock.app = {
            "outbound_message_router": async_mock.CoroutineMock(),
            "request_context": async_mock.patch.object(
                aio_web, "BaseRequest", autospec=True
            ),
        }
        mock.app["request_context"].settings = {}

        with async_mock.patch.object(
            test_module, "V10CredentialExchange", autospec=True
        ) as mock_cred_ex, async_mock.patch.object(
            test_module.web, "json_response"
        ) as mock_response:
            mock_cred_ex.retrieve_by_id = async_mock.CoroutineMock()
            mock_cred_ex.retrieve_by_id.return_value = mock_cred_ex

            mock_cred_ex.delete_record = async_mock.CoroutineMock()

            await test_module.credential_exchange_remove(mock)

            mock_response.assert_called_once_with({})

    async def test_credential_exchange_remove_bad_cred_ex_id(self):
        mock = async_mock.MagicMock()

        mock_outbound = async_mock.CoroutineMock()

        with async_mock.patch.object(
            test_module, "V10CredentialExchange", autospec=True
        ) as mock_cred_ex:
            # Emulate storage not found (bad cred ex id)
            mock_cred_ex.retrieve_by_id = async_mock.CoroutineMock(
                side_effect=StorageNotFoundError()
            )

            with self.assertRaises(test_module.web.HTTPNotFound):
                await test_module.credential_exchange_remove(mock)

    async def test_credential_exchange_remove_x(self):
        mock = async_mock.MagicMock()

        mock_outbound = async_mock.CoroutineMock()

        with async_mock.patch.object(
            test_module, "V10CredentialExchange", autospec=True
        ) as mock_cred_ex:
            # Emulate storage not found (bad cred ex id)
            mock_rec = async_mock.MagicMock(
                delete_record=async_mock.CoroutineMock(
                    side_effect=test_module.StorageError()
                )
            )
            mock_cred_ex.retrieve_by_id = async_mock.CoroutineMock(
                return_value=mock_rec
            )

            with self.assertRaises(test_module.web.HTTPBadRequest):
                await test_module.credential_exchange_remove(mock)

    async def test_credential_exchange_revoke(self):
        mock = async_mock.MagicMock(
            query={"rev_reg_id": "rr_id", "cred_rev_id": "23", "publish": "false",}
        )
        mock.app = {
            "request_context": async_mock.patch.object(
                aio_web, "BaseRequest", autospec=True
            ),
        }
        mock.app["request_context"].settings = {}

        with async_mock.patch.object(
            test_module, "CredentialManager", autospec=True
        ) as mock_cred_mgr, async_mock.patch.object(
            test_module.web, "json_response"
        ) as mock_response:

            mock_cred_mgr.return_value.revoke_credential = async_mock.CoroutineMock()

            await test_module.credential_exchange_revoke(mock)

            mock_response.assert_called_once_with({})

    async def test_credential_exchange_revoke_not_found(self):
        mock = async_mock.MagicMock(
            query={"rev_reg_id": "rr_id", "cred_rev_id": "23", "publish": "false",}
        )
        mock.app = {
            "request_context": async_mock.patch.object(
                aio_web, "BaseRequest", autospec=True
            ),
        }
        mock.app["request_context"].settings = {}

        with async_mock.patch.object(
            test_module, "CredentialManager", autospec=True
        ) as mock_cred_mgr, async_mock.patch.object(
            test_module.web, "json_response"
        ) as mock_response:

            mock_cred_mgr.return_value.revoke_credential = async_mock.CoroutineMock(
                side_effect=StorageNotFoundError()
            )

            with self.assertRaises(test_module.web.HTTPBadRequest):
                await test_module.credential_exchange_revoke(mock)

    async def test_credential_exchange_publish_revocations(self):
        mock = async_mock.MagicMock()
        mock.app = {
            "request_context": async_mock.patch.object(
                aio_web, "BaseRequest", autospec=True
            ),
        }
        mock.app["request_context"].settings = {}

        with async_mock.patch.object(
            test_module, "CredentialManager", autospec=True
        ) as mock_cred_mgr, async_mock.patch.object(
            test_module.web, "json_response"
        ) as mock_response:
            pub_pending = async_mock.CoroutineMock()
            mock_cred_mgr.return_value.publish_pending_revocations = pub_pending

            await test_module.credential_exchange_publish_revocations(mock)

            mock_response.assert_called_once_with({"results": pub_pending.return_value})

    async def test_credential_exchange_publish_revocations_x(self):
        mock = async_mock.MagicMock()
        mock.app = {
            "request_context": async_mock.patch.object(
                aio_web, "BaseRequest", autospec=True
            ),
        }
        mock.app["request_context"].settings = {}

        with async_mock.patch.object(
            test_module, "CredentialManager", autospec=True
        ) as mock_cred_mgr:
            pub_pending = async_mock.CoroutineMock(
                side_effect=test_module.RevocationError()
            )
            mock_cred_mgr.return_value.publish_pending_revocations = pub_pending

            with self.assertRaises(test_module.web.HTTPBadRequest):
                await test_module.credential_exchange_publish_revocations(mock)

    async def test_credential_exchange_problem_report(self):
        mock = async_mock.MagicMock()
        mock.json = async_mock.CoroutineMock()

        mock_outbound = async_mock.CoroutineMock()

        mock.app = {
            "outbound_message_router": mock_outbound,
            "request_context": async_mock.patch.object(
                aio_web, "BaseRequest", autospec=True
            ),
        }
        mock.app["request_context"].settings = {}

        with async_mock.patch.object(
            test_module, "ConnectionRecord", autospec=True
        ) as mock_connection_record, async_mock.patch.object(
            test_module, "CredentialManager", autospec=True
        ) as mock_credential_manager, async_mock.patch.object(
            test_module, "V10CredentialExchange", autospec=True
        ) as mock_cred_ex, async_mock.patch.object(
            test_module, "ProblemReport", autospec=True
        ) as mock_prob_report, async_mock.patch.object(
            test_module.web, "json_response"
        ) as mock_response:

            mock_cred_ex.retrieve_by_id = async_mock.CoroutineMock()

            await test_module.credential_exchange_problem_report(mock)

            mock_response.assert_called_once_with({})
            mock_outbound.assert_called_once_with(
                mock_prob_report.return_value,
                connection_id=mock_cred_ex.retrieve_by_id.return_value.connection_id,
            )

    async def test_credential_exchange_problem_report_bad_cred_id(self):
        mock = async_mock.MagicMock()
        mock.json = async_mock.CoroutineMock()

        mock_outbound = async_mock.CoroutineMock()

        mock.app = {
            "outbound_message_router": mock_outbound,
            "request_context": async_mock.patch.object(
                aio_web, "BaseRequest", autospec=True
            ),
        }
        mock.app["request_context"].settings = {}

        with async_mock.patch.object(
            test_module, "V10CredentialExchange", autospec=True
        ) as mock_cred_ex:
            mock_cred_ex.retrieve_by_id = async_mock.CoroutineMock(
                side_effect=StorageNotFoundError()
            )

            with self.assertRaises(test_module.web.HTTPNotFound):
                await test_module.credential_exchange_problem_report(mock)

    async def test_register(self):
        mock_app = async_mock.MagicMock()
        mock_app.add_routes = async_mock.MagicMock()

        await test_module.register(mock_app)
        mock_app.add_routes.assert_called_once()

    async def test_post_process_routes(self):
        mock_app = async_mock.MagicMock(_state={"swagger_dict": {}})
        test_module.post_process_routes(mock_app)
        assert "tags" in mock_app._state["swagger_dict"]
