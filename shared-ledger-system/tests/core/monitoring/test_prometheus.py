# tests/core/monitoring/test_prometheus.py
from core.monitoring.prometheus import PrometheusMetrics
import pytest_asyncio


@pytest_asyncio.fixture(scope="session")
async def metrics():
    prometheus_metrics = PrometheusMetrics()
    yield prometheus_metrics
    if hasattr(prometheus_metrics, "shutdown"):
        await prometheus_metrics.shutdown()


def test_prometheus_metrics_initialization(metrics):
    assert metrics.ledger_operations_counter is not None
    assert metrics.balance_queries_counter is not None
    assert metrics.operation_duration_histogram is not None
    assert metrics.api_error_counter is not None
    assert metrics.cache_hit_count is not None
    assert metrics.cache_miss_count is not None


def test_prometheus_metrics_increment(metrics):
    metrics.ledger_operations_counter.labels(operation_type="test_op").inc()
    metrics.balance_queries_counter.inc()
    metrics.api_error_counter.labels(
        endpoint="/test_endpoint", error_type="ValueError"
    ).inc()
    metrics.cache_hit_count.labels(endpoint="/test_endpoint").inc()
    metrics.cache_miss_count.labels(endpoint="/test_endpoint").inc()
    metrics.operation_duration_histogram.labels(operation_type="test_op").observe(0.5)

    assert True
