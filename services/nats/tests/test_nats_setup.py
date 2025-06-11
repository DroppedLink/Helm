#!/usr/bin/env python3

import asyncio
import json
from datetime import datetime
from nats.aio.client import Client as NATS
from nats.js.client import JetStreamContext

async def run_tests():
    # Connect to NATS server
    nc = NATS()
    await nc.connect("nats://localhost:4222")
    print("✓ Connected to NATS server")

    # Get JetStream context
    js = nc.jetstream()
    print("✓ JetStream context acquired")

    # Test 1: Ensure streams exist
    async def ensure_stream_exists(stream_name, subjects):
        try:
            stream = await js.stream_info(stream_name)
            print(f"✓ Stream '{stream_name}' already exists.")
        except Exception as e:
            print(f"Stream '{stream_name}' not found, creating...")
            try:
                await js.add_stream(
                    name=stream_name,
                    subjects=subjects,
                    retention="limits" if stream_name == "AUDIT_EVENTS" else "workqueue",
                    max_age=604800 if stream_name == "AUDIT_EVENTS" else 0, # 7 days in seconds for AUDIT_EVENTS
                    storage="file"
                )
                print(f"✓ Stream '{stream_name}' created successfully.")
            except Exception as create_e:
                print(f"✗ Error creating stream '{stream_name}': {str(create_e)}")
                return False
        return True

    # Streams from STREAMS.md
    streams_to_create = {
        "AGENT_SPAWN": ["agent.spawn.>"],
        "AGENT_STATUS": ["agent.status.>"],
        "AGENT_TASK_CREATED": ["agent.task.created.>"],
        "AGENT_TASK_COMPLETED": ["agent.task.completed.>"],
        "AGENT_TASK_FAILED": ["agent.task.failed.>"],
        "AGENT_PROMPT_INPUT": ["agent.prompt.input.>"],
        "AGENT_PROMPT_OUTPUT": ["agent.prompt.output.>"],
        "INFRA_PROXMOX_STATUS": ["infra.proxmox.status.>"],
        "INFRA_PROXMOX_NEW_VM": ["infra.proxmox.new_vm.>"],
        "INFRA_ESXI_STATUS": ["infra.esxi.status.>"],
        "INFRA_VM_CREATED": ["infra.vm.created.>"],
        "INFRA_VM_DELETED": ["infra.vm.deleted.>"],
        "INFRA_VM_METRICS": ["infra.vm.metrics.>"],
        "MONITOR_ZABBIX_ALERT": ["monitor.zabbix.alert.>"],
        "MONITOR_ZABBIX_STATUS": ["monitor.zabbix.status.>"],
        "MONITOR_CHECKMK_ALERT": ["monitor.checkmk.alert.>"],
        "MONITOR_HEALTHCHECK_RESULT": ["monitor.healthcheck.result.>"],
        "MONITOR_DISKSPACE_WARN": ["monitor.diskspace.warn.>"],
        "MONITOR_UPTIME_STATUS": ["monitor.uptime.status.>"],
        "SECURITY_LOGIN_SUCCESS": ["security.login.success.>"],
        "SECURITY_LOGIN_FAILED": ["security.login.failed.>"],
        "SECURITY_PATCH_STATUS": ["security.patch.status.>"],
        "SECURITY_VULN_DETECTED": ["security.vuln.detected.>"],
        "SECURITY_AUDIT_RESULT": ["security.audit.result.>"],
        "SECURITY_OS_MISMATCH": ["security.os.mismatch.>"],
        "INVENTORY_SERVER_ADDED": ["inventory.server.added.>"],
        "INVENTORY_SERVER_UPDATED": ["inventory.server.updated.>"],
        "INVENTORY_SERVER_DELETED": ["inventory.server.deleted.>"],
        "INVENTORY_QUERY_REQUEST": ["inventory.query.request.>"],
        "INVENTORY_QUERY_RESPONSE": ["inventory.query.response.>"],
        "MSG_USER_CHAT": ["msg.user.chat.>"],
        "MSG_AGENT_LOG": ["msg.agent.log.>"],
        "MSG_AGENT_NOTIFY": ["msg.agent.notify.>"],
        "MSG_SYSTEM_BROADCAST": ["msg.system.broadcast.>"],
        "MSG_SMTP_SENT": ["msg.smtp.sent.>"],
        "MSG_SMTP_FAILED": ["msg.smtp.failed.>"],
        "BACKUP_STATUS": ["backup.status.>"],
        "BACKUP_FAILED": ["backup.failed.>"],
        "STORAGE_USAGE_WARNING": ["storage.usage.warning.>"],
        "STORAGE_MOUNT_ERROR": ["storage.mount.error.>"],
        "TOOL_SCAN_STARTED": ["tool.scan.started.>"],
        "TOOL_SCAN_FINISHED": ["tool.scan.finished.>"],
        "TOOL_DIAGNOSTIC_OUTPUT": ["tool.diagnostic.output.>"],
        "TOOL_EXECUTION_ERROR": ["tool.execution.error.>"],
        "USER_LOGIN": ["user.login.>"],
        "USER_LOGOUT": ["user.logout.>"],
        "USER_REGISTERED": ["user.registered.>"],
        "USER_ROLE_ASSIGNED": ["user.role.assigned.>"],
        "USER_PREFERENCES_UPDATED": ["user.preferences.updated.>"],
        # Original streams
        "AUDIT_EVENTS": ["audit.>"],
        "COMMAND_APPROVALS": ["command.approval.>"]
    }

    for stream_name, subjects in streams_to_create.items():
        # AUDIT_EVENTS has specific retention and max_age settings
        if stream_name == "AUDIT_EVENTS":
            await ensure_stream_exists(stream_name, subjects)
        else:
            # Default for other streams (including COMMAND_APPROVALS and new ones)
            await ensure_stream_exists(stream_name, subjects)

    # Test 2: Publish and consume test messages

    # Test 2: Publish and consume test messages
    async def test_pub_sub(stream, subject):
        # Create a test message
        test_msg = {
            "timestamp": datetime.now().isoformat(),
            "test_id": "test-message-1",
            "content": f"Test message for {stream}"
        }

        # Publish message
        ack = await js.publish(subject, json.dumps(test_msg).encode())
        print(f"✓ Published message to {subject}, sequence: {ack.seq}")

        # Subscribe and verify
        sub = await js.pull_subscribe(subject, "test-consumer")
        msgs = await sub.fetch(1, timeout=1)
        if msgs:
            msg = msgs[0]
            received_data = json.loads(msg.data.decode())
            if received_data["test_id"] == "test-message-1":
                print(f"✓ Successfully received message from {subject}")
            await msg.ack()
        else:
            print(f"✗ Failed to receive message from {subject}")

    # Test audit events stream
    await test_pub_sub("AUDIT_EVENTS", "audit.test")
    # Test command approvals stream
    await test_pub_sub("COMMAND_APPROVALS", "command.approval.test")

    # Cleanup
    await nc.close()
    print("✓ Connection closed")

if __name__ == "__main__":
    print("Starting NATS Setup Tests...")
    asyncio.run(run_tests())