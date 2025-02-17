# tests/apps/app1/test_prometheus.py
import pytest
from httpx import AsyncClient
from prometheus_client import parser
from tests.apps.app1.test_auth import get_access_token_for_test_user
from core.auth.models import User
from redis import asyncio as aioredis


@pytest.mark.asyncio
async def test_prometheus_metrics_increment(client: AsyncClient, db_test_user: User):
    owner_id = str(db_test_user.id)
    cache_key = f"balance:{owner_id}"
    await client.app.state.redis.delete(cache_key)
    access_token = await get_access_token_for_test_user(db_test_user)
    headers = {"Authorization": f"Bearer {access_token}"}

    response_before = await client.get("/metrics/")
    assert response_before.status_code == 200
    metrics_before = parser.text_string_to_metric_families(response_before.text)

    balance_queries_before = 0
    for metric in metrics_before:
        if metric.name == "balance_queries_counter":
            for sample in metric.samples:
                balance_queries_before = int(sample.value)
                break
            break

    api_endpoint_response = await client.get(f"/ledger/{owner_id}", headers=headers)
    assert api_endpoint_response.status_code == 200

    response_after = await client.get("/metrics/")
    assert response_after.status_code == 200
    metrics_after = parser.text_string_to_metric_families(response_after.text)

    balance_queries_after = 0
    for metric in metrics_after:
        if metric.name == "balance_queries_counter":
            for sample in metric.samples:
                balance_queries_after = int(sample.value)
                break
            break

    assert (
        balance_queries_after == balance_queries_before + 1
    ), f"Expected balance_queries_total to increment by 1, but got: before={balance_queries_before}, after={balance_queries_after}"
