class hasspygpio:
    def __init__(self,config):
        #Requires config:
            #{
            # gpio_pin: 23, #GPIO Pin
            # gpio_function: toggle, # Possible values: toggle, on, off
            # host: {
            #     addr: 'local', # If set to local, then run on local machine, otherwise set to ip or fqdn
            #     user: 'user' # If set to local ignored, otherwise user to ssh into host with
            #     },
            # }
        self.config = config
        self.config['local_ip'] = self.get_local_ip()

    def gpio_remote(self):
        # This requires the following:
        # Remote host is a Raspberry PI 2B or greater
        # remote/hasspypi.py installed on remote host
        # SSH Passwordless Login Configured on remote host
        if self.config['host']['addr'] == 'local':
            self.retval = {'code': '001','msg': 'Attempted to run remote command with local config'}
        else:
            try:
                import subprocess
                remote_gpio = ['ssh', self.config['remote_user']+"@"+self.config['remote_host'],'sudo /usr/local/bin/hasspypi',self.config['gpio_pin'], self.config['gpio_function']]
                remote_gpio_output = subprocess.run(remote_gpio)
                self.retval = {'code': '000','msg': 'OK'}
            except:
                self.retval = {'code': '002','msg': f'remote command failed: \n{remote_gpio}\n{remote_gpio_output}'}
        return self.retval


    def gpio_local(self):
        if self.config['host']['addr'] == 'local':
            import lgpio
            h = lgpio.gpiochip_open(0)
            lgpio.gpio_claim_output(h, self.config['gpio_pin'])
            if self.config['gpio_function'] == 'on' or self.config['gpio_function'] == 'toggle':
                try:
                    local_gpio_0 = lgpio.gpio_write(h,self.config['gpio_pin'],0)
                    self.retval = {'code': '000','msg': 'OK'}
                except:
                    self.retval = {'code': '003','msg': f'Error setting GPIO {self.config["gpio_pin"]} to LO\n{local_gpio_0}'}
            if self.config['gpio_function'] == 'toggle':
                from time import sleep
                sleep(1)
            if self.config['gpio_function'] == 'off' or self.config['gpio_function'] == 'toggle':
                try:
                    local_gpio_l = lgpio.gpio_write(h,self.config['gpio_pin'],1)
                    self.retval = {'code': '000','msg': 'OK'}
                except:
                    self.retval = {'code': '004','msg': f'Error setting GPIO {self.config["gpio_pin"]} to HI\n{local_gpio_l}'}
        else:
            self.retval = {'code': '005','msg': f'Attempting to run local gpio when configured to use {self.config["host"]["addr"]}'}
        return self.retval