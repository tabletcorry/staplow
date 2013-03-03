class staplow {
    exec { 'pacman':
        command => '/usr/bin/pacman -Sy'
    }

    Package {
        require => Exec['pacman']
    }

    package { 
        "python2":
            ensure => present;
        "python2-pip":
            ensure => present,
            require => Package['python2'];
    }

    exec { 
        "install deps":
            command => '/usr/bin/pip2 install -r /vagrant/requirements.txt',
            require => Package['python2-pip'],
            timeout => 0;
        "install staplow":
            cwd => "/vagrant",
            command => '/usr/bin/python2 setup.py install',
            require => Exec['install deps'],
            timeout => 0;
    }

    file { '/home/vagrant/.bashrc':
        source => 'puppet:///modules/default/bashrc',
    }
}

include staplow
