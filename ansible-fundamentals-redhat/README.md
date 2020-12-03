# Notes to Red Hat Ansible Fundamentals Course

Link to the course on [PluralSight](https://app.pluralsight.com/course-player?clipId=47938779-c3ce-44d1-a031-731010d94559)

## Ansible Inventory

```bash
$ ansible --version
ansible 2.10.3
  config file = None
  configured module search path = ['/home/user/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /home/user/bin/anaconda3/lib/python3.7/site-packages/ansible
  executable location = /home/user/bin/anaconda3/bin/ansible
  python version = 3.7.6 (default, Jan  8 2020, 19:59:22) [GCC 7.3.0]
```

## INI-Formatted Inventory File

```ini
[webservers]
web1.example.com
web2.example.com
web3.example.com
192.0.2.42

[db_servers]
db1.example.com
db2.example.com
```

A host can be a member of multiple groups. Predefined groups are `all` and `ungrouped`.

### Nested Groups

```ini
[usa]
web1.example.com
db1.example.com

[canada]
web2.example.com
db2.example.com

[north_america:children]
usa
canada
```

### Ranges

- `192.168.[4:7].[0:255]`
- `server[01:20].example.com`
- `[a:c].dns.example.com`

### Verifying the Inventoty

```bash
# Verify inventory in the current directory
$ ansible-inventory
```

```bash
# The `-i` option can be used to check a specific file
$ ansible-inventory -i some_inventory
```

```bash
# List the inventory in YAML format
$ ansible-inventory -y --list
```

```bash
# Look for a machine in the inventory
$ ansible web2.example.com --list-hosts
```

```bash
# Verify connection by pinging the group|machine
$ ansible <group> --limit <hostname> -m ping
```

## Checking Configuration

```bash
# Display all configuration settings
$ ansible-config dump
```

```bash
# Display configuration settings that have been changed
$ ansible-config dump --only-changed
```

## Running Ad Hoc Commands

```bash
$ ansible host-pattern -m module [-a 'module arguments'] [-i inventory]
```

### Overriding Default Configuration Settings

- `-i` or `--inventory` or `--inventory-file` specifies inventory configuration file to use
- `-k` or `--ask-pass` will prompt for the connection password
- `-u REMOTE_USER` or `--user` overrides the `remote_user` setting in `ansible.cfg`
- `-b` option enables privilege escalation, running operations with `become: yes`
- `--become-method` enables privilege escalation using a specific method like `sudo`
- `--become-user` option defines what user should be used when escalating privileges
- `-K` or `--ask-become-pass` will prompt for the privilege escalation password

### Managing Users

```bash
# Ensure a user USER_NAME with id 4000 present on the remote host
$ ansible -m user -a 'name=USER_NAME uid=4000 state=present' host

# Create a user
$ ansible webservers -m user -a 'name=test password=secure_password state=present'

# Delete a user
$ ansible webservers -m user -a 'name=test state=absent'
```

### Using Modules

```bash
# Restart a service sshd on all machines
$ ansible all -m service -a 'state=restarted name=sshd'

# Ensure a package is installed
# state can be: present, absent or latest
$ ansible all -m package -a 'name=httpd state=present'
```

### File Modules

- `copy`: Copy a local file to the manages host
- `file`: Set permissions and other properties of files
- `lineinfile`: Ensure a particular line is or is not in a file
- `synchronize`: Syncronize content using `rsync`

### Software Package Modules

- `package`: Ensure the package is installed using the generic OS package manager
- `apt`: Manage packages using `apt`
- `yum`: Manage packages using `yum`
- `dnf`: Manage packages using `dnf`
- `gem`: Manage Ruby gems

### System Modules

- `firewalld`: Manage arbitrary ports and services using `firewalld`
- `reboot`: Reboot a machine
- `service`: Manage services
- `user`: Add, remove and manage user accounts

### Net Tools Modules

- `get_url`: Download files over HTTP, HTTPS or FTP
- `nmcli`: Manage networking
- `uri`: Interact with web services and communicate with APIs

### Command Modules

- `command`: Runs a single command on a remote system
- `shell`: Runs a command on a remote system's shell
- `raw`: Simply runs a command with no processing (can be dangerous)

## Looking Up in The Documentation

```bash
# Request a list of available modules
$ ansible-doc -l

# Display information on a given module
$ ansible-doc ping
```
## Working With Playbooks

### Running a Playbook

```bash
# Run playbook_filename.yml file
$ ansible-playbook playbook_filename.yml

# Limit execution to specific hosts or groups
$ ansible-playbook playbook_filename.yml --limit host
```

## Variables

### Scopes

- Global
- Group (group_vars)
- Host (host_vars)
- Play
- Command line vars, specified with the `-e` option

### Using Directories to Set Host and Group Variables

```
project
├── group_vars
|   ├── all
│   ├── datacenters
│   ├── datacenter1
│   └── datacenter2
├── host_vars
│   ├── demo1.example.com
│   ├── demo2.example.com
│   ├── demo3.example.com
│   └── demo4.example.com
└── playbook.yml
```

### Definig Variables

```yml
# Vars defined at the top of the play
- hosts: all
  vars:
    user_name: joe
    user_state: present

# Vars defined in external files
- hosts: all
  vars_files:
    - vars/users.yml
```

### Referencing Variables

```yml
- name: Example play
  hosts: all
  vars:
    user_name: joe

  tasks:
    - name: Creates the user {{ user_name }}
      user:
        name: {{ user_name }}
        state: present
```

```bash
# Set a variable in a command line
$ ansible-playbook playbook_file -e "varname=value"
```

### Selecting Items from a Dictionary

```yml
vars:
  users:
    aditya:
      uname: aditya
      fname: Aditya
      lname: Atwal
      home: /home/aditya
      shell: /bin/bash
    carlotta:
      uname: carlotta
      fname: Carlotta
      lname: Spencer
      home: /home/carlotta
      shell: /bin/zsh

# Using vars
users['aditya']['fname']
users['carlotta']['home']
```
### Storing The Output in a Variable

`register` module captures the output in a variable.

## Protecting Sensitive Data

```bash
# Create a new encrypted file
$ ansible-vault create filename

# View a new encrypted file
$ ansible-vault view filename

# Edit a new encrypted file
$ ansible-vault edit filename

# Encrypt an existing file
$ ansible-vault encrypt filename

# Decrypt an existing file
$ ansible-vault decrypt filename

# Change the password of an encrypted file
$ ansible-vault rekey filename
```

### Accessing Secrets

```bash
$ ansible-playbook --ask-vault-pass playbook.yml
```

## Task Iteration with Loops

```yml
# using loop for iteration
vars:
  myusers:
    - ivan
    - boris
    - joe

tasks:
  - name: Create users
    user:
      name: "{{ item }}"
      state: present
    loop: "{{ myusers }}" # iterates over myusers variable
```

```yml
# using with_dict for iteration
tasks:
  - name Create groups
    group:
      name: "{{ item }}"
    loop:
      - admins
      - lamers

  - name Create users
    user:
      name: "{{ item.name }}"
      groups: "{{ item.groups }}"
    with_dict:
      - { name: 'fred', groups: 'admins' }
      - { name: 'bob', groups: 'admin' }
      - { name: 'joe', groups: 'lamers' }
      - { name: 'kirk', groups: 'lamers' }
```

## Conditions with Ansible Facts

```yml
- name: Demonstrate "in" in a condition
  hosts: all
  gather_facts: yes
  become: yes
  vars:
    my_service: httpd
    supported_os:
      - RedHat
      - Fedora
  tasks:
    - name: Install "{{ my_service }}"
      yum:
        name: "{{ my_service }}"
        state: present
      when: ansible_facts['distribution'] in supported_os
```

### Combinig Loops and Conditional Tasks

```yml
- name: Restart HTTPD if Postfix is running
  hosts: all
  tasks:
    - name: Get Postfix server status
      command: /usr/bin/systemctl is-active postfix
      ignore_errors: yes
      register: result

    - name: Restart Apache HTTPD based on Postfix status
      service:
        name: httpd
        state: restarted
      when: result.rc == 0
```

## Handlers

Handlers are tasks that respond to a notification triggered by other tasks.

```yml
tasks:
  - name: copy demo.example.conf configuration template
    template:
      src: /var/lib/templates/demo.example.conf.template
      dest: /etc/httpd/conf.d/demo.example.conf
    notify:
      - restart apache

handlers:
  - name restart apache
    service:
      name: httpd
      state: restarted      
```

## Recovering from Errors

```yml
tasks:
  - name: Upgrade DB
    block:
      - name: upgrade the database
        shell:
          cmd: /usr/local/lib/upgrade-database

    rescue:
      - name: revert the database upgrade
        shell: 
          cmd: /usr/local/lib/revert-database

    always:
      - name: always restart the database
        service:
          name: mariadb
          state: restarted
```

## Jinja2 Templates

Jinja2 template files allow to deploy a template that contains Jinja2 variables. Those variables are replaced with their values when the template is deployed. The `template` module is used to deploy a template file. It takes most of the same arguments as `copy` module.

```yml
- name: Make sure sshd_config is customized
  template:
    src: sshd_config.j2
    dest: /etc/ssh/sshd_config
    owner: root
    group: root
    mode: "0600"
    setype: etc_c
```

### Comments

```jinja
{# This is a Jinja2 comment #}
```

### Expressions

```jinja
{# Only included if finished is True #}
{% if finished %}
{{ result % }}
{% endif %}
```

### Cycles

```jinja
{% for host in groups['all'] %}

{# Loop body here #}

{% endfor %}
```

### Special Variables

- `hostvars` - contains all host variables, including gathered facts
- `groups` - contains all defined groups

## Lookup Plugins

Lookup plugins import and format data from external sources for use in variables and templates.

```bash
# List all available look up plugins
$ ansible-doc -t lookup -l

# Display documentation for the 'file' lookup plugin
$ ansible-doc -t lookup file
```

### Lookup and Query

Two ways to call a lookup plugin:
- `lookup` returns a string of comma-separated items
- `query` returns an actual YAML list of items

```yml
- name: Example of a lookup plugin in use
  hosts: all
  vars:
    mxvar: "{{ query('dig', 'gmail.com', 'qtype=MX') }}"
  
  tasks:
    - name: List each MX record for gmail.com
      debug:
        msg: An MX record is: {{ item }}
      loop: "{{ mxvar }}"
```

### File Lookups

The `file` lookup plugin can be used to load the contents of a file into a variable.

```yml
- name: Add authorized keys
  hosts: all
  vars:
    users:
      - naoko
  
  tasks:
    - name: Add authorized keys
      authorized_key:
        user: "{{ item }}"
        key: "{{ lookup('file', item + '.key.pub') }}"
      loop: "{{ users }}"
```

### Command Output Lookups with Lines as Items

The `lines` lookup plugin will read output from a command, making each line an item in the list.

```yml
- name: Print the name of each account in /etc/passwd
  debug:
    msg: A user is {{ item | regex_replace(':.+$') }}
  loop: "{{ query('lines', 'cat /etc/passwd') }}"
```

### Template Lookups

The `template` lookup plugin will take Jinja2 template and evaluate that when setting the value.

```jinja
{# Template file "my.template.j2" #}
Hello {{ my_name }}
```

```yml
- name: Print "Hello class!"
  hosts: all
  vars:
    my_name: class

  tasks:
    - name: Demonstrate template lookup plugin
      debug:
        msg: {{ lookup('template', 'my.template.j2') }}
```

### URL Lookups

The `url` lookup plugin is useful to grab the content of a web page or the output of an API.

```yml
- name: test url lookups
  hosts: localhost
  become: no
  vars:
    amazon_ip_ranges: "{{ lookup('url', 'https://ip-ranges.amazonaws.com/ip-ranges.json', split_lines=False) }}"

  tasks:
    - name: display IPv4 ranges
      debug:
        msg: "{{ item['ip_prefix'] }}"
      loop: "{{ amazon_ip_ranges['prefixes'] }}"

    - name: display IPv6 ranges
      debug:
        msg: "{{ item['ipv6_prefix'] }}"
      loop: "{{ amazon_ip_ranges['ipv6_prefixes'] }}"
```

