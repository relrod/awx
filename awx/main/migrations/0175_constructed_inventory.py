# Generated by Django 3.2.16 on 2022-12-07 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0174_ensure_org_ee_admin_roles'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventory',
            name='source_inventories',
            field=models.ManyToManyField(
                blank=True,
                help_text='Only valid for constructed inventories, this links to the inventories that will be used.',
                related_name='destination_inventories',
                to='main.Inventory',
            ),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='kind',
            field=models.CharField(
                blank=True,
                choices=[
                    ('', 'Hosts have a direct link to this inventory.'),
                    ('smart', 'Hosts for inventory generated using the host_filter property.'),
                    ('constructed', 'Parse list of source inventories with the constructed inventory plugin.'),
                ],
                default='',
                help_text='Kind of inventory being represented.',
                max_length=32,
            ),
        ),
        migrations.AlterField(
            model_name='inventorysource',
            name='source',
            field=models.CharField(
                choices=[
                    ('file', 'File, Directory or Script'),
                    ('constructed', 'Template additional groups and hostvars at runtime'),
                    ('scm', 'Sourced from a Project'),
                    ('ec2', 'Amazon EC2'),
                    ('gce', 'Google Compute Engine'),
                    ('azure_rm', 'Microsoft Azure Resource Manager'),
                    ('vmware', 'VMware vCenter'),
                    ('satellite6', 'Red Hat Satellite 6'),
                    ('openstack', 'OpenStack'),
                    ('rhv', 'Red Hat Virtualization'),
                    ('controller', 'Red Hat Ansible Automation Platform'),
                    ('insights', 'Red Hat Insights'),
                ],
                default=None,
                max_length=32,
            ),
        ),
        migrations.AlterField(
            model_name='inventoryupdate',
            name='source',
            field=models.CharField(
                choices=[
                    ('file', 'File, Directory or Script'),
                    ('constructed', 'Template additional groups and hostvars at runtime'),
                    ('scm', 'Sourced from a Project'),
                    ('ec2', 'Amazon EC2'),
                    ('gce', 'Google Compute Engine'),
                    ('azure_rm', 'Microsoft Azure Resource Manager'),
                    ('vmware', 'VMware vCenter'),
                    ('satellite6', 'Red Hat Satellite 6'),
                    ('openstack', 'OpenStack'),
                    ('rhv', 'Red Hat Virtualization'),
                    ('controller', 'Red Hat Ansible Automation Platform'),
                    ('insights', 'Red Hat Insights'),
                ],
                default=None,
                max_length=32,
            ),
        ),
    ]
