Message Bus Channel Structure

A structured starting list of message bus channels grouped by function, designed for HELM or similar modular agent-based platforms.

🧠 Core AI Agent / Task Coordination

agent.spawn

agent.status

agent.task.created

agent.task.completed

agent.task.failed

agent.prompt.input

agent.prompt.output

📦 Infrastructure Management

infra.proxmox.status

infra.proxmox.new_vm

infra.esxi.status

infra.vm.created

infra.vm.deleted

infra.vm.metrics

📊 Monitoring and Alerts

monitor.zabbix.alert

monitor.zabbix.status

monitor.checkmk.alert

monitor.healthcheck.result

monitor.diskspace.warn

monitor.uptime.status

🛡 Security and Compliance

security.login.success

security.login.failed

security.patch.status

security.vuln.detected

security.audit.result

security.os.mismatch

📁 Data and Inventory

inventory.server.added

inventory.server.updated

inventory.server.deleted

inventory.query.request

inventory.query.response

📮 Messaging and Comms

msg.user.chat

msg.agent.log

msg.agent.notify

msg.system.broadcast

msg.smtp.sent

msg.smtp.failed

💾 Storage and Backup

backup.status

backup.failed

storage.usage.warning

storage.mount.error

🧪 Tools and Tests

tool.scan.started

tool.scan.finished

tool.diagnostic.output

tool.execution.error

🧱 User Management

user.login

user.logout

user.registered

user.role.assigned

user.preferences.updated

