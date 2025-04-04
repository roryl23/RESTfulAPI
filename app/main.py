import time
from fastapi import FastAPI, Request, Response
from opentelemetry import trace, metrics
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

from app.api.routes import router
from app.config import settings

app = FastAPI(
    title="RESTfulAPI",
    description="A FastAPI application",
    version="0.1.0"
)

# telemetry
resource = Resource(attributes={"service.name": "restfulapi"})
# traces
trace.set_tracer_provider(TracerProvider(resource=resource))
tracer = trace.get_tracer(__name__)
otlp_exporter = OTLPSpanExporter(
    endpoint=settings.JAEGER_ENDPOINT,
    insecure=True,
)
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)
FastAPIInstrumentor.instrument_app(app)

# metrics
metric_reader = PrometheusMetricReader()
metrics_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
metrics.set_meter_provider(metrics_provider)
meter = metrics.get_meter(__name__)

request_counter = meter.create_counter(
    name="http_requests_total",
    description="Total number of HTTP requests",
    unit="1"
)
request_duration = meter.create_histogram(
    name="http_request_duration",
    description="Duration of HTTP requests in ms",
    unit="ms"
)

app.include_router(router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the RESTfulAPI!"}


@app.get("/metrics")
async def get_metrics():
    """
    Expose Prometheus metrics at /metrics endpoint.
    """
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )


@app.middleware("httpmetrics")
async def add_metrics(request: Request, call_next):
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("http-request") as span:
        start_time = time.time_ns() / 1000000
        request_counter.add(1, {"method": request.method, "endpoint": request.url.path})
        response = await call_next(request)
        duration = (time.time_ns() / 1000000) - start_time
        request_duration.record(duration, {"method": request.method, "endpoint": request.url.path})
        return response


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
