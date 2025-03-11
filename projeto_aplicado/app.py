from fastapi import FastAPI
from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
    OTLPSpanExporter,
)
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(
    debug=True,
    title='Projeto Aplicado SENAI 2025',
    version='0.1.0',
    description='API para o projeto aplicado do SENAI 2025',
)

provider = TracerProvider()
exporter = OTLPSpanExporter(endpoint='http://grafana:3000')
processor = BatchSpanProcessor(exporter)
provider.add_span_processor(processor)


@app.get('/')
async def read_root():
    return {'message': 'Hello World'}


Instrumentator().instrument(app).expose(app)
FastAPIInstrumentor.instrument_app(app, tracer_provider=provider)
