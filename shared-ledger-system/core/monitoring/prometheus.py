# core/monitoring/prometheus.py
from prometheus_client import CollectorRegistry, Counter, Histogram, make_asgi_app
from fastapi import FastAPI
from core.config import core_settings


class PrometheusMetrics:
    def __init__(self):
        self.prometheus_enabled = core_settings.prometheus.prometheus_enabled
        self.registry = CollectorRegistry()

        if self.prometheus_enabled:
            self.ledger_operations_counter = Counter(
                "ledger_operations_total",
                "Total number of ledger operations performed, by operation type.",
                ["operation_type"],
                registry=self.registry,
            )
            self.balance_queries_counter = Counter(
                "balance_queries_counter",
                "Total number of balance queries executed.",
                registry=self.registry,
            )
            self.operation_duration_histogram = Histogram(
                "operation_duration_seconds",
                "Time spent processing ledger operations, by operation type.",
                ["operation_type"],
                registry=self.registry,
            )
            self.api_error_counter = Counter(
                "api_errors_total",
                "Total number of API errors encountered, by endpoint and error type.",
                ["endpoint", "error_type"],
                registry=self.registry,
            )
            self.cache_hit_count = Counter(
                "cache_hit_total",
                "Total number of cache hits, by endpoint.",
                ["endpoint"],
                registry=self.registry,
            )
            self.cache_miss_count = Counter(
                "cache_miss_total",
                "Total number of cache misses, by endpoint.",
                ["endpoint"],
                registry=self.registry,
            )
        else:
            self.ledger_operations_counter = self._dummy_metric()
            self.balance_queries_counter = self._dummy_metric()
            self.operation_duration_histogram = self._dummy_metric()
            self.api_error_counter = self._dummy_metric()
            self.cache_hit_count = self._dummy_metric()
            self.cache_miss_count = self._dummy_metric()

    def _dummy_metric(self):
        class DummyMetric:
            def labels(self, *args, **kwargs):
                return self

            def inc(self, *args, **kwargs):
                pass

            def observe(self, *args, **kwargs):
                pass

            def time(self):
                return self

        return DummyMetric()

    def init_app(self, app: FastAPI):
        if self.prometheus_enabled:
            metrics_app = make_asgi_app(registry=self.registry)
            app.mount("/metrics", metrics_app)
        else:
            print("Prometheus metrics are disabled.")


metrics = PrometheusMetrics()
