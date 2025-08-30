# Monitoring Protocol Instructions

## Purpose
The Monitoring Protocol tracks system health, worker performance, and session progress in real-time, enabling proactive issue detection and performance optimization.

## When to Use
- **Continuous Monitoring**: Active throughout entire session
- **Performance Tracking**: Monitor resource usage and response times
- **Health Checks**: Regular validation of system components
- **Progress Tracking**: Monitor task completion and milestones
- **Anomaly Detection**: Identify unusual patterns or behaviors

## How to Execute

### Step 1: Import and Initialize
```python
from monitoring_protocol import MonitoringProtocol

# Initialize with session context
monitor = MonitoringProtocol(
    session_id="2024-03-15-14-30-payment-api",
    worker_name="backend-worker"
)

# Start monitoring
monitor.start()
```

### Step 2: Register Metrics
```python
# Register custom metrics
monitor.register_metric("api_requests", "counter", "Total API requests")
monitor.register_metric("response_time", "histogram", "API response times")
monitor.register_metric("active_connections", "gauge", "Current DB connections")
```

### Step 3: Track Metrics
```python
# Increment counter
monitor.increment("api_requests")

# Record timing
monitor.record_time("response_time", 145)  # milliseconds

# Update gauge
monitor.set_gauge("active_connections", 42)

# Track operation
with monitor.track_operation("database_query"):
    result = db.execute(query)
```

## Parameters

### Metric Types
- **Counter**: Incrementing values (requests, errors, completions)
- **Gauge**: Current values (memory, connections, queue size)
- **Histogram**: Distribution of values (response times, sizes)
- **Summary**: Statistical aggregation (percentiles, averages)

### Monitoring Configuration
```python
config = {
    "interval_seconds": 30,        # Metric collection interval
    "retention_hours": 24,         # Metric retention period
    "alert_thresholds": {
        "error_rate": 0.05,       # 5% error rate threshold
        "response_time_p95": 1000, # 95th percentile < 1 second
        "memory_usage_mb": 512     # Memory limit
    },
    "health_check_interval": 60    # Health check frequency
}
```

## Output

### Metrics Storage
- **Real-time Metrics**: `Docs/hive-mind/sessions/{session_id}/metrics/current.json`
- **Historical Metrics**: `Docs/hive-mind/sessions/{session_id}/metrics/history.jsonl`
- **Health Status**: `Docs/hive-mind/sessions/{session_id}/HEALTH.json`
- **Alerts**: `Docs/hive-mind/sessions/{session_id}/ALERTS.jsonl`

### Dashboard Format
```json
{
  "timestamp": "2024-03-15T14:45:00Z",
  "session_id": "2024-03-15-14-30-payment-api",
  "worker": "backend-worker",
  "status": "healthy",
  "metrics": {
    "performance": {
      "requests_per_second": 125,
      "average_response_ms": 45,
      "p95_response_ms": 120,
      "error_rate": 0.002
    },
    "resources": {
      "cpu_percent": 35,
      "memory_mb": 256,
      "disk_io_mb": 12,
      "network_kb": 450
    },
    "progress": {
      "tasks_completed": 8,
      "tasks_remaining": 2,
      "completion_percent": 80
    }
  }
}
```

## Integration

### Automatic Monitoring
The protocol automatically monitors:
- **System Resources**: CPU, memory, disk, network
- **Worker Activity**: Task progress, idle time, throughput
- **Session Progress**: Completion percentage, estimated time
- **Error Rates**: Failures, retries, exceptions
- **Performance**: Response times, processing speed

### Alert Generation
```python
# Configure alerts
monitor.set_alert("high_error_rate", 
                 condition=lambda m: m["error_rate"] > 0.05,
                 action="escalate")

monitor.set_alert("slow_response",
                 condition=lambda m: m["p95_response_ms"] > 1000,
                 action="notify")

# Check for alerts
alerts = monitor.check_alerts()
if alerts:
    handle_alerts(alerts)
```

## Best Practices

1. **Start Early**: Begin monitoring at session start
2. **Track Key Metrics**: Focus on business-critical metrics
3. **Set Realistic Thresholds**: Avoid alert fatigue
4. **Regular Health Checks**: Validate system state frequently
5. **Correlate Metrics**: Look for relationships between metrics
6. **Clean Up**: Remove old metrics after retention period

## Advanced Features

### Anomaly Detection
```python
# Enable anomaly detection
monitor.enable_anomaly_detection(
    sensitivity="medium",
    baseline_period_hours=24
)

# Check for anomalies
anomalies = monitor.detect_anomalies()
for anomaly in anomalies:
    logger.log_warning(f"Anomaly detected: {anomaly}")
```

### Predictive Monitoring
```python
# Predict resource exhaustion
prediction = monitor.predict_resource_exhaustion()
if prediction["memory"]["hours_until_exhausted"] < 1:
    scale_up_resources()
```

### Comparative Analysis
```python
# Compare with previous sessions
comparison = monitor.compare_with_baseline(
    baseline_session="2024-03-14-10-00-similar-task"
)
print(f"Performance delta: {comparison['performance_change']}%")
```

## Health Checks

### System Health
```python
# Comprehensive health check
health = monitor.check_health()

health_status = {
    "overall": "healthy|degraded|unhealthy",
    "components": {
        "database": {"status": "healthy", "latency_ms": 5},
        "api": {"status": "healthy", "uptime_percent": 99.9},
        "workers": {"active": 3, "idle": 1, "failed": 0}
    },
    "issues": []
}
```

### Worker Health
```python
# Worker-specific health monitoring
worker_health = monitor.check_worker_health("backend-worker")

if worker_health["status"] == "unhealthy":
    escalate_to_queen(worker_health["issues"])
```

## Performance Optimization

### Bottleneck Detection
```python
# Identify performance bottlenecks
bottlenecks = monitor.find_bottlenecks()

for bottleneck in bottlenecks:
    print(f"Bottleneck: {bottleneck['component']}")
    print(f"Impact: {bottleneck['impact_percent']}%")
    print(f"Recommendation: {bottleneck['recommendation']}")
```

### Resource Optimization
```python
# Get optimization recommendations
optimizations = monitor.suggest_optimizations()

for opt in optimizations:
    if opt["potential_savings_percent"] > 20:
        apply_optimization(opt)
```

## Real-time Dashboards

### Generate Dashboard
```python
# Create real-time dashboard data
dashboard = monitor.generate_dashboard()

# Dashboard includes:
# - Current metrics
# - Trend graphs
# - Alert status
# - Health indicators
# - Progress tracking
```

### Export Metrics
```python
# Export for external monitoring
monitor.export_metrics(
    format="prometheus",  # or "datadog", "grafana"
    endpoint="http://metrics.example.com"
)
```

## Example: Complete Monitoring Flow

```python
from monitoring_protocol import MonitoringProtocol

# Initialize monitoring
monitor = MonitoringProtocol("2024-03-15-14-30-api", "backend-worker")
monitor.start()

# Configure monitoring
monitor.register_metric("api_calls", "counter")
monitor.register_metric("db_query_time", "histogram")
monitor.register_metric("cache_hit_rate", "gauge")

# Set up alerts
monitor.set_alert("high_latency",
                 condition=lambda m: m["p95_query_time"] > 100,
                 action="warn")

# Main work loop
for task in tasks:
    # Track operation
    with monitor.track_operation("process_task"):
        try:
            # Record start
            monitor.increment("api_calls")
            
            # Process with timing
            start = time.time()
            result = process_task(task)
            duration = (time.time() - start) * 1000
            
            # Record metrics
            monitor.record_time("db_query_time", duration)
            monitor.set_gauge("cache_hit_rate", cache.hit_rate())
            
            # Check health periodically
            if monitor.should_check_health():
                health = monitor.check_health()
                if health["status"] != "healthy":
                    handle_degraded_health(health)
            
        except Exception as e:
            monitor.record_error("task_processing", str(e))
            
    # Check for alerts
    alerts = monitor.check_alerts()
    if alerts:
        for alert in alerts:
            logger.log_warning(f"Alert: {alert['name']} - {alert['message']}")

# Generate final report
report = monitor.generate_report()
monitor.save_report(report)

# Stop monitoring
monitor.stop()
```

## Troubleshooting

### Common Issues
- **Metric Overflow**: Automatic rotation at size limits
- **Missing Metrics**: Check registration and collection
- **False Alerts**: Adjust thresholds based on baseline
- **Performance Impact**: Reduce collection frequency if needed

### Debug Mode
```python
# Enable debug monitoring
monitor.debug = True  # Verbose metric logging
monitor.trace_metrics = True  # Log every metric update
```

## Notes

- Metrics are collected asynchronously to minimize impact
- Historical data is compressed after 24 hours
- Supports multiple workers monitoring same session
- Thread-safe for concurrent metric updates
- Integrates with standard monitoring tools (Prometheus, Grafana)
- Automatic cleanup of metrics older than retention period