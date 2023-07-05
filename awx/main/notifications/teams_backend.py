import logging
import requests

from django.utils.encoding import smart_str
from django.utils.translation import gettext_lazy as _

from awx.main.notifications.base import AWXBaseEmailBackend
from awx.main.notifications.custom_notification_base import CustomNotificationBase
from awx.main.utils.licensing import server_product_name

logger = logging.getLogger('awx.main.notifications.teams_backend')


def teams_payload(color, event_type, title, subtitle, facts):
    url = '{{ url }}' if event_type == 'job' else '{{ workflow_url }}'
    return {
        "@type": "MessageCard",
        "@context": "https://schema.org/extensions",
        "themeColor": color,
        "summary": title,
        "sections": [
            {
                "activityTitle": title,
                "activitySubtitle": subtitle,
                "facts": [{"name": k, "value": v} for k, v in facts.items()],
                "potentialAction": [
                    {
                        "@type": "OpenUri",
                        "name": _("View in %(product_name)s") % {'product_name': server_product_name()},
                        "targets": [{"os": "default", "uri": url}],
                    }
                ],
            }
        ],
    }


class TeamsBackend(AWXBaseEmailBackend, CustomNotificationBase):
    init_parameters = {"teams_url": {"label": "Target URL", "type": "string"}, "teams_no_verify_ssl": {"label": "Verify SSL", "type": "bool"}}
    recipient_parameter = "teams_url"
    sender_parameter = None

    JOB_TITLE = "{{ job_friendly_name }} #{{ job.id }} '{{ job.name }}' {{ job.status }}"
    WORKFLOW_TITLE = 'Approval node "{{ approval_node_name }}" {}'
    default_messages = {
        "started": {
            "body": teams_payload(
                color='0076D7',
                event_type='job',
                title=JOB_TITLE,
                subtitle='{{ job.name }}',
                facts={
                    "Created By": "{{ job_metadata.created_by }}",
                    "Started": "{{ job.started }}",
                },
            )
        },
        "success": {
            "body": teams_payload(
                color='00D776',
                event_type='job',
                title=JOB_TITLE,
                subtitle='{{ job.name }}',
                facts={
                    "Created By": "{{ job_metadata.created_by }}",
                    "Started": "{{ job.started }}",
                    "Finished": "{{ job.finished }}",
                    "Status": "{{ job.status }}",
                },
            )
        },
        "error": {
            "body": teams_payload(
                color='D70076',
                event_type='job',
                title=JOB_TITLE,
                subtitle='{{ job.name }}',
                facts={
                    "Created By": "{{ job_metadata.created_by }}",
                    "Started": "{{ job.started }}",
                    "Finished": "{{ job.finished }}",
                    "Status": "{{ job.status }}",
                },
            )
        },
        "workflow_approval": {
            "running": {
                "body": teams_payload(
                    color='0076D7',
                    event_type='workflow',
                    title=WORKFLOW_TITLE.format('needs review'),
                    subtitle='{{ approval_node_name }}',
                    facts={
                        "Created By": "{{ job_metadata.created_by }}",
                        "Started": "{{ job.started }}",
                        "Status": "{{ job.status }}",
                    },
                )
            },
            "approved": {
                "body": teams_payload(
                    color='00D776',
                    event_type='workflow',
                    title=WORKFLOW_TITLE.format('was approved'),
                    subtitle='{{ approval_node_name }}',
                    facts={
                        "Created By": "{{ job_metadata.created_by }}",
                        "Started": "{{ job.started }}",
                        "Finished": "{{ job.finished }}",
                        "Status": "{{ job.status }}",
                    },
                )
            },
            "denied": {
                "body": teams_payload(
                    color='D70076',
                    event_type='workflow',
                    title=WORKFLOW_TITLE.format('was denied'),
                    subtitle='{{ approval_node_name }}',
                    facts={
                        "Created By": "{{ job_metadata.created_by }}",
                        "Started": "{{ job.started }}",
                        "Finished": "{{ job.finished }}",
                        "Status": "{{ job.status }}",
                    },
                )
            },
            "timed_out": {
                "body": teams_payload(
                    color='D70076',
                    event_type='workflow',
                    title=WORKFLOW_TITLE.format('has timed out'),
                    subtitle='{{ approval_node_name }}',
                    facts={
                        "Created By": "{{ job_metadata.created_by }}",
                        "Started": "{{ job.started }}",
                        "Finished": "{{ job.finished }}",
                        "Status": "{{ job.status }}",
                    },
                )
            },
        },
    }

    def __init__(self, teams_no_verify_ssl=False, fail_silently=False, **kwargs):
        super(TeamsBackend, self).__init__(fail_silently=fail_silently)
        self.teams_no_verify_ssl = teams_no_verify_ssl

    def format_body(self, body):
        return body

    def send_messages(self, messages):
        sent_messages = 0
        for m in messages:
            r = requests.post("{}".format(m.recipients()[0]), json=m.body, verify=(not self.teams_no_verify_ssl))
            if r.status_code >= 400:
                logger.error(smart_str(_("Error sending notification teams: {}").format(r.status_code)))
                if not self.fail_silently:
                    raise Exception(smart_str(_("Error sending notification teams: {}").format(r.status_code)))
            sent_messages += 1
        return sent_messages
