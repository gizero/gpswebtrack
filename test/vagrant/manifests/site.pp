package { 'debconf-utils':
  ensure => present,
  before => Package['gpsd'],
}

package { 'gpsd':
  ensure => present,
  before => File['/tmp/gpsd-debconf'],
}

file { '/tmp/gpsd-debconf':
  content => "gpsd  gpsd/start_daemon  boolean  true
gpsd  gpsd/device  string
gpsd  gpsd/daemon_options  string
gpsd  gpsd/socket  string  /var/run/gpsd.sock
gpsd  gpsd/autodetection  boolean  true
",
}

exec { 'debconf-set-selections-gpsd':
  command => '/usr/bin/debconf-set-selections /tmp/gpsd-debconf',
  subscribe => File['/tmp/gpsd-debconf'],
}

exec { 'dpkg-reconfigure-gpsd':
  command => '/usr/sbin/dpkg-reconfigure --frontend noninteractive gpsd',
  require => Exec['debconf-set-selections-gpsd'],
}

service { 'gpsd':
  ensure => 'running',
  enable => 'true',
  subscribe => Exec['dpkg-reconfigure-gpsd'],
}


