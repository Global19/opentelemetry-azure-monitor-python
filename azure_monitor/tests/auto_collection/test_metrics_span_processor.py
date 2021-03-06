# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import unittest

from opentelemetry.sdk.trace import Span
from opentelemetry.trace import SpanContext, SpanKind
from opentelemetry.trace.status import Status, StatusCanonicalCode

from azure_monitor.sdk.auto_collection.metrics_span_processor import (
    AzureMetricsSpanProcessor,
)


# pylint: disable=protected-access
class TestMetricsSpanProcessor(unittest.TestCase):
    def test_document_collection(self):
        """Test the document collection."""
        span_processor = AzureMetricsSpanProcessor()
        span_processor.is_collecting_documents = True
        test_span = Span(
            name="test",
            kind=SpanKind.SERVER,
            context=SpanContext(
                trace_id=36873507687745823477771305566750195431,
                span_id=12030755672171557338,
                is_remote=False,
            ),
        )
        test_span.set_status(Status(StatusCanonicalCode.INTERNAL, "test"))
        test_span._start_time = 5000000
        test_span._end_time = 15000000
        span_processor.on_end(test_span)
        document = span_processor.documents.pop()
        self.assertIsNotNone(document)
        self.assertEqual(
            document.name, "Microsoft.ApplicationInsights.Request"
        )
