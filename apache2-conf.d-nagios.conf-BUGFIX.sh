
CFG=/etc/apache2/conf.d/nagios.conf.orig

AA1=`cat $CFG | grep  "^</Directory>" | wc -l `
AA2=`cat $CFG | grep  "^<Directory " | wc -l`

echo $AA1
echo $AA2

if [ $AA1 -ne  $AA2 ] ; then
        echo "/etc/apache2/conf.d/nagios.conf has an isse with <Directory or </Directory>"
        echo " backup existing /etc/apache2/conf.d/nagios.conf to /etc/apache2/conf.d/nagios.conf.orig"
        echo " replacing /etc/apache2/conf.d/nagios.conf"
        >/etc/apache2/conf.d/nagios.conf
        cat >>/etc/apache2/conf.d/nagios.conf.test << EOF
# SAMPLE CONFIG SNIPPETS FOR APACHE WEB SERVER
#
# This file contains examples of entries that need
# to be incorporated into your Apache web server
# configuration file.  Customize the paths, etc. as
# needed to fit your system.

ScriptAlias /nagios/cgi-bin "/usr/lib/nagios/cgi"

<Directory "/usr/lib/nagios/cgi">
#  SSLRequireSSL
   Options ExecCGI
   AllowOverride None
   Order allow,deny
   Allow from all
#  Order deny,allow
#  Deny from all
#  Allow from 127.0.0.1
   AuthName "Nagios Access"
   AuthType Basic
   AuthUserFile /etc/nagios/htpasswd.users
   Require valid-user
</Directory>

Alias /nagios "/usr/share/nagios"

<Directory "/usr/share/nagios">
#  SSLRequireSSL
   Options None
   AllowOverride None
   Order allow,deny
   Allow from all
#  Order deny,allow
#  Deny from all
#  Allow from 127.0.0.1
   AuthName "Nagios Access"
   AuthType Basic
   AuthUserFile /etc/nagios/htpasswd.users
   Require valid-user
    <IfDefine KOHANA2>
      DirectoryIndex index.html index.php
    </IfDefine>
</Directory>
EOF

else
        echo "/etc/apache2/conf.d/nagios.conf is ok"
fi
