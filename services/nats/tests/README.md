# NATS System Tests

This directory contains test scripts to verify the NATS messaging system setup and functionality.

## Test Coverage

The test suite (`test_nats_setup.py`) verifies:

1. NATS Server Connection
   - Basic connectivity to the NATS server
   - JetStream availability

2. Stream Configuration
   - Existence and configuration of AUDIT_EVENTS stream
   - Existence and configuration of COMMAND_APPROVALS stream

3. Message Publishing and Consumption
   - Publishing to audit events stream
   - Publishing to command approvals stream
   - Message consumption from both streams
   - Message acknowledgment

## Prerequisites

- Python 3.7 or higher
- Running NATS server (configured as per `/services/nats/config/nats.conf`)
- Required Python packages (see `requirements.txt`)

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Ensure NATS server is running:
   ```bash
   docker-compose -f ../nats-compose.yml ps
   ```

## Running Tests

Execute the test script:
```bash
python test_nats_setup.py
```

### Expected Output

Successful test execution will show:
```
Starting NATS Setup Tests...
✓ Connected to NATS server
✓ JetStream context acquired
✓ Stream 'AUDIT_EVENTS' exists and is properly configured
✓ Stream 'COMMAND_APPROVALS' exists and is properly configured
✓ Published message to audit.test, sequence: 1
✓ Successfully received message from audit.test
✓ Published message to command.approval.test, sequence: 1
✓ Successfully received message from command.approval.test
✓ Connection closed
```

## Troubleshooting

1. Connection Issues
   - Verify NATS server is running
   - Check if ports 4222 and 8222 are accessible
   - Ensure no firewall rules are blocking connections

2. Stream Configuration Issues
   - Verify nats.conf contains correct stream definitions
   - Check NATS server logs for configuration errors

3. Message Publishing/Consumption Issues
   - Verify JetStream is enabled and properly configured
   - Check available storage space for message persistence
   - Verify stream subjects match the test configuration