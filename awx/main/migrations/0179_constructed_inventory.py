# Generated by Django 3.2.16 on 2022-12-07 14:20

import awx.main.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('main', '0178_instance_group_admin_migration'),
    ]

    operations = [
        migrations.CreateModel(
            name='InventoryConstructedInventoryMembership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.PositiveIntegerField(db_index=True, default=None, null=True)),
                (
                    'constructed_inventory',
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.inventory', related_name='constructed_inventory_memberships'),
                ),
                ('input_inventory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.inventory')),
            ],
        ),
        migrations.AddField(
            model_name='inventory',
            name='input_inventories',
            field=awx.main.fields.OrderedManyToManyField(
                blank=True,
                through_fields=('constructed_inventory', 'input_inventory'),
                help_text='Only valid for constructed inventories, this links to the inventories that will be used.',
                related_name='destination_inventories',
                through='main.InventoryConstructedInventoryMembership',
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
        migrations.AddField(
            model_name='inventorysource',
            name='limit',
            field=models.TextField(blank=True, default='', help_text='Enter host, group or pattern match'),
        ),
        migrations.AddField(
            model_name='inventoryupdate',
            name='limit',
            field=models.TextField(blank=True, default='', help_text='Enter host, group or pattern match'),
        ),
        migrations.AlterField(
            model_name='inventorysource',
            name='host_filter',
            field=models.TextField(
                blank=True,
                default='',
                help_text='This field is deprecated and will be removed in a future release. Regex where only matching hosts will be imported.',
            ),
        ),
        migrations.AlterField(
            model_name='inventoryupdate',
            name='host_filter',
            field=models.TextField(
                blank=True,
                default='',
                help_text='This field is deprecated and will be removed in a future release. Regex where only matching hosts will be imported.',
            ),
        ),
        migrations.AddField(
            model_name='jobhostsummary',
            name='constructed_host',
            field=models.ForeignKey(
                default=None,
                editable=False,
                help_text='Only for jobs run against constructed inventories, this links to the host inside the constructed inventory.',
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='constructed_host_summaries',
                to='main.host',
            ),
        ),
    ]
