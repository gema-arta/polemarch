from ._base import BaseTestCase
from ... import __version__
import re


class OApiTestCase(BaseTestCase):

    re_path = re.compile(r"(?<={).+?(?=})")

    def test_openapi_schema(self):
        api_version = self._settings('VST_API_VERSION')
        api_path = self._settings('API_URL')
        schema = self.get_result('get', '/api/openapi/?format=openapi')

        # Test base info
        self.assertEqual(schema.get('swagger', None), '2.0')
        self.assertEqual(schema['info']['title'], 'Polemarch')
        self.assertEqual(schema['info']['x-versions']['application'], __version__)
        self.assertEqual(schema['info']['version'], api_version)
        self.assertEqual(schema['basePath'], '/{}/{}'.format(api_path, api_version))

        definitions = schema['definitions']
        id_value = dict(type='integer', readOnly=True)
        name_value = dict(type='string', maxLength=512, minLength=1)
        notes_value = dict(type='string', format='textarea')
        # Test definitions
        group = definitions['Group']
        objName = 'Group'

        self.check_fields(objName, group['properties']['id'], **id_value)

        self.check_fields(objName, group['properties']['name'], **name_value)

        self.check_fields(
            objName, group['properties']['children'], type='boolean', readOnly=True
        )
        del group

        error = definitions['Error']
        objName = 'Error'

        self.check_fields(objName, error['required'], 'detail')
        self.check_fields(
            objName, error['properties']['detail'], **dict(type='string', minLength=1)
        )
        del error

        user = definitions['User']
        objName = 'User'

        self.check_fields(objName, user['required'], 'username')
        self.check_fields(objName, user['properties']['id'], **id_value)
        self.check_fields(
            objName, user['properties']['username'], type='string', pattern='^[\w.@+-]+$',
            maxLength=150, minLength=1, description=True
        )
        self.check_fields(
            objName, user['properties']['is_active'], type='boolean', default=True
        )
        del user

        groupCreateMaster = definitions['GroupCreateMaster']
        objName = 'GroupCreateMaster'
        ref = '#/definitions/User'

        self.check_fields(objName, groupCreateMaster['properties']['id'], **id_value)
        self.check_fields(objName, groupCreateMaster['properties']['name'], **name_value)
        self.check_fields(
            objName, groupCreateMaster['properties']['notes'], **notes_value
        )
        self.check_fields(
            objName, groupCreateMaster['properties']['children'],
            type='boolean', default=False
        )
        self.check_fields(
            objName, groupCreateMaster['properties']['owner'], **{'$ref': ref}
        )
        self.check_ref(schema, ref)
        del groupCreateMaster

        oneGroup = definitions['OneGroup']
        objName = 'OneGroup'

        self.check_fields(objName, oneGroup['properties']['id'], **id_value)
        self.check_fields(objName, oneGroup['properties']['name'], **name_value)
        self.check_fields(objName, oneGroup['properties']['notes'], **notes_value)
        self.check_fields(
            objName, oneGroup['properties']['children'], type='boolean', readOnly=True
        )
        self.check_fields(objName, oneGroup['properties']['owner'], **{'$ref': ref})
        self.check_ref(schema, ref)
        del oneGroup

        setOwner = definitions['SetOwner']
        objName = 'SetOwner'

        self.check_fields(objName, setOwner['required'], 'user_id')
        self.check_fields(
            objName, setOwner['properties']['user_id'],
            type='integer', format='select2',
            additionalProperties=dict(
                value_field='id', view_field='username', model={'$ref': ref}
            )
        )
        del setOwner

        inventoryVariable = definitions['InventoryVariable']
        objName = 'InventoryVariable'
        enum = [
            'ansible_host', 'ansible_port', 'ansible_user', 'ansible_connection',
            'ansible_ssh_pass', 'ansible_ssh_private_key_file', 'ansible_ssh_common_args',
            'ansible_sftp_extra_args', 'ansible_scp_extra_args', 'ansible_ssh_extra_args',
            'ansible_ssh_executable', 'ansible_ssh_pipelining', 'ansible_become',
            'ansible_become_method', 'ansible_become_user', 'ansible_become_pass',
            'ansible_become_exe', 'ansible_become_flags', 'ansible_shell_type',
            'ansible_python_interpreter', 'ansible_ruby_interpreter',
            'ansible_perl_interpreter', 'ansible_shell_executable'
        ]

        self.check_fields(objName, inventoryVariable['required'], 'key')
        self.check_fields(objName, inventoryVariable['properties']['id'], **id_value)
        self.check_fields(
            objName, inventoryVariable['properties']['value'], type='string', default=''
        )
        self.check_fields(
            objName, inventoryVariable['properties']['key'],
            type='string', format='autocomplete', enum=enum
        )
        del inventoryVariable

        host = definitions['Host']
        objName = 'Host'

        self.check_fields(objName, host['properties']['id'], **id_value)
        self.check_fields(objName, host['properties']['name'], **name_value)
        self.check_fields(
            objName, host['properties']['type'],
            type='string', default='HOST', enum=['HOST', 'RANGE']
        )
        del host

        oneHost = definitions['OneHost']
        objName = 'OneHost'

        self.check_fields(objName, oneHost['properties']['id'], **id_value)
        self.check_fields(objName, oneHost['properties']['name'], **name_value)
        self.check_fields(objName, oneHost['properties']['notes'], **notes_value)
        self.check_fields(
            objName, oneHost['properties']['type'],
            type='string', default='HOST', enum=['HOST', 'RANGE']
        )
        self.check_fields(objName, oneHost['properties']['owner'], **{'$ref': ref})
        self.check_ref(schema, ref)
        del oneHost

        history = definitions['History']
        objName = 'History'

        self.check_fields(objName, history['required'], 'status', 'mode')
        self.check_fields(objName, history['properties']['id'], **id_value)
        self.check_fields(
            objName, history['properties']['status'],
            type='string', maxLength=50, minLength=1
        )
        self.check_fields(objName, history['properties']['executor'], type='integer')
        self.check_fields(objName, history['properties']['project'], type='integer')
        self.check_fields(
            objName, history['properties']['kind'],
            type='string', maxLength=50, minLength=1
        )
        self.check_fields(
            objName, history['properties']['mode'],
            type='string', maxLength=256, minLength=1
        )
        self.check_fields(objName, history['properties']['inventory'], type='integer')
        self.check_fields(
            objName, history['properties']['start_time'],
            type='string', format='date-time'
        )
        self.check_fields(
            objName, history['properties']['stop_time'], type='string', format='date-time'
        )
        self.check_fields(objName, history['properties']['initiator'], type='integer')
        self.check_fields(
            objName, history['properties']['initiator_type'],
            type='string', maxLength=50, minLength=1
        )
        self.check_fields(
            objName, history['properties']['options'], type='string', readOnly=True
        )

        oneHistory = definitions['OneHistory']
        objName = 'OneHistory'

        self.check_fields(
            objName, oneHistory['required'], 'status', 'mode', 'execution_time'
        )
        self.check_fields(objName, oneHistory['properties']['id'], **id_value)
        self.check_fields(
            objName, oneHistory['properties']['status'],
            type='string', maxLength=50, minLength=1
        )
        self.check_fields(objName, oneHistory['properties']['executor'], type='integer')
        self.check_fields(objName, oneHistory['properties']['project'], type='integer')
        self.check_fields(
            objName, oneHistory['properties']['revision'], type='string', maxLength=256
        )
        self.check_fields(objName, oneHistory['properties']['inventory'], type='integer')
        self.check_fields(
            objName, oneHistory['properties']['kind'],
            type='string', maxLength=50, minLength=1
        )
        self.check_fields(
            objName, oneHistory['properties']['mode'],
            type='string', maxLength=256, minLength=1
        )
        self.check_fields(
            objName, oneHistory['properties']['execute_args'],
            type='string', readOnly=True
        )
        self.check_fields(
            objName, oneHistory['properties']['execution_time'],
            type='integer', format='uptime'
        )
        self.check_fields(
            objName, oneHistory['properties']['start_time'],
            type='string', format='date-time'
        )
        self.check_fields(
            objName, oneHistory['properties']['stop_time'],
            type='string', format='date-time'
        )
        self.check_fields(objName, oneHistory['properties']['initiator'], type='integer')
        self.check_fields(
            objName, oneHistory['properties']['initiator_type'],
            type='string', maxLength=50, minLength=1
        )
        self.check_fields(
            objName, oneHistory['properties']['options'], type='string', readOnly=True
        )
        self.check_fields(
            objName, oneHistory['properties']['raw_args'], type='string', minLength=1
         )
        self.check_fields(
            objName, oneHistory['properties']['raw_stdout'], type='string', readOnly=True
        )
        self.check_fields(
            objName, oneHistory['properties']['raw_inventory'], type='string', minLength=1
        )
        del oneHistory

        empty = definitions['Empty']
        self.assertTrue(not empty['properties'])
        del empty

        actionResponse = definitions['ActionResponse']
        objName = 'ActionResponse'

        self.check_fields(objName, actionResponse['required'], 'detail')
        self.check_fields(
            objName, actionResponse['properties']['detail'], type='string', minLength=1
        )
        del actionResponse

        data = definitions['Data']
        self.assertTrue(not data['properties'])
        del data

        hook = definitions['Hook']
        objName = 'Hook'
        enum = [
            'on_execution', 'after_execution', 'on_user_add', 'on_user_upd',
            'on_user_del', 'on_object_add', 'on_object_upd', 'on_object_del'
            ]

        self.check_fields(objName, hook['required'], 'type', 'recipients')
        self.check_fields(objName, hook['properties']['id'], **id_value)
        self.check_fields(objName, hook['properties']['name'], **name_value)
        self.check_fields(
            objName, hook['properties']['type'], type='string', enum=['HTTP', 'SCRIPT']
        )
        self.check_fields(objName, hook['properties']['when'], type='string', enum=enum)
        self.check_fields(objName, hook['properties']['enable'], type='boolean')
        self.check_fields(
            objName, hook['properties']['recipients'],
            type='string', maxLength=16383, minLength=1
        )
        del hook

        inventory = definitions['Inventory']
        objName = 'Inventory'

        self.check_fields(objName, inventory['properties']['id'], **id_value)
        self.check_fields(objName, inventory['properties']['name'], **name_value)
        del inventory

        oneInventory = definitions['OneInventory']
        objName = 'OneInventory'

        self.check_fields(objName, oneInventory['properties']['id'], **id_value)
        self.check_fields(objName, oneInventory['properties']['name'], **name_value)
        self.check_fields(objName, oneInventory['properties']['notes'], **notes_value)
        self.check_fields(objName, oneInventory['properties']['owner'], **{'$ref': ref})
        self.check_ref(schema, ref)
        del oneInventory

        project = definitions['Project']
        objName = 'Project'

        self.check_fields(objName, project['properties']['id'], **id_value)
        self.check_fields(objName, project['properties']['name'], **name_value)
        self.check_fields(
            objName, project['properties']['type'],
            type='string', readOnly=True, minLength=1
        )
        self.check_fields(
            objName, project['properties']['status'],
            type='string', readOnly=True, minLength=1
        )
        del project

        projectCreateMaster = definitions['ProjectCreateMaster']
        objName = 'ProjectCreateMaster'

        self.check_fields(objName, projectCreateMaster['required'], 'name')
        self.check_fields(objName, projectCreateMaster['properties']['id'], **id_value)
        self.check_fields(
            objName, projectCreateMaster['properties']['name'], **name_value
        )
        self.check_fields(
            objName, projectCreateMaster['properties']['status'],
            type='string', readOnly=True, minLength=1
        )
        self.check_fields(
            objName, projectCreateMaster['properties']['type'],
            type='string', default='MANUAL', enum=['MANUAL', 'GIT', 'TAR']
        )
        self.check_fields(
            objName, projectCreateMaster['properties']['repository'],
            type='string', default='MANUAL', minLength=1
        )
        self.check_fields(
            objName, projectCreateMaster['properties']['repo_auth'],
            type='string', default='NONE', enum=['NONE', 'KEY', 'PASSWORD']

        )
        additional_properties = dict(
            field='repo_auth', choices={},
            types=dict(KEY='secretfile', PASSWORD='password', NONE='disabled')
        )

        self.check_fields(
            objName, projectCreateMaster['properties']['auth_data'],
            type='string', format='dynamic', default='',
            additionalProperties=additional_properties
        )
        del projectCreateMaster

        oneProject = definitions['OneProject']
        objName = 'OneProject'

        self.check_fields(objName, oneProject['properties']['id'], **id_value)
        self.check_fields(objName, oneProject['properties']['name'], **name_value)
        self.check_fields(
            objName, oneProject['properties']['repository'],
            type='string', default='MANUAL', minLength=1
        )
        self.check_fields(
            objName, oneProject['properties']['status'],
            type='string', readOnly=True, minLength=1
        )
        self.check_fields(
            objName, oneProject['properties']['revision'],
            type='string', readOnly=True
        )
        self.check_fields(
            objName, oneProject['properties']['branch'],
            type='string', readOnly=True
        )
        self.check_fields(objName, oneProject['properties']['owner'], **{'$ref': ref})
        self.check_ref(schema, ref)
        self.check_fields(objName, oneProject['properties']['notes'], **notes_value)
        self.check_fields(
            objName, oneProject['properties']['readme_content'],
            type='string', format='html', readOnly=True
        )
        del oneProject

        ansibleModule = definitions['AnsibleModule']
        objName = 'AnsibleModule'
        ref = '#/definitions/Module'
        additional_properties = dict(
            value_field='name', view_field='path', model={'$ref': ref}
        )

        self.check_fields(objName, ansibleModule['required'], 'module')
        self.check_fields(
            objName, ansibleModule['properties']['module'],
            type='string', format='autocomplete',
            additionalProperties=additional_properties
        )
        self.check_fields(
            objName, ansibleModule['properties']['args'],
            type='string', description=True
        )
        self.check_fields(
            objName, ansibleModule['properties']['background'],
            type='integer', description=True
        )
        self.check_fields(
            objName, ansibleModule['properties']['become'],
            type='boolean', description=True, default=False
        )
        self.check_fields(
            objName, ansibleModule['properties']['become_method'],
            type='string', description=True
        )
        self.check_fields(
            objName, ansibleModule['properties']['become_user'],
            type='string', description=True
        )
        self.check_fields(
            objName, ansibleModule['properties']['check'],
            type='boolean', description=True, default=False
        )
        self.check_fields(
            objName, ansibleModule['properties']['connection'],
            type='string', description=True
        )
        self.check_fields(
            objName, ansibleModule['properties']['diff'],
            type='boolean', description=True, default=False
        )
        self.check_fields(
            objName, ansibleModule['properties']['extra_vars'],
            type='string', description=True
        )
        self.check_fields(
            objName, ansibleModule['properties']['forks'],
            type='integer', description=True
        )

        ref = '#/definitions/Inventory'
        additional_properties = dict(
            value_field='id', view_field='name', model={'$ref': ref}
        )

        self.check_fields(
            objName, ansibleModule['properties']['inventory'],
            type='string',
            format='autocomplete',
            description=True,
            additionalProperties=additional_properties
        )
        self.check_fields(
            objName, ansibleModule['properties']['key_file'],
            type='string', format='secretfile', description=True
        )
        self.check_fields(
            objName, ansibleModule['properties']['limit'],
            type='string', description=True
        )
        self.check_fields(
            objName, ansibleModule['properties']['list_hosts'],
            type='boolean', default=False, description=True
        )
        self.check_fields(
            objName, ansibleModule['properties']['module_path'],
            type='string', description=True
        )
        self.check_fields(
            objName, ansibleModule['properties']['one_line'],
            type='boolean', default=False, description=True
        )
        self.check_fields(
            objName, ansibleModule['properties']['playbook_dir'],
            type='string', description=True
        )
        self.check_fields(
            objName, ansibleModule['properties']['poll'],
            type='integer', description=True
        )
        self.check_fields(
            objName, ansibleModule['properties']['private_key'],
            type='string', format='secretfile', description=True
        )
        self.check_fields(
            objName, ansibleModule['properties']['scp_extra_args'],
            type='string', description=True
        )
        self.check_fields(
            objName, ansibleModule['properties']['sftp_extra_args'],
            type='string', description=True
        )
        self.check_fields(
            objName, ansibleModule['properties']['ssh_common_args'],
            type='string', description=True
        )
        self.check_fields(
            objName, ansibleModule['properties']['ssh_extra_args'],
            type='string', description=True
        )
        self.check_fields(
            objName, ansibleModule['properties']['su'],
            type='boolean', default=False, description=True
        )
        self.check_fields(
            objName, ansibleModule['properties']['su_user'],
            type='string', description=True
        )
        self.check_fields(
            objName, ansibleModule['properties']['sudo'],
            type='boolean', default=False, description=True
        )
        self.check_fields(
            objName, ansibleModule['properties']['sudo_user'],
            type='string', description=True
        )
        self.check_fields(
            objName, ansibleModule['properties']['syntax_check'],
            type='boolean', default=False, description=True
        )
        self.check_fields(
            objName, ansibleModule['properties']['timeout'],
            type='integer', description=True
        )
        self.check_fields(
            objName, ansibleModule['properties']['tree'], type='string', description=True
        )
        self.check_fields(
            objName, ansibleModule['properties']['user'], type='string', description=True
        )
        self.check_fields(
            objName, ansibleModule['properties']['vault_id'],
            type='string', description=True
        )
        self.check_fields(
            objName, ansibleModule['properties']['vault_password_file'],
            type='string', format='secretfile', description=True
        )
        self.check_fields(
            objName, ansibleModule['properties']['verbose'],
            type='integer', default=0, maximum=4, description=True
        )
        self.check_fields(
            objName, ansibleModule['properties']['group'], type='string', default='all'
        )
        del ansibleModule

        executeResponse = definitions['ExecuteResponse']
        objName = 'ExecuteResponse'

        self.check_fields(objName, executeResponse['required'], 'detail')
        self.check_fields(
            objName, executeResponse['properties']['detail'], type='string', minLength=1
        )
        self.check_fields(
            objName, executeResponse['properties']['executor'], type='integer'
        )
        self.check_fields(
            objName, executeResponse['properties']['history_id'],
            type='integer', additionalProperties=dict(redirect=True)
        )
        del executeResponse

        ansiblePlaybook = definitions['AnsiblePlaybook']
        objName = 'AnsiblePlaybook'
        ref = '#/definitions/Playbook'

        self.check_fields(objName, ansiblePlaybook['required'], 'playbook')

        additional_properties = dict(
            value_field='playbook', view_field='name', model={'$ref': ref})

        self.check_fields(
            objName, ansiblePlaybook['properties']['playbook'],
            type='string', format='autocomplete',
            additionalProperties=additional_properties
        )
        self.check_fields(
            objName, ansiblePlaybook['properties']['become'],
            type='boolean', description=True, default=False
        )
        self.check_fields(
            objName, ansiblePlaybook['properties']['become_method'],
            type='string', description=True
        )
        self.check_fields(
            objName, ansiblePlaybook['properties']['become_user'],
            type='string', description=True
        )
        self.check_fields(
            objName, ansiblePlaybook['properties']['check'],
            type='boolean', description=True, default=False
        )
        self.check_fields(
            objName, ansiblePlaybook['properties']['connection'],
            type='string', description=True
        )
        self.check_fields(
            objName, ansiblePlaybook['properties']['diff'],
            type='boolean', description=True, default=False
        )
        self.check_fields(
            objName, ansiblePlaybook['properties']['extra_vars'],
            type='string', description=True
        )
        self.check_fields(
            objName, ansiblePlaybook['properties']['flush_cache'],
            type='boolean', description=True, default=False
        )
        self.check_fields(
            objName, ansiblePlaybook['properties']['force_handlers'],
            type='boolean', description=True, default=False
        )
        self.check_fields(
            objName, ansiblePlaybook['properties']['forks'],
            type='integer', description=True
        )

        ref = '#/definitions/Inventory'
        additional_properties = dict(
            value_field='id', view_field='name', model={'$ref': ref}
        )

        self.check_fields(
            objName, ansiblePlaybook['properties']['inventory'],
            type='string', format='autocomplete', description=True,
            additionalProperties=additional_properties
        )
        self.check_fields(
            objName, ansiblePlaybook['properties']['key_file'],
            type='string', format='secretfile', description=True
        )
        self.check_fields(
            objName, ansiblePlaybook['properties']['limit'],
            type='string', description=True
        )
        self.check_fields(
            objName, ansiblePlaybook['properties']['list_hosts'],
            type='boolean', default=False, description=True
        )
        self.check_fields(
            objName, ansiblePlaybook['properties']['list_tags'],
            type='boolean', default=False, description=True
        )
        self.check_fields(
            objName, ansiblePlaybook['properties']['list_tasks'],
            type='boolean', default=False, description=True
        )
        self.check_fields(
            objName, ansiblePlaybook['properties']['module_path'],
            type='string', description=True
        )
        self.check_fields(
            objName, ansiblePlaybook['properties']['private_key'],
            type='string', format='secretfile', description=True
        )
        self.check_fields(
            objName, ansiblePlaybook['properties']['scp_extra_args'],
            type='string', description=True
        )
        self.check_fields(
            objName, ansiblePlaybook['properties']['sftp_extra_args'],
            type='string', description=True
        )
        self.check_fields(
            objName, ansiblePlaybook['properties']['skip_tags'],
            type='string', description=True
        )
        self.check_fields(
            objName, ansiblePlaybook['properties']['ssh_common_args'],
            type='string', description=True
        )
        self.check_fields(
            objName, ansiblePlaybook['properties']['ssh_extra_args'],
            type='string', description=True
        )
        self.check_fields(
            objName, ansiblePlaybook['properties']['start_at_task'],
            type='string', description=True
        )
        self.check_fields(
            objName, ansiblePlaybook['properties']['step'],
            type='boolean', default=False, description=True
        )
        self.check_fields(
            objName, ansiblePlaybook['properties']['su'],
            type='boolean', default=False, description=True
        )
        self.check_fields(
            objName, ansiblePlaybook['properties']['su_user'],
            type='string', description=True
        )
        self.check_fields(
            objName, ansiblePlaybook['properties']['sudo'],
            type='boolean', default=False, description=True
        )
        self.check_fields(
            objName, ansiblePlaybook['properties']['sudo_user'],
            type='string', description=True
        )
        self.check_fields(
            objName, ansiblePlaybook['properties']['syntax_check'],
            type='boolean', default=False, description=True
        )
        self.check_fields(
            objName, ansiblePlaybook['properties']['tags'],
            type='string', description=True
        )
        self.check_fields(
            objName, ansiblePlaybook['properties']['timeout'],
            type='integer', description=True
        )
        self.check_fields(
            objName, ansiblePlaybook['properties']['user'],
            type='string', description=True
        )
        self.check_fields(
            objName, ansiblePlaybook['properties']['vault_id'],
            type='string', description=True
        )
        self.check_fields(
            objName, ansiblePlaybook['properties']['vault_password_file'],
            type='string', format='secretfile', description=True
        )
        self.check_fields(
            objName, ansiblePlaybook['properties']['verbose'],
            type='integer', default=0, maximum=4, description=True
        )
        del ansiblePlaybook

        projectHistory = definitions['ProjectHistory']
        objName = 'ProjectHistory'

        self.check_fields(objName, projectHistory['required'], 'status', 'mode')
        self.check_fields(objName, projectHistory['properties']['id'], **id_value)
        self.check_fields(
            objName, projectHistory['properties']['status'],
            type='string', minLength=1, maxLength=50
        )
        self.check_fields(
            objName, projectHistory['properties']['revision'],
            type='string', maxLength=256
        )
        self.check_fields(
            objName, projectHistory['properties']['executor'], type='integer'
        )
        self.check_fields(
            objName, projectHistory['properties']['kind'], type='string',
            maxLength=50, minLength=1
        )
        self.check_fields(
            objName, projectHistory['properties']['mode'],
            type='string', maxLength=256, minLength=1
        )
        self.check_fields(
            objName, projectHistory['properties']['inventory'], type='integer'
        )
        self.check_fields(
            objName, projectHistory['properties']['start_time'],
            type='string', format='date-time'
        )
        self.check_fields(
            objName, projectHistory['properties']['stop_time'],
            type='string', format='date-time'
        )
        self.check_fields(
            objName, projectHistory['properties']['initiator'], type='integer'
        )
        self.check_fields(
            objName, projectHistory['properties']['initiator_type'],
            type='string', minLength=1, maxLength=50
        )
        self.check_fields(
            objName, projectHistory['properties']['options'], type='string', readOnly=True
        )
        del projectHistory

        module = definitions['Module']
        objName = 'Module'

        self.check_fields(objName, module['required'], 'path')
        self.check_fields(objName, module['properties']['id'], **id_value)
        self.check_fields(
            objName, module['properties']['path'],
            type='string', minLength=1, maxLength=1024
        )
        self.check_fields(
            objName, module['properties']['name'], type='string', readOnly=True
        )
        del module

        oneModule = definitions['OneModule']
        objName = 'OneModule'
        ref = '#/definitions/Data'

        self.check_fields(objName, oneModule['required'], 'path', 'data')
        self.check_fields(objName, oneModule['properties']['id'], **id_value)
        self.check_fields(
            objName, oneModule['properties']['name'], type='string', readOnly=True
        )
        self.check_fields(
            objName, oneModule['properties']['path'],
            type='string', minLength=1, maxLength=1024
        )
        self.check_fields(objName, oneModule['properties']['data'], **{'$ref': ref})
        del oneModule

        periodicTask = definitions['Periodictask']
        objName = 'Periodictask'

        self.check_fields(objName, periodicTask['required'], 'schedule')
        self.check_fields(objName, periodicTask['properties']['id'], **id_value)
        self.check_fields(objName, periodicTask['properties']['name'], **name_value)
        self.check_fields(
            objName, periodicTask['properties']['type'],
            type='string', default='CRONTAB', enum=['CRONTAB', 'INTERVAL']
        )

        additional_properties = dict(
            field='type', choices={}, types=dict(CRONTAB='crontab', INTERVAL='integer')
        )
        self.check_fields(
            objName, periodicTask['properties']['schedule'],
            type='string', format='dynamic', additionalProperties=additional_properties
        )

        additional_properties = dict(
            field='kind', choices={},
            types=dict(PLAYBOOK='autocomplete', MODULE='autocomplete', TEMPLATE='hidden')
        )
        self.check_fields(
            objName, periodicTask['properties']['mode'],
            type='string', format='dynamic', additionalProperties=additional_properties
        )

        self.check_fields(
            objName, periodicTask['properties']['kind'],
            type='string', default='PLAYBOOK', enum=['PLAYBOOK', 'MODULE', 'TEMPLATE']
        )

        additional_properties = dict(
            field='kind', choices={},
            types=dict(PLAYBOOK='select2', MODULE='select2', TEMPLATE='hidden')
        )
        self.check_fields(
            objName, periodicTask['properties']['inventory'],
            type='string', format='dynamic', additionalProperties=additional_properties
        )

        self.check_fields(
            objName, periodicTask['properties']['save_result'], type='boolean'
        )
        self.check_fields(
            objName, periodicTask['properties']['template'], type='integer'
        )

        additional_properties = dict(
            field='kind', choices={},
            types=dict(PLAYBOOK='hidden', MODULE='hidden', TEMPLATE='autocomplete')
        )
        self.check_fields(
            objName, periodicTask['properties']['template_opt'],
            type='string', format='dynamic', additionalProperties=additional_properties
        )
        self.check_fields(objName, periodicTask['properties']['enabled'], type='boolean')
        del periodicTask

        onePeriodicTask = definitions['OnePeriodictask']
        objName = 'OnePeriodictask'

        self.check_fields(objName, onePeriodicTask['required'], 'schedule')
        self.check_fields(objName, onePeriodicTask['properties']['id'], **id_value)
        self.check_fields(objName, onePeriodicTask['properties']['name'], **name_value)
        self.check_fields(objName, onePeriodicTask['properties']['notes'], **notes_value)
        self.check_fields(
            objName, onePeriodicTask['properties']['type'],
            type='string', default='CRONTAB', enum=['CRONTAB', 'INTERVAL']
        )

        additional_properties = dict(
            field='type', choices={}, types=dict(CRONTAB='crontab', INTERVAL='integer')
        )
        self.check_fields(
            objName, onePeriodicTask['properties']['schedule'],
            type='string', format='dynamic', additionalProperties=additional_properties
        )

        additional_properties = dict(
            field='kind', choices={},
            types=dict(PLAYBOOK='autocomplete', MODULE='autocomplete', TEMPLATE='hidden')
        )
        self.check_fields(
            objName, onePeriodicTask['properties']['mode'],
            type='string', format='dynamic', additionalProperties=additional_properties
        )

        self.check_fields(
            objName, onePeriodicTask['properties']['kind'],
            type='string', default='PLAYBOOK', enum=['PLAYBOOK', 'MODULE', 'TEMPLATE']
        )

        additional_properties = dict(
            field='kind', choices={},
            types=dict(PLAYBOOK='select2', MODULE='select2', TEMPLATE='hidden')
        )
        self.check_fields(
            objName, onePeriodicTask['properties']['inventory'],
            type='string', format='dynamic', additionalProperties=additional_properties
        )
        self.check_fields(
            objName, onePeriodicTask['properties']['save_result'], type='boolean'
        )
        self.check_fields(
            objName, onePeriodicTask['properties']['template'], type='integer'
        )

        additional_properties = dict(
            field='kind', choices={},
            types=dict(PLAYBOOK='hidden', MODULE='hidden', TEMPLATE='autocomplete')
        )
        self.check_fields(
            objName, onePeriodicTask['properties']['template_opt'],
            type='string', format='dynamic', additionalProperties=additional_properties
        )
        self.check_fields(
            objName, onePeriodicTask['properties']['enabled'], type='boolean'
        )
        del onePeriodicTask

        periodicTaskVariable = definitions['PeriodicTaskVariable']
        objName = 'PeriodicTaskVariable'

        self.check_fields(objName, periodicTaskVariable['required'], 'key')
        self.check_fields(objName, periodicTaskVariable['properties']['id'], **id_value)
        self.check_fields(
            objName, periodicTaskVariable['properties']['key'],
            type='string', minLength=1, maxLength=128
        )
        self.check_fields(
            objName, periodicTaskVariable['properties']['value'],
            type='string', default=''
        )
        del periodicTaskVariable

        playbook = definitions['Playbook']
        objName = 'Playbook'

        self.check_fields(objName, playbook['required'], 'playbook')
        self.check_fields(objName, playbook['properties']['id'], **id_value)
        self.check_fields(
            objName, playbook['properties']['name'],
            type='string', maxLength=256, minLength=1
        )
        self.check_fields(
            objName, playbook['properties']['playbook'],
            type='string', minLength=1, maxLength=256
        )
        del playbook

        onePlaybook = definitions['OnePlaybook']
        objName = 'OnePlaybook'

        self.check_fields(objName, onePlaybook['properties']['id'], **id_value)
        self.check_fields(
            objName, onePlaybook['properties']['name'],
            type='string', maxLength=256, minLength=1
        )
        self.check_fields(
            objName, onePlaybook['properties']['playbook'],
            type='string', readOnly=True, minLength=1
        )
        del onePlaybook

        template = definitions['Template']
        objName = 'Template'
        ref = '#/definitions/Data'

        self.check_fields(objName, template['required'], 'name', 'data', 'options')
        self.check_fields(objName, template['properties']['id'], **id_value)
        self.check_fields(objName, template['properties']['name'], **name_value)
        self.check_fields(
            objName, template['properties']['kind'],
            type='string', default='Task', enum=['Task', 'Module']
        )
        self.check_fields(objName, template['properties']['data'], *{'$ref': ref})
        self.check_fields(objName, template['properties']['options'], **{'$ref': ref})
        self.check_fields(
            objName, template['properties']['options_list'],
            type='array', readOnly=True, items=dict(type='string')
        )
        del template

        oneTemplate = definitions['OneTemplate']
        objName = 'OneTemplate'

        self.check_fields(objName, oneTemplate['required'], 'name', 'data')
        self.check_fields(objName, oneTemplate['properties']['id'], **id_value)
        self.check_fields(objName, oneTemplate['properties']['name'], **name_value)
        self.check_fields(objName, oneTemplate['properties']['notes'], **notes_value)
        self.check_fields(
            objName, oneTemplate['properties']['kind'],
            type='string', default='Task', enum=['Task', 'Module']
        )
        self.check_fields(objName, oneTemplate['properties']['data'], **{'$ref': ref})
        self.check_fields(objName, oneTemplate['properties']['options'], **{'$ref': ref})
        self.check_fields(
            objName, oneTemplate['properties']['options_list'],
            type='array', readOnly=True, items=dict(type='string')
        )
        del oneTemplate

        templateExec = definitions['TemplateExec']
        objName = 'TemplateExec'

        self.check_fields(
            objName, templateExec['properties']['option'],
            type='string', minLength=0, description=True
        )
        del templateExec

        projectVariable = definitions['ProjectVariable']
        objName = 'ProjectVariable'

        self.check_fields(objName, projectVariable['required'], 'key', 'value')
        self.check_fields(objName, projectVariable['properties']['id'], **id_value)

        key_list = [
            'repo_type', 'repo_sync_on_run', 'repo_branch',
            'repo_password', 'repo_key'
        ]
        self.check_fields(objName, projectVariable['properties']['key'],
                          type='string', enum=key_list
                          )
        additional_properties = dict(
            field='key',
            types=dict(repo_password='password', repo_key='secretfile'),
            choices=dict(
                repo_type=['MANUAL', 'GIT', 'TAR'],
                repo_sync_on_run=[True, False]
            )
        )

        self.check_fields(
            objName, projectVariable['properties']['value'],
            type='string', format='dynamic', additionalProperties=additional_properties
        )
        del projectVariable

        team = definitions['Team']
        objName = 'Team'

        self.check_fields(objName, team['required'], 'name')
        self.check_fields(objName, team['properties']['id'], **id_value)
        self.check_fields(
            objName, team['properties']['name'], type='string', maxLength=80, minLength=1
        )
        del team

        oneTeam = definitions['OneTeam']
        objName = 'OneTeam'

        self.check_fields(objName, oneTeam['required'], 'name')
        self.check_fields(objName, oneTeam['properties']['id'], **id_value)
        self.check_fields(
            objName, oneTeam['properties']['name'],
            type='string', minLength=1, maxLength=80
        )
        self.check_fields(objName, oneTeam['properties']['notes'], **notes_value)
        ref = '#/definitions/User'
        self.check_fields(objName, oneTeam['properties']['owner'], **{'$ref': ref})
        del oneTeam

        createUser = definitions['CreateUser']
        objName = 'CreateUser'

        self.check_fields(
            objName, createUser['required'], 'username', 'password', 'password2'
        )
        self.check_fields(objName, createUser['properties']['id'], **id_value)
        self.check_fields(
            objName, createUser['properties']['username'],
            description=True, type='string', pattern='^[\w.@+-]+$',
            maxLength=150, minLength=1
        )
        self.check_fields(
            objName, createUser['properties']['is_active'], type='boolean', default=True
        )
        self.check_fields(
            objName, createUser['properties']['first_name'], type='string', maxLength=30
        )
        self.check_fields(
            objName, createUser['properties']['last_name'], type='string', maxLength=30
        )
        self.check_fields(
            objName, createUser['properties']['email'],
            type='string', format='email', minLength=1
        )
        self.check_fields(
            objName, createUser['properties']['password'], type='string', minLength=1
        )
        self.check_fields(
            objName, createUser['properties']['password2'], type='string', minLength=1
        )
        del createUser

        oneUser = definitions['OneUser']
        objName = 'OneUser'

        self.check_fields(objName, oneUser['required'], 'username')
        self.check_fields(objName, oneUser['properties']['id'], **id_value)
        self.check_fields(
            objName, oneUser['properties']['username'],
            type='string',
            description=True,
            maxLength=150,
            minLength=1,
            pattern='^[\w.@+-]+$'
        )
        self.check_fields(
            objName, oneUser['properties']['is_active'], type='boolean', default=True
        )
        self.check_fields(
            objName, oneUser['properties']['first_name'], type='string', maxLength=30
        )
        self.check_fields(
            objName, oneUser['properties']['last_name'], type='string', maxLength=30
        )
        self.check_fields(
            objName, oneUser['properties']['email'],
            type='string', format='email', minLength=1
        )
        del oneUser

        changePassword = definitions['ChangePassword']
        objName = 'ChangePassword'
        self.check_fields(
            objName, changePassword['required'], 'old_password', 'password', 'password2'
        )
        self.check_fields(
            objName, changePassword['properties']['old_password'],
            type='string', minLength=1
        )
        self.check_fields(
            objName, changePassword['properties']['password'],
            type='string', minLength=1
        )
        self.check_fields(
            objName, changePassword['properties']['password2'],
            type='string', minLength=1
        )
        del changePassword

        chartLineSetting = definitions['ChartLineSetting']
        objName = 'ChartLineSetting'

        self.check_fields(
            objName, chartLineSetting['properties']['active'],
            type='boolean', default=True
        )
        del chartLineSetting

        chartLineSettings = definitions['ChartLineSettings']
        objName = 'ChartLineSettings'
        ref = '#/definitions/ChartLineSetting'
        chart_line_list = ['all_tasks', 'delay', 'ok', 'error', 'interrupted', 'offline']

        self.check_fields(objName, chartLineSettings['required'], *chart_line_list)

        self.check_fields(
            objName, chartLineSettings['properties']['all_tasks'], **{'$ref': ref}
        )
        self.check_fields(
            objName, chartLineSettings['properties']['delay'], **{'$ref': ref}
        )
        self.check_fields(
            objName, chartLineSettings['properties']['ok'], **{'$ref': ref}
        )
        self.check_fields(
            objName, chartLineSettings['properties']['error'], **{'$ref': ref}
        )
        self.check_fields(
            objName, chartLineSettings['properties']['interrupted'], **{'$ref': ref}
        )
        self.check_fields(
            objName, chartLineSettings['properties']['offline'], **{'$ref': ref}
        )

        del chartLineSettings

        counterWidgetSetting = definitions['CounterWidgetSetting']
        objName = 'CounterWidgetSetting'

        self.check_fields(
            objName, counterWidgetSetting['properties']['active'],
            type='boolean', default=True
        )
        self.check_fields(
            objName, counterWidgetSetting['properties']['collapse'],
            type='boolean', default=False, readOnly=True
        )
        self.check_fields(
            objName, counterWidgetSetting['properties']['sort'], type='integer', default=0
        )
        del counterWidgetSetting

        widgetSetting = definitions['WidgetSetting']
        objName = 'WidgetSetting'

        self.check_fields(
            objName, widgetSetting['properties']['active'], type='boolean', default=True
        )
        self.check_fields(
            objName, widgetSetting['properties']['collapse'],
            type='boolean', default=False
        )
        self.check_fields(
            objName, widgetSetting['properties']['sort'], type='integer', default=0
        )
        del widgetSetting

        widgetSettings = definitions['WidgetSettings']
        objName = 'WidgetSettings'

        widgetList = ['pmwUsersCounter', 'pmwProjectsCounter', 'pmwInventoriesCounter',
                      'pmwGroupsCounter', 'pmwHostsCounter', 'pmwChartWidget',
                      'pmwAnsibleModuleWidget'
                      ]
        self.check_fields(objName, widgetSettings['required'], *widgetList)
        ref = '#/definitions/CounterWidgetSetting'
        self.check_fields(
            objName, widgetSettings['properties']['pmwUsersCounter'], **{'$ref': ref}
        )
        self.check_fields(
            objName, widgetSettings['properties']['pmwProjectsCounter'], **{'$ref': ref}
        )
        self.check_fields(
            objName, widgetSettings['properties']['pmwInventoriesCounter'],
            **{'$ref': ref}
        )
        self.check_fields(
            objName, widgetSettings['properties']['pmwGroupsCounter'], **{'$ref': ref}
        )
        self.check_fields(
            objName, widgetSettings['properties']['pmwHostsCounter'], **{'$ref': ref}
        )
        ref = '#/definitions/WidgetSetting'
        self.check_fields(
            objName, widgetSettings['properties']['pmwChartWidget'], **{'$ref': ref}
        )
        self.check_fields(
            objName, widgetSettings['properties']['pmwAnsibleModuleWidget'],
            **{'$ref': ref}
        )
        del widgetSettings

        userSettings = definitions['UserSettings']
        objName = 'UserSettings'

        self.check_fields(
            objName, userSettings['required'], 'chartLineSettings', 'widgetSettings'
        )

        ref = '#/definitions/ChartLineSettings'
        self.check_fields(
            objName, userSettings['properties']['chartLineSettings'], **{'$ref': ref}
        )
        ref = '#/definitions/WidgetSettings'
        self.check_fields(
            objName, userSettings['properties']['widgetSettings'], **{'$ref': ref}
        )
        del userSettings

        # Test path responses and schemas
        default_params = ['ordering', 'limit', 'offset']
        pm_default_params = ['id', 'name', 'id__not', 'name__not']
        inv_params = ['variables']

        group = schema['paths']['/group/']
        self.assertEqual(group['get']['operationId'], 'group_list')
        self.assertTrue(group['get']['description'])
        for param in group['get']['parameters']:
            self.assertIn(param['name'], default_params + pm_default_params + inv_params)
        self.assertEqual(param['in'], 'query')
        self.assertEqual(param['required'], False)
        self.assertIn(param['type'], ['string', 'integer'])

        # Check responses via cycle for path
        # for key in obj

        response_schema = group['get']['responses']['200']['schema']
        self.assertEqual(response_schema['required'], ['count', 'results'])
        self.assertEqual(response_schema['type'], 'object')
        self.assertEqual(response_schema['properties']['results']['type'], 'array')
        self.assertEqual(
            response_schema['properties']['results']['items']['$ref'],
            '#/definitions/Group'
        )

        # paths = schema['paths']

        # group_pk_vars = paths['/group/{pk}/variables/']
        # self.check_variables(group_pk_vars)

    def check_fields(self, objname, obj, *args, **kwargs):
        if args:
            self.assertTrue(
                all(val in args for val in obj), 'input_data doesn\'t have enough keys'
            )
            msg = '{} doesn\'t have enough keys'.format(objname)
            self.assertTrue(
                all(val in obj for val in args), msg
            )
        if kwargs:

            objKeys = obj.keys()
            objName = objname + ':' + obj.pop('title', '')
            try:
                objKeys.remove('title')
            except:
                pass

            keys_in_kwargs = all(key in kwargs for key in objKeys)
            keys_in_obj = all(key in obj for key in kwargs.keys())
            self.assertTrue(keys_in_kwargs, 'kwargs doesn\'t have enough keys')
            self.assertTrue(keys_in_obj, 'object doesn\'t have enough keys')

            if keys_in_kwargs and keys_in_obj:
                for key in objKeys:
                    if key == 'description':
                        self.assertTrue(obj[key], 'Description is empty')
                        continue
                    elif key == 'additionalProperties' or isinstance(obj[key], dict):
                        self.check_fields(objName, obj[key], **kwargs[key])
                    elif key == 'enum' or isinstance(obj[key], list):
                        self.check_fields(objName, obj[key], *kwargs[key])
                    else:
                        msg = 'input_data[{key}]:{in_val} != {obj}[{key}]:{obj_val}'
                        msg = msg.format(
                            key=key, in_val=kwargs[key], obj=objName, obj_val=obj[key]
                        )
                        self.assertEqual(obj[key], kwargs[key], msg)

    def check_ref(self, schema, ref, *args, **kwargs):
        path = ref[2:].split('/')
        obj = schema
        for val in path:
            try:
                obj = obj[val]
            except: # nocv
                raise Exception('Definition \'#/' + '/'.join(path) + '\' doesn\'t exist')
